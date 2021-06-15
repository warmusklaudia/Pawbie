from RPi import GPIO
from helpers.Class_MCP import SPI
from helpers.Class_LCD import LCD
from helpers.Class_steppermotor import Motor
from repositories.DataRepository import DataRepository


from subprocess import check_output
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request, redirect

from datetime import datetime
import time
import threading
import os


# Code voor hardware


weekDays = ("Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday")

mcp = SPI()
motor = Motor()

waterpump = 18

btn_food = 6
btn_water = 5

motor_channel = (22, 27, 17, 4)


def btn_food_callback(pin):
    if (GPIO.event_detected(btn_food)):
        print("BTN food PRESS, pin {}".format(pin))
        control_motor(5)


def btn_water_callback(pin):
    if (GPIO.event_detected(btn_water)):
        print("BTN water PRESS, pin {}".format(pin))
        control_waterpump(2)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(btn_food, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn_water, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(waterpump, GPIO.OUT)
GPIO.add_event_detect(btn_water, GPIO.BOTH,
                      callback=btn_water_callback, bouncetime=150)
GPIO.add_event_detect(btn_food, GPIO.FALLING,
                      callback=btn_food_callback, bouncetime=150)

GPIO.setup(motor_channel, GPIO.OUT, initial=GPIO.LOW)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)
CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


def lcd():
    lcd = LCD()
    lcd.setup()
    lcd.init_LCD()

    hour = datetime.now().strftime('%H')
    minute = datetime.now().strftime('%M')
    day = datetime.today().strftime('%A')
    date = f'{day} {hour}:{minute}'

    ips = check_output(['hostname', '--all-ip-addresses'])
    ips = str(ips)
    ip = ips.strip("b'").split(" ")

    lcd.write_message(date)
    lcd.cursor_line(1)
    lcd.write_message(ip[1])


def control_waterpump(duration):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("start waterpomp")
    DataRepository.update_status_actuator(7, 1)
    GPIO.output(waterpump, 1)
    DataRepository.add_historiek(7, 7, time_now, 0)
    time.sleep(duration)
    GPIO.output(waterpump, 0)
    DataRepository.update_status_actuator(7, 0)
    print("stop waterpomp")


def control_motor(duration):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('Start motor')
    DataRepository.update_status_actuator(6, 1)
    motor.start(duration)
    DataRepository.update_status_actuator(6, 0)
    DataRepository.add_historiek(6, 6, time_now, 0)
    print('Stop motor')


def value_to_gram(waarde):
    return (-0.31 * waarde + 272.5)


def value_to_cm(waarde):
    return (-.02 * waarde + 24.8)


def get_value_fsr_food():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_value_fsr_food_dict = DataRepository.read_last_value_fsr_food()
    value_fsr_food = round(value_to_gram(mcp.read_channel(1)))
    for key, last_value_fsr_food in last_value_fsr_food_dict.items():
        x = int(last_value_fsr_food)
        # print(f'Vorige waarde FSR Food: {x}')
        # print(f'nieuwe waarde FSR Food: {value_fsr_food}')
        if (value_fsr_food + 10) < x:
            DataRepository.add_historiek(3, 3, time_now, value_fsr_food)
            # print('less food: data added')
        elif (value_fsr_food - 10) > last_value_fsr_food:
            DataRepository.add_historiek(3, 3, time_now, value_fsr_food)
        #     print('more food: data added')
        # else:
        #     print('food: no changes')
    socketio.emit('B2F_update_value_fsr_food', {"Waarde": value_fsr_food})


def get_value_fsr_water():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_value_fsr_water_dict = DataRepository.read_last_value_fsr_water()
    value_fsr_water = round(value_to_gram(mcp.read_channel(0)))
    for key, last_value_fsr_water in last_value_fsr_water_dict.items():
        x = int(last_value_fsr_water)
        # print(f'Vorige waarde FSR Water: {x}')
        # print(f'Nieuwe waarde FSR Water: {value_fsr_water}')
        if (value_fsr_water + 10) < x:
            DataRepository.add_historiek(2, 2, time_now, value_fsr_water)
            # print('Less water: data added')
        elif (value_fsr_water - 10) > last_value_fsr_water:
            DataRepository.add_historiek(2, 2, time_now, value_fsr_water)
        #     print('More water: data added')
        # else:
        #     print('Water: no changes')
    socketio.emit('B2F_update_value_fsr_water', {"Waarde": value_fsr_water})


