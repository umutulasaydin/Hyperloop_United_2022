from tkinter import *
from tkinter import ttk
import socket
import time
import csv

condition = True
def extract_ip():
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count = 0
    while count < 10:
        try:
            tcp.connect(("10.255.255.255",1))
            IP = tcp.getsockname()[0]
            tcp.close()
            return(IP)
        except Exception as e:
            print("An error was encountered while taking IP address.")
            print(e)
            count+=1
            continue

   
def save_csv():
    try:
        with open("veri.csv", "w") as file:
            writer = csv.writer(file)
            data = ["Zaman (sn)", "Ivme", "Hiz", "Konum"]
            writer.writerow(data)
            for i in range(1,len(time_difference)):
                data = [sum(time_difference[1:i+1]), acce_x[i], velocity_x[i], location_x[i]]
                writer.writerow(data)
    except Exception as e:
        print("Save")
        print(e)

locations = [0, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50,
                54, 58, 62, 66, 70, 74, 78, 78.1, 78.2, 78.3, 78.4,
                78.5, 78.6, 78.7, 78.8, 78.9, 79, 79.1, 79.2, 79.3,
                79.4, 79.5, 79.6, 79.7, 79.8, 79.9, 82, 86, 90, 94,
                98, 102, 106, 110, 114, 118, 122, 126, 130, 130.1,
                130.2, 130.3, 130.4, 130.5, 130.6, 130.7, 130.8,
                130.9, 134, 138, 142, 146, 150, 154, 158, 162, 166,
                170, 174]






    


temp_elec = [0]
temp_2s = [0]
temp_6s = [0]
temp_12s = [0]
temp_bms = [0]

pow_2s = [0]
pow_6s = [0]
pow_12s = [0]



on_2s = False
on_6s = False
on_12s = False

roll = [0]
yaw = [0]
pitch = [0]

time_difference = [0]

location_x = [0]
location_y = [0]
location_z = [0]

velocity_x = [0]
velocity_y = [0]
velocity_z = [0]

acce_x = [0]
acce_y = [0]
acce_z = [0]


def change_status():
    global condition
    try:

        temp_1.set("Electronics Temperature: {}C".format(temp_elec[-1]))
        temp_2.set("2S Battery Temperature: {}C".format(temp_2s[-1]))
        temp_3.set("6S Battery Temperature: {}C".format(temp_6s[-1]))
        temp_4.set("12S Battery Temperature: {}C".format(temp_12s[-1]))
        temp_5.set("BMS Temperature: {}C".format(temp_bms[-1]))
        power_cons.set("Power Consumption: {}KW".format(float(pow_2s[-1])+float(pow_6s[-1])+float(pow_12s[-1])))
        topsp.set("Top Speed: {}m/s".format(max(velocity_x)))

        cruzperc.set(round((location_x[-1]/178)*100,2))
        cruzstat.set(status[stat_index])     
        powercons_2s.set("{}kW".format(pow_2s[-1]))
        powercons_6s.set("{}kW".format(pow_6s[-1]))
        powercons_12s.set("{}kW".format(pow_12s[-1]))
        powercons_t.set("{}kW".format(float(pow_2s[-1])+float(pow_6s[-1])+float(pow_12s[-1])))
        xpozlaz.set("{}m".format(location_x[-1]))
        ypozlaz.set("{}m".format(location_y[-1]))
        zpozlaz.set("{}m".format(location_z[-1]))
        xvellaz.set("{}m/s".format(velocity_x[-1]))
        yvellaz.set("{}m/s".format(velocity_y[-1]))
        zvellaz.set("{}m/s".format(velocity_z[-1]))
        xacclaz.set("{}m/s^2".format(acce_x[-1]))
        yacclaz.set("{}m/s^2".format(acce_y[-1]))
        zacclaz.set("{}m/s^2".format(acce_z[-1]))
        rol.set("{} degree".format(roll[-1]))
        yav.set("{} degree".format(yaw[-1]))
        pich.set("{} degree".format(pitch[-1]))
        refc.set("{}".format(len(time_difference)-1))
        if on_2s:
            a.configure("2s_bar.Vertical.TProgressbar", foreground = "green", background = "green")
        else:
            a.configure("2s_bar.Vertical.TProgressbar", foreground = "red", background = "red")
        if on_6s:
            a.configure("6s_bar.Vertical.TProgressbar", foreground = "green", background = "green")
        else:
            a.configure("6s_bar.Vertical.TProgressbar", foreground = "red", background = "red")
        if on_12s:
            a.configure("12s_bar.Vertical.TProgressbar", foreground = "green", background = "green")
        else:
            a.configure("12s_bar.Vertical.TProgressbar", foreground = "red", background = "red")
        
        window.update()
        if refc.get() == str(len(locations)-1):
            condition = False
            save_csv()
    except Exception as e:
        feededit.insert("Status\n", END)
        feededit.insert(e+"\n", END)



