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