import paramiko
password = 'pi'
username = 'pi'
host = '192.168.0.145'
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname = host, username=username, password=password)


stdin, stdout, stderr = client.exec_command('pgrep -o -x python')
pid = stdout.read().decode("utf-8")
stdin, stdout, stderr = client.exec_command('kill ' + format(pid))

# print errors if there are any
err = stderr.read().decode()
if err:
    print(err)
    # close the connection
stdin.close()