host = extract_ip()
port = 4005
tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp.bind((host,port))




def read_data():

    global on_2s, on_6s, on_12s, condition
    if condition:
        try:
            data = tcp.recv(1024).decode("utf-8")
     
            if data.startswith("!"):
                data = data[1:]
                feededit.insert(END, "Info: " +data+"\n")
            elif data.startswith("+"):
                
                data = data[1:]
                data_list = data.split("/")
                temp_2s.append(data_list[0])
                temp_6s.append(data_list[1])
                temp_12s.append(data_list[2])
                temp_bms.append(data_list[3])
                pow_2s.append(data_list[4])
                pow_6s.append(data_list[5])
                pow_12s.append(data_list[6])
                on_2s = bool(data_list[7])
                on_6s = bool(data_list[8])
                on_12s = bool(data_list[9])
                SoC_2s.set(float(data_list[10]))
                SoC_6s.set(float(data_list[11]))
                SoC_12s.set(float(data_list[12]))
                feededit.insert(END, "Power Arduino: " +data+"\n")
            elif data.startswith("-"):
                data = data[1:]
                data_list = data.split("/")
                location_x.append(float(data_list[0]))
                location_y.append(data_list[1])
                location_z.append(float(data_list[2])/10)
                velocity_x.append(float(data_list[3]))
                velocity_y.append(data_list[4])
                velocity_z.append(data_list[5])
                acce_x.append(data_list[6])
                acce_y.append(data_list[7])
                acce_z.append(data_list[8])
                roll.append(data_list[9])
                pitch.append(data_list[10])
                yaw.append(data_list[11])
                temp_elec.append(data_list[12])
                time_difference.append(float(data_list[13]))
                feededit.insert(END, "Sensor Arduino: " +data+"\n")
            elif data.startswith(":"):
                data = data[1:]
                data_list = data.split("/")
                location_z.append(float(data_list[0])/10)
                acce_y.append(data_list[1])
                acce_z.append(data_list[2])
                roll.append(data_list[3])
                pitch.append(data_list[4])
                yaw.append(data_list[5])
                temp_elec.append(data_list[6])
                feededit.insert(END, "Sensor Arduino: " +data+"\n")
                
            change_status()
            window.after(100, read_data)
        except Exception as e:
            feededit.insert("Read Data\n")
            feededit.insert(e+"\n", END)
            window.after(100, read_data)

def clean_data():
    global temp_elec, temp_2s, temp_6s, temp_12s, temp_bms, pow_2s, pow_6s, pow_12s, on_2s, on_6s, on_12s, roll, pitch, yaw, time_difference, SoC_2s, SoC_6s, SoC_12s
    global location_x, location_y, location_z, velocity_x, velocity_y, velocity_z, acce_x, acce_y, acce_z, stat_index
    temp_elec = [0]
    temp_2s = [0]
    temp_6s = [0]
    temp_12s = [0]
    temp_bms = [0]

    pow_2s = [0]
    pow_6s = [0]
    pow_12s = [0]

    SoC_2s.set(100)
    SoC_6s.set(100)
    SoC_12s.set(100)
    on_2s = False
    on_6s = False
    on_12s = False

    roll = [0]
    yaw = [0]
    pitch = [0]

    time_difference = [0]

    location_x = [0]
    location_y = [0]
    location_z = [0]

    velocity_x = [0]
    velocity_y = [0]
    velocity_z = [0]

    acce_x = [0]
    acce_y = [0]
    acce_z = [0]

    stat_index = 0
    change_status()

#------------------------------------Window Setup------------------------------------------------------------
window = Tk()
window.resizable(False,False)
window.title("Hyperloop United Control Panel")
window.geometry("1225x690")



client_host = StringVar()
client_port = IntVar()
client = (client_host.get(), client_port.get())

