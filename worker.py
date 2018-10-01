import socket
import os
import json
import subprocess


# server class
class Machine:
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", 7002))
        # only one machine greps at a time, queue size 1 is good
        sock.listen(1)
        max_data = 8192

        # server keeps listening on port 7002, never returns. whenever instruction comes, process it
        while True:
            current_data = ""
            connection, client_address = sock.accept()
            while True:
                data = connection.recv(max_data)
                current_data += data.decode()
                if len(data) == 0:
                    break
                elif len(data) != max_data:
                    break

            # once this method finishes, server is ready for another instruction
            self.message_handler(current_data, connection)

    # this method handles the request from client
    #@staticmethod
    def message_handler(self,current_data, connection):
            message = json.loads(current_data)
            if "instruction" in message:
                query = message["instruction"]
                command = ''
                for q in query:
                    command = command + str(q) + ' '
                try:
                    # run the command and extract output
                    #os.system(command)
                    #output = subprocess.check_output(command, shell=True)
                    #result = output.decode()
                    result = subprocess.Popen(query,stdout=subprocess.PIPE).communicate()[0]
                    result = result.decode()
                # in case the command is invalid, server sends back an empty message ends with ?
                except:
                    print(result)
                    result = ""
                    connection.send((result+'?').encode())
                    connection.close()
                    return
                # server sends back the grep result on this machine's log file, use ? to mark the end
                connection.send((result + "?").encode())


if __name__ == "__main__":
    m = Machine()
    m.start()
