#!/usr/bin/python

from phue import Bridge
import websocket
import _thread as thread
import time
import json
from get_pass import get_bridge_ip, get_pb_address

b = Bridge(get_bridge_ip())
b.connect()
b.get_api()
app_colors = {
        "Messenger":{
            "hue": 46920,
            "sat": 100
        },
        "Snapchat":{
            "hue": 12750,
            "sat": 255
        },
        "Twitch":{
            "hue": 56100,
            "sat": 255
        },
        "Facebook":{
            "hue": 46920,
            "sat": 255
        },
        "Gmail":{
            "hue": 65280,
            "sat": 255
        },
        "Messages":{
            "hue": 25500,
            "sat": 255
        }
    }

def change_light(app):
    def_color = b.get_light("Floor Lamp", "hue")
    def_sat = b.get_light("Floor Lamp", "sat")
    def_bri = b.get_light("Floor Lamp", "bri")
    if app in app_colors:
        b.set_light("Floor Lamp", "sat", app_colors[app]['sat'])
        b.set_light("Floor Lamp", "hue", app_colors[app]['hue'])
    else:
        b.set_light("Floor Lamp", "bri", 0)
    time.sleep(1)
    b.set_light("Floor Lamp", "bri", def_bri)
    b.set_light("Floor Lamp", "sat", def_sat)
    b.set_light("Floor Lamp", "hue", def_color)

def on_message(ws, message):
    response = json.loads(message)
    if response['type'] == "push":
        if response['push']['type'] != "dismissal":
            print("notif received")
            change_light(response['push']['application_name'])
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            #ws.send("Hello %d" %i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(get_pb_address(),
            on_message = on_message,
            on_error = on_error,
            on_close = on_close)
    #ws.on_open = on_open
    ws.run_forever()
