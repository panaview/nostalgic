+++
date = '2026-07-08T22:05:09+02:00'
draft = false
title = 'Deep-Dive: Network Card Offload'
+++


# Reference: 
Deep Dive on NIC - IETF: https://www.youtube.com/watch?v=wHM7RVk3-yk
Network Performance in Linux Kernel Maxime Chevallier: https://www.youtube.com/watch?v=g4w3ydS62S0&t=617s

## Presentation Introduction

Scope of the presentation is
- Basic NIC support
- Hardware offload from host stack functionality
- Linux kernel is reference for architecture and APIs

More interesting details which are out-of-scope here:
- Kernel bypass (DPDK)
- Smaller CPE level devices or Large ASICs
- Virtualization Offload technology (SR-IOV)
- Storage/NIC interfacing

IETF has interests in NIC because:
- NIC can play a role in protocol implementation
- Nodes that perform both host and forwarding functions
- NICs can acelerate host protocol processing (TCP, UDP, QUIC, TLS, IPsec)
- Accelerate forwarding functions (L2 -> Ln filtering and forwarding, QOS
  handling)

---
## Basics of NIC operation

Fundamentals and Basic offloads:
- Network Interface Card: Host's interface to physical network
  - receiver/transmitter of packets to the physical network
- Host Stack: Software stack that performs host side processing of packets at L2, L3, L4
  protocols 
- Kernel Stack: Host stack implemented in an OS kernel
- Offload: operation done in HW NIC that is could also be done in host stack
- Acceleration: offload for performance gains

NIC connects into the system through a system bus (PCIe usually)
NIC have two queues:  RX/TX.

They store packets and are composed of a set of descriptors, that describe the packet for the NIC (Where is it stored in host memory, packet length, aux information like if packet is broadcast)

[9:03]  - Diagram

At Tx, host stack fills a transmit descriptor (where packet is in memory, length of packet..). Host stack then puts it into TX queue and bumps queue pointer. The queue follows a producer/consumer model. PCIe register write is used to notify the NIC that packets are ready to be processed.

NIC wakes up, pull packets into local memory using DMA, might perform offload processing, serializes the data and sends it into the network

On receive path, the host sets up a set of packet buffers where packets will be stored in its memory and put these into the RX descriptors.

When the NIC receives a packet it deserializes the packet and does some processing nd takes next receive descriptor in the queue, dmas the packet into the host memory, sets the length in the receive descirptor, increases receiver pointer in its receive queue. Then sends an actual sysmte inerrupt to warn the host that packets have been received

---

## History of network interface cards:
- Fundamentals support (1900s)
  - Transmit and receive packets
  - Basic Offloads (Ethernet checksum ofload)
- Data plane acceleration (2000s)
  - Optimization for multicore cpus
  hardware data plane offload - mostly fixed function devices tunneling ipsec qos offloads
- Programmability (2010s)
  - FPGAs and NPUs with programmable data plane
  - General purpose processors with programmable data and control planes

---
## Basic NIC offloads
### Motivaton & Consideration
Offload Motivation:
- Free up CPU cycles for application
- Specialized processing can be more efficient
- Save host resources
- Scaling performance (low latency/high throughput)
- Power savings

Question to ask: do we really benefit from offload ? What is the trade-off with running uniquely on the host cpu ?

"Less is More" Principle
- Protocol agnostic over protocol specific solutions helps to support new protocols without needing new solutions
- Common APIs are better than proprietary ones to avoid vendor lock in, and to differentiate by features/performance/implementation
- Programmability allows users to do whatever they want and make theeir NICs adaptable

Offload Considerations:
- TX and RX
- Protocol agnostic vs Protocol specific
- Stateful versus stateless
- Encapsulation
- Always on vs Opportunistic
- Building protocols to be NIC offload friendly

### Basic offloads
Basic Offloads (here since the 90s)
- Checksum offload
- Segmentation offload
- Multi-queue and packet steering

Checksum offload:
- Offload computation of checksum in TCP, UDP, GRE, etc
- NIC offload calculation over data
- Checksum offload is ubiquitous (i.e. everywhere)
- Encapsulation allows multiple checksums in same packet

TX Checksum offload:
- Protocol-specific: Device parses transports layer (TCP/UDP) and set checksum
- More generic: Instruct device where to start and write checksum, init csum field, indicate start offset and offset to write checksum
[19:44] diagram 

RX Checksum offload:
- Protocol specific: checksum unnecessary, device parses packet and verifies udp or tcp checksum
- more generic: device returns 1's complement sum across words in the ethernet payload
[21:0] diagram 

Segmentation Offload
- Stack operates more efficiently on large packets
- Combines with checksum offload to minimize header processing and per packet overhead

TSO - Transmit segmentation offload (TX):
- If packet has large amount of data (e.g. 64k TCP packet)
- Split big packet into smaller one low in the stack, with each having its' own IP and TCP header
- Generic Segmentation offload (GSO) : SW variants
- LSO Large Segemntation Offload (Large Send offload ?) or also called TSO (Tcp segmentation offload): HW variant

