from Network.Devices import Spokes, Area_0, Area_10, Area_23, Firewall_A_10, Firewalls_A_51, Area_51, Switches
from itertools import chain
from netmiko import ConnectHandler
from rich import print as rp
from csv import writer


rp('[cyan]----------DHCP Helper address----------[/cyan]')
for devices in Spokes.values():
    c = ConnectHandler(**devices)
    c.enable()
    commands = ['int e0/0', 'ip helper-address 192.168.10.254']
    rp(c.send_config_set(commands))
    c.save_config()
    c.disconnect()
   


print('\n')
rp('[cyan]----------Configuring SNMP on all devices----------[/cyan]')
for devices in chain(Firewall_A_10.values(), Firewalls_A_51.values(), Area_0.values(),
                     Area_10.values(),Area_23.values(), Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    commands = ['ip access-list standard SNMP-ACL',
                'permit host 192.168.10.254',
                'snmp-server system-shutdown',
                'snmp-server community device_snmp SNMP-ACL',
                'snmp-server enable traps config',
                'snmp-server host 192.168.10.254 traps version 2c device_snmp']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()



print('\n')
rp('[cyan]----------Configuring Netflow on Area 23 and Spoke routers----------[/cyan]')
for devices in chain( Spokes.values(), Area_23.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    interface = input(f'{host}{" "}Source Interface: ')
    udp_port  = input(f'{host}{" "}UDP port: ')
    commands  = ['ip flow-export version 9',
                 'ip flow-export source '+interface,
                 'ip flow-export destination 192.168.10.254 '+udp_port,
                 'ip flow-cache timeout active 1',
                 'interface '+interface,
                 'ip nbar protocol-discovery',
                 'ip flow ingress',
                 'ip flow egress',
                 ]
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()
    


print('\n')
rp('[cyan]----------Configuring Access-class restricting remote connection to 192.168.2.0/24----------[/cyan]')
for devices in chain(Firewall_A_10.values(), Firewalls_A_51.values(), Area_0.values(),Area_10.values(),
                     Area_23.values(), Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    commands = ['ip access-list extended VTY_ACL',
                'permit tcp 192.168.2.0 0.0.0.255 any eq 22',
                'permit tcp host 192.168.11.100 any eq 22',
                'deny tcp any any log',
                'line vty 0 4',
                'logging sync',
                'no privilege level 15',
                'access-class VTY_ACL in']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()



print('\n')
rp('[cyan]----------Configuring Cryptography on DMVPN Network---------[/cyan]')
secret_key = input('Input pre-shared key: ')
for devices in chain(Firewalls_A_51.values(),Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable() 
    commands = ['crypto isakmp policy 100',
                'hash sha256',
                'authentication pre-share',
                'group 14',
                'lifetime 7200',
                'encryption aes 192',
                'crypto isakmp key '+secret_key+' address 0.0.0.0',
                'crypto ipsec transform-set Crypt-ts esp-sha256-hmac esp-aes 192',
                'mode transport',
                'crypto ipsec profile Crypt_profile',
                'set transform-set Crypt-ts']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()



print('\n')
rp('[cyan]----------Configuring NAT on Spoke routers---------[/cyan]')
for devices in chain(Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    nat_out_intf = input(f'{host}{" "} NAT Outside Interface: ')
    nat_in_intf = input(f'{host}{" "} NAT Inside Interface: ')
    LAN_IP = input(f'{host}{" "} LAN IP address: ')
    wildmask = input(f'{host}{" "} Wildcard Mask: ')

    commands = ['ip access-list standard nat_acl',
                'permit '+LAN_IP+' '+wildmask,
                'interface '+nat_in_intf,
                'ip nat inside',
                'interface '+nat_out_intf,
                'ip nat outside',
                'ip nat inside source list nat_acl interface '+nat_out_intf+ ' overload',
                ]
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()



print('\n')
rp('[cyan]----------Configuring NTP on DMVPN network---------[/cyan]')
for devices in chain(Area_51.values(), Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    commands = ['ip domain lookup',
                'ip name-server 8.8.8.8 192.168.10.254',
                'ntp server ke.pool.ntp.org',
                'clock timezone UTC +3',
                'service timestamps log datetime localtime year',
                'service timestamps debug datetime localtime year']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()



print('\n')
rp('[cyan]----------Configuring MOTD banner---------[/cyan]')
for devices in chain(Firewall_A_10.values(),Firewalls_A_51.values(), Area_0.values(),Area_10.values(),
                     Area_23.values(),Area_51.values(), Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    commands = [
                'banner login @',
               f'{"*"*50}',
               f'{" "*10}{host}-ROUTER',
               f'{" "*5}Configured using CLI and Netmiko',
               f'{" "}Unauthorized access is strictly forbidden',
               f'{"*"*50}',
               '@']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()



print('\n')
rp('[cyan]----------Configuring Syslog---------[/cyan]')
for devices in chain(Firewall_A_10.values(), Firewalls_A_51.values(), Area_0.values(),
                     Area_10.values(),Area_23.values(),Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    commands = ['logging monitor informational',
                'logging host 192.168.10.254']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()



print('\n')    
rp('[cyan]----------Verifying OSPF routes----------[/cyan]')
filepath = input('Input OSPF backup filepath: ')
for devices in chain(Firewall_A_10.values(), Firewalls_A_51.values(), Area_0.values(),
                     Area_10.values(),Area_23.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip route ospf',use_textfsm=True)
    with open (f'{filepath}/{host}{" "}Routes','w') as f:
        f.write(output)
        c.disconnect()
    rp(f'{host}{" "}Routes have been documented!!')



print('\n')
rp('[cyan]----------Verifying EIGRP routes----------[/cyan]')
filepath = input(f'Input EIGRP backup filepath: ')
for devices in chain(Firewalls_A_51.values(),Spokes.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip route eigrp',use_textfsm=True)
    with open (f'{filepath}/{host}{" "}Routes','w') as f:
        f.write(output)
        c.disconnect()
    rp(f'{host}{" "}Routes have been documented!!')



print('\n')
rp('[cyan]----------Getting Devices\' running configurations----------[/cyan]')
filepath = input('Input backup filepath: ')
for devices in chain(Spokes.values(),Firewall_A_10.values(),Area_0.values(),Area_10.values(),Area_23.values(),
                     Firewalls_A_51.values(), Area_51.values(),Switches.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    output = c.send_command('show run')
    with open (f'{filepath}/{host}','w') as f:
        f.write(output)
        c.disconnect()
    rp(f'The running-configuration of ',host,' has been successfully backed up!!')



print('\n')
rp('[cyan]----------Device Inventory----------[/cyan]')
filepath = input('Inventory filepath: ')
with open (f'{filepath}/Data.csv', 'w')as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP address','Software Image','Version','Serial number'])
    for devices in chain(Firewall_A_10.values(), Firewalls_A_51.values(), Area_0.values(),
                         Area_10.values(),Area_23.values(),Spokes.values(), Area_51.values(), Switches.values()):
        c = ConnectHandler(**devices)
        c.enable()
        output = c.send_command('show version',use_textfsm=True)[0]

        hostname = output['hostname']
        ip_addr  = devices['ip']
        image    = output['software_image']
        version  = output['version']
        serial   = output['serial']

        write_data.writerow([hostname,ip_addr,image,version,serial])
        rp(f'Finished taking {hostname} Inventory')
        c.disconnect()



print('\n')
for devices in chain(Firewall_A_10.values(), Firewalls_A_51.values(), Area_0.values(), Switches.values(),
                     Area_10.values(), Area_23.values(), Spokes.values(), Area_51.values()):
    c = ConnectHandler(**devices)
    c.enable()
    output = c.send_command('show version', use_textfsm=True)[0]
    rp(f'[cyan]---------------{output["hostname"]}---------------[/cyan]\n')
    for key, value in output.items():
        rp((f'{key:>15} : {value}'))
    print('\n')
            