from machine import Pin, I2C
import ssd1306

# Initialize the I2C bus and the display
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


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

    # Clear the display and print the distance
    display.fill(0)
    display.text(f"Distance: {distance:.2f} cm", 0, 0)
    display.show()

    utime.sleep(0.1)