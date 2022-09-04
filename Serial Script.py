import time
import pyfirmata
import serial.tools.list_ports
print(list(serial.tools.list_ports.comports()))
print([comport.device for comport in serial.tools.list_ports.comports()])



'''
with serial.Serial() as ser:
    ser.baudrate = 115200
    ser.port = 'COM7'
    message = ''
    ser.open()
    ser.write(str('Lft_0\n').encode())
    ser.close()
'''
my_string = ""
final = False
with serial.Serial() as ser:
    ser.baudrate = 115200
    ser.port = 'COM7'
    ser.open()
    while True:
        char = ser.read(1).decode('utf-8')
        if char != '\n':
            my_string += char
        else:
            print(my_string)
            char = ''
            my_string = ""
    ser.close()


'''
with serial.Serial() as ser:
    ser.baudrate = 115200
    ser.port = 'COM7'
    ser.open()
    for i in range(0, 255):
        ser.write(str(i).encode())
        ser.write('\n'.encode())
        print(i)
        #time.sleep(0.1)
    ser.close()



board = pyfirmata.Arduino('COM7')
it = pyfirmata.util.Iterator(board)
it.start()

LED = board.digital[10]
LED.mode = pyfirmata.PWM

while True:
    for i in range(0, 255):
        print(i)
        LED.write(i/255)
        time.sleep(0.01)




ser = serial.Serial("COM7", 9600)
for i in range(0, 255):
    ser.write(str(i).encode())
    time.sleep(1)
    print(i)

print("Done")


board = pyfirmata.Arduino('COM7')
it = pyfirmata.util.Iterator(board)
it.start()

potentiometer = board.analog[5]
potentiometer.enable_reporting()

LED = board.digital[6]
LED.mode = pyfirmata.PWM

speed = potentiometer.read()
time.sleep(1)

while True:
    speed = potentiometer.read()
    print(int(speed*255))
    LED.write(speed)
    time.sleep(0.01)

'''