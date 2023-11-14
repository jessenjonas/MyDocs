---
tags:
    - Networking
title: OSPF
---
# OSPF
*[OSPF]: Open Shortest Path First
*[IETF]: Internet Engineering Task Force
*[LSA]: Link-state advertisements
*[RID]: Router-ID
*[LSDB]: Link-state database
*[SPF]: Shortest Path First
*[SPT]: SPF Tree

<img src=../assets/OSPF.png width=500>

## What is OSPF
OSPF is one of the most deployed routing protocols in the world. Developed by the IETF to overcome the limitations of distance vector routing protocols.

OSPF uses it’s link-state algorithm, Djikstra, to build a link-state database, called LSDB, which contains all the shortest path to all known destinations, including inter-area, - This database is identical for all routers within an area.  
LSAs will be exchanged when neighbor adjencies are made. When synchronized and converged, an OSPF router only sends partial updates to it’s neighbor(s), which will then be flooded to all OSPF routers within an area.

It’s design means that area 0, the backbone area, is a requirement when create a multi-area OSPF AS. If there is only a single area in the AS, the area ID is your choice.  
When creating a multi-area OSPF, since OSPF expects all areas to inject routing information into Area 0, all areas must be directly attached to area 0.  
In situations where an area is either not connected to area 0, or are both connected to area 0 and another area, but the link to area 0 goes down, a virtual link can be created.

OSPF Multi-area uses different LSAs and area types, where the various LSAs, depending on the configuration of the routers, improves convergence and scalability.
This makes it possible to summarize routes from other areas, whereas different area types makes it possible to alter the database as you desire.
The various LSAs and area types, and their definition, can be found in the section "Link State Advertisements".

| OSPF                  | OSPFv3         | Facts        |                  |
| ---------------------- | ------------------------- | ------------ | ---------------- |
| IPv4<br>*Global config*      | IPv6<br>*Int config*             | Type         | Link-state  |
|       | IPv4 & IPv6<br>*Address Family (AF)*<br>*Global & Interface configuration*   | Algorithm    | SPF (Dijkstra)     |
|    |    | Standard     | Non proprietary  |
|                        |                           | Protocol     | IP              |
|                        |                           | Group        | IGP              |

## SPF Tree
As each router contains an LSDB, they each create a SPT, which contains all the routes to known destinations, with the router as the tree root.  
Therefore the SPT differs from each router. But the LSDB, used to create the SPT is identical. This ensures that the network is loop-free.

While each router have the same LSDB's (one for each area), the internal topology of an area, is invisible from outside of the area.  When a topology is changing, all routers inside an area does a full SPT calculation, while routers outside the area, only does a partial calculation.

In essence, an OSPF area hides the topology from another area but allows the networks to be visible in other areas within the OSPF domain.  
Segmenting the OSPF domain into multiple areas reduces the size of the LSDB for each area, making SPT calculations faster and decreasing LSDB flooding between routers when a link flaps.

<img src=../assets/OSPF_SPT.png width=600>

## Router types

## Area types

## Link State Advertisements

## Neighbor States
Each OSPF process maintains a table for adjacent OSPF neighbors and the state of each router.  
The table below shows the available states for a neighboring router, in that order. 

| State | Description |
| ---- | ---- |
|Down| The initial state of a neighbor relationship. It indicates that the router has not received any OSPF hello packets.|
|Attempt| A state that is relevant to nonbroadcast multi-access (NBMA) networks thatdo not support broadcast and that require explicit neighbor configuration. Thisstate indicates that no recent information has been received, but the router isstill attempting communication.|
|Init| A state in which a hello packet has been received from another a router, butbidirectional communication has not been established.|
|2-Way| A state in which bidirectional communication has been established. If a DR orBDR is needed, the election occurs during this state.|
|ExStart| The first state in forming an adjacency. Routers identify which router will be themaster or slave for the LSDB synchronization.|
|Exchange| A state during which routers are exchanging link states by using DBD packets.|
|Loading| A state in which LSR packets are sent to the neighbor, asking for the morerecent LSAs that have been discovered (but not received) in the Exchange state.|
|Full| A state in which neighboring routers are fully adjacent.|

## Requirements for Neighbor Adjacency
For routers to establish neighbor adjancy, they must follow all of the requirements below:

- The RIDs must be unique between the two devices.  
To prevent errors, they should be unique for the entire OSPF routing domain.
- The interfaces must share a common subnet. OSPF uses the interface’s primary IP address when sending out OSPF hellos.  
The network mask (netmask) in the hello packet is used to extract the network ID of the hello packet.
- The interface maximum transmission unit (MTU) must match because the OSPF protocol does not support fragmentation.
- The area ID must match for that segment.
- The need for a DR must match for that segment.
- OSPF hello and dead timers must match for that segment.
- The authentication type and credentials (if any) must match for that segment.
- Area type flags must be identical for that segment (stub, NSSA, and so on).

## Router ID
By default the Router ID is set dynamically, but can also be set manually using the `Router-id <32-bit router ID>` command.
The algorithm for dynamically choosing the OSPF RID uses the following order:

1. Highest IPv4 address of any up loopback interfaces.
2. If there are not any up loopback interfaces, the highest IPv4 address of any active up physical interfaces becomes the RID.

If the conditions above aren't fulfilled, the OSPF process isn't started

## Configuration
### OSPFv2
    Router ospf <process number>
    router-id <32-bit Router ID>
    Network <Network adress> <Wildcard mask> area <area id>
    Passive-interface [<Interface> | Default]

### OSPFv3 IPv6
    ipv6 unicast-routing
    ipv6 router ospf <process number>
    router-id <32-bit Router ID>
    int <interface>
    ipv6 ospf <process number> area <area>

### OSPFv3 Address Family
!!! info
    Depending on OS version. May only be on newer versions
```
ipv6 unicast-routing
Router ospfv3 <process number>
router-id <32-bit Router ID> !Must on IPv6
```

#### Global configuration
    address-family [ipv6 | ipv4] unicast
    passive-interface [<interface> | default]
    area <area id> range <network adress> <subnet mask> !IPv4
    area <area id> range <ipv6-prefix> !IPv6

#### Interface configuration
    int <interface>
    ipv6 enable
    ospfv3 <process number> [ipv4 | ipv6] area <area id>

## Redistribution
### OSPFv2
    Router ospf <process number>
    redistribute <Protocol | ...> [subnets]

### OSPFv3 IPv6
    ipv6 unicast-routing
    ipv6 router ospf <process number>
    redistribute <Protocol | ...> [subnets]

### OSPFv3 Address Family
    Router ospfv3 <process number>
    address-family [ipv6 | ipv4] unicast
    redistribute <Protocol | ...> <process-id> [subnets]

[^1]: OSPFv3 is using IPv6 Link-Local addresses. Therefore IPv6 must be enabled regardless if using IPv4 or IPv6.

## Additional Configuration
### Authentication on OSPF
    key chain <keychain-name>
    key <number>
    key-string <secret key>
    cryptographic-algorithm <algorithm>
    int <interface>
    ip authentication key-chain <keychain-name>