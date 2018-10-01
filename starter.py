
import time
import sys
import socket
import json

# This file is the client to issue grep command to all the available servers

# this function send the user query to the server specified by the
# function argument.If exception happens return 0, else return 1
# result from server is saved in the argument output


def grep_query(output, host, query, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        return 1
    max_data = 8192
    try:
        sock.send(json.dumps(query).encode())
    except:
        return 1

    while True:
        # if server receives command but does not respond, wait 5 seconds
        sock.settimeout(5)
        try:
            data = sock.recv(max_data)
        except:
            return 1

        # receive the grep result from the server into the output list
        output.append(data.decode())
        if len(data) == 0:
            sock.close()
            break
        elif len(data) != max_data:
            # ? marks the end of the result from server(only for the specified logfile which does not have ?)
            if output[len(output) - 1].endswith("?"):
                sock.close()
                return 0


if __name__ == "__main__":
    query = []
    count = 0
    #user input grep command through command line argument
    for arg in sys.argv:
        if count < 1:
            count += 1
        else:
            query.append(arg)
    query = {"instruction": query}
    input_list = []
    ip_list = []

    # get all the ips of the servers
    with open("ips.txt", 'r') as file:
        for line in file:
            ip_list.append(line.split("\n")[0])

    # create input list for each server.
    for i in range(len(ip_list)):
        input_list.append([])

    # store the status for each server, so our output message could be clearer
    status_list = []
    linecounts = [0]*len(ip_list)

    for i in range(len(input_list)):
        # store the status for each server
        status_list.append(grep_query(input_list[i], ip_list[i], query, 7002))
        linecount = 0
        if len(input_list[i]) != 0:
            print('From VM' + ip_list[i][14:17] + ':')
            j = -1
            # print the message received from each server
            for j in range(len(input_list[i]) - 1):
                sys.stdout.write(input_list[i][j])
                linecount += input_list[i][j].count('\n')
            # the last line has an extra marking the end of message from server, so take the ? off
            linecount += input_list[i][j + 1][:-1].count('\n')
            sys.stdout.write(input_list[i][j + 1][:-1])
            sys.stdout.flush()
        linecounts[i] = linecount
    
    for i, j in enumerate(ip_list):
        # server is good
        if status_list[i] == 0:
            print('VM' + ip_list[i][14:17] + ':' + str(linecounts[i]))
        # server is down
        else:
            print('VM' + ip_list[i][14:17] + ': Connection failed.')