SoC_2s = DoubleVar(value = 100)
SoC_6s = DoubleVar(value = 100)
SoC_12s = DoubleVar(value = 100)
temp_1 = StringVar(value = "Electronics Temperature: {}C".format(temp_elec[-1]))
temp_2 = StringVar(value = "2S Battery Temperature: {}C".format(temp_2s[-1]))
temp_3 = StringVar(value = "6S Battery Temperature: {}C".format(temp_6s[-1]))
temp_4 = StringVar(value = "12S Battery Temperature: {}C".format(temp_12s[-1]))
temp_5 = StringVar(value = "BMS Temperature: {}C".format(temp_bms[-1]))
power_cons  = StringVar(value = "Power Consumption: {}KW".format(pow_2s[-1]+pow_6s[-1]+pow_12s[-1]))
topsp  = StringVar(value = "Top Speed: {}m/s".format(max(velocity_x)))
cruzperc = DoubleVar(value = location_x[-1]/178)
cruzstat = StringVar(value = status[stat_index]) 
powercons_2s = StringVar(value = "{}kW".format(pow_2s[-1]))
powercons_6s = StringVar(value = "{}kW".format(pow_6s[-1]))
powercons_12s = StringVar(value = "{}kW".format(pow_12s[-1]))
powercons_t = StringVar(value = "{}kW".format(pow_2s[-1]+pow_6s[-1]+pow_12s[-1]))
### Laser
xpoz = StringVar(value ="{}m".format(location_x[-1]))
ypoz = StringVar(value ="{}m".format(location_y[-1]))
zpoz = StringVar(value ="{}m".format(location_z[-1]))
xvel = StringVar(value ="{}m/s".format(velocity_x[-1]))
yvel = StringVar(value ="{}m/s".format(velocity_y[-1]))
zvel = StringVar(value ="{}m/s".format(velocity_z[-1]))
xacc = StringVar(value ="0 m/s^2")
yacc = StringVar(value ="{}m/s^2".format(acce_y[-1]))
zacc = StringVar(value ="0 m/s^2")
###Unframed
rol = StringVar()
yav = StringVar()
pich = StringVar()
refc = StringVar()


status = ["Waiting", "Merged", "Launching", "Breaking", "EMERGENCY"]
stat_index = 0


temp_1.set("Electronics Temperature: {}C".format(temp_elec[-1]))
temp_2.set("2S Battery Temperature: {}C".format(temp_2s[-1]))
temp_3.set("6S Battery Temperature: {}C".format(temp_6s[-1]))
temp_4.set("12S Battery Temperature: {}C".format(temp_12s[-1]))
temp_5.set("BMS Temperature: {}C".format(temp_bms[-1]))
power_cons.set("Power Consumption: {}KW".format(pow_2s[-1]+pow_6s[-1]+pow_12s[-1]))
topsp.set("Top Speed: {}m/s".format(max(velocity_x)))
cruzperc.set(location_x[-1]/178)
cruzstat.set(status[stat_index])
powercons_2s.set("{}kW".format(pow_2s[-1]))
powercons_6s.set("{}kW".format(pow_6s[-1]))
powercons_12s.set("{}kW".format(pow_12s[-1]))
powercons_t.set("{}kW".format(pow_2s[-1]+pow_6s[-1]+pow_12s[-1]))
xpozlaz.set("{}m".format(location_x[-1]))
ypozlaz.set("{}m".format(location_y[-1]))
zpozlaz.set("{}m".format(location_z[-1]))
xvellaz.set("{}m/s".format(velocity_x[-1]))
yvellaz.set("{}m/s".format(velocity_y[-1]))
zvellaz.set("{}m/s".format(velocity_z[-1]))
xacclaz.set("{}m/s^2".format(acce_x[-1]))
yacclaz.set("{}m/s^2".format(acce_y[-1]))
zacclaz.set("{}m/s^2".format(acce_z[-1]))
rol.set("{} degree".format(roll[-1]))
yav.set("{} degree".format(yaw[-1]))
pich.set("{} degree".format(pitch[-1]))
refc.set("{}".format(len(time_difference)-1))

connvar = IntVar()
podmvar = IntVar()
compvar = IntVar()
idevar = IntVar()        #--------------variables for checkboxes
sensvar = IntVar()
ipvar = IntVar()


#----------Variables for telemetry



latency = StringVar()   #-----------Connection vars




##Variables
frender = IntVar()
brakman = IntVar()
brakman.set(0)
limslow = IntVar()  #----------Text Drive Vars
limslow.set(0)
direct_radio = IntVar()
direct_radio.set(1)
overr = IntVar()
overr.set(0)
#------------------------------------------------------------------------------------------------------------

#8b0000 DARK RED
#006400 DARK GREEN

#------------------------------------Fixed Window Setup----------------------------------------------
s = ttk.Style()
s.configure('TButton', font = ("SegoeUi",10, "bold"))

t1 = ttk.Label(window, text = "Hyperloop United Control Panel", font = ("SegoeUi",15, "bold") )
t1.place(relx =0.5, rely = 0.05, anchor = CENTER)

def merge_command():
    global client, stat_index
    tcp.sendto("Merge".encode("utf-8"), client)
    stat_index = 1 
    change_status()
merge = ttk.Button(window, text = "Merge", command = merge_command)
merge.place(x = 20, y = 520 , height = 40)

def launch_command():
    global  client, stat_index, condition
    tcp.sendto("Launch".encode("utf-8"), client)
    stat_index = 2
    condition = True
    read_data()
    
    
launch = ttk.Button(window, text = "Launch", command = launch_command, state = DISABLED)
launch.place(x = 120, y = 520,height = 40)

