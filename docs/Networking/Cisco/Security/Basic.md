---
tags:
    - Networking
    - Security
title: Cisco Basic Security
---
# Basic Security
## Priviledge Levels
By default, the Cisco IOS software CLI has two levels of access to commands:

- **User EXEC mode (privilege level 1)**  
This provides the lowest EXEC mode user privileges and allows only user-level commands available at the Router> prompt.  
- **Privileged EXEC mode (privilege level 15)**  
This includes all enable-level commands at the Router# prompt.

There are 16 privilege levels in total, as listed below. The higher the privilege level, the more router access a user has. Commands that are available at lower privilege levels are also executable at higher levels.

- **Level 0:** Predefined for user-level access privileges. Seldom used, but includes five commands: disable, enable, exit, help, and logout.
- **Level 1:** The default level for login with the router prompt Router >. A user cannot make any changes or view the running configuration file.
- **Levels 2 - 14:** May be customized for user-level privileges. Commands from lower levels may be moved up to another higher level, or commands from higher levels may be moved down to a lower level.
- **Level 15:** Reserved for the enable mode privileges (enable command). Users can change configurations and view configuration files.

### Command example

    Router(config)# privilege mode {level level|reset} command

| Command | Description |
|---|---|
| *mode* | Specifies the configuration mode. Use the **privilege ?** command to see a complete list of router configuration modes available on your router. |
| level | (Optional) Enables setting a privilege level with a specified command. |
| *level | (Optional) The privilege level that is associated with a command. You can specify up to 16 privilege levels, using numbers 0 to 15. |
| reset | 	(Optional) Resets the privilege level of a command. |
|*command* | (Optional) Argument to use when you want to reset the privilege level. |

There are two methods for assigning passwords to the different privilege levels:  
To a user that is granted a specific privilege level, use the username name privilege level secret password global configuration mode command
To the privilege level, use the enable secret level level password global configuration mode command

Use the username command to assign a privilege level to a specific user. Use the enable secret command to assign a privilege level to a specific EXEC mode password.

    Router(config)# !Level 5 and SUPPORT user configuration
    Router(config)# privilege exec level 5 ping
    Router(config)# enable algorithm-type scrypt secret level 5 cisco5
    Router(config)# username SUPPORT privilege 5 algorithm-type scrypt secret cisco5

### Limitiations
- There is no access control to specific interfaces, ports, logical interfaces, and slots on a router.
- Commands available at lower privilege levels are always executable at higher levels.
- Commands specifically set at a higher privilege level are not available for lower privileged users.
- Assigning a command with multiple keywords allows access to all commands that use those keywords. For example, allowing access to show ip route allows the user access to all show and show ip commands.

## Views (Role Based CLI)
<img src=../assets/Role-Based+Views+Role-Based+Views.jpg width=800>

Role-based CLI provides three types of views that dictate which commands are available:

**Note:** Max 15 views (excluding root view)

- **Root View**  
To configure any view for the system, the administrator must be in root view. Root view has the same access privileges as a user who has level 15 privileges. However, a root view is not the same as a level 15 user. Only a root view user can configure a new view and add or remove commands from the existing views.

- **CLI View**  
A specific set of commands can be bundled into a CLI view. Unlike privilege levels, a CLI view has no command hierarchy and no higher or lower views. Each view must be assigned all commands associated with that view. A view does not inherit commands from any other view. Additionally, the same commands can be used in multiple views.

- **Superview**  
    A superview consists of one or more CLI views.  
    Administrators can define which commands are accepted and which configuration information is visible.
  
    Superviews allow a network administrator to assign users and groups of users multiple CLI views at once, instead of having to assign a single CLI view per user with all commands associated with that one CLI view.

    Superviews have several specific characteristics:

    - A single CLI view can be shared within multiple superviews.
    - Commands cannot be configured for a superview.
    - An administrator must add commands to the CLI view and add that CLI view to the superview.
    - Users who are logged into a superview can access all the commands that are configured for any of the CLI views that are part of the superview.
    - Each superview has a password that is used to switch between superviews or from a CLI view to a superview.
    - Deleting a superview does not delete the associated CLI views. The CLI views remain available to be assigned to another superview.

*AAA must be enabled using the* ***aaa new-model*** *command, before an view can be created.*

### Accessing View

    Router# enable [view [view-name]]


| Parameter | Description |
|---|---|
| view | This parameter enters root view if no view-name is specified, which enables an administrator to configure CLI views. The view parameter is required to configure a CLI view. |
| view-name | (Optional) This parameter enters or exits a specified CLI view. This parameter can be used to switch from one CLI view to another CLI view. |


### Configure View

    Router(config)# parser view *view-name* !Create view
    Router(config-view)# secret *password* !Sets password to protect access to view
    Router(config-view)# commands *parser-mode* {include | include-exclusive | exclude} [all] [interface interface-name | command]

