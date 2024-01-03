
**CAMPUS NETWORK**
====================

.. figure:: /Inventory/Topology.png
   :align: center

EIGRP
----------------
* Stub Router Configuration: All spoke routers are configured as stub routers, limiting 
  the query scope in the network.
* Route Filtering: Implemented to allow communication within regions and with HQ while restricting 
  inter-regional router communication.
* EIGRP Bandwidth Allocation: EIGRP is allocated 25% of the bandwidth on links participating in the 
  EIGRP process.
* EIGRP Authentication: Authentication is enabled for EIGRP neighborship to enhance security.
* EIGRP Metric Calculation: Configured to use only the delay metric value for path metric calculation 
  with a uniform delay setting of 10 microseconds.
* Passive Interfaces: LAN-facing interfaces are configured as passive to reduce unnecessary 
  EIGRP traffic.
* EIGRP add-path feature is used to advertise redundant links to spoke routers.

OSPF
-----------------
* Area 23: Configured as a totally stub area, propagating only a default type 3 LSA.

.. code-block:: bash
   
   Gateway of last resort is 10.0.23.1 to network 0.0.0.0
   O*IA  0.0.0.0/0 [110/10001] via 10.0.23.1, 00:25:14, Ethernet0/1


* Area 10: Configured as an NSSA, receiving type 3 IA LSAs and Type 7 LSAs for the default route.
* Area 51 and Backbone: Configured as normal areas.
* ASBR (R7): Redistributes EIGRP prefixes into OSPF and redistributes OSPF routes into EIGRP-20.

.. code-block:: bash

   router eigrp 20
   network 10.1.1.0 0.0.0.3
   redistribute ospf 1 metric 100000 1 255 1 1500 route-map OSPF-to-EIGRP
   !         
   router ospf 1
   router-id 10.0.0.7
   auto-cost reference-bandwidth 100000
   area 10 nssa
   redistribute eigrp 20 subnets route-map EIGRP-to-OSPF
   !         

* Area 0: Serves as the backbone with R1 as the DR and R2 as the BDR, featuring point-to-point links.
* HUBs 1 and 2: Serve as the internet and VPN gateways for OSPF and EIGRP domains in the spoke networks; 
  they also Redistribute prefixes between OSPF and EIGRP domains.
* Reference bandwidth for all routers used in OSPF cost calculation is 100Gbps


Security
-------------------
* EIGRP: Configured with MD5 authentication.
* OSPF: Configured with MD5 authentication.*
* Firewalls act as zone-based firewalls for stateful inspection, with specific rules for traffic.
  * FW-Area-10 
    * Ingress Traffic:
      * RDS to windows server 192.168.10.254
      * SNMP-traps,SYSLOG,DHCP and Netflow traffic
        
      * Egress traffic:
        * All UDP, TCP and ICMP traffic

   * FW-AREA-51
    *  Ingress traffic
        * All traffic originating from spokes and Hubs
      * Egress traffic

        * All UDP, TCP and ICMP traffic
                
* CoPP: Configured on Backbone routers.
* Edge routers: Disable CDP and LLDP on internet-facing interfaces.
* IPsec: Configured in conjunction with DMVPN for enhanced security.
* Remote access via SSH can only be accessed via 192.168.2.0/24 network.


IP Services
-------------------
* DHCP Server: windows-server serves as the DHCP/DNS server.
* QoS: Configured on routers facing end devices to block torrent sites and police social media sites to 1Mbps.
* NAT: Configured on spoke routers and Area 51 firewalls to provide independent internet connectivity for regional offices.
* NTP: Configured on all devices for time synchronization.
* windows server is configured to enable Remote desktop connection, the firewall only permits this from 192.168.2.0/24 network.
* In Area 23 HSRPv2 is configured for redundancy and load sharing of traffic for both VLAN 2 and 3



Network Assurance
---------------------
* SNMP: Configured on all routers for proactive monitoring using PRTG installed on windows server.
* SPAN and RSPAN: Configured on Edge switches to inspect all traffic entering from and leaving towards
  the internet.
* NetFlow: Configured on all Spokes and Area 23 routers to monitor traffic trends.
* Syslog has been configured on all devices with windows server as the syslog server
    * VTY access has been configured with syslog level 6



Network Automation
-----------------------
* Python Netmiko: Installed on Ubuntu server to automate repetitive tasks related to 
  SNMP, NetFlow and DHCP.
* EEM applets have been configured to automate back-up of running configurations.
      


   