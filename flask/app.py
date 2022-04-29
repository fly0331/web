from flask import Flask, jsonify, request, render_template
from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811 
from adafruit_dht import DHT11
import board
import os
import time
import RPi.GPIO as GPIO

app = Flask(__name__)

ccs =  Adafruit_CCS811()
dht = DHT11(board.D26)
humi = dht.humidity
temp = dht.temperature

while not ccs.available():
	pass

@app.route("/")
def index():
   return render_template('index.html')

def get_co2_data():
    while True:
        if ccs.available():
            if not ccs.readData():
              co2=ccs.geteCO2()
              if co2 is not None:
                return co2

def get_dht_data():
    while True:
        try:
            temperature, humidity = dht.temperature, dht.humidity
            if temperature is not None and humidity is not None:
                return temperature, humidity
            else:
                raise
        except:
            time.sleep(0.5)
            
def get_light_data():
    channel =4  #GPIO4，作为后续BCM编码模式，即第7号口
    GPIO.setmode(GPIO.BCM) 
    time.sleep(1)
    GPIO.setup(channel, GPIO.IN)
    count=0
    todark="太暗囉請開燈"
    ok="光線充足"
    while count<10:
        if GPIO.input(channel) == GPIO.LOW:
            
            return ok
        else:
            return todark
        

@app.route("/<pin>/<action>")
def status(pin,action):
    if pin == "dhtpin" and action == "get":
        co22 = get_co2_data()
        co2='co2:'+str(co22)
        temp, humi = get_dht_data() 
        humi = '{0:0.1f}' .format(humi)
        temp = '{0:0.1f}' .format(temp)
        temperature = 'Temperature: ' + temp 
        humidity =  'Humidity: ' + humi
        lighting=get_light_data()
        light='Light:'+lighting
       
    templateData = {
       'temperature' : temperature,
       'humidity' : humidity,
       'co2' : co2,
       'light':light
    }
    return render_template('index.html', **templateData)




@app.route("/accounts") #代表我們要處理的網站路徑
def accounts():
    return render_template("accounts.html")

@app.route("/add-product")
def addproduct():
    return render_template("add-product.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/management")
def management():
    return render_template("management.html")

if __name__=="__main__": #如果以主程式執行
    app.run() #立刻啟動伺服器