| Commands | Description |
|---|---|
| commands | Adds commands or interfaces to a view. |
| *parser-mode* | The mode in which the specified command exists; for example, EXEC mode. |
| include | Adds a command or an interface to the view and allows the same command or interface to be added to other views. |
| include-exclusive | Adds a command or an interface to the view and excludes the same command or interface from being added to all other views. |
| exclude  | Excludes a command or an interface from the view. |
| all | 	A "wildcard" that allows every command in a specified configuration mode that begins with the same keyword or every subinterface for a specified interface to be part of the view.. |
| interface *interface-name* | Interface that is added to the view. |
|*command* | Command that is added to the view. |

### Configure Superview

    Router(config)# parser view *view-name* !Create superview
    Router(config-view)# secret *password* !Sets password to protect access to view
    Router(config-view)# view *view-name* !Assign an existing view

### Verify CLI Views
From the root view, use the following command to see a summary of all views. Notice how the asterisk identifies superviews.

    Router# show parser view all command

## Secure IOS image and Configuration file
The Cisco IOS resilient configuration feature allows for faster recovery if someone maliciously or unintentionally reformats flash memory or erases the startup configuration file in nonvolatile random-access memory (NVRAM).  
The feature maintains a secure working copy of the router IOS image file and a copy of the running configuration file.  
These secure files cannot be removed by the user and are referred to as the primary bootset.

- The configuration file in the primary bootset is a copy of the running configuration that was in the router when the feature was first enabled.
- The feature secures the smallest working set of files to preserve persistent storage space.
- No extra space is required to secure the primary Cisco IOS image file. The feature automatically detects image or configuration version mismatch.
- Only local storage is used for securing files, eliminating scalability maintenance challenges from storing multiple images and configurations on TFTP servers.
- The feature can be disabled only through a console session.

**Note:** The feature is only available on older routers that support a PCMCIA Advanced Technology Attachment (ATA) flash interface.  
Newer routers such as the ISR 4000 do not support this feature.

### Enabling IOS Image Resilience Feature

    R1(config)# secure boot-image !Securing Boot Image
    R1(config)# secure boot-config !Securing Boot Config

Use the **show secure bootset** command to verify the existence of the archive.

### Restore a primary bootset from a secure archive
Reload into ROM monitor (ROMmon) mode, boot into the secured bootset image, in Global Config restore the configuration to a filename of your choice using the *secure boot-config restore* command followed by the flash memory location.  
Then exit Global Config and issue the copy command to copy the rescued config file to the running configuration.

    Router# reload 
    <Issue Break sequence, if necessary> 
    rommon 1 > dir flash0:
    rommon 2 > boot flash0:c2900-universalk9-mz.SPA.154-3.M.bin <Router reboots with specified image>
    Router> enable
    Router# conf t
    Router(config)# secure boot-config restore flash0:*rescue-cfg*
    Router(config)# end 
    Router# copy flash0:rescue-cfg running-config

### remotely copy Secured IOS and configuration files
The Secure Copy Protocol (SCP) feature is used to remotely copy these files.  
SCP provides a secure and authenticated method for copying router configuration or router image files to a remote location.

The process to configure a router for server-side SCP with local AAA is:
1. Configure SSH, if not already configured.
2. For local authentication, configure at least one local database user with privilege level 15.
3. Enable AAA with the aaa new-model global configuration mode command.
4. Use the aaa authentication login default local command to specify that the local database be used for authentication.
5. Use the aaa authorization exec default local command to configure command authorization. In this example, all local users will have access to EXEC commands.
6. Enable SCP server-side functionality with the ip scp server enable command.

Now assume that we want to securely copy the backup configuration of a router named R2 to the SCP server, which is R1.  
As shown in the command output below, we would use the copy command on R2, and specify specify the source file location first (flash0:R2backup.cfg), and then the destination (scp:).  
After answering the series of prompts to establish a connection to the SCP server on R1, the file will be copied.

    R2# copy flash0:R2backup.cfg scp: 
    Address or name of remote host []? 10.1.1.1 
    Destination username [R2]? Bob 
    Destination filename [R2backup.cfg]?  
    Writing R2backup.cfg  
    Password: <cisco12345> 

On R1, you can enter the debug ip scp command to watch the transfer proceed, as shown in the following example. The most common authentication issue is an incorrect username/password combination. There is also an authentication failure if the username/password combination was not configured with the privilege 15 keyword on the SCP server.

    R1# debug ip scp
    Incoming SCP debugging is on 
    R1# 
    *Feb 18 20:37:15.363: SCP: [22 -> 10.1.1.2:61656] send  *Feb 18 20:37:15.367: SCP: [22 <- 10.1.1.2:61656] recv C0644 1381 R2backup.cfg *Feb 18 20:37:15.367: SCP: [22 -> 10.1.1.2:61656] send