def break_command():
    global client, stat_index
    tcp.sendto("Break".encode("utf-8"), client)
    stat_index = 3
    change_status()
Break = ttk.Button(window, text = "Break", command = break_command,  state = DISABLED)
Break.place(x = 220, y = 520,height = 40)

def emergency_command():
    global  client, stat_index
    tcp.sendto("Emergency".encode("utf-8"), client)
    stat_index = 4
    change_status()
emergency = ttk.Button(window, text = "EMERGENCY", command = emergency_command, state = DISABLED)
emergency.place(x = 320, y = 520,height = 40, width = 120)



ping = Label(window, textvariable = latency, fg="green", font = ("SegoeUi",8, "bold"))
ping.place(x=20, y = 650)



temp1 = Label(window, textvariable = temp_1, fg="#E64A19", font = ("SegoeUi",8, "bold"))
temp1.place(x=1200, y = 515, anchor = E)

temp2 = Label(window, textvariable = temp_2, fg="#E64A19", font = ("SegoeUi",8, "bold"))
temp2.place(x=1200, y = 535, anchor = E)

temp3 = Label(window, textvariable = temp_3, fg="#E64A19", font = ("SegoeUi",8, "bold"))
temp3.place(x=1200, y = 555, anchor = E)

temp4 = Label(window, textvariable = temp_4, fg="#E64A19", font = ("SegoeUi",8, "bold"))
temp4.place(x=1200, y = 575, anchor = E)

temp5 = Label(window, textvariable = temp_5, fg="#E64A19", font = ("SegoeUi",8, "bold"))
temp5.place(x=1200, y = 595, anchor = E)

power_consumption = Label(window, textvariable = power_cons,fg="#512DA8", font = ("SegoeUi",8, "bold"))
power_consumption.place(x=1200, y = 615, anchor = E)

max_speed = Label(window, textvariable= topsp, fg="#1976D2", fon = ("SegoeUi", 8, "bold"))
max_speed.place(x=1200, y = 635, anchor = E)

t2 = Label(window, text = "Cruise Progress", font = ("SegoeUi",11, "bold"))
t2.place(relx =0.505, rely = 0.855, anchor = CENTER) 

pb = ttk.Progressbar(window, orient = "horizontal", mode= "determinate", variable = cruzperc, length = 534)
pb.place(relx = 0.505, rely = 0.9, anchor = CENTER)

value_label = ttk.Label(window, textvariable= cruzperc, font= ("SegoeUi",10, "italic"))
value_label.place(relx = 0.270, rely = 0.9, anchor = CENTER)


state_label = ttk.Label(window, textvariable= cruzstat, font= ("SegoeUi",10))
state_label.place(x = 580, y = 640)


save_button = ttk.Button(window, text = "Save Info", command= save_csv)
save_button.place(x= 20, y =600, height=50, width = 80)

clean_button = ttk.Button(window, text = "Clean Page", command = clean_data)
clean_button.place(x = 120, y = 600, height= 50, width = 80)
#------------------------------------------------------------------------------------------------------------

#------------------------------------Tab Setup----------
tab = ttk.Notebook(window, height = 421, width = 881)
pre_check = ttk.Frame(tab)
tele = ttk.Frame(tab)
conn = ttk.Frame(tab)
test = ttk.Frame(tab)
energy = ttk.Frame(tab) 
feed = ttk.Frame(tab)

tab.add(pre_check, text="Preflight Checks")
tab.add(tele, text="Telemetry")
tab.add(conn, text="Connection")
tab.add(test, text="Test Drive")
tab.add(energy, text="Energy")
tab.add(feed, text="Feed")

tab.place(x = 20, y=60)
#--------------------------------------------------------------------------------------------------------------




#------------------------------------Preflight check tab-------------------------------------------------------

#----------Checks function to enable
def prefcheckboxes():
    
    if (connvar.get() and podmvar.get() and compvar.get() and idevar.get() and sensvar.get() and ipvar.get()) == 1:
        launch['state'] = NORMAL
        Break['state'] = NORMAL
        emergency['state'] = NORMAL
        ready_label['text'] = 'Ready To Launch'
        ready_label['foreground'] = "#006400"
    else:
        launch['state'] = DISABLED
        Break['state'] = DISABLED
        emergency['state'] = DISABLED
        ready_label['text'] = 'Not Ready To Launch'
        ready_label['foreground'] = "#8b0000"
    pre_check.update()


#----------Checkboxes
conn_check = ttk.Checkbutton(pre_check, text= "Connected", variable = connvar , onvalue = 1, offvalue= 0, command = prefcheckboxes)
conn_check.place(x = 30, y= 30)

podmont_check = ttk.Checkbutton(pre_check, text= "Pod Mounted", variable = podmvar , onvalue = 1, offvalue= 0, command = prefcheckboxes)
podmont_check.place(x = 30, y= 55)

