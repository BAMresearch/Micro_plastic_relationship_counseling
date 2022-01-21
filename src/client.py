#!/usr/bin/env python3

import configparser
import pyautogui
import time
import datetime
import websocket

class ClientData:

    def __init__(self):
        """Initializes the client data."""
        # Set up the ConfigParser. Used to read all the client data from the config.ini file
        config = configparser.ConfigParser()
        config.read('../config/config.ini')

        # Ip address and port used to communicate with server
        self.ip_address = config['IP']['ip_address']
        self.port = config['IP']['port']

        # Positions for reset button and the reset confirmation button
        self.reset_x_pos = config['RESET_POSITION']['reset_x_pos']
        self.reset_y_pos = config['RESET_POSITION']['reset_y_pos']
        self.confirm_reset_x_pos = config['CONFIRM_RESET_POSITION']['confirm_reset_x_pos']
        self.confirm_reset_y_pos = config['CONFIRM_RESET_POSITION']['confirm_reset_y_pos']

class UserWebsocketEngine:
    """Sets up websocket to talk to the server."""

    def __init__(self, client_data: ClientData):
        self.client_data = client_data
        self.main()

    def main(self):

        def on_message(ws, message):
            """Function that processes all incoming messages except for error messages."""
            if message == "STATUS SERVER: Error detected":
                # Click the reset button
                pyautogui.click(self.client_data.reset_x_pos, self.client_data.reset_y_pos)
                
                # Wait a little and then press the reset confirmation button
                time.sleep(2)
                pyautogui.click(self.client_data.confirm_reset_x_pos, self.client_data.confirm_reset_y_pos)

                # Send the server an acknolegement about the error message
                ws.send("STATUS CLIENT: Error successfully detected!")
                ws.close()
            else:
                ws.send("STATUS CLIENT: Ok")

        def on_error(ws, error):
            """Function that handles websocket connection errors."""
            print(error)

        def on_close(ws):
            """Function that deals with the closure of the websocket connection."""
            print('CONNECTION CLOSED AT: ' + str(datetime.now().time().strftime('%H:%M:%S')))

        def on_open(ws):
            """Function that deals with the opening of the websocket connection."""
            response_message = "STATUS CLIENT: Ok"
            ws.send(response_message)

        # Initialize Websocket App
        url_address = f'ws://{self.client_data.ip_address}:{self.client_data.port}'
        ws = websocket.WebSocketApp(url_address,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        
        ws.on_open = on_open

        ws.run_forever()


def stay_connected(client_data: ClientData):
    """
    Function that tries to reconnect with the server if the connection is interrupted.
    It does so by creating a new websocket engine object each time we're getting disconnected.   
    """
    try:
        while True:
            UserWebsocketEngine(client_data)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program terminated due to keyboard interruption.")


def main():
    """Initializes and runs the client."""
    # Initialize the client data
    client_data = ClientData()

    # Run the client in an asyncio loop
    stay_connected(client_data)


if __name__ == "__main__":
    main()
