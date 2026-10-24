# ===============================================================
#   My First Library  -  MicroPython Helpers for Cool Hardware
#   Made by Harman (age 10)  -  Raspberry Pi Pico / Pico W
# ---------------------------------------------------------------
#   A friendly toolbox of ready-to-use functions for sensors,
#   motors, buzzers, WiFi and even a tiny web server!
# ===============================================================


def Ultrasonic(Trigger_Pin, Echo_Pin):
    """Measure distance in centimeters using an HC-SR04 sensor.

    Returns 400.0 if nothing is found (that means "too far / nothing there").
    """
    from machine import Pin
    import utime
    Trig = Pin(Trigger_Pin, Pin.OUT)
    Ech = Pin(Echo_Pin, Pin.IN)

    # Send a tiny 10 microsecond "ping"
    Trig.low()
    utime.sleep_us(2)
    Trig.high()
    utime.sleep_us(10)
    Trig.low()

    signal_off = utime.ticks_us()
    signal_on = signal_off

    # Wait for the echo to start (pin goes HIGH)
    timeout_start = utime.ticks_us()
    while Ech.value() == 0:
        signal_off = utime.ticks_us()
        if utime.ticks_diff(signal_off, timeout_start) > 30000:
            return 400.0

    # Wait for the echo to come back (pin goes LOW)
    while Ech.value() == 1:
        signal_on = utime.ticks_us()
        if utime.ticks_diff(signal_on, signal_off) > 30000:
            return 400.0

    time_passed = utime.ticks_diff(signal_on, signal_off)
    distance = (time_passed * 0.0343) / 2

    if distance > 400.0 or distance < 0:
        return 400.0

    return distance


def Joystick(x, y, sw):
    """Read an analog joystick.

    Returns (x_value, y_value, button).
    x and y go 0..65535, button is 0 when pressed.
    """
    from machine import Pin, ADC
    joy_x = ADC(Pin(x))
    joy_y = ADC(Pin(y))
    joy_sw = Pin(sw, Pin.IN, Pin.PULL_UP)

    x_val = joy_x.read_u16()
    y_val = joy_y.read_u16()
    btn_val = joy_sw.value()
    return x_val, y_val, btn_val


def WIFI():
    """Ask for a WiFi name + password and connect (Pico W only).

    Returns True if connected, False if it failed.
    """
    import network
    import utime
    ssid = input("Enter WiFi Name: ")
    password = input("Enter WiFi Password: ")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting to WiFi...")

    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        utime.sleep(1)
        timeout = timeout - 1

    if wlan.isconnected():
        print("\nConnected successfully!")
        print("IP Address:", wlan.ifconfig())
        return True
    else:
        print("\nConnection failed! Check name or password.")
        return False


def Servo(pin_num, angle=None):
    """Move a servo motor to an angle from 0 to 180 degrees.

    Pass an angle like Servo(0, 90), or leave it empty to be asked.
    """
    from machine import Pin, PWM
    if angle is None:
        angle = int(input("Enter servo angle (0 to 180): "))

    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180

    servo = PWM(Pin(pin_num))
    servo.freq(50)

    duty = int(1638 + (angle / 180) * 6554)
    servo.duty_u16(duty)


def ABUZZER(pin, command=None):
    """Turn a simple (active) buzzer ON or OFF.

    Pass ABUZZER(15, "ON") or leave it empty to be asked.
    """
    from machine import Pin
    if command is None:
        command = input("Type ON to beep or OFF to silence: ")
    buzzer = Pin(pin, Pin.OUT)

    if command.upper() == "ON":
        buzzer.high()
    elif command.upper() == "OFF":
        buzzer.low()


def PBUZZER(pin, frequency=None, duration_ms=None):
    """Play a tone on a passive buzzer.

    Pass PBUZZER(15, 440, 500) to play A4 for half a second,
    or leave the numbers empty to be asked. Use frequency 0 to stop.
    """
    from machine import Pin, PWM
    import utime
    if frequency is None:
        frequency = int(input("Enter tone frequency in Hz (or 0 to stop): "))
    if duration_ms is None:
        duration_ms = int(input("Enter duration in milliseconds: "))

    buzzer = PWM(Pin(pin))
    if frequency == 0:
        buzzer.deinit()
    else:
        buzzer.freq(frequency)
        buzzer.duty_u16(32768)
        utime.sleep_ms(duration_ms)
        buzzer.deinit()


def LED(pin_num, state=1):
    """Turn an LED on (state=1) or off (state=0).

    Fun fact: on a Pico W the onboard LED is "LED", not a pin number.
    On a normal Pico it is pin 25 (or "LED" also works).
    """
    from machine import Pin
    led = Pin(pin_num, Pin.OUT)
    led.value(state)


def Start_Server(html_content):
    """Start a tiny web server that shows your HTML page (Pico W).

    Connect to WiFi first with WIFI(), then open the printed IP in a browser.
    """
    import socket
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Please connect to WiFi first!")
        return

    address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen(1)

    print("Web server running! Visit:", wlan.ifconfig()[0])

    while True:
        client, addr = server_socket.accept()
        request = client.recv(1024)

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html_content
        client.send(response)
        client.close()
