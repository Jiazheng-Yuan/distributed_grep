import paramiko
import socket
import json
import subprocess

#file for unittesting.

# copy from starter.py
def grep_thread(output, host, query, port):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect((host, port))
    except:
        output.append("failure")
        return
    max_data = 8192
    try:
        mySocket.send(json.dumps(query).encode())
    except:
        return

    while True:
        mySocket.settimeout(10)
        try:
            data = mySocket.recv(max_data)
        except:
            return
        output.append(data.decode())
        if len(data) == 0:
            mySocket.close()
            break
        elif len(data) != max_data:

            if output[len(output) - 1].endswith("?"):
                mySocket.close()
                return


# copy from starter.py
def grep(query):
    query = {"instruction": query}
    input_list = []
    ip_list = []
    with open("test_ips.txt", 'r') as file:
        for line in file:
            ip_list.append(line.split("\n")[0])

    for i in range(len(ip_list)):
        input_list.append([])

    file = open("distributed_result.txt","w")

    # save the result of distribtued grep for  diff check
    for i in range(len(input_list)):
        grep_thread(input_list[i], ip_list[i], query, 7002)
        if len(input_list[i]) != 0:
            j = -1
            for j in range(len(input_list[i]) - 1):
                file.write(input_list[i][j])
            file.write(input_list[i][j + 1][:-1])
    file.flush()


if __name__ == '__main__':


    file = open("test_ips.txt",'r')
    file_writer = open("test.txt","w")
    query = ["grep", "abc", "test.txt"]
    result_writer = open("result.txt", "w")

    # this loop copies all the test files from tested server and
    # combine them into a local file.
    for ip in file:
        ip = ip.split("\n")[0]
        transport = paramiko.Transport(ip)
        transport.connect(username="yixinz6", password="Zyyy9-9-")
        sftp = paramiko.SFTPClient.from_transport(transport)
        filepath = "/home/yixinz6/CS_425_MP1/test.txt"
        localpath = 'trial.txt'
        sftp.get(filepath, localpath)
        sftp.close()
        transport.close()
        with open("trial.txt",'r') as file_reader:
            for line in file_reader:
                file_writer.write(line)
        file_writer.flush()
    # locally grep on the combined local file, which is the correct result
    output = subprocess.Popen(query, stdout=subprocess.PIPE).communicate()[0]
    result = output.decode()

    for line in result:
        result_writer.write(line)
    result_writer.flush()
    grep(query)

    # compare the result of distributed grep and the grep done locally
    query=["diff","distributed_result.txt","result.txt"]
    output = subprocess.Popen(query, stdout=subprocess.PIPE).communicate()[0]
    result = output.decode()
    print(result)


