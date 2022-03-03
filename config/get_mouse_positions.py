import pyautogui

while True:
    try:
        user_input = input("Press the 'Enter' key to get the x- any y-position of your current mouse pointer location. Type 'close' and then press the 'Enter' key to terminate this program.\n")
        if user_input == "close":
            break
        currentMouseX, currentMouseY = pyautogui.position()
        print(f"x-position: {currentMouseX}, y-position: {currentMouseY}.")
    except KeyboardInterrupt:
        break
