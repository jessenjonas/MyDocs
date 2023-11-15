---
tags:
    - Networking
    - Security
title: Cisco VPN
---
# Cisco VPN

## Configuring Site-to-Site VPN (S2S)
The first task is to configure the ISAKMP policy for IKE Phase 1.  
The ISAKMP policy lists the SAs that the router is willing to use to establish the IKE Phase 1 tunnel.  
The Cisco IOS comes with default ISAKMP policies already in place.  
To view the default policies, enter the **show crypto isakmp default policy** command.

### Configuring ISAKMP Policy

To configure a new ISAKMP policy, use the crypto isakmp policy command, as shown in the figure.  
The only argument for the command is to set a priority for the policy (from 1 to 10000).  
Peers will attempt to negotiate using the policy with the lowest number (highest priority).  

**NOTE!** Peers do not require matching priority numbers.

When in ISAKMP policy configuration mode, the SAs for the IKE Phase 1 tunnel can be configured.  
Use the mnemonic **HAGLE** to remember the five SAs to configure:

- **H**ash
- **A**uthentication
- **G**roup
- **L**ifetime
- **E**ncryption

    crypto isakmp policy <number>
    encryption <encryption>
    hash <hash>
    authentication <authentication method>
    group <Diffie-hellman group>
    lifetime <lifetime> !Seconds

### Configuring ISAKMP Pre-sharedKey
Pre-shared key may be used for authentication between the peers.  
The administrator can either specify a host name or an IP address for the peer.

    crypto isakmp key <keystring> address <peer-address>
    crypto isakmp key <keystring> hostname <peer-hostname>

### Defining Interesting Traffic
Although the ISAKMP policy for the IKE Phase 1 tunnel is configured, the tunnel does not yet exist.  
Interesting traffic must be detected before IKE Phase 1 negotiations can begin.

    ip access-list extended <ACL Name>
    permit ip <source> <wildcard> <destination> <wildcard>

### Configuring IPsec Transform Set
The next step is to configure the set of encryption and hashing algorithms that will be used to transform the data sent through the IPsec tunnel. This is called the transform set.  
During IKE Phase 2 negotiations, the peers agree on the IPsec transform set to be used for protecting interesting traffic.

    crypto ipsec transform-set <tag> esp-aes 256 esp-sha-hmac !Example - There are more combinations

### Configuring Crypto Map
Now that the interesting traffic is defined, and an IPsec transform set is configured, it is time to bind those configurations with the rest of the IPsec policy in a crypto map.  

1. Bind the ACL and the transform set to the map.
2. Specify the peer’s IP address.
3. Configure the DH group.
4. Configure the IPsec tunnel lifetime.

The sequence number is important when configuring multiple crypto map entries.

    crypto map <mapName> <SequenceNumber> {ipsec-isakmp | ipsec-manual}
    match address <ACL Name>
    set transform-set <tag>
    set peer <peer IP>
    set pfs <DH group>

*Use the crypto map map-name seq-num command without any keyword to modify the existing crypto map entry or profile.*

| Parameter | Description |
|---|---|
| map-name | Identifies the crypto map set.|
| seq-num  | Sequence number you assign to the crypto map entry. |
| ipsec-isakmp | Indicates that IKE will be used to establish the IPsec for protecting the traffic specified by this crypto map entry. |
| ipsec-manual | Indicates that IKE will not be used to establish the IPsec SAs for protecting the traffic specified by this crypto map entry. |

### Apply to interface
Apply the following to the tunnel Interfaces

    interface <interface>
    crypto map <mapName>

### Verify Configuration
Use the following command to verify the configuration

    show crypto map