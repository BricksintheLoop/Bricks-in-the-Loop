import RPi.GPIO as GPIO
from buildhat import Motor

class BIL:
    # This list of dictionaries is the default var for when the init func is called
    global pins
    global ports
    pins = [{'room': 'fireplace_1', 'pin_num': 3, 'PWM': 30},
            {'room': 'fireplace_2', 'pin_num': 6, 'PWM': 30},
            {'room': 'entry_way', 'pin_num': 17, 'PWM': 100},
            {'room': 'dining_room', 'pin_num': 27, 'PWM': 100},
            {'room': 'camera', 'pin_num': 26, 'PWM': 100},
            {'room': 'big_brothers_room', 'pin_num': 7, 'PWM': 100},
            {'room': 'hallway', 'pin_num': 5, 'PWM': 100},
            {'room': 'bathroom', 'pin_num': 13, 'PWM': 100},
            {'room': 'attic', 'pin_num': 21, 'PWM': 100},
            {'room': 'kitchen', 'pin_num': 20, 'PWM': 100},
            {'room': 'basement', 'pin_num': 12, 'PWM': 100},
            {'room': 'back_porch', 'pin_num': 22, 'PWM': 100}]

    ports = [{'motor': 'door', 'port': 'A', 'speed': 80},
             {'motor': 'party_trick', 'port': 'B', 'speed': 80}]

    """initiates the class BIL (__init__ is a constructor)"""
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for i in pins: GPIO.setup(i['pin_num'], GPIO.OUT)

    def receive(self, message):
        try:
            p = pins[next(i for i, x in enumerate(pins) if x['room'] == message.split()[0])]['pin_num']
            #
            if message.split()[1] == 'on':
                print("turning on")
                GPIO.output(p, GPIO.HIGH)
            elif message.split()[1] == 'off':
                print("turning off")
                GPIO.output(p, GPIO.LOW)
            elif message.split()[1] == 'brightness':
                print("adjusting brightness")
            elif message.split()[1] == 'flicker':
                print("adjusting flicker")
            elif message.split()[1] == 'blink':
                print("adjusting blink")
            else:
                print("unrecognized command")
        except:
            print("input error")

    def __del__(self):
        print("Shutting Down")
        GPIO.cleanup()

def main():
    #Code below is in order of which prog executes functions called from above code
    one = BIL()                # call to execute class (BIL) when prog runs
    while(1):
        inp = input("Enter Command: ")
        if inp == "exit": break
        one.receive(inp)

    del one

if __name__ == '__main__':
    main()