+++
date = '2026-07-13T14:12:14+02:00'
draft = false
title = 'Dev: Introduction to eBPF'
+++

# Overview

- Why is eBPF needed
  - User space programs need to communicate with underlying hardware, but are not aware of the specifics of each devices.
  - Kernel space sits between the user space and the underlying hardware, and offers the appropriate APIs to facilitate communication (device modules and drivers, system calls)
  - Extending the Kernel space is challenging and requires modifying/rebuilding the kernel, or developing additional kernel modules.
  - Also, Kernel and Hardware have long innovation cycles which make innovation difficult

- eBPF originally is an extension of the Berkley Packet Filter, but now can do much more than packet filtering
  - "eBPF is a programming language & runtime to extend operating systems"
  - Enables additionall Networking/Service Mesh (Cilium, Calico CNI), Observability, Security.. features in the kernel
  - Attach to various hooks and responds to specific actions: kernel trace points, network events, etc
  - Written in restricted version of C language, which is checked beforehand to run safely in kernel-context
  - Process calls `bpf()` syscall to inject BPF bytecode, kernel contains eBPF verifier and JIT compiler before running it
  - Process <--> System Call (Kernel Space) <--> eBPF <--> Scheduler
  - JIT compiler, can run with higher-level languages like Python/C, and convert to eBPF bytecode
  - SDKs and Compilers to get eBPF bytecode: Go (cilium/ebpf), Rust (libbpf-rs), C++ (libbpf), bcc

- Helper Calls
  - Triggering an eBPF hook point, it can call a helper function (getting data, re-direct packets, chain eBPF packets)  

- eBPF Maps
  - Key/value store, where values can be any type of data
  - Can be used to store/share information in collective state across processes
  - Accessible from within eBPF programs, but also user-space programs using system calls

...

# Code Example

```python
{{% get-page-resource-content localPath="ebpf_example.py" %}}
```

Cisco-U has a basic course showing how to create a packet filtering program with eBPF: https://u.cisco.com/tutorials/packet-filtering-with-ebpf-5582

# Reference

- Cisco's [Introduction to eBPF](https://www.youtube.com/watch?v=clxOil-rars) video.
- Thomas Graf's [Keynote on eBPF at CNCF](https://www.youtube.com/watch?v=KhPrMW5Rbbc).
