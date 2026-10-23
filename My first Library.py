def Ultrasonic(Trigger_Pin, Echo_Pin):
    from machine import Pin
    import utime
    Trig = Pin(Trigger_Pin, Pin.OUT)
    Ech = Pin(Echo_Pin, Pin.IN)
    
    Trig.low()
    utime.sleep_us(2)
    Trig.high()
    utime.sleep_us(10) 
    Trig.low()
    
    timeout_start = utime.ticks_us()
    while Ech.value() == 0:
        signal_off = utime.ticks_us()
        if utime.ticks_diff(signal_off, timeout_start) > 30000:
            return 400.0

    while Ech.value() == 1:
        signal_on = utime.ticks_us()
        if utime.ticks_diff(signal_on, signal_off) > 30000:
            return 400.0
    
    time_passed = signal_on - signal_off
    distance = (time_passed * 0.0343) / 2
    
    if distance > 400.0 or distance < 0:
        return 400.0
        
    return distance

def Joystick(x, y, sw):
    from machine import Pin, ADC
    import utime
    joy_x = ADC(Pin(x))
    joy_y = ADC(Pin(y))
    joy_sw = Pin(sw, Pin.IN, Pin.PULL_UP)
    
    x_val = joy_x.read_u16()
    y_val = joy_y.read_u16()
    btn_val = joy_sw.value()
    return x_val, y_val, btn_val

def WIFI():
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

def Servo(pin_num):
    from machine import Pin, PWM
    import utime
    user_input = input("Enter servo angle (0 to 180): ")
    angle = int(user_input)
    
    if angle < 0: angle = 0
    if angle > 180: angle = 180
        
    servo = PWM(Pin(pin_num))
    servo.freq(50)
    
    duty = int(1638 + (angle / 180) * 6554)
    servo.duty_u16(duty)

def ABUZZER(pin):
    from machine import Pin
    command = input("Type ON to beep or OFF to silence: ")
    buzzer = Pin(pin, Pin.OUT)
    
    if command.upper() == "ON":
        buzzer.high()
    elif command.upper() == "OFF":
        buzzer.low()

def PBUZZER(pi):2
    from machine import Pin, PWM
    import utime
    user_freq = input("Enter tone frequency in Hz (or 0 to stop): ")
    user_time = input("Enter duration in milliseconds: ")
    
    frequency = int(user_freq)
    duration_ms = int(user_time)
    
    buzzer = PWM(Pin(pi))
    if frequency == 0:
        buzzer.deinit()
    else:
        buzzer.freq(frequency)
        buzzer.duty_u16(32768)
        utime.sleep_ms(duration_ms)
        buzzer.deinit()

def LED(pin_num):
    from machine import Pin
    led = Pin(pin_num, Pin.OUT)
    led.value(1)
    #Fun Fact- if your Raspberry PI PICO W, is actually a normal non Wifi Pico, then you could write it either 0, or 25, if you want to like turn on
    #LED on the board, but for Pico W, it is "LED", not a Pin no.

def Start_Server(html_content):
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