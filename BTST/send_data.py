import screen_brightness_control as sbc
from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import urllib.request

process_time={}
timestamp = {}

def BrightNessCalculation():# get the brightness of the primary display
        primary_brightness = sbc.get_brightness(display=0)
        time.sleep(1)
        print(f"System Brightness : {primary_brightness}")
        data=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=HL3XAT1LKWZYF9ZF&field1=" + str(primary_brightness))
        print(data)

def ScreentTimeCalculation():
    current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
    timestamp[current_app] = int(time.time())
    time.sleep(1)
    if current_app not in process_time.keys():
        process_time[current_app] = 0
    process_time[current_app] = process_time[current_app]+int(time.time())-timestamp[current_app]
    print(process_time)
    ScreenTime = sum(process_time.values())
    print(sum(process_time.values()))
    data = urllib.request.urlopen(f"https://api.thingspeak.com/update?api_key=HL3XAT1LKWZYF9ZF&field2={ScreenTime}")
    print(data)

#Read data from temp.txt file and sending Age and Gender data to cloud
f = open('temp.txt','r')
gender = f.readline()
Age = f.readline()
print(gender)
print(Age)
f.close()
while True :
        gender_response = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=HL3XAT1LKWZYF9ZF&field3=" + str(gender))
        ScreentTimeCalculation()
        BrightNessCalculation()
        age_response = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=HL3XAT1LKWZYF9ZF&field4=" + str(Age))
        print(f"Age response :{age_response}")
        print(f"gender response : {gender_response}")


        