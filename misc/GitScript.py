import paramiko

# all functions in the script ssh into the server specified by ../ips.txt
# and execute a command in shell

# pull from gitlab on all machines
def pull():
    with open("../ips.txt",'r') as file:
        for line in file:
            ip = line.split("\n")[0]
            try:
                #ssh into servers
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username="yixinz6", password="Zyyy9-9-")
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cd ~/CS_425_MP1/;git stash;git pull")
                print(ssh_stdout.read().decode())
            except:
                print(ip)
                print("error!")

#start servers on all machines
def start_server():
    with open("../ips.txt", 'r') as file:
        for line in file:
            ip = line.split("\n")[0]
            try:
                # ssh into servers
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username="yixinz6", password="Zyyy9-9-")
                ssh.exec_command("cd ~/CS_425_MP1/;python worker.py &")
            except Exception as e:
                print(ip)
                print(e)
                print("error!")

#kill  servers on all machines
def kill_server():
    with open("../ips.txt", 'r') as file:
        for line in file:
            # ssh into servers
            ip = line.split("\n")[0]
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username="yixinz6", password="Zyyy9-9-")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("netstat -tulpn")
            lines = (ssh_stdout.readlines())

            #find the process listening on port 7002, which is server, and kills it
            for line in lines:
                if line.count(":7002") == 1:
                    line = line.split(" ")
                    for i in line:
                        if(i.count("/python") == 1):
                            pid = i.split("/")[0]
            ssh.exec_command("kill -9 " + pid)

if __name__=="__main__":
    start_server()
    #()
