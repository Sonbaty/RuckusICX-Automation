from netmiko import ConnectHandler

with open('DevicesLogSRVR.txt') as switches:
    for IP in switches:
        Switch = {
            'device_type': 'ruckus_fastiron',
            'ip': IP,
            'username': 'User Cerdentials Here',
            'password': 'the Password',
        }

        net_connect = ConnectHandler(**Switch)

        print('Connecting to ' + IP)
        print('-' * 79)
        output = net_connect.send_command('sh version')
        print(output)
        print()
        print('-' * 79)
        LogSrvr = input('Enter The Log Server IP : ')
        NtpSrvr = input('Enter The NTP Server IP : ')
        if IP =="172.26.96.10":
            print(f'Detected SW {IP} , Applying Config')
            config_commands = [

                f'logging host {LogSrvr}',
                'ntp',
                f'server {NtpSrvr}',
                'exit',
                'wr mem'

            ]
            net_connect.send_config_set(config_commands)

        elif IP =="172.26.96.11":
           print('test')
        else:
            print("Configuration/Device Not Found in this ip list")
print('done')
print('Result For Syslog: ')
print(net_connect.send_config_set('sh run | include logging'))
print('Result for NTP : ')
print(net_connect.send_config_set('sh run | include server'))
net_connect.disconnect()
