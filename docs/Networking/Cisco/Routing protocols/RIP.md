---
tags:
    - Networking
title: RIP
---
# RIP
## What is RIP
RIP is an distance vector routing protocol and is using hop count as its routing metric - the less hops to the destination, the better.

*[RIP]: Routing Information Protocol

To prevent routing loop, RIP implements split-horizion, which prevent routing information being sent out the same interface as it was received.  
Combining split-horizon with poison reverse resulting a metric of 16, where a metric of 15 is the max amount of hops before a router consider a route as unreachable, therefore it tells the neighbors that a route is inaccesible rather than not saying anything.

RIPv1, among other limitiations, is limited to classfull routing and are therefore obsolete. Use RIPv2 instead, at least.

| RIPv2                  | RIPng (Next Gen)          | Facts        |                  |
| ---------------------- | ------------------------- | ------------ | ---------------- |
| Classless routing      | Same as RIPv2             | Type         | Distance Vector  |
| Triggered updates      | IPv6                      | Algorithm    | Bellman-Ford     |
| Global configuration   | Interface configuration   | Standard     | Non proprietary  |
|                        |                           | Protocol     | UDP              |
|                        |                           | Group        | IGP              |

## Configuration
### RIPv2
    Router rip
    Version 2
    No auto-summary
    Network <Network adress>
    Passive-interface [<Interface> | Default]

### RIPng
    ipv6 unicast-routing
    Router rip <Name>
    exit
    int <interface>
    ipv6 rip <Name> enable