# 🤖 MicroPython Libraries for Hardware and Stuff

> Cool, ready-to-use MicroPython functions for sensors, motors, buzzers, WiFi and more — made for the **Raspberry Pi Pico / Pico W**.
>
> Made with ❤️ by **Harman** (age 10). This is my **first library** — more coming soon! 🚀

![MicroPython](https://img.shields.io/badge/MicroPython-Pico%20%2F%20Pico%20W-brightgreen)
![Made by a 10 year old](https://img.shields.io/badge/Made%20by-a%2010%20year%20old%20legend-ff69b4)
![License MIT](https://img.shields.io/badge/License-MIT-blue)

---

## ✨ What is this?

A little toolbox of simple functions so you don't have to rewrite the same hardware
code every time. Just drop the file on your Pico and call a function — done!

Each function handles one piece of hardware: an ultrasonic sensor, a joystick, a
servo motor, buzzers, an LED, WiFi, or even a tiny web server.

---

## 📦 How to use it

1. Copy **`My first Library.py`** onto your Pico (for example, rename it `mylib.py`).
2. Import the functions you want:

```python
from mylib import Ultrasonic, Joystick, Servo, LED, ABUZZER, PBUZZER, WIFI, Start_Server
```

3. Call them! Examples are below. 👇

---

## 🧰 The Functions

### 📏 `Ultrasonic(Trigger_Pin, Echo_Pin)`
Measures distance in **centimeters** with an HC-SR04 sensor.
Returns `400.0` when nothing is close (that means "too far / nothing there").

```python
distance = Ultrasonic(3, 2)
print("Distance:", distance, "cm")
```

### 🕹️ `Joystick(x, y, sw)`
Reads an analog joystick. Returns `(x_value, y_value, button)`.
`x` and `y` go `0..65535`, and `button` is `0` when pressed.

```python
x, y, pressed = Joystick(27, 26, 16)
print(x, y, pressed)
```

### ⚙️ `Servo(pin_num, angle=None)`
Moves a servo to an angle from **0 to 180** degrees.

```python
Servo(0, 90)   # go to the middle
Servo(0)       # or leave it empty and it will ask you
```

### 🔊 `ABUZZER(pin, command=None)`
Turns a simple **active** buzzer ON or OFF.

```python
ABUZZER(15, "ON")
ABUZZER(15, "OFF")
```

### 🎵 `PBUZZER(pin, frequency=None, duration_ms=None)`
Plays a tone on a **passive** buzzer. Use frequency `0` to stop.

```python
PBUZZER(15, 440, 500)   # play note A for half a second
```

### 💡 `LED(pin_num, state=1)`
Turns an LED on (`1`) or off (`0`).

```python
LED("LED")     # onboard LED on a Pico W
LED(25)        # onboard LED on a normal Pico
LED(15, 0)     # turn an LED on pin 15 OFF
```

> **Fun fact:** on a **Pico W** the onboard LED is `"LED"`, not a pin number.
> On a normal Pico it's pin `25` (or `"LED"` works too).

### 📶 `WIFI()`  *(Pico W only)*
Asks for a WiFi name + password and connects. Returns `True` or `False`.

```python
if WIFI():
    print("We are online!")
```

### 🌐 `Start_Server(html_content)`  *(Pico W only)*
Starts a tiny web server showing your own HTML page. Connect to WiFi first!

```python
WIFI()
page = "<h1>Hello from Harman's Pico!</h1>"
Start_Server(page)
```

---

## 🔌 Quick wiring tips

| Part | Connect to |
|------|-----------|
| HC-SR04 Trig / Echo | any GPIO pins (use a voltage divider on Echo!) |
| Joystick VRx / VRy | **ADC** pins (26, 27, 28) |
| Joystick SW | any GPIO pin |
| Servo signal | any PWM-capable GPIO pin |
| Buzzer | any GPIO pin (passive buzzer = PWM pin) |

---

## 🗺️ Coming soon
More modules and sensors are on the way. Watch this space! ⭐

## 📄 License
MIT — free to use, learn from, and share.