comput_check = ttk.Checkbutton(pre_check, text= "Computer", variable = compvar , onvalue = 1, offvalue= 0, command = prefcheckboxes)
comput_check.place(x = 30, y= 80)

ides_check = ttk.Checkbutton(pre_check, text= "IDE's", variable = idevar , onvalue = 1, offvalue= 0, command = prefcheckboxes)
ides_check.place(x = 30, y= 105)

sensor_check = ttk.Checkbutton(pre_check, text= "Sensors", variable = sensvar , onvalue = 1, offvalue= 0, command = prefcheckboxes)
sensor_check.place(x = 30, y= 130)

ipcam_check = ttk.Checkbutton(pre_check, text= "IPCAM", variable = ipvar , onvalue = 1, offvalue= 0, command = prefcheckboxes)
ipcam_check.place(x = 30, y= 155)

def start_sensor():
    global condition,  client
    tcp.sendto("Sensor_on".encode("utf-8"), client)
    condition = True
    read_data()
sensor_on = ttk.Button(pre_check, text = "Sensors On", command = start_sensor) #command = 
sensor_on.place(x = 30, y = 195 , height = 40, width=100) #command = 

def sensor_close():
    global condition, client
    condition = False
    tcp.sendto("Sensor_off".encode("utf-8"), client)
    clean_data()
sensor_off = ttk.Button(pre_check, text = "Sensors Off", command = sensor_close)
sensor_off.place(x = 150, y = 195 , height = 40, width = 100)
    

ready_label = ttk.Label(pre_check, text = "Not Ready To Launch", foreground = '#8b0000', font = ("SegoeUi", 12, "bold"))
ready_label.place(x=33, y = 270)



#------------------------------------Telemetry tab------------------------------------------------------------------------
livetitle = ttk.Label(tele, text = "Live Flight Feed", foreground= "#006400" , font = ("SegoeUi", 11, "italic"))
livetitle.place(x= 30, y = 20)
s.configure('TFrame', borderwidth = 3, bordercolor= "#000000")

#---------------Laser Frame
laserframe = ttk.Frame(tele, relief=GROOVE, height= 150 , width = 460)
laserframe.place(x= 70, y = 65)

basref = ttk.Label(laserframe, text = "Based On Reflectors" , font = ("SegoeUi", 12))
basref.place(x= 10, y = 10)


poz = ttk.Label(laserframe, text = "Positions" , font = ("SegoeUi", 11,"bold", UNDERLINE))
poz.place(x= 40, y = 35)
velo = ttk.Label(laserframe, text = "Velocity" , font = ("SegoeUi", 11,"bold", UNDERLINE))
velo.place(x= 180, y = 35)
ax = ttk.Label(laserframe, text = "Acceleration" , font = ("SegoeUi", 11,"bold", UNDERLINE))
ax.place(x= 310, y = 35)


telex = ttk.Label(laserframe, text = "X", font = ("SegoeUi", 10, "bold", UNDERLINE))
telex.place(x = 25, y = 60)

teley = ttk.Label(laserframe, text = "Y", font = ("SegoeUi", 10, "bold", UNDERLINE))
teley.place(x = 25, y = 85)

telez = ttk.Label(laserframe, text = "Z", font = ("SegoeUi", 10, "bold", UNDERLINE))
telez.place(x = 25, y = 110)

xax = ttk.Label(laserframe, textvariable = xacclaz , font = ("SegoeUi", 10,))
xax.place(x= 320, y = 60)
yax = ttk.Label(laserframe, textvariable = yacclaz , font = ("SegoeUi", 10))
yax.place(x= 320, y = 85)
zax = ttk.Label(laserframe, textvariable = zacclaz , font = ("SegoeUi", 10))
zax.place(x= 320, y = 110)
xax = ttk.Label(laserframe, textvariable = xpozlaz , font = ("SegoeUi", 10,))
xax.place(x= 50, y = 60)
yax = ttk.Label(laserframe, textvariable = ypozlaz , font = ("SegoeUi", 10))
yax.place(x= 50, y = 85)
zax = ttk.Label(laserframe, textvariable = zpozlaz , font = ("SegoeUi", 10))
zax.place(x= 50, y = 110)
xax = ttk.Label(laserframe, textvariable = xvellaz , font = ("SegoeUi", 10,))
xax.place(x= 190, y = 60)
yax = ttk.Label(laserframe, textvariable = yvellaz , font = ("SegoeUi", 10))
yax.place(x= 190, y = 85)
zax = ttk.Label(laserframe, textvariable = zvellaz , font = ("SegoeUi", 10))
zax.place(x= 190, y = 110)


#-------------------Degrees and counters
livetitle = ttk.Label(tele, text = "Degrees" , font = ("SegoeUi", 11, "bold", UNDERLINE))
livetitle.place(x= 560, y = 55)