## Password Recovery
Using the *no service password-recovery* Global Config command, all access to ROMmon mode is disabled.  
This way an attacker who gains physical access to a router, and tries to boot into ROMmon, the startup configuration will be erased, completely, and it will boot into the factory default configuration.

    no service password-recovery

*When the router is booted, the initial boot sequence displays a message stating PASSWORD RECOVERY FUNCTIONALITY IS DISABLED.*

**CAUTION: **If the router flash memory does not contain a valid Cisco IOS image because of corruption or deletion, the ROMmon xmodem command cannot be used to load a new flash image. To repair the router, an administrator must obtain a new Cisco IOS image on a flash SIMM or on a PCMCIA card. However, if an administrator has access to ROMmon they can restore an IOS file to flash memory using a TFTP server. Refer to Cisco.com for more information regarding backup flash images.

## AutoSecure
Released in IOS version 12.3, Cisco AutoSecure is a feature that is initiated from the CLI and executes a script.  
AutoSecure first makes recommendations for fixing security vulnerabilities and then modifies the security configuration of the router, as shown in the figure.

AutoSecure can lock down the management plane functions and the forwarding plane services and functions of a router. There are several management plane services and functions:

- Secure BOOTP, CDP, FTP, TFTP, PAD, UDP, and TCP small servers, MOP, ICMP (redirects, mask-replies), IP source routing, Finger, password encryption, TCP keepalives, gratuitous ARP, proxy ARP, and directed broadcast
- Legal notification using a banner
- Secure password and login functions
- Secure NTP
- Secure SSH access
- TCP intercept services

There are three forwarding plane services and functions that AutoSecure enables:

- Cisco Express Forwarding (CEF)
- Traffic filtering with ACLs
- Cisco IOS firewall inspection for common protocols

### Configure AutoSecure
Use the auto secure command to enable the Cisco AutoSecure feature setup.  
This setup can be interactive or non-interactive.

    Router# auto secure {no-interact | full} [forwarding | management] [ntp | login | ssh | firewall | top-intercept]

| Optional Parameters | Description |
|---|---|
| no-interact | The user will not be prompted for any interactive configurations. No interactive dialogue parameters will be configured, including usernames or passwords. |
| full | The user will be prompted for all interactive questions. This is the default setting. |
| forwarding | Only the forwarding plane[^1] will be secured. |
| management | Only the management plane[^1]will be secured. |
| ntp | Specifies the configuration of the NTP feature in the AutoSecure CLI. |
| login | Specifies the configuration of the login feature in the AutoSecure CLI. |
| ssh | Specifies the configuration of the SSH feature in the AutoSecure CLI. |
| firewall | Specifies the configuration of the firewall feature in the AutoSecure CLI. |
| tcp-intercept | Specifies the configuration of the TCP intercept feature in the AutoSecure CLI. |

