from netmiko import ConnectHandler
import xlrd


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
        workbook = xlrd.open_workbook("Ports.xlsx")
        worksheet = workbook.sheet_by_name('Sw1')
        curr_row=0
        print(f" port-names  of SW[ {IP} ]: ")

        for num_rows in range(1, worksheet.nrows):

            PortName = worksheet.cell(num_rows, 1).value
            interface = worksheet.cell(num_rows, 0).value
            print(interface, PortName)
            config_commands = [
                f'interface eth {interface}',
                f'port-name {PortName}',
                'exit'
            ]
            net_connect.send_config_set(config_commands)

print('done')
print(net_connect.send_config_set('sh int br'))
net_connect.disconnect()
