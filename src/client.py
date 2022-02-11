#!/usr/bin/env python3

import configparser
import pyautogui
import time
import datetime
import websocket
import os
from log import Log

class ClientData:

    def __init__(self, log_name: str):
        """Initializes the client data."""
        # Set up logger
        self.log = Log(log_name)

        # Set up the ConfigParser. Used to read all the client data from the config.ini file
        config = configparser.ConfigParser()
        config.read('../config/config.ini')

        # Ip address and port used to communicate with server
        self.ip_address = config['IP']['ip_address']
        self.port = config['IP']['port']

        # Positions for reset button and the reset confirmation button
        self.reset_x_pos = int(config['RESET_POSITION']['reset_x_pos'])
        self.reset_y_pos = int(config['RESET_POSITION']['reset_y_pos'])
        self.confirm_reset_x_pos = int(config['CONFIRM_RESET_POSITION']['confirm_reset_x_pos'])
        self.confirm_reset_y_pos = int(config['CONFIRM_RESET_POSITION']['confirm_reset_y_pos'])

        # Delay before shutting down the client after an error message has been received
        self.client_shutdown_delay_mins = float(config['DELAY_TIME']['client_shutdown_delay_mins'])


class UserWebsocketEngine:
    """Sets up websocket to talk to the server."""

    def __init__(self, client_data: ClientData):
        self.client_data = client_data
        self.main()

    def main(self):

        def on_message(ws, message):
            """Function that processes all incoming messages except for error messages."""
            if message == "STATUS SERVER: Error detected":

                # Wait some time before shutting down the client
                self.client_data.log.logger.debug(f"Waiting {self.client_data.client_shutdown_delay_mins} minutes for safety reasons before shutting down the client.")
                time.sleep(self.client_data.client_shutdown_delay_mins * 60)

                self.client_data.log.logger.debug("Resetting the program.")
                # Click the reset button
                pyautogui.click(self.client_data.reset_x_pos, self.client_data.reset_y_pos)
                
                # Wait a little and then press the reset confirmation button
                time.sleep(2)
                self.client_data.log.logger.debug("Confirming the program's reset.")
                pyautogui.click(self.client_data.confirm_reset_x_pos, self.client_data.confirm_reset_y_pos)

                # Remove logging handler to stop logging at this point
                self.client_data.log.logger.removeHandler(self.client_data.log.handler)

                # Send the server an acknolegement about the error message
                ws.send("STATUS CLIENT: Error detected!")
                ws.close()
            else:
                ws.send("STATUS CLIENT: Ok")

        def on_error(ws, error):
            """Function that handles websocket connection errors."""
            self.client_data.log.logger.debug(error)

        def on_close(ws):
            """Function that deals with the closure of the websocket connection."""
            self.client_data.log.logger.debug('CONNECTION CLOSED AT: ' + str(datetime.now().time().strftime('%H:%M:%S')))

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
        client_data.log.logger.debug("Program terminated due to keyboard interruption.")


def main():
    """Main method. Initializes and runs the client."""    
    # Change working directory to file path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Initialize the client data
    client_data = ClientData('client')

    # Run the client in an asyncio loop
    stay_connected(client_data)


if __name__ == "__main__":
    main()
