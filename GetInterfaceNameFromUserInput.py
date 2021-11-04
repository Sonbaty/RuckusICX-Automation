from netmiko import ConnectHandler

with open('devices.txt') as switches:
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
        Device_Model = 24



       # net_connect.send_config_set('en', 'conf t')
        for interface in range(Device_Model):
            PortName = input(f"enter port-name for eth 1/1/{interface +1} of SW[ {IP} ]: ")
            config_commands = [
                f'interface eth 1/1/{interface +1}',
                f'port-name {PortName}'
            ]
            net_connect.send_config_set(config_commands)
            #PortName = input(f"inter port-name for eth 1/1/{interface + 1} : ")
            #net_connect.send_comand(f'interface eth 1/1/{interface+1}', f"port-name {PortName}", 'exit')
            #net_connect.send_config_set()
            print('done')
            #net_connect.send_config_set()

net_connect.disconnect()
