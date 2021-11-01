# cmd -> (python -m) pip install pyserial
import serial
import csv
import time

arduino = serial.Serial('COM4', 9600, timeout=.1)

while True:
    data = arduino.readline()

    if data:
        with open('plant_data.csv', mode='a+', newline='') as file:

            local_time = time.localtime()
            time_string = time.strftime('%d/%m/%Y %H:%M:%S', local_time)
            time_string = time_string.split()


            data = str(data)[2:-1]
            data = data.split()

            info = [time_string[0], time_string[1], data[0], data[1], data[2], data[3]]

            write_info = csv.writer(file, delimiter=',')
            write_info.writerow(info)

            print(info)
