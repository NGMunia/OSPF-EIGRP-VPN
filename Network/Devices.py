from login import username, password, secret


Firewall_A_10= {
         'FW1-A-10':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'192.168.11.1'
                    }
                }
Spokes  =   {
            'NBI-1':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.1.50.1',
                    },
            'NBI-2':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.1.50.2'
                    },
              'NKR':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.1.52.1'
                    },
              'MSA':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.1.60.1'
                    },
              'MLD':{
                      'device_type':'cisco_ios',
                     'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.1.61.1'
                    }  
          }

Area_0 =  {
          'R1-A-0': {
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.0.0.1'
                    },
          'R2-A-0': {
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.0.0.2'
                    },  
          'R3-A-0': {
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.0.0.3'
                    }, 
          'R4-A-0': {
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.0.0.4'
                    }
          }

Area_10 = {
          'R5-A-10':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.0.10.9',
                    },
          'R6-A-10':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.0.10.13'
                    },  
          'R7-A-10':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'10.0.10.18'
                    },
          'R8-A-10':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'172.20.20.1'
                    }   
          }

Area_23 = {
          'R1-A-23':{
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'192.168.2.1',
                    },
          'R2-A-23':{
                      'device_type':'cisco_ios',
                     'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'192.168.2.2'
                    }
         }

Firewalls_A_51 =    {
          'FW-1':  {
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'51.0.0.1',
                   },
          'FW-2':  {
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'51.0.0.2'
                    }
          }

Area_51 = {
          'Edge-1': {
                      'device_type':'cisco_ios',
                     'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'51.0.0.3',
                    },
          'Edge-2': {
                      'device_type':'cisco_ios',
                      'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'51.0.0.4'
                    }
          }
Switches= {
      'SW-AREA-23': {
                      'device_type':'cisco_ios',
                     'username': username,
                      'secret': secret,
                      'password': password,
                      'ip':'192.168.2.10'
                    }
          }
