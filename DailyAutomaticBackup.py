import netmiko
import paramiko
from netmiko import ConnectHandler
from datetime import datetime
import schedule
import time
from multiprocessing import Pool

import os

Location = input('Enter The Switches Group Name First : ')
print("Backup Schduled For EveryDay at 1 AM")
def DailyBackup(self):
    print("Its 1 AM Making A Backup ...")
    with open('DevicesBackups.txt') as switches:
        for IP in switches:
            Switch = {
                'device_type': 'ruckus_fastiron',
                'ip': IP,
                'username': 'User Cerdentials Here',
                'password': 'the Password',
                #'banner_timeout': 80
                'global_delay_factor': 2,



            }

            #time.sleep(20)

            for i in range(3):
                try:
                    net_connect = ConnectHandler(**Switch)
                    print('Connecting to ' + IP)
                    print('-' * 79)
                    print('waiting For Authentication ...')
                    output = net_connect.send_command('sh version')
                    print(output)
                    print()
                    print('-' * 79)

                    hostname = net_connect.send_command('show run | i hostname')
                    hostname.split(" ")
		    if hostname == "":
                        device = "SW_name"
                        print('Notice : This Switch has no hostname configured')
                    else:
                        hostname, device = hostname.split(" ")
                    hostname, device = hostname.split(" ")
                    MyIP = IP.strip('\n')
                    now = datetime.now()
                    CurrTime = now.strftime("%Y-%m-%d %H-%M-%S")
                    print("Backing up " + device)

                    if not os.path.exists(Location):
                        os.mkdir(Location)
                        print("Directory ", Location, " Created ")
                    else:
                        print("Directory ", Location, " already exists")

                    if not os.path.exists(f'{Location}/{device}-IP[{MyIP}]'):
                        os.makedirs(f'{Location}/{device}-IP[{MyIP}]')
                        print("Directory ", device, " Created ")
                    else:
                        print("Directory ", device, " already exists")

                    # filename = '/home/sonbaty/Automation/backups/' + device + '.txt'
                    filename = f'{Location}/{device}-IP[{MyIP}]/' + f'{device} AT {CurrTime}' + '.txt'
                    showrun = net_connect.send_command('show run')
                    showvlan = net_connect.send_command('show vlan')
                    showver = net_connect.send_command('show ver')
                    log_file = open(filename, "a")  # append mode
                    log_file.write(showrun)
                    log_file.write("\n")
                    log_file.write(showvlan)
                    log_file.write("\n")
                    log_file.write(showver)
                    log_file.write("\n")

                except paramiko.ssh_exception.SSHException as err:
                    print(f"Oops! {err}")
                    print('Trying Again ...')
                    continue

    print('done')
    net_connect.disconnect()

    print('Next Backup Is Tomorrow At 01:00 AM')
    print('Waiting  ...')

    return


schedule.every().day.at('01:00').do(DailyBackup, 'Backing Up Its 1 AM')
# For Testing
#DailyBackup()

while True:
    schedule.run_pending()






