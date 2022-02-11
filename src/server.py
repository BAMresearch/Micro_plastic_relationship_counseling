#!/usr/bin/env python3

import asyncio
import websockets
import configparser
import os
import time
import functools
import glob
from log import Log
from datetime import datetime

class ServerData:

    def __init__(self, log_name: str, log_file_automatic=True):
        """Initializes the server data."""
        # Set up logger
        self.log = Log(log_name)

        # Set up the ConfigParser. Used to read all the server data from the config.ini file
        config = configparser.ConfigParser()
        config.read('../config/config.ini')

        # Ip address and port used to communicate with client
        self.ip_address = config['IP']['ip_address']
        self.port = int(config['IP']['port'])

        # Name of the log file
        self.log_file_path = config['LOG_FILE']['log_file_path']
        if log_file_automatic: # Automatically find and use the latest log file created in this directory
            try:
                current_date = f"{datetime.today().year}{datetime.today().strftime('%m')}{datetime.today().strftime('%d')}"
                log_files = glob.glob(f"{self.log_file_path}/{current_date}*.log")
                self.log_file_name = os.path.basename(max(log_files, key=os.path.getctime))
            except ValueError:
                self.log.logger.debug("No log file found in the specified directory.")
        else: # Use the log file specified in the config.ini file
            self.log_file_name = config['LOG_FILE']['log_file_name']

        # Trigger words that are used to determine whether an error has occured
        self.triggers = config.get('TRIGGER_WORDS', 'triggers').split(',')

        # Delay between server loop iterations in seconds
        self.server_repeat_delay_secs = int(config['DELAY_TIME']['server_repeat_delay_secs'])


def errors_in_log_file(server_data: ServerData):
    """
    Searches the log file for errors (i.e. trigger words that indicate an error)

    Returns True if an error was found.
    Returns False else.
    """

    # Open the log file and create a list that contains all lines as strings
    with open(f"{server_data.log_file_path}/{server_data.log_file_name}", "r") as f:
        lines = f.readlines()
    
    # Search all lines for errors
    for line in lines:
        for trigger in server_data.triggers:
            if trigger in line:
                server_data.log.logger.debug('Found an error: ')
                server_data.log.logger.debug(line)
                return True
    
    return False


async def serve(websocket, path, server_data: ServerData):
    """Runs an async loop of server side tasks."""

    async for received_message in websocket:
        # Shut down the script if the client has acknowledged that it has received the error message 
        if received_message == "STATUS CLIENT: Error detected!":
            asyncio.get_event_loop().stop()
        
        # Check for error(s) in log file
        errors = errors_in_log_file(server_data)

        # Determine an appropriate response to be sent to the client
        # Response depends on whether an error has been found or not
        if errors:
            response_message = "STATUS SERVER: Error detected"
        else:
            response_message = "STATUS SERVER: Ok"

        # Send the response to the client
        await websocket.send(response_message)

        # Wait some time before repeating the cycle
        time.sleep(server_data.server_repeat_delay_secs)


def main():
    """Main method. Initializes and runs the server."""
    # Change working directory to file path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Initialize the server data
    server_data = ServerData('server', log_file_automatic=True)

    # Start the server
    start_server = websockets.serve(functools.partial(serve, path="Whatever", server_data=server_data), host=server_data.ip_address, port=server_data.port)

    # Run the server in an asyncio loop
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
