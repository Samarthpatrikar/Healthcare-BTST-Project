import conf
from boltiot import Sms
import json, time  
import urllib.request
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)

ageList = {
    '0-2': 0, '4-6': 1, '8-12': 2, '15-20': 3, '25-32': 4, '38-43': 5, '48-53': 6, '60-100': 7
}
genderList=['Male','Female']

def ReadField1() :  
        print ("Reading System Brightness percentage")
        with urllib.request.urlopen('https://api.thingspeak.com/channels/1537960/fields/1.json?results=1') as response:
            data1 = json.load(response)
        return  data1['feeds'][0]['field1']
def ReadField2():
        print("Reading Working Screen Time  duration ")
        with urllib.request.urlopen('https://api.thingspeak.com/channels/1537960/fields/2.json?results=2') as response:
            data2 = json.load(response)
        return data2['feeds'][0]['field2']
    
def ReadField3():
        print("Reading the Estimate gender of user ")
        with urllib.request.urlopen('https://api.thingspeak.com/channels/1537960/fields/3.json?results=1') as response:
            data3 = json.load(response)
        return  data3['feeds'][0]['field3']
def ReadField4():
        print("Reading the Estimate Age of user ")
        with urllib.request.urlopen('https://api.thingspeak.com/channels/1537960/fields/4.json?results=1') as response:
            data4 = json.load(response)
        return  data4['feeds'][0]['field4']
def Sending_sms(SMS):
            print("Making request to Twilio to send a SMS")
            response = sms.send_sms(SMS)
            print("Response received from Twilio is: " + str(response))
            print("Status of SMS at Twilio is :" + str(response.status))
val = None     
while True:
    brightness=  ReadField1()
    print(brightness)
    screentime = ReadField2()
    print(screentime)
    gender = ReadField3()
    print(gender)
    Age  = ReadField4()
    print(Age)
    if Age is not None :
            Age = ageList.get(Age)
    try:

        if screentime is not None :
            if( screentime >= '10') :
                  Sending_sms("You have been  working for 1 hr !! \n you should take rest for 15-20 min")       
        if Age is not None :
            if  Age == ageList['0-2'] :
                    Sending_sms("you should have no screentime per day !!")
            if  Age == ageList['4-6'] :
                    Sending_sms("you should have 1 hr screentime per day !! \n you should follow 20-20-20 Rule to keep your eyes healthy")
            if  Age == ageList['8-12'] :
                    Sending_sms("you should have 1-2 hr screentime per day !! \n You should take break of 15-20 min after one hr of work to keep your eyes healthy")
            if  Age == ageList['15-20'] :
                    Sending_sms("you should have no screentime per day !!""you should have 1 hr screentime !! \n  Follow 20-20-20 Rule to keep your eyes  \n Should take break of 15-20 min after one hr of work to keep your eyes healthy ")
            if  (Age == ageList['25-32'])  or ( Age == ageList['38-43']) or (Age == ageList['48-53'])  or (Age == ageList['60-100']):
                    Sending_sms("you should have 4-5 hr screentime per day !! \n You should take break of 15-20 min after one hr of work to keep your eyes healthy")
        if brightness is not None :
             if(brightness <= '30') : 
                 Sending_sms("Your System Brightness is too LOW !!! \n you should increase it to stay productive and healthy")
             if(brightness >= '60') :
                 Sending_sms("Your System Brightness is too HIGH !!! \n you should decrese it to stay productive and healthy")
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