livetitle = ttk.Label(tele, text = "Roll:" , font = ("SegoeUi", 10))
livetitle.place(x= 580, y = 85)

livetitle = ttk.Label(tele, text = "Yaw:" , font = ("SegoeUi", 10))
livetitle.place(x= 580, y = 115)

livetitle = ttk.Label(tele, text = "Pitch:" , font = ("SegoeUi", 10))
livetitle.place(x= 580, y = 145)


livetitle = ttk.Label(tele, textvariable= rol , font = ("SegoeUi", 10))
livetitle.place(x= 620, y = 85)
livetitle = ttk.Label(tele, textvariable = yav , font = ("SegoeUi", 10))
livetitle.place(x= 620, y = 115)
livetitle = ttk.Label(tele, textvariable = pich , font = ("SegoeUi", 10))
livetitle.place(x= 620, y = 145)



livetitle = ttk.Label(tele, text = "Reflectors Counted:" , font = ("SegoeUi", 10, "bold"))
livetitle.place(x= 580, y = 175)



livetitle = ttk.Label(tele, textvariable = refc , font = ("SegoeUi", 10, "bold"))
livetitle.place(x= 708, y = 175)



#------------------------------------Connection tab------------------------------------------------------------------------
tconn = Label(conn, text = "IP Address:", font = ("SegoeUi", 10))
tconn.place(x = 20, y = 28)

ip = Entry(conn, relief= GROOVE, borderwidth= 2, width = 25 , textvariable= client_host)
ip.place(x=100, y=30)

tpconn = Label(conn, text = "Port:", font = ("SegoeUi", 10))
tpconn.place(x = 20, y = 58)

portt = Entry(conn, relief= GROOVE, borderwidth= 2, width = 25 , textvariable= client_port)
portt.place(x=100, y=60)



def check_ping(client):
    time1 = time.time()
    import subprocess
    while True:
        try:
            test = subprocess.Popen(["ping","-n", "1", client.get()], stdout=subprocess.PIPE)
            output = test.communicate()[0].decode("utf-8")
            index = output.find("time=")
            index2 = output.find("ms")
            data = output[index+5: index2]
            data = str(round(float(data)))
            latency.set("Latency: "+data +" ms")
            time2 = time.time()
            time2 = round(time2-time1)
            tconn3["text"] = "Elapsed time: " + str(time2)+"s"
            window.update()
            time.sleep(0.1)
        except:
            break
    
def connect():
    global client
    client = (client_host.get(), client_port.get())
    tconn2["text"] = "Connected: "+client_host.get()
    check_ping(client_host)

bconn = ttk.Button(conn, text = "Connect", command = connect)
bconn.place(x = 300, y = 27, height = 30)


tconn2 = Label(conn, text = "Connected:", fg="green",font = ("SegoeUi", 11))
tconn2.place(x=450, y=27)



tconn3 = Label(conn, text= "Elapsed time: " , fg="green",font = ("SegoeUi", 10, "bold"))
tconn3.place(x=450, y=52)

tconn4 = Label(conn, textvariable= latency, fg="green",font = ("SegoeUi", 10, "bold"))
tconn4.place(x=450, y=77)


#------------------------------------Test Drive tab------------------------------------------------------------------------

##Functions
def breakactivate():
    if brakman.get() == 1:
        frenslid['state'] = NORMAL
    else:
        frenslid['state'] = DISABLED
        frender.set(0)

def limactivate():
    if limslow.get() == 1:
        limslowbutton['state'] = NORMAL
        limfastbutton['state'] = NORMAL
        limsstop["state"] = NORMAL
        direcbackw['state'] = NORMAL
        levbut['state'] = NORMAL
        direcforw['state'] = NORMAL
        levstop['state'] = NORMAL
        forw_label['foreground'] = "#006400"
        backw_label['foreground'] = "#8b0000"
    else:#808080
        limslowbutton['state'] = DISABLED
        limfastbutton['state'] = DISABLED
        limsstop["state"] = DISABLED
        direcbackw['state'] = DISABLED
        direcforw['state'] = DISABLED
        levbut['state'] = DISABLED
        levstop['state'] = DISABLED
        forw_label['foreground'] = "#808080"
        backw_label['foreground'] = "#808080"




frenslid = Scale(test, from_=0, to=2, variable = frender, orient=VERTICAL, length=340, tickinterval= 1, state= DISABLED)
frenslid.place(x = 50, y = 50)

basw = ttk.Label(test, text = "Brake Control", font = ("SegoeUi", 12, "bold"))
basw.place(x= 35, y = 20)

