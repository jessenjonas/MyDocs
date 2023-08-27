---
tags:
    - Networking
title: Routing Protocols
---
# Routing Protocols

## Administrative Distance (AD)
Routing information sources are each assigned an administrative distance (AD).

Think of an administrative distance of a routing information source as the believability or trustworthiness of that routing source when comparing it to the other routing information sources.  

The table below lists the default ADs of routing information sources. The lower the AD, the more preferred the source of information

| Source of Routing information | Default AD |
|----|----|
| Connected interface | 0
Static route | 1
EIGRP summary route | 5
eBGP (External Border Gateway Protocol) | 20
EIGRP (internal) | 90
OSPF | 110
IS-IS (Intermediate System to Intermediate System) | 115
RIP | 120
ODR (On-Demand Routing) | 160
EIGRP (external) | 170
iBGP (Internal Border Gateway Protocol) | 200
Unknown (not believable) | 255 |    |