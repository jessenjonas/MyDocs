---
tags:
    - Networking
title: Basic
---
## Basic Configuration
    Hostname <hostname>
    Service password-encryption
    Enable secret <secret>
    Username <username> secret <secret>
    AAA new-model
    login block-for 120 attempts 2 within 120 !Block for 2 minutes, after 2 failed attempts in 2 minute period

## SSH
    Ip domain-name <DomainName>
    Crypto key generate rsa modulus 4096
    Ip SSH version 2
    Ip SSH authentication-retries 2
    Ip SSH time-out 60
    Line VTY 0 15
    Transport input SSH

## Console
    AAA authentication login default local
    Line con 0
    login authentication default
    logging synchronous

## Privilege levels
    Enable secret level 2 <secret>
    Privilege exec level 2 <command>

## Default route
    ip route 0.0.0.0 0.0.0.0 [<Next hop IP | <Exit interface>]
    ipv6 route ::/0 [<Next hop IP> | <Exit interface>]

## Plane
<img src=../Security/assets/Cisco_Plane.png width=600>

**Control-Plane** is something we call it as the heart of the process..... it is something handles that comes to the box.... if any traffic is destined or defined to the box/device... then it is handled by control plane....

**Data Plane** is something which has the forwarding information we can say that as forwarding plane.... which has the routing table and other access-rule information to define how that traffic to be handled.... on which interface it enter and how it goes out of the box.....

**Management Plane:** Whatever you do: editing/moniotoring/managing the device.... say SNMP/CLI/GUI are some functionalities we can say it as management plane... it is a sub-component of control plane we can say.... management plane can be controlled by control-plane