RSO - Receive segmentation offload (RX):
- Coalesce small packets into bigger ones low in stack
- Usually done for packets of one flow
- Generic receive offload, GRO: sw variant
- Large Receive offload, LRO: hw variant
- Difficult to make protocol agnostic
- Must have checksum offload available in conjunction. From DPDK docs: "The GRO library doesn’t check if input packets have correct checksums and doesn’t re-calculate checksums for merged packets" - https://doc.dpdk.org/guides/prog_guide/generic_receive_offload_lib.html

Multi-queue:
- Multi-queue is done in conjunction with multi processor cpus
- Multiple RX and TX queues.
- Load-balancing: Queues can be accessed and processed in parallel
- Each queue is assigned to a CPU, to have queue to CPU affinity
- Queues can be assigned certain attributes: low/high priority queues
- OoO: out-of-order packets are problematic.
- Solution to keep packets in order is to maintain flow-to-queue affinity

Transmit Queue selection / TX:
- Two methods
- First method (XPS, Transmit packet steering): Each cpu is assigned to a queue. When an application sends a packet, the queue chosen is the one
associated with the CPU the application runs on.
- This enables for siloing (e.g. isolate) locality, and there is therefore no contention for lock or
the structures of the queue.
- Second method (Driver selects queue):  driver to select the queues. Driver has 'rich semantic' and might better understand the queue topology. Host stack asks driver which queue to use to send packets, there can be metadata in the packet (e.g. priority of the queue), the driver looks up the queue that is appropriate e.g a queue with higher priority.
- `ndo_select_queue` in Linux
- Other attributes like rate limiting could apply.

Receive Packet Steering / Rx
- Packets are received on the NIC, they need to be distributed among the queues
- Very similar to ECMP
- Stateless variant: Steer to queue based on hash on 5-tuple if transport layer is available, or 3-tuple if we use the flow label
- Map hash into one of the queues, to be consistent for a flow and always have it be associated to one queue
- RPS Receive Packet Steering is SW stateless variant
- RSS Receive Side scaling, is HW variant
- Stateful variant: Receive Flow steering, allows flow-to-queue association 
- Host can program for each flow which queue to use.
- Can be very useful for isolation. Pinning application to CPU, and Receive flow steering
is used to only have flows associated with this application go on a specific queue associated with this CPU
- RFS Receive Flow Steering is software variant
- aRFS accelerated RFS is the hardware variant


## Data Plane in Hardware:
- Solutions depends on use-case, and not mutually exclusive 
- Fixed or minimally configurable pipelines: ASIC implementing a pipeline in hardware with TCAM
- Network processing Unit/Network Flow Processor (NPU/NFP): multi-threaded execution environment for data-plane programs, can have special instructions related to network processing
- FPGA: most control with abilit to program the hardware itself, and describe pipeline at gateway level
- General Purpose Processor: e.g. ARM processor on the NIC to execute the pipeline

Data Plane acceleration topics:
- Match/Action
- Forwarding
- QoS
- TLS and IPsec

Match/Action:
- Extract headers / 5-tuple and input device, to provide a hash
- Using hash we try to find a match and apply related action
- actions include forward to port or mirror, drop, packet or metadata modification
- Also stateful actions like policing and connection tracking

Forwarding:
- Match/Action pipeline can be used to program forwarding pipeline
- Extract L2 -> Ln headers information, and create special rules to do 
special actions on certain types of traffic e.g. on a specific port
- HW datapath misses (no processing rules) can fall back to host software datapath
- Tunnel encapsulation (VXLAN, GRE, GENEVE) and tagging (VLAN, MPLS) can also be done in HW datapath

QOS:
- At ingress: No queue available at RX, but we can do filtering/meter/filter
- at Egress: More can be done since queue is available, classifier to select priority, priority scheduler (Deficit round robin, TSN, shaping (DCB)), rate limiting, MQ + RED offload

TLS:
- Crypto tends to be quite complex
- Host is still responsible for TLS handshake
- TLS connection is handled by kTLS module in kernel, and then offloaded to NIC
- On TX: NIC driver marks packets for crypto offload based on packet socket, and NIC encrypts and then TX
- On RX: NIC performs decrypt and auth, notifies kTLS of queued data, kTLS skips decrypt on queued data and handles out-of-order traffic

IPsec:
- Crypto offload: HW handles encrypt, decrypt, integrity, lso, checksum; Kernel handles Padding/anti-replay/counters/security policy DB; User-space IKE
- Full offload: HW handles Replay/Encap/Decap/SPD/LSO/Checksum/LRO; Kernel handles IP fragmentation, counters, configuration; and user-space handles IKE

## Programmability:
- Two types are mainly used today: FPGA/NPU and General Purpose processor
- Facilitates rapid protocol development

Programmablity with FPGA/NPU:
- Data plane can be expressed by P4, eBPF, NPL, etc

# Glossary
Network Interface Card
Host Stack
Kernel Stack
Offload
Acceleration
RPS
RSS
RFS
aRFS
XPS
PCIe
