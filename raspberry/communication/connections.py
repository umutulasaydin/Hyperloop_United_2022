import socket
import serial
import communication.commands as comm
import time

def extract_ip():
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            tcp.connect(("10.255.255.255",1))
            IP = tcp.getsockname()[0]
            tcp.close()
            return(IP)
        except Exception as e:
            print("An error was encountered while taking IP address.")
            print(e)
            continue
    

def status_check(tcp, client_host, client_port):
    try:
        tcp.sendto("".encode("utf-8"), (client_host, client_port))
    except:
        return False
    return True

def tcp_connect(server_host, server_port):

    server = (server_host, server_port)
    while True:
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tcp.bind(server)
            print("TCP connection is done")
            print("SERVER STARTED")
        except Exception as e:
            print("There is a problem in TCP connection. Retrying...")
            print(e)
            continue
        return tcp
    


def power_connect(tcp, client):
    while True:
        try:
            power = serial.Serial("/dev/POWER_ARDUINO", baudrate = 9600)
            power.reset_input_buffer()
            comm.tcp_send(tcp, "!Power Arduino connection is done", client)
        except Exception as e:
            comm.tcp_send(tcp, "!There is a problem in Power Arduino. Retrying...", client)
            comm.tcp_send(tcp, "!"+str(e), client)
            continue
        return power


def sensor_connect(tcp, client):
    while True:
        try:
            sensor = serial.Serial("/dev/SENSOR_ARDUINO", baudrate = 250000)
            comm.tcp_send(tcp, "!Sensor Arduino connection is done", client)
            sensor.write(bytes(" ", "utf-8"))
            sensor.reset_input_buffer()
        except Exception as e:
            comm.tcp_send(tcp, "!There is a problem in Sensor Arduino. Retrying...", client)
            comm.tcp_send(tcp, "!"+str(e), client)
            continue
        return sensor



def driver_connect(tcp, client):
   
    while True:
        try:
            driver = serial.Serial("/dev/DRIVER_ARDUINO", baudrate = 250000)
            driver.reset_input_buffer()
            comm.tcp_send(tcp, "!Driver Arduino connection is done", client)
        except Exception as e:
            comm.tcp_send(tcp, "!There is a problem in Driver Arduino. Retrying...", client)
            comm.tcp_send(tcp, "!"+str(e), client)
            continue
        return driver
