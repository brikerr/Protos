from machine import Pin, PWM
import utime

# HC-SR04 setup
trig_pin = Pin(28 , Pin.OUT)
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
    distance = (time_passed * 0.0343) / 2  # Calculate distance
    
    return distance

# Initialize PWM for 4 RGB LEDs
leds = [
    (PWM(Pin(0)), PWM(Pin(1)), PWM(Pin(2))),
    (PWM(Pin(3)), PWM(Pin(4)), PWM(Pin(5))),
    (PWM(Pin(10)), PWM(Pin(11)), PWM(Pin(12))),
    (PWM(Pin(13)), PWM(Pin(14)), PWM(Pin(15)))
]

for r, g, b in leds:
    r.freq(1000)
    g.freq(1000)
    b.freq(1000)

def set_brightness(brightness):
    # Adjusts brightness for white light
    duty = int((brightness / 100) * 65535)
    for red, green, blue in leds:
        red.duty_u16(duty)
        green.duty_u16(duty)
        blue.duty_u16(duty)

def set_green():
    # Sets LEDs to green at maximum brightness
    duty = 65535
    for red, green, blue in leds:
        red.duty_u16(0)
        green.duty_u16(duty)
        blue.duty_u16(0)

# Main loop
while True:
    distance = measure_distance()
    print("Distance:", distance, "cm")  # For debugging
    
    if distance < 10:  # Very close
        set_green()  # Set LEDs to green
    elif distance > 10:  # Adjust threshold as needed
        brightness = max(2, (50 - distance) * 2)  # Scale brightness based on distance
        set_brightness(min(brightness, 100))  # Increase brightness with white color
    else:
        set_brightness(0)  # Off
        
    utime.sleep(0.1)
