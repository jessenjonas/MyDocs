---
tags:
    - Networking
title: EIGRP
---
# EIGRP
*[EIGRP]: Enhanced Interior Gateway Routing Protocol
*[FD]: Feasible distance
*[RD]: Reported distance
*[RID]: Router-ID

<img src=../assets/EIGRP.png width=400>

## What is EIGRP
EIGRP, developed by Cisco - and proprietary to Cisco, is an advanced distance vector routing protocol. In contrary to the older IGRP, which are a distance vector routing protocol, EIGRP includes features, found in link-state protocols, that are not present in IGRP or RIP, which is why it is reffered to as an advanced distance vector.

By storing it’s neighbors routing table, EIGRPs algorithm, DUAL, ensures that a router running EIGRP quickly can adapt to changes in the network - resulting in rapid convergence and a loop free network.

<img src=../assets/EIGRP_Successor.png width=400>

EIGRP uses DUAL to calculate the cost for each path to a destination network in it’s AS using the path’s distance information, AKA composite metric.  
Then it stores up to 4 successor routes, if having the same RD, and all the feasible successors, which all must satisfy the feasiblity condition of having a RD lower than the RD of the successor route, AKA the FD. The lower the cost, the better.

With `show ip eigrp topology` we can see the successor, and feasible successor, routes, alongside their reported distances.

<img src=../assets/EIGRP_Topology.png width=400>

|Term |Definition|
|---|---|
|Successor route |The route with the lowest path metric to reach a destination.<br>The successor route for R1 to reach 10.4.4.0/24 on R4 is R1→R3→R4.|
|Successor |The first next-hop router for the successor route.<br>The successor for 10.4.4.0/24 is R3.|
|Feasible distance (FD) |The metric value for the lowest-metric path to reach a destination. The feasible distance is calculated locally using the formula shown in the “Path Metric Calculation” section.<br>The FD calculated by R1 for the 10.4.4.0/24 network is 3328<br>(that is, 256 + 256 + 2816).|
|Reported distance (RD) |Distance reported by a router to reach a prefix. The reported distance value<br>is the feasible distance for the advertising router.<br>R3 advertises the 10.4.4.0/24 prefix with an RD of 3072. R4 advertises the 10.4.4.0/24 to R1 and R2 with an RD of 2816.|
|Feasibility condition |For a route to be considered a backup route, the RD received for that route<br>must be less than the FD calculated locally. This logic guarantees a loop-free path.|
|Feasible successor |A route with that satisfies the feasibility condition is maintained as a backup route. The feasibility condition ensures that the backup route is loop free.<br>The route R1→R4 is the feasible successor because the RD of 2816 is lower than the FD of 3328 for the R1→R3→R4 path.|

EIGRIP uses IP protocol number 88 and is using multicast packets where possible, and unicast packets when necessary. Communication between routers is done using the group address 224.0.0.10 or the MAC address 01:00:5e:00:00:0a when possible.

| EIGRP                  | EIGRPv6          | Named EIGRP                  | Facts        |                  |
| ---------------------- | ------------------------- | ---------------------- | ------------ | ---------------- |
| IPv4<br>*Global config* |  IPv6<br>*Int config*  | IPv4 & IPv6<br>*Global configuration* | Type  | Advanced<br>Distance Vector  |
|                                |  No VRF support           | Single place configuration | Algorithm    | DUAL     |
|                                |                           | IPv6 VRF support | Standard     | Cisco proprietary  |
|                                |                           |                        | Protocol     | RTP              |
|                                |                           |                        | Group        | IGP              |
|                                |                           |                        | Load balacing | Equal & Unequal     |

*[RTP]: Reliable Transport Protocol

## Summarization
<img src=../assets/EIGRP_Summarization.png width=400>

EIGRP summarizes network prefixes on an interface-by-interface basis.  
When summarization is applied on a interface, all previously advertised routes contained by the summarization address will be suppresed, and the new summarized route is advertised instead.

**OBS** - This can cause issues when having networks that are not desirable to be advertised.

This can however be somewhat solved by using the `leak-map` option, which allows to only discard routes belonging in an route-map.

To prevent looping, a discard route (Null route) is will be used for the summary route. This results in packages being discarded, when the destination network doesn't exist in the routing table.

## Stub router
<img src=../assets/EIGRP_Stub.png width=400>

The EIGRP stub functionality prevents scenarios like this from happening and allows an EIGRP router to conserve router resources.    
An EIGRP stub router, depening on the configuration, does not advertise routes that it learns from other EIGRP peers.

- **Receive-only:** The stub router will not advertise any network.
- **Connected:** allows the stub router to advertise directly connected networks.
- **Static:** allows the stub router to advertise static routes (you have to redistribute them).
- **Summary:** allows the stub router to advertise summary routes.
- **Redistribute:** allows the stub router to advertise redistributed routes.

The EIGRP stub router announces itself as a stub within the EIGRP hello packet.  
This provides faster convergence within an EIGRP autonomous system because it decreases the size of the query domain for that prefix.

