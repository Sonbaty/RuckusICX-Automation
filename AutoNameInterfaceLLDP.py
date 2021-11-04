from netmiko import ConnectHandler


with open('DevicesBackups.txt') as switches:
    for IP in switches:
        Switch = {
            'device_type': 'ruckus_fastiron',
            'ip': IP,
            'username': 'User Cerdentials Here',
            'password': 'the Password',
            # 'banner_timeout': 80
            'global_delay_factor': 2,

        }

        net_connect = ConnectHandler(**Switch)
        print('Connecting to ' + IP)
        print('-' * 79)
        print('waiting For Authentication ...')
        output = net_connect.send_command('sh version')
        print(output)
        print()
        print('-' * 79)
        ou_List = []
        query = net_connect.send_command('show lldp neighbors')
        ou_List = query.splitlines()
        Nei_List = ou_List[1:]
        Nei_List2 = ou_List[2:]
        print('The Following Mapping Detected : ')
        for line in Nei_List:
            lldpOutputLine = str(line).split()
            if len(lldpOutputLine) <= 3:
                AssociatedDevice = 'Unknown-Device'
                # print(lldpOutputLine)
                InterfaceNum = lldpOutputLine[0]
                print(f'{InterfaceNum} =>> {AssociatedDevice}')

            elif len(lldpOutputLine) == 4:
                if "1/" in lldpOutputLine[3]:
                    AssociatedDevice = 'Unknown-Device'
                    InterfaceNum = lldpOutputLine[0]
                    print(f'{InterfaceNum} =>> {AssociatedDevice}')
                else:
                    AssociatedDevice = lldpOutputLine[3]
                    InterfaceNum = lldpOutputLine[0]
                    print(f'{InterfaceNum} =>> {AssociatedDevice}')

            else:
                lldpOutputLine = str(line).split()
                InterfaceNum = lldpOutputLine[0]
                AssociatedDevice = lldpOutputLine[4]
                print(f'{InterfaceNum} =>> {AssociatedDevice}')

            config_commands = [

                f'int eth {InterfaceNum}',
                f'port-name {AssociatedDevice}',
                'exit',
                'wr mem'

            ]
            net_connect.send_config_set(config_commands)
            print(f'{InterfaceNum} config done result is :')
            print(net_connect.send_command(f'show int br | i {InterfaceNum}'))
    net_connect.disconnect()





