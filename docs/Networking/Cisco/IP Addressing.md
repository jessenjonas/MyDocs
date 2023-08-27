---
tags:
    - Networking
title: IP Addressing
---
# IP Addressing
## IPv4 Addressing
### Router & Access Point
    Int <interface>
    ip address [<ip> <subnet> | dhcp]
    no shutdown

### Switch - L3
    ip routing
    Int <interface>
    no switchport
    ip address [<ip> <subnet> | dhcp]
    no shutdown

### Switch - L2 (Management IP)
    Int <vlanID>
    ip address [<ip> <subnet> | dhcp]
    no shutdown
## IPv6 Addressing