def brake_test():

    if frender.get() == 0:
        tcp.sendto("Brake0".encode("utf-8"), client)
    elif frender.get() == 1:
        tcp.sendto("Brake1".encode("utf-8"), client)
    elif frender.get() == 2:
        tcp.sendto("Brake2".encode("utf-8"), client)
    
brake = ttk.Button(test, text = "Brake Test", command = brake_test)
brake.place(x = 110, y=200)

testsep = ttk.Separator(test, orient= VERTICAL)
testsep.place(x= 200, y= 30 , height = 360, width = 20)

brak_check = ttk.Checkbutton(test, text = "Manual Breaks Activation", variable = brakman , onvalue = 1, offvalue= 0, command = breakactivate)
brak_check.place(x = 250, y = 20)

lim_check = ttk.Checkbutton(test, text = "Levitation and LIM Activation", variable = limslow , onvalue = 1, offvalue= 0, command = limactivate)
lim_check.place(x = 250, y = 40)

def LIM_Slow():
    global  client
    if direct_radio.get() == 1:
        tcp.sendto("Half_Forward".encode("utf-8"), client)
    else:
        tcp.sendto("Half_Backward".encode("utf-8"), client)
limslowbutton = ttk.Button(test, text = "Start LIM Slow", command = LIM_Slow, state = DISABLED) #commmand
limslowbutton.place(x=250 , y =70, height = 40, width = 150)

def LIM_Fast():
    global client
    if direct_radio.get() == 1:
        tcp.sendto("Full_Forward".encode("utf-8"), client)
    else:
        tcp.sendto("Full_Backward".encode("utf-8"), client)
limfastbutton = ttk.Button(test, text = "Start LIM Fast", command = LIM_Fast, state = DISABLED) #commmand
limfastbutton.place(x=250 , y =120, height = 40, width = 150)

def LIM_Stop():
    global client
    tcp.sendto("Stop".encode("utf-8"), client)
limsstop = ttk.Button(test, text = "Stop LIM Slow", command = LIM_Stop, state = DISABLED) #commmand
limsstop.place(x=400 , y =95, height = 40, width = 150)



direcforw = ttk.Radiobutton(test, text = "" , variable = direct_radio, value = 1, state = DISABLED)
direcforw.place(x = 285 , y =230)

direcbackw = ttk.Radiobutton(test, text = "" , variable = direct_radio, value = 0, state = DISABLED)
direcbackw.place(x = 410 , y =230)

forw_label = ttk.Label(test, text = "FORWARD", foreground = "#808080", font = ("SegoeUi", 12, "bold"))
forw_label.place(x = 250, y = 250)

backw_label = ttk.Label(test, text = "BACKWARD", foreground = "#808080", font = ("SegoeUi", 12, "bold"))
backw_label.place(x = 370, y = 250)

def Lev_test():
    global client
    tcp.sendto("Lev_on".encode("utf-8"), client)
levbut = ttk.Button(test, text = "LevM Test", state = DISABLED, command = Lev_test)
levbut.place(x = 250, y= 170, height = 40, width = 150)

def Lev_stop():
    global client
    tcp.sendto("Lev_off".encode("utf-8"), client)
levstop = ttk.Button(test, text = "LevM Stop", state = DISABLED, command = Lev_stop)
levstop.place(x = 400, y= 170, height = 40, width = 150)




#---------------UI Override


def override():
    if overr.get() == 1:
        launchover['state'] = NORMAL
        Breakover['state'] = NORMAL
        emergencyover['state'] = NORMAL
    else:
        launchover['state'] = DISABLED
        Breakover['state'] = DISABLED
        emergencyover['state'] = DISABLED


over_check = ttk.Checkbutton(test, text= "UI Fault Override", variable = overr , onvalue = 1, offvalue= 0, command = override)
over_check.place(x = 250, y= 300)

launchover = ttk.Button(test, text = "Launch", command = launch_command, state = DISABLED)
launchover.place(x = 250, y = 340 , height = 40)

Breakover = ttk.Button(test, text = "Break", command = break_command,  state = DISABLED)
Breakover.place(x = 450, y = 340 , height = 40)

emergencyover = ttk.Button(test, text = "EMERGENCY", command = emergency_command, state = DISABLED)
emergencyover.place(x = 650, y = 340, height = 40, width = 120)



#------------------------------------Energy tab------------------------------------------------------------------------
tenergy = Label(energy, text = "2S", font = ("SegoeUi", 10, "bold"))
tenergy.place( x =70, y = 30)

tenergy2 = Label(energy, text = "6S", font = ("SegoeUi", 10, "bold"))
tenergy2.place( x =170, y = 30)

