---
tags:
    - Networking
title: BGP
---
# BGP
*[RID]: Router-ID
*[SAFI]: Subsequent Address Family Identifier
*[AFI]: Address Family Identifier
*[PBR]: Policy Based Routing
*[BGP]: Border Gateway Protocol
*[MP-BGP]: Multiprotocol-BGP
*[ASN]: Autonomous System Numbers
*[IANA]: Internet Assigned Numbers Authority

<img src=../assets/BGP.png width=500>

## What is BGP

BGP, opposing to EIGRP and OSPF, is an EGP, and are therefore used for cummincation between ISPs and enterprises. BGP is an succesor to EGP (Note the dual use of EGP).  
Distingushed by eBGP and iBGP, BGP, besides being external, can be internal - The configuration is the same, but iBGP is setup within the same AS.

In contrary to other routing protocols, BGP establishes neighbor relationships without explicitly advertising any networks. When an adjacency is established, neighbors will exchange their best BGP routes which includes some attributes.  
A router will use these attributes to offer the single best route for a network from the BGP table, to the ip routing table.  
This also means that the neighbor don't have the be directly connected neighbor, but can be any router that is pingable over the network.

<img src=../assets/BGP_Multi-hop_Neighbor.png width=500>

To be selected for the best BGP route, the next-hop ip address must be reachable.  
Even though that the best BGP route is being propogated to its neighbors, it doesn’t have to be in the ip routing table.

Since BGP doesn’t accept a route with its own AS number in the path, it is guranteed to loop free, and BGPs interdomain routing is usually based on policies, which differentiates it from IGPs which usually focus on the fastest route.

When having a single-homed network, BGP doesn’t provide benefit. In a multi-homed network, BGP is used to manipulate how your network traffic is being routed between multiple paths.  
Apart from keepalive messages, because of it’s reliable link, only changes are exchanged.

## Autonomous System Numbers
An organization requiring connectivity to the Internet must obtain an ASN.  
ASNs were originally 2 bytes (in the 16-bit range), which made 65,535 ASNs possible. Due to exhaustion, RFC 4893 expanded the ASN field to accommodate 4 bytes (in the 32-bit range).  
This allows for 4,294,967,295 unique ASNs, providing quite an increase from the original 65,535 ASNs.

Two blocks of private ASNs are available for any organization to use, as long as these ASNs are never exchanged publicly on the Internet.  
ASNs 64,512 through 65,535 are private ASNs in the 16-bit ASN range, and 4,200,000,000 through 4,294,967,294 are private ASNs in the extended 32-bit range.

!!! warning
    Use **ONLY** ASNs assigned by IANA, your service provider or a private ASN!  
    Failure to do so, or using another organization's ASN publicly could result in traffic loss and cause havoc on the internet!

| BGP                  | MP-BGP         | Facts        |                  |
| ---------------------- | ------------------------- | ------------ | ---------------- |
| IPv4<br>*Global config*      | Pv6 over IPv6 & IPv6 over IPv4<br>*Global config*             | Type         | Path Vector  |
|       | SAFI & AFI   | Algorithm    | PBR     |
|    |    | Standard     | Non proprietary  |
|                        |                           | Protocol     | TCP              |
|                        |                           | Group        | EGP              |

## AFI & SAFI

Originally, BGP was intended for routing of IPv4 prefixes between organizations, but RFC 2858 added Multi-Protocol BGP (MP-BGP) capability by adding an extension called the address family identifier (AFI). An address family correlates to a specific network protocol, such as IPv4 or IPv6, and additional granularity is provided through a subsequent address family identifier (SAFI), such as unicast or multicast.

The MP-BGP extensions include an AFI that describes the supported protocols, along with SAFI attribute fields that describe whether the prefix applies to the unicast or multicast routing table:

- IPv4 unicast: AFI:1, SAFI:1
- IPv6 unicast: AFI:2, SAFI:1
- IPv4 Multicast: AFI:1, SAFI:2
- IPv6 Multicast: AFI:2, SAFI:2

AFI & SAFI is configured during the configuration of MP-BGP address families with the following command `Address-family AFI [SAFI]`, where `AFI` is either IPv4 or IPv6, and `SAFI` is either Unicast or Multicast, depending on the network topology.

### Default IPv4 Unicast

The command `bgp default ipv4-unicast` is set by default and tell's the router that the AFI & SAFI, for the BGP peering session, is a IPv4 Unicast by default for the global configuration.

It doesn't prevent IPv6 prefixes to be advertised. This means that IPv4 address family routing information is advertised by default for each BGP routing session configured with the `neighbor <remote-as>` command, unless you first configure the `no bgp default ipv4-unicast` command before configuring the `<neighbor remote-as>` command.

## Router ID

By default the Router ID is set dynamically, but can also be set manually using the `Router-id <32-bit router ID>` command.
The algorithm for dynamically choosing the OSPF RID uses the following order:

1. Highest IPv4 address of any up loopback interfaces.
2. If there are not any up loopback interfaces, the highest IPv4 address of any active up physical interfaces becomes the RID.

If the conditions above aren't fulfilled, the BGP process isn't started

## Route filtering & Manipulation

*Not yet finished*

## Configuration
### BGP
    Router bgp <AS-number>
    Neighbor <Neighbor IP> remote-as <Remote AS-number>
    Network <Network adress> [<Subnet mask>]

### MP-BGP | IPv4 over IPv4
    ipv6 unicast-routing
    Router bgp <AS-number>
    Neighbor <Neighbor IPv4> remote-as <Remote AS-number>
    Address-family IPv4
    Neighbor <Neighbor IPv4> activate
    Network <Network address> mask <network mask>

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

### Summarization 
    aggregate-address prefix/prefix-length [summary-only] [as-set]
    !Summary-only don't advertise routes that overlap with the aggregate-address
    !as-set Advertise the aggregates-address AS-Path, that otherwise wouln't be advertised.

## Redistribution
### BGP
    Router bgp <AS-number>
    redistribute <Protocol | ...> [Route-map <name>]

### MP-BGP
    Router bgp <AS-number>
    Address-family [IPv6 | IPv4]
    redistribute <Protocol | ...> [Route-map <name>]