[^1]: Please see the [Basic configuration](/Networking/Cisco/Basic/#plane) for further details about Management plane and forwarding plane.

## AAA
AAA network security services provide the primary framework to set up access control on a network device.  
AAA is a way to control who is permitted to access a network (**authenticate**) and what they can do while they are there (**authorize**).  
AAA also allows auditing of the actions that users perform while accessing the network (**accounting**).

Network and administrative AAA security in the Cisco environment has three functional components:

- **Authentication -** Users and administrators must prove their identity before accessing the network and network resources.  
Authentication can be established using username and password combinations, challenge and response questions, token cards, and other methods.  
For example: “I am user ‘student’ and I know the password to prove it.”
- **Authorization -** After the user is authenticated, authorization services determine which resources the user can access and which operations the user is allowed to perform.  
An example is “User ‘student’ can access host serverXYZ using SSH only.”
- **Accounting and auditing** - Accounting records what the user does, including what is accessed, the amount of time the resource is accessed, and any changes that were made.  
Accounting keeps track of how network resources are used. An example is "User 'student' accessed host serverXYZ using SSH for 15 minutes."

### Authentication Modes
AAA Authentication can be used to authenticate users for administrative access or it can be used to authenticate users for remote network access.  
Cisco provides two common methods of implementing AAA services:
- **Local AAA Authentication**
- **Server-Based AAA Authentication:** The router uses either the Remote Authentication Dial-In User Service (RADIUS) or Terminal Access Controller Access Control System (TACACS+) protocols to communicate with the AAA server.  
When there are multiple routers and switches, server-based AAA is more appropriate because accounts can be administered from a central location rather than on individual devices.

### Configure Local AAA

    Router(config)# aaa authentication login {default | list-name} method1…[ method4 ]

| Command | Description |
|---|---|
| default  | Uses the listed authentication methods that follow this keyword as the default list of methods when a user logs in. |
| list-name  | Instead of using default list name, the administrator may wish to specify a name for documentation purposes. The name can be up to 31 characters. |
| method1...[method4]  | Identifies the list of methods that the AAA authentication process will query in the given sequence. At least one method must be specified. A maximum of four methods may be specified. |

| Method Type Keywords | Description |
|---|---|
| enable | Uses the enable password for authentication. |
| local | Uses the local username database for authentication. |
| local-case | Uses case-sensitive local username authentication.|
| none | Uses no authentication. |
| group radius | Uses the list of all RADIUS servers for authentication.|
| group tacacs+ | Uses the list of all TACACS+ servers for authentication. |
| group *group-name* | Uses a subset of RADIUS or TACACS+ servers for authentication as defined by the aaa group server radius or aaa group server tacacs+ command. |

Then apply it on the VTY lines:

    login authentication <list>

### Configure Server AAA

#### TACACS+ Authentication
    
    R1(config)# aaa new-model 
    R1(config)# tacacs server Server-T
    R1(config-server-tacacs)# address ipv4 192.168.1.101
    R1(config-server-tacacs)# single-connection
    R1(config-server-tacacs)# key TACACS-Pa55w0rd !Shared Secret
    R1(config-server-tacacs)# exit

#### RADIUS Authentication

    R1(config)# aaa new-model
    R1(config)# radius server SERVER-R
    R1(config-radius-server)# address ipv4 192.168.1.100 auth-port 1812 acct-port 1813
    R1(config-radius-server)# key RADIUS-Pa55w0rd !Shared Secret
    R1(config-radius-server)# exit 

#### Authorization

- **network** - for network services such as PPP and SLIP
- **exec** - for User EXEC terminal sessions
- **commands level** - command authorization attempts authorization for all EXEC mode commands, including global configuration commands, associated with a specific privilege level

    Router(config)# aaa authorization (network | exec | commands level) {default | list-name} method1… [method4]

**Note:** When AAA authorization is not enabled, all users are allowed full access.  
After authentication is started, the default changes to allow no access.  
This means that the administrator must create a user with full access rights before authorization is enabled, as shown in the example.  
Failure to do so immediately locks the administrator out of the system the moment the aaa authorization command is entered. The only way to recover from this is to reboot the router.  
If this is a production router, rebooting might be unacceptable.  
Be sure that at least one user always has full rights.

#### Accounting

- **network** - Runs accounting for all network-related service requests, including PPP.
- **exec** - Runs accounting for the EXEC shell session.
- **connection** - Runs accounting on all outbound connections such as SSH and Telnet.

    Router(config)# aaa accounting {network | exec | connection} {default | list-name} {start-stop | stop-only | none } [broadcast] method1...[method4]

Next, the record type, or trigger, is configured. 
The trigger specifies what actions cause accounting records to be updated. 
Possible triggers include:

- **start-stop** - Sends a "start" accounting notice at the beginning of a process and a "stop" accounting notice at the end of a process.
- **stop-only** - Sends a "stop" accounting record for all cases including authentication failures.
- **none** - Disables accounting services on a line or interface.

### TACACS+ vs RADIUS
#### TACACS+
A Cisco enhancement to the original TACACS protocol. Despite its name, TACACS+ is an entirely new protocol that is incompatible with any previous version of TACACS.  
TACACS+ is supported by the Cisco family of routers and access servers.

TACACS+ provides separate AAA services.  
Separating the AAA services provides flexibility in implementation because it is possible to use TACACS+ for authorization and accounting while using another method of authentication.

The extensions to the TACACS+ protocol provide more types of authentication requests and response codes than were in the original TACACS specification.  
TACACS+ offers multiprotocol support, such as IP and legacy AppleTalk.  
Normal TACACS+ operation encrypts the entire body of the packet for more secure communications and utilizes TCP port 49.

#### RADIUS
An open IETF standard AAA protocol for applications such as network access or IP mobility.  
RADIUS works in both local and roaming situations and is commonly used for accounting purposes.

The RADIUS protocol hides passwords during transmission, even with the Password Authentication Protocol (PAP), using a rather complex operation that involves Message Digest 5 (MD5) hashing and a shared secret.  
However, the rest of the packet is sent in plaintext.

RADIUS combines authentication and authorization as one process.  
When a user is authenticated, that user is also authorized.  
RADIUS uses UDP port 1645 or 1812 for authentication and UDP port 1646 or 1813 for accounting.

RADIUS is widely used by VoIP service providers.  
It passes login credentials of a SIP endpoint, such as a broadband phone, to a SIP registrar using digest authentication, and then to a RADIUS server using RADIUS.  
RADIUS is also a common authentication protocol that is utilized by the 802.1X security standard.
