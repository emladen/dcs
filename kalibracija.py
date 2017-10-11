import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

def setpwm(input):
    pwm.set_pwm(0,0,input)
    pwm.set_pwm(1,0,input)

while True:
    print("Insert speed value")
    choice = raw_input("inser choice: ")
    setpwm(int(choice))
