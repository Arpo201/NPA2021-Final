from netmiko import ConnectHandler

device_ip = "10.0.15.111"
username  = "admin"
password =  "cisco"

device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password,
}

with ConnectHandler(**device_params) as ssh:
    result = ssh.send_command('show ip int br')
    if 'Loopback62070174' in result:
        ssh.send_config_set(['no int loopback 62070174'])
    else:
        ssh.send_config_set(['int loopback 62070174', 'ip address 192.168.1.1 255.255.255.0'])
    ssh.save_config()
    result = ssh.send_command('show ip int br')
    print(result)