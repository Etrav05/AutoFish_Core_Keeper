import pyautogui
import time
import keyboard
import win32api, win32con
import threading

running = True  ## shared flag for stopping threads
inventory = False

def watch_for_quit():
    global running
    keyboard.wait('q')  ## block until 'q' is pressed
    running = False
    print("\n[!] Quit key pressed — stopping...")

def watch_for_inventory():
    global inventory
    while True:
        keyboard.wait('tab')
        inventory = not inventory
        print(f"\n[?] Inventory mode {'ON' if inventory else 'OFF'}")
        time.sleep(0.3)  ## Preventing double trigger

caughtX = 955
caughtY_lower, caughtY_upper = 338, 441
## (227, 228, 235))

castX, castY = 1200, 500
## (  1,  14,  26)

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def reel():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def cast():
    win32api.SetCursorPos((castX, castY))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(0.200)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def cast_when_caught():
    image = pyautogui.screenshot()

    for y in range(caughtY_lower, caughtY_upper + 1):
        colour = image.getpixel((caughtX, y))
        if colour == (227, 228, 235):
            print("reeling")
            reel()
            time.sleep(0.1)
            print("casting")
            cast()

            while True:  ## Wait for the "caught" symbol to go away
                image = pyautogui.screenshot()
                if image.getpixel((caughtX, y)) != (227, 228, 235):
                    break
                time.sleep(0.05)

            return  ## exit function

def main():
    global running
    global inventory
    threading.Thread(target=watch_for_quit, daemon=True).start()  ## start another thread so we can force quit
    threading.Thread(target=watch_for_inventory, daemon=True).start()  ## start another thread so we can force quit

    cast()

    while running:
        if not inventory:
            cast_when_caught()
        else:
            continue

if __name__ == "__main__":
    main()
