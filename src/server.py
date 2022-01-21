#!/usr/bin/env python3

import asyncio
from xmlrpc.client import Server
import websockets
import configparser
import os
import time
import functools

class ServerData:

    def __init__(self):
        """Initializes the server data."""
        # Set up the ConfigParser. Used to read all the server data from the config.ini file
        config = configparser.ConfigParser()
        config.read('../config/config.ini')

        # Ip address and port used to communicate with client
        self.ip_address = config['IP']['ip_address']
        self.port = config['IP']['port']

        # Name of the log file
        self.log_file_name = config['LOG_FILE']['log_file_name']

        # Trigger words that are used to determine whether an error has occured
        self.triggers = config.get('TRIGGER_WORDS', 'triggers').split(',')

        # Delay between server cycles in seconds
        self.delay = config['DELAY_TIME']['delay']


def errors_in_log_file(server_data: ServerData):
    """
    Searches the log file for errors (i.e. trigger words that indicate an error)

    Returns True if an error was found.
    Returns False else.
    """

    # Open the log file and create a list that contains all lines as strings
    file_path = os.path.abspath('')
    with open(file_path + "../Testing/20220121-1443-3-TGATDU_error_simulation.log", "r") as f:
        lines = f.readlines()
    
    # Search all lines for errors
    for line in lines:
        for trigger in server_data.triggers:
            if trigger in line:
                print('Found an error: ')
                print(line)
                return True
    
    return False


async def serve(websocket, path, server_data):
    """Runs one server side task cycle."""
    # Receive a message from the client
    received_message = await websocket.recv()

    # Shut down the script if the client has acknowledged that it has received the error message 
    if received_message == "Error successfully detected!":
        asyncio.get_event_loop().stop()
    
    # Check for error(s) in log file
    errors = errors_in_log_file(server_data)

    # Determine an appropriate response to be sent to the client
    # Response depends on whether an error has been found or not
    if errors:
        response_message = "STATUS: Error detected"
    else:
        response_message = "STATUS: Ok"

    # Send the response to the client
    await websocket.send(response_message)

    # Wait some time before repeating the cycle
    time.sleep(server_data.delay)


def main():
    """Initializes and runs the server."""
    # Initialize the server data
    server_data = ServerData()

    # Start the server
    start_server = websockets.serve(functools.partial(serve, server_data=server_data), host=server_data.ip_address, port=server_data.port)

    # Run the server in an asyncio loop
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()