def get_value_dms_food():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_time = datetime.now().strftime('%H:%M')
    value_dms_food = round(value_to_cm(mcp.read_channel(2)))
    x = weekDays[datetime.now().weekday()]
    if value_dms_food < 12:
        DataRepository.add_historiek(4, 5, time_now, value_dms_food)
        socketio.emit('B2F_update_value_dms_food', {
                      "Dag": x, "Uur": current_time})
    #     print(f'Data added DMS Food {value_dms_food}')
    # else:
    #     print('Food DMS: no changes')


def get_value_dms_water():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_time = datetime.now().strftime('%H:%M')
    value_dms_water = round(value_to_cm(mcp.read_channel(3)))
    x = weekDays[datetime.now().weekday()]
    if value_dms_water < 12:
        DataRepository.add_historiek(5, 4, time_now, value_dms_water)
        socketio.emit('B2F_update_value_dms_water', {
            "Dag": x, "Uur": current_time})
        # print(f'Data added DMS Water {value_dms_water}')
    # else:
    #     print('Water DMS: no changes')


def get_watersensor():
    value_watersensor = mcp.read_channel(4)
    if value_watersensor < 200:
        value_watersensor = 0
    elif value_watersensor > 200:
        value_watersensor = 1
    socketio.emit('B2F_update_value_watersensor',
                  {"Waarde": value_watersensor})


def checkSchema():
    current_time = datetime.now().strftime('%H:%M')
    time_food_dict1 = DataRepository.read_voederschema(1)
    if time_food_dict1['Uur'] == current_time and time_food_dict1['Hoeveelheid'] != 0:
        control_motor(10)
    time_food_dict2 = DataRepository.read_voederschema(2)
    if time_food_dict2['Uur'] == current_time and time_food_dict2['Hoeveelheid'] != 0:
        control_motor(10)
    time_food_dict3 = DataRepository.read_voederschema(3)
    if time_food_dict3['Uur'] == current_time and time_food_dict3['Hoeveelheid'] != 0:
        control_motor(10)
    time_water_dict1 = DataRepository.read_drankschema(4)
    if time_water_dict1['Uur'] == current_time and time_water_dict1['Hoeveelheid'] != 0:
        control_waterpump(3)
    time_water_dict2 = DataRepository.read_drankschema(5)
    if time_water_dict2['Uur'] == current_time and time_water_dict2['Hoeveelheid'] != 0:
        control_waterpump(3)
    time_water_dict3 = DataRepository.read_drankschema(6)
    if time_water_dict3['Uur'] == current_time and time_water_dict3['Hoeveelheid'] != 0:
        control_waterpump(3)


def threading_lcd_schema():
    while True:
        print('*** CHECK ***')
        lcd()
        checkSchema()
        time.sleep(60)


thread_x = threading.Thread(target=threading_lcd_schema)
thread_x.start()


print('*** PROGRAM STARTED ***')


def read():
    while True:
        print('*** READ ***')
        get_value_fsr_food()
        get_value_fsr_water()
        get_value_dms_food()
        get_value_dms_water()
        get_watersensor()
        time.sleep(10)


thread = threading.Thread(target=read)
thread.start()


# API endpoints


@app.route('/schemawater', methods=['GET'])
def get_schema_water():
    data = DataRepository.read_voederschema_water()
    return jsonify(data), 200


@app.route('/schemafood', methods=['GET'])
def get_schema_food():
    data = DataRepository.read_voederschema_food()
    return jsonify(data), 200


@app.route('/lasttimeate', methods=['GET'])
def get_last_time_ate():
    data = DataRepository.read_last_time_ate()
    return jsonify(data), 200


@app.route('/lasttimedrank', methods=['GET'])
def get_last_time_drank():
    data = DataRepository.read_last_time_drank()
    return jsonify(data), 200


@app.route('/schema/<id>', methods=['PUT'])
def update_schema(id):
    gegevens = DataRepository.json_or_formdata(request)
    data = DataRepository.update_schema(
        gegevens['Uur'], gegevens['Hoeveelheid'], id)
    print(data)
    return jsonify(data), 200


# Socketio


@socketio.on('connect')
def initial_connection():
    print('New client connected')
    send('Welkom!')


@socketio.on('F2B_data')
def read_data():
    get_value_fsr_food()
    get_value_fsr_water()
    get_watersensor()
    get_value_dms_food()
    get_value_dms_water()


@socketio.on('F2B_activate_motor')
def activate_motor(data):
    control_motor(10)


@socketio.on('F2B_activate_waterpump')
def activate_waterpump(data):
    print('Start water pump')
    control_waterpump(3)


@socketio.on('F2B_shutdown')
def shutdown():
    print("Shutting down")
    time.sleep(3)
    os.system("sudo shutdown -h now")


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
