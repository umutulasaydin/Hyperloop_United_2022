

def tcp_send(tcp, data, client):
    count = 0
    while count < 10:
        try:
            tcp.sendto(data.encode("utf-8"), client)
        except Exception as e:
            print("An error was encountered  while sending a command to client. Retrying...")
            print(e)
            count += 1
            continue
        return True
    return False

def custom(serial, command, tcp, client):
    count = 0
    while count < 10:
        try:
            serial.write(bytes(command, "utf-8"))
            serial.reset_input_buffer()
            print("data: ", command)
        except Exception as e:
            tcp_send(tcp,"!An error was encountered while sending a command to " + str(serial) + ". Retrying...", client)
            tcp_send(tcp, "!"+str(e), client)
            count += 1
            continue
        return True
    return False




def tcp_recv(tcp):
    count = 0
    while count < 10:
        try:
            data = tcp.recv(1024)
            return data
        except Exception as e:
            print("An error was encountered while receving data from tcp. Retrying...")
            print(e)
            count += 1
            continue
    return False

