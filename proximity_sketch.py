from machine import Pin, PWM
import utime

# HC-SR04 setup
trig_pin = Pin(28, Pin.OUT)
echo_pin = Pin(27, Pin.IN)

def measure_distance():
    trig_pin.low()
    utime.sleep_us(2)
    trig_pin.high()
    utime.sleep_us(5)
    trig_pin.low()
    
    while echo_pin.value() == 0:
        signal_off = utime.ticks_us()
    while echo_pin.value() == 1:
        signal_on = utime.ticks_us()
        
    time_passed = signal_on - signal_off
    distance = (time_passed * 0.0343) / 2  # Speed of sound wave divided by 2 (go and back)
    
    return distance

# Initialize PWM for each LED on specific pins
led_pwm_pins = [PWM(Pin(18)), PWM(Pin(19)), PWM(Pin(15)), PWM(Pin(21))]

for led in led_pwm_pins:
    led.freq(1000)  # 1000 Hz

def set_brightness(led, brightness):
    duty = int((brightness / 100) * 65535)
    led.duty_u16(duty)

# Main loop
while True:
    distance = measure_distance()
    print("Distance:", distance, "cm")  # For debugging
    
    # Adjust the brightness based on the distance
    if distance < 25:  # Adjust this threshold as needed
        brightness = max(2, (25  - distance) * 2)  # Example scaling, adjust as needed
        for led in led_pwm_pins:
            set_brightness(led, min(brightness, 100))
    else:
        for led in led_pwm_pins:
            set_brightness(led, 0)
    
    utime.sleep(0.1)  # Short delay to debounce sensor

# end of proximity_sketch.py