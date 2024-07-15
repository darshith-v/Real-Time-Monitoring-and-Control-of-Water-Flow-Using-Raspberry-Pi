import time  # For sleep functions and time-related operations
from gpiozero import DigitalInputDevice  # For interacting with GPIO pins and reading sensor data
from smbus2 import SMBus  # For I2C communication with the LCD

# I2C LCD Configuration
I2C_ADDR = 0x27  # I2C address of the LCD (depends on your specific LCD)
LCD_WIDTH = 16   # Maximum characters per line

# LCD constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Water Flow Sensor Configuration
FLOW_SENSOR_PIN = 17  # GPIO pin number for the water flow sensor
flow_sensor = DigitalInputDevice(FLOW_SENSOR_PIN, pull_up=True)  # Initialize the sensor with a pull-up resistor

# Global variables
pulse_count = 0  # Counter for pulses from the sensor
flow_rate = 0  # Calculated flow rate in L/min

def lcd_init():
    """Initialize the LCD display."""
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    """Send byte to data pins."""
    bits_high = mode | (bits & 0xF0) | 0x08
    bits_low = mode | ((bits << 4) & 0xF0) | 0x08
    with SMBus(1) as bus:
        bus.write_byte(I2C_ADDR, bits_high)
        lcd_toggle_enable(bits_high)
        bus.write_byte(I2C_ADDR, bits_low)
        lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    """Toggle enable pin to latch data."""
    time.sleep(E_DELAY)
    with SMBus(1) as bus:
        bus.write_byte(I2C_ADDR, (bits | 0x04))
    time.sleep(E_PULSE)
    with SMBus(1) as bus:
        bus.write_byte(I2C_ADDR, (bits & ~0x04))
    time.sleep(E_DELAY)

def lcd_string(message, line):
    """Send string to display."""
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def count_pulse():
    """Increment pulse count for each pulse detected by the sensor."""
    global pulse_count
    pulse_count += 1

flow_sensor.when_activated = count_pulse  # Call count_pulse() when a pulse is detected

def calculate_flow_rate():
    """Calculate flow rate in liters per minute based on pulse count."""
    global pulse_count, flow_rate
    pulses_per_liter = 450  # Adjust based on your sensor's specifications
    flow_rate = pulse_count / pulses_per_liter
    pulse_count = 0  # Reset pulse count after calculation

def main():
    """Main program loop."""
    lcd_init()  # Initialize the LCD
    while True:
        time.sleep(1)  # Wait for 1 second
        calculate_flow_rate()  # Calculate the flow rate
        lcd_string(f"Flow Rate:", LCD_LINE_1)  # Display the label on the first line
        lcd_string(f"{flow_rate:.2f} L/min", LCD_LINE_2)  # Display the flow rate on the second line
        print(f"Flow Rate: {flow_rate:.2f} L/min")  # Print the flow rate to the console for debugging

if __name__ == "__main__":
    main()  # Run the main loop
