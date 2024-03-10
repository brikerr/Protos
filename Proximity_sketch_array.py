from machine import Pin
import utime
import pimoroni_pico_unicorn as unicorn  # Make sure this library is installed

# Initialize Unicorn Pack
unicorn.init()
width, height = unicorn.get_shape()

# Initialize HC-SR04 sensor pins
trig_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)

# Function to measure distance
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
    distance = (time_passed * 0.0343) / 2
    return distance

# Function to update LED brightness based on distance
def update_led_brightness(distance):
    brightness = max(min((100 - distance) * (1 / 100), 1), 0)  # Scale distance to brightness (0 to 1)
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x, y, 255, 105, 180, brightness)  # Example: pink color, modify as needed
    unicorn.show()

# Main loop
while True:
    distance = measure_distance()
    update_led_brightness(distance)
    print("Distance:", distance, "cm")
    utime.sleep(0.1)