## Path Metric Calculation
When calculating the paths for a destination network. All paths to a destination network must be added together, including the path after the destination router.  
The reason for this, is that the destination router could have multiple redundant links. This way the fastest link will be choosen over a slower link.

<img src=../assets/EIGRP_Metric.png width=400>
<img src=../assets/EIGRP_Wide_Metric.png width=650>

When calculating the metric for a path, one of the formulas above is used.  
Since the classic metric, especially due to the delay constant, didn’t scale well with higher-speed interfaces, like 10 gbps and 20 gbps, a Wide metric was added, including and extended attribute for jitter, lag or other future parameters.

As long as the K6 value, isn’t used. The Wide metric are backwards compatible. However, since the Wide metric is scaled by 65.535, instead of 256, which supports interface speeds up to 655 Terabits, it has to be rescaled to be used in a mix setup, the unscaled bandwidth can be found using a separate formula, not listed here.

|Media type	|Link Speed (kbps)|Delay|Metric|
|---|---|---|---|
|Serial	|64	|20.000 μs	|40,512,000|
|T1	|1544	|20.000 μs	|2.170.031|
|Ethernet	|10.000	|1000 μs	|281.600|
|FastEthernet	|100.000	|100 μs	|28.160|
|GigabitEthernet	|1.000.000	|10 μs	|2816|
|10 GigabitEthernet	|10.000.000	|10 μs	|512|
|11 GigabitEthernet	|11.000.000	|10 μs	|256|
|20 GigabitEthernet	|20.000.000	|10 μs	|256|

## Router ID
By default the Router ID is set dynamically, but can also be set manually using the `eigrp Router-id <32-bit router ID>` command.
The algorithm for dynamically choosing the EIGRP RID uses the following order:

1. Highest IPv4 address of any up loopback interfaces.
2. If there are not any up loopback interfaces, the highest IPv4 address of any active up physical interfaces becomes the RID when the EIGRP process initializes.

## Configuration
### EIGRP
    Router eigrp <AS number>
    eigrp router-id <32-bit Router ID>
    Network <Network adress> [Wildcard mask]
    Passive-interface [<Interface> | Default]

### EIGRPv6
    ipv6 unicast-routing
    ipv6 router eigrp <AS number>
    eigrp router-id <32-bit Router ID>
    int <interface>
    ipv6 eigrp <AS number>

### Named EIGRP IPv4
    Router eigrp <Virtual-Instance name>
    address-family ipv4 autonomous-system <AS number>
    network <network address> <Wildcard mask>
    eigrp router-id <32-bit Router ID>
    af-interface [<interface> | default]
    passive-interface !Supress updates
    or
    shutdown !Disable EIGRP address-family on interface

### Named EIGRP IPv6
    ipv6 unicast-routing
    Router eigrp <Virtual-Instance name>
    address-family ipv6 autonomous-system <AS number>
    eigrp router-id <32-bit Router ID>
    af-interface [<interface> | default]
    passive-interface !Supress updates
    or
    shutdown !Disable EIGRP address-family on interface

## Additional Configuration
### Summarization
    int <interface>
    ip summary-address eigrp as-number network subnet-mask [leak-map route-map-name]
    or
    af-interface [<interface> | default]
    summary-address network subnet-mask [leak-map route-map-name]

### Stub Configuration
    Router eigrp <AS number>
    eigrp stub [connected | receive-only | redistributed | static | summary]
    or
    Router eigrp <Virtual-Instance name>
    address-family [ipv4 | ipv6] autonomous-system <AS number>
    eigrp stub [connected | receive-only | redistributed | static | summary]

### Altering the K values
    int <interface>
    metric weights <TOS> <K1> <K2> <K3> <K4> <K5> [<K6>] !TOS is always “0”

### Altering the delay value
    int <interface>
    delay <number> !Microseconds

### Authentication on EIGRP 
    key chain <keychain-name>
    key 2
    key string <secret key>
    int <interface>
    ip authentication mode eigrp <as-number> md5
    ip authentication key-chain eigrp <as-number> <keychain-name>

### Authentication on Named EIGRP 
    key chain <keychain-name>
    key <number> !Must be between 0 to 2147483647
    key string <secret key>
    router eigrp EIGRP-NAMED
    address-family ipv4 unicast autonomouse-system <as-number>
    authentication mode <md5 | hmacsha-256>
    authentication mode <md5 | hmacsha-256>
    authentication key-chain <keychain-name>

## Redistribution
### EIGRP
    Router eigrp <Virtual-Instance name>
    redistribute <Protocol | ...> [metric [bandwitdh delay reliability effective-bandwitdh MTU]]

### EIGRPv6
    ipv6 unicast-routing
    ipv6 router eigrp <Virtual-Instance name>
    redistribute <Protocol | ...> [metric [bandwitdh delay reliability effective-bandwitdh MTU]]

### EIGRP Named configuration
    Router eigrp <Virtual-Instance name>
    address-family ipv6 autonomous-system <AS number>
    Topology base
    redistribute <Protocol | ...> [metric [bandwitdh delay reliability effective-bandwitdh MTU]]

### Example
    redistribute ospf metric 100000 1000 255 1 1500