+++
date = '2025-04-28T23:18:08+02:00'
title = 'Deep-Dive: Sockets'
+++

Reference #1: https://www.youtube.com/watch?v=D26sUZ6DHNQ

Reference #2: https://man7.org/linux/man-pages/man2/socket.2.html

Socket State-machine
Socket Programming
Socket lifecycle
Sockets
Port Exhaustion
Socket leaks
Anonymous Pipes
Epheremal Ports
File Descriptors
Global File Table
Inode Table

<iframe frameborder="0" style="width:100%;height:393px;"
src="https://viewer.diagrams.net/?url=https://raw.githubusercontent.com/dry-han/stage-bloggy/refs/heads/master/assets/test.drawio"></iframe>


### Defining Sockets
Sockets are a software construct/an abstraction offered by the operating system so that different processes can communicate over the same machine or network. They offer a clean interface between application logic and the underlying
network stack, to application developers from networking complexity (routing, packet fragmentation, transmission, etc..)

Sockets operate primarly at the L4/Transport layer, and applications (at L7) invoke system sockets APIs to send/receive
data through sockets, which will wrap the data in TCP/UDP segments and send it to L3/Network layer.

The OS identifies which socket to route messages to according to their associated five-tuple: protocol (UDP or TCP),
src/dst IP, src/dst port. 

### System Call
The `socket(2)` system call can be used to create sockets. Sockets can be created in C using the following:
```c
/* 'domain' specifies the protocol family used for communication */
/* AF_UNIX, AF_NETLINK, AF_PACKET, AF_INET (IPv4), AF_INET6 (IPv6), AF_MPLS, AF_XDP */
/* 'type' specifies the communication semantics */
/* SOCK_STREAM (TCP), SOCK_DGRAM (UDP), SOCK_RAW */
/* 'protocol' specified a particular protocol to be used with a socket */
/*  Normally, a single protocol exists to support a particular socket type, but there can be exceptions */
 int socket(int domain, int type, int protocol);
```

### TCP Sockets
TCP sockets are connection-oriented and provide reliable, ordered and error-checked transmission.
There is an initial 3-way handshake (SYN -->, SYNACK <--, ACK -->) to guarantee that both sides are ready.
TCP ensures that packets arrive in order and without duplication.
TCP can be used for unicast (one-on-one) traffic.
The system maintains a TCP finite state machine for each TCP sockets

### UDP Sockets
UDP is connectionless and unreliable without any guarantee, however it is much faster and lightweight
than TCP.
It can be used for unicast, multicast, and broadcast traffic depending on use-cases.

### Unix Sockets
There is a special type of sockets, which differs from network sockets: Unix sockets.

Unix domain sockets / UDS are used for inter-process communication on the same host, and are not network
sockets. They do not use an IP/Port tuple but rahter use a path on the file system. They
are much faster than network sockets as they bypass the network stack and do not require routing
or protocol overhead.

In Unix systems, where 'everything is a file', sockets are treated as file descriptors
meaning that they can be used with common system calls such as 'read/write'.

File descriptors are created by the OS when a file is opened to represent that file.
In short, it is an integer that uniquely represents an open file for a process.
Similarly, sockets have socket descriptors that are also integers.

## Socket Lifecycle

### Server-side Socket Lifecycle
On server-side, sockets follow a specific lifecycle which start with the creation of a listening socket
and which waits for incoming client connections. Once client requests connections, and the server accepts
it, the server creates a dedicated socket instance which the server will use to communicate with that
specific client, and the original socket continues listening for new requests. This mechanism can allows
server to handle simultaneous communication with several clients.

After the communication ends, the server is expected to close the socket
to free up system resources.

#### Scalability Concerns
This is usually handled with multi-processing or multi-threading, however this model is not scalable
as each thread consumes memory and context switching is expensive, leading to performance
degradation.

In high-performance system, these limitations are addressed using non-blocking techniques such as
message brokers/pub-sub systems, and architectures which are non-blocking/have async I/O.
With this approach, a limited number of threads can service a large number of users.

This is achieved using system calls such as select/poll/epoll which notify the application only
when specific sockets are ready to receive/send data e.g. they can be used to monitor multiple
file descriptors associated with sockets to see if I/O is possible on any of them.

### Client-side Socket Lifecycle
On the client's side, the socket lifecycle is as follow: it creates a socket bound a specific
IP and port, and initiates a connection to the server's IP and port. In TCP sockets, this
initiates the 3-way handshake. Once connected, the client can read/write data to a socket.

After the communication ends, the client is expected to close the socket
to free up system resources.

### Security
Sockets are inherently insecure as data is communicated in plain-text across them, however
security can be achieved by using SSL/TLS, which wraps existing socket connections
and ensures that all data sent is encrypted and authenticated