tenergy3 = Label(energy, text = "12S", font = ("SegoeUi", 10, "bold"))
tenergy3.place( x =270, y = 30)
a = ttk.Style()
a.theme_use("winnative")
a.configure("2s_bar.Vertical.TProgressbar", foreground = "red", background = "red")
a.configure("6s_bar.Vertical.TProgressbar", foreground = "red", background = "red")
a.configure("12s_bar.Vertical.TProgressbar", foreground = "red", background = "red")
pbenergy = ttk.Progressbar(energy, style = "2s_bar.Vertical.TProgressbar", orient = "vertical", mode= "determinate", variable = SoC_2s, length = 200)
pbenergy.place(x = 72, y = 80)


pbenergy2 = ttk.Progressbar(energy, style = "6s_bar.Vertical.TProgressbar", orient = "vertical", mode= "determinate", variable = SoC_6s, length = 200)
pbenergy2.place(x = 172, y = 80)

pbenergy3 = ttk.Progressbar(energy, style = "12s_bar.Vertical.TProgressbar", orient = "vertical", mode= "determinate", variable = SoC_12s, length = 200)
pbenergy3.place(x = 277, y = 80)


tenergy5 = Label(energy, textvariable = SoC_2s, font = ("SegoeUi", 10))
tenergy5.place( x= 72, y = 290)

tenergy6 = Label(energy, textvariable = SoC_6s, font = ("SegoeUi", 10))
tenergy6.place( x= 172, y = 290)

tenergy7 = Label(energy, textvariable = SoC_12s, font = ("SegoeUi", 10))
tenergy7.place( x= 272, y = 290)

def onn_2s():
    tcp.sendto("2Son".encode("utf-8"), client)
benergy = ttk.Button(energy, text="2S ON", command = onn_2s)
benergy.place(x = 22, y = 350)

def off_2s():
    tcp.sendto("2Soff".encode("utf-8"), client)
benergy2 = ttk.Button(energy, text="2S OFF", command = off_2s)
benergy2.place(x=22, y = 380)

def onn_6s():
    tcp.sendto("6Son".encode("utf-8"), client)
benergy = ttk.Button(energy, text="6S ON", command = onn_6s)
benergy.place(x = 122, y = 350)

def off_6s():
    tcp.sendto("6Soff".encode("utf-8"), client)
benergy2 = ttk.Button(energy, text="6S OFF", command = off_6s)
benergy2.place(x=122, y = 380)

def onn_12s():
    tcp.sendto("12Son".encode("utf-8"), client)
benergy3 = ttk.Button(energy, text ="12S ON", command = onn_12s)
benergy3.place(x = 222, y = 350)

def off_12s():
    tcp.sendto("12Soff".encode("utf-8"), client)
benergy4 = ttk.Button(energy, text = "12S OFF", command = off_12s)
benergy4.place(x = 222, y = 380)


energysep = ttk.Separator(energy, orient= VERTICAL)
energysep.place(x= 400, y= 30 , height = 360, width = 20)

tenergy9 = Label(energy, text = "Power Consumption (2S)", font = ("SegoeUi", 12, "bold"))
tenergy9.place(x = 470, y = 70)

tenergy10 = Label(energy, text = "Power Consumption (6S)", font = ("SegoeUi", 12, "bold"))
tenergy10.place(x = 470, y = 145)

tenergy11 = Label(energy, text = "Power Consumption (12S)", font = ("SegoeUi", 12, "bold"))
tenergy11.place(x = 470, y = 220)

tenergy12 = Label(energy, text = "Power Consumption Total", font = ("SegoeUi", 12, "bold"))
tenergy12.place(x = 470, y = 295)

tenergy13 = Label(energy, textvariable = powercons_2s, width = 10,fg = "white", bg = "#311B92", font = ("SegoeUi", 12))
tenergy13.place(x = 750, y = 70)

tenergy14 = Label(energy, textvariable = powercons_6s, width = 10,fg = "white", bg = "#311B92", font = ("SegoeUi", 12))
tenergy14.place(x = 750, y = 145)

tenergy15 = Label(energy, textvariable = powercons_12s, width = 10,fg = "white", bg = "#311B92", font = ("SegoeUi", 12))
tenergy15.place(x = 750, y = 220)

tenergy16 = Label(energy, textvariable = powercons_t, width = 10,fg = "white", bg = "#311B92", font = ("SegoeUi", 12))
tenergy16.place(x = 750, y = 295)





#------------------------------------Feed tab------------------------------------------------------------------------
def clearfeed():
    feededit.delete('1.0' , END)
feededit = Text(feed, height = 23.4, width = 108)
feededit.place(x= 5, y = 5)
def savefeed():
    with open("feed_veri.txt", "w") as file:
        file.write(feededit.get("0.0", END))
saveallbut = ttk.Button(feed, text= "Save All", command=savefeed) 
saveallbut.place(x = 785 ,y = 390)

clearallbut = ttk.Button(feed, text = "Clear All", command = clearfeed)
clearallbut.place(x = 5, y = 390)


window.mainloop()
tcp.close()