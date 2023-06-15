import communication.connections as conn
import communication.commands as comm
import communication.order as order
import threading




def Main():

    server_host = conn.extract_ip()
    server_port = 4000
    server = (server_host, server_port)
    client_host = "192.168.43.254"
    client_port = 4005
    client = (client_host, client_port)
    
    tcp = conn.tcp_connect(server_host, server_port)
    power = conn.power_connect(tcp, client)
    sensor = conn.sensor_connect(tcp, client)
   # driver = conn.driver_connect(tcp, client)
    
    sensor.flushInput()
    sensor.flushOutput()

    def read_data2(client):
        global on_2s, on_6s, on_12s, SoC_2s, SoC_6s, SoC_12s
        
        data2 = (power.readline()).decode("utf-8")
        
        if data2 == False:
            return False
        
        data2_list = data2.split("/")
        temp2_value = data2_list[0]
        temp3_value = data2_list[1]
        temp4_value = data2_list[2]
        temp5_value = data2_list[3] 
        pow_2s_value = round(float(data2_list[4])*float(data2_list[8]),2)
        pow_6s_value = round(float(data2_list[5])*float(data2_list[9]),2)
        pow_12s_value = round((float(data2_list[6])+float(data2_list[7]))*float(data2_list[10]),2)
        if data2_list[11] == "1":
            on_2s = "1"
        elif data2_list[11] == "0":
            on_2s = ""
        if data2_list[12] == "1":
            on_6s = "1"
        elif data2_list[12] == "0":
            on_6s = ""
        if data2_list[13] == "1":
            on_12s = "1"
        elif data2_list[13] == "0":
            on_12s = ""
        SoC_2s = data2_list[14]
        SoC_6s = data2_list[15]
        SoC_12s = data2_list[16]
        data3 = "+"+temp2_value+"/"+temp3_value+"/"+temp4_value+"/"+temp5_value+"/"+str(pow_2s_value)+"/"+str(pow_6s_value)+"/"+str(pow_12s_value)+"/"+on_2s+"/"+on_6s+"/"+on_12s+"/"+SoC_2s+"/"+SoC_6s+"/"+SoC_12s
        comm.tcp_send(tcp, data3, (client_host, client_port))

    def read_data1(client):
        

        data1 = (sensor.readline()).decode("utf-8")
        
        
        
        if data1.startswith("!"):
            comm.tcp_send(tcp, data1, client)
        elif data1.startswith("+"):
            data1 = data1[1:]
       
       
            data1_list = data1.split("/")
            if float(data1_list[0])!= 0.0:
                try:
                    time_diff = float(data1_list[0])
                    print(time_diff)
                    time_difference.append(time_diff)
                    location_x.append(locations[len(time_difference)-1])
                    x_velocity = (location_x[-1]-location_x[-2])/time_difference[-1]
                    velocity_x.append(x_velocity)
                    x_acce = (velocity_x[-1]-velocity_x[-2])/time_difference[-1]
                    y_acce = float(data1_list[1])
                    acce_y.append(y_acce)
                    y_velocity = velocity_y[-1]+(acce_y[-1]+acce_y[-2])*time_difference[-1]/2
                    velocity_y.append(y_velocity)
                    y_location = location_y[-1]+(velocity_y[-1]+velocity_y[-2])*time_difference[-1]/2
                    z_acce = float(data1_list[2])
                    acce_z.append(z_acce)
                    z_velocity = velocity_z[-1]+(acce_z[-1]+acce_z[-2])*time_difference[-1]/2
                    velocity_z.append(z_velocity)
                    roll_value = data1_list[3]
                    pitch_value = data1_list[4]
                    yaw_value = data1_list[5]
                    temp1_value = data1_list[6]
                    z_location = float(data1_list[7])
                    data3 = "-"+str(location_x[-1])+"/"+str(y_location)+"/"+str(z_location)+"/"+str(x_velocity)+"/"+str(y_velocity)+"/"+str(z_velocity)+"/"+str(x_acce)+"/"+str(y_acce)+"/"+str(z_acce)+"/"+roll_value+"/"+pitch_value+"/"+yaw_value+"/"+temp1_value+"/"+str(time_diff)
                    comm.tcp_send(tcp, data3, client)
                    print("data yollandı")
                except Exception as e:
                    print(e)
                

            else:
                y_acce = float(data1_list[1])
                z_acce = float(data1_list[2])
                roll_value = data1_list[3]
                pitch_value = data1_list[4]
                yaw_value = data1_list[5]
                temp1_value = data1_list[6]
                z_location = float(data1_list[7])
                data3 = ":"+str(z_location)+"/"+str(y_acce)+"/"+str(z_acce)+"/"+roll_value+"/"+pitch_value+"/"+yaw_value+"/"+temp1_value
                comm.tcp_send(tcp, data3, client)
        
           
        
        
        
    
    def clean_data():
        global time_difference, location_x, location_y, velocity_x, velocity_y, velocity_z, acce_y, acce_z
        time_difference = [0]
        location_x = [0]
        location_y = [0]
        velocity_x = [0]
        velocity_y = [0]
        velocity_z = [0]
        acce_y = [0]
        acce_z = [0]

    locations = [0, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50,
                 54, 58, 62, 66, 70, 74, 78, 78.1, 78.2, 78.3, 78.4,
                 78.5, 78.6, 78.7, 78.8, 78.9, 79, 79.1, 79.2, 79.3,
                 79.4, 79.5, 79.6, 79.7, 79.8, 79.9, 82, 86, 90, 94,
                 98, 102, 106, 110, 114, 118, 122, 126, 130, 130.1,
                 130.2, 130.3, 130.4, 130.5, 130.6, 130.7, 130.8,
                 130.9, 134, 138, 142, 146, 150, 154, 158, 162, 166,
                 170, 174]
    
    locations = [0, 1, 2, 3, 4, 4.1, 4.2]

    
    time_difference = [0]

    location_x = [0]
    location_y = [0]
    location_z = []

    velocity_x = [0]
    velocity_y = [0]
    velocity_z = [0]

    acce_y = [0]


    dece = False
    brake_point = 122

    
    while True:
    
#                                       order.do_command(tcp, power, sensor, driver, client)

        
        if read_data1(client) == False :
            comm.tcp_send(tcp, "An error encountered. Communication lost procedure is starting...", (client_host, client_port))
            comm.custom(driver, "10", tcp, client)
            comm.custom(power, "99", tcp, client)
            clean_data()
        
        if dece == False and location_x[-1] >= brake_point :
            comm.custom(power, "22", tcp, client)
            comm.custom(driver, "6", tcp, client)
            dece = True                                                                                   
        
        if conn.status_check(tcp, client_host, client_port) == False:
            comm.custom(driver, "10", tcp, client)
            comm.custom(power, "99", tcp, client)
            clean_data()
        
            


    
if __name__ == "__main__":

    Main()
  