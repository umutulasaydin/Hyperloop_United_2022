import threading
import time
import communication.commands as comm
import select

def do_command(tcp, power, sensor, driver, client):
    global dece
    data = ""
    ready = select.select([tcp], [],[], 0.1)
    if ready[0]:
        data = comm.tcp_recv(tcp)
        data = data.decode("utf-8")
    if data == "Merge":
        print("Merge")
        comm.custom(power, "4", tcp, client)

        
    elif data == "Launch":
        print("Launch")
        comm.custom(power, "1", tcp, client)
        comm.custom(driver, "5", tcp, client)
        comm.custom(sensor, "1", tcp, client)

        
    elif data == "Emergency":
        print("Emergency")
        comm.custom(driver, "10", tcp, client)
        comm.custom(power, "99", tcp, client)


        
    elif data == "Break":
        print("Break")
        comm.custom(power, "22", tcp, client)
        comm.custom(driver, "6", tcp, client)
        dece = True
      
    elif data == "Brake0":
        print("Brake0")
        comm.custom(power, "4", tcp, client)
        
    elif data == "Brake1":
        print("Brake1")
        comm.custom(power, "3", tcp, client)
           
    elif data == "Brake2":
        print("Brake2")
        comm.custom(power, "2", tcp, client)
        
    elif data == "Full_Forward":
        print("Full_Forward")
        comm.custom(driver, "5", tcp, client)
        
    elif data == "Half_Forward":
        print("Half_Forward")
        comm.custom(driver, "7", tcp, client)
    
    elif data == "Full_Backward":
        print("Full_Backward")
        comm.custom(driver, "6", tcp, client)
        
    elif data == "Half_Backward":
        print("Half_Backward")
        comm.custom(driver, "8", tcp, client)
    
    elif data == "Stop":
        print("Stop")
        comm.custom(driver, "10", tcp, client)
        
    elif data == "12Son":
        print("12Son")
        comm.custom(power, "121", tcp, client)
    
    elif data == "12Soff":
        print("12Soff")
        comm.custom(power, "120", tcp, client)
    
    elif data == "6Son":
        print("6Son")
        comm.custom(power, "91", tcp, client)
    
    elif data == "6Soff":
        print("6Soff")
        comm.custom(power, "90", tcp, client)
        
    elif data == "2Son":
        print("2Son")
        comm.custom(power, "21", tcp, client)
        
    elif data ==  "2Soff":
        print("2Soff")
        comm.custom(power, "20", tcp, client)
    
    elif data == "Sensor_on":
        sensor.reset_input_buffer()
        comm.custom(sensor, "1", tcp, client)
        print("Sensor_on")
    
    elif data == "Sensor_off":
        print("Sensor_off")
        comm.custom(sensor, "0", tcp, client)
    
    elif data == "Lev_on":
        print("Lev_on")
        comm.custom(power, "1", tcp, client)
        
    elif data == "Lev_off":
        print("Lev_off")
        comm.custom(power, "0", tcp, client)
       
        
            
