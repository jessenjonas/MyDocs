---
tags:
    - Networking
title: BGP
---
# BGP
*[RID]: Router-ID
*[SAFE]: Subsequent Address Family Identifier
*[AFI]: Address Family Identifier
*[PBR]: Policy Based Routing
*[BGP]: Border Gateway Protocol
*[MP-BGP]:Multiprotocol-BGP

<img src=../assets/BGP.png width=500>

## What is BGP

| BGP                  | MP-BGP         | Facts        |                  |
| ---------------------- | ------------------------- | ------------ | ---------------- |
| IPv4<br>*Global config*      | Pv6 over IPv6 & IPv6 over IPv4<br>*Global config*             | Type         | Path Vector  |
|       | SAFI & AFI   | Algorithm    | PBR     |
|    |    | Standard     | Non proprietary  |
|                        |                           | Protocol     | TCP              |
|                        |                           | Group        | EGP              |

## Router ID

## Configuration
### BGP
R1(config)# Router bgp <AS-number>
R1(config-rtr)# Neighbor <Neighbor IP> remote-as <Remote AS-number>
R1(config-rtr)# Network <Network adress> [<Subnet mask>]

### MP-BGP | IPv6 over IPv4
    ipv6 unicast-routing
    Router bgp <AS-number>
    Neighbor <Neighbor IPv4> remote-as <Remote AS-number>
    Address-family IPv6
    Neighbor <Neighbor IPv4> activate
    Network <Network IPv6/Prefix-lenght>

### MP-BGP | IPv6 over IPv6
    ipv6 unicast-routing
    Router bgp <AS-number>
    bgp router-id <32-bit Router ID>
    Neighbor <Neighbor IPv6> remote-as <Remote AS-number>
    Address-family IPv6
    Neighbor <Neighbor IPv6> activate
    Network <Network IPv6/Prefix-lenght>

## Additional Configuration
### Manupulate
    Neighbor <Neighbor IPv4> route-map <name> out
    route-map <name> permit <sequence number>
    set ipv6 next-hop <IPv6 address on interface on link>

## Redistribution
### BGP
    Router bgp <AS-number>
    redistribute <Protocol | ...> [Route-map <name>]

### MP-BGP
    Router bgp <AS-number>
    Address-family IPv6
    redistribute <Protocol | ...> [Route-map <name>]