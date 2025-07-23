#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <iostream>
#include <iomanip>
#include <unistd.h>

#define I2C_ADDR 0x27
#define LCD_WIDTH 16

#define LCD_CHR 1
#define LCD_CMD 0
#define LCD_LINE_1 0x80
#define LCD_LINE_2 0xC0

#define E_PULSE 500
#define E_DELAY 500

#define FLOW_SENSOR_PIN 0  // WiringPi pin 0 = BCM GPIO 17

volatile int pulse_count = 0;
float flow_rate = 0.0;
int lcd_fd;

void lcd_toggle_enable(int bits) {
    usleep(E_DELAY);
    wiringPiI2CWrite(lcd_fd, bits | 0x04);
    usleep(E_PULSE);
    wiringPiI2CWrite(lcd_fd, bits & ~0x04);
    usleep(E_DELAY);
}

void lcd_byte(int bits, int mode) {
    int bits_high = mode | (bits & 0xF0) | 0x08;
    int bits_low = mode | ((bits << 4) & 0xF0) | 0x08;

    wiringPiI2CWrite(lcd_fd, bits_high);
    lcd_toggle_enable(bits_high);

    wiringPiI2CWrite(lcd_fd, bits_low);
    lcd_toggle_enable(bits_low);
}

void lcd_init() {
    lcd_byte(0x33, LCD_CMD);
    lcd_byte(0x32, LCD_CMD);
    lcd_byte(0x06, LCD_CMD);
    lcd_byte(0x0C, LCD_CMD);
    lcd_byte(0x28, LCD_CMD);
    lcd_byte(0x01, LCD_CMD);
    usleep(E_DELAY);
}

void lcd_string(const std::string &message, int line) {
    lcd_byte(line, LCD_CMD);
    for (int i = 0; i < LCD_WIDTH; ++i) {
        char c = i < message.length() ? message[i] : ' ';
        lcd_byte(c, LCD_CHR);
    }
}

void count_pulse() {
    pulse_count++;
}

void calculate_flow_rate() {
    const float pulses_per_liter = 450.0;
    flow_rate = pulse_count / pulses_per_liter;
    pulse_count = 0;
}

int main() {
    wiringPiSetup();
    pinMode(FLOW_SENSOR_PIN, INPUT);
    pullUpDnControl(FLOW_SENSOR_PIN, PUD_UP);
    wiringPiISR(FLOW_SENSOR_PIN, INT_EDGE_FALLING, &count_pulse);

    lcd_fd = wiringPiI2CSetup(I2C_ADDR);
    lcd_init();

    while (true) {
        sleep(1);
        calculate_flow_rate();
        lcd_string("Flow Rate:", LCD_LINE_1);
        lcd_string(std::to_string(flow_rate).substr(0, 5) + " L/min", LCD_LINE_2);
        std::cout << "Flow Rate: " << std::fixed << std::setprecision(2) << flow_rate << " L/min" << std::endl;
    }

    return 0;
}
