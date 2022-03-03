# Microplastic relationship counseling

Server-Client socket implementation that allows for log file based error detection and termination of a program with a GUI.

The implementation addresses a very specific issue in a very specific use case.
First things first: The use case.
The target use case is the execution of experiments with a thermal gravimetric analysis (TGA) together with a mass spectrometer to identify micro plastic in given specimen. The two machines exchange their specimen with a robotic arm.
The issue:
Sometimes the mass spectrometer (MS) throws (an) error(s) that lead(s) to it shutting down. The TGA doesn't know about this however and continues its operation, thus destroying all the valuable specimen.
The implemented solution:
Setting up a websocket locally (server and client script) to make the two machines communicate with each other and terminate the TGA's operation if an error is detected in the MS's log file. Since we currently only have a GUI to work with in our use case, the TGA's operation is terminated by making the client script click on the respective buttons using the "pyautogui" package.

Simply put: Two computers that simply need to talk to one another to fix their issues. Or: Micro plastic relationship counseling.

## Script setup:
It is possible to either use this repository's software if you run both the TGA and the GC/MS machines from the same computer (i.e. the “Star Software” and “Mass Hunter” software both run on the same computer) or if you are using one computer for each machine. Jump to the setup description for your use case:

### Single PC setup:
1. Python installation
   - There are various ways to install Python on your computer. We will be using Miniconda in this demonstration. If you want to go a different way (e.g. using the Microsoft store or Anaconda), continue with step 2 after you have installed Python 3.8 or later on your PC as well as pip. Otherwise continue with the next bullet point.
   - Head to `https://docs.conda.io/en/latest/miniconda.html#windows-installers`
   - Download Python 3.8 or later. Earlier versions like Python 2.7 might work as well but have not been tested.
   - Install Python by following the installation instructions.
2. Download and configure software
   - Now we need to install the software that will allow the two computers/two softwares to talk to one another.
   - Download this Github repository to a location that suits you (e.g. your Desktop).
   - Install the required Python packages that are specified in the `requirements.txt` file. You can use pip to do this automatically by running `pip3 install -r requirements.txt` in the downloaded folder.
   - Head into its "config" folder.
   - Open the `config.ini` file.
   - We need to first figure out where the mouse is supposed to click when we want it to terminate the "Star Software":
     - Open the "Star Software" and make sure that it is in full screen mode. It must be run in full screen mode from now on to ensure proper functionality of this project's scripts.
     - Run the `get_mouse_positions.py` script inside the config folder and follow the instructions to get both the supposed mouse location for pressing the `Reset` button in the "Star Software".
     - Place the mouse in the middle of the `Reset` button before pressing `Enter` on your keyboard to get the x- and y-position.
     - Note down the shown coordinates.
     - Press the `Reset` button.
     - Place the mouse in the middle of the `Confirm reset` button before pressing `Enter` again.
     - Note down the shown shown coordinates again.
   - Inside the previously opened `config.ini` file edit the `reset_x_pos`, `reset_y_pos`, `confirm_reset_x_pos` and `confirm_reset_y_pos` values to the ones that you have just noted down.
   - Leave the `ip_address` as is ("localhost"). This is used to indicate the local IP address of the server script's PC. This is however irrelevant for a single PC setup.
   - Leave the `port` as is ("8765") unless you know what you are doing and need to change it.
   - The `log_file_path` specifies where the “Mass Hunter” software saves its log files. Once you have found this folder on your computer, copy its path and repplace the default value here. You need to make sure to only use forward slashes ("/") instead of back slashes ("\\") in the path.
   - The `log_file_name` is mostly used for debugging purposes and can be left as is.
   - The `triggers` specifies which words in the log file indicate to us that we want to shut down the "Star Software". Please note that some words in the log file might indicate a critical error only in some occasions but are not critical in other occasions. Therefore make sure that a trigger word is "safe" to be used here. Also ensure that you separate trigger words by comma but without spaces.
   - The `client_shutdown_delay_mins` specifies how long we want to wait in minutes before shutting down the "Star Software" after detecting an error in the log file. By default this is set to "2" which should be fine for most applications.
   - The `server_repeat_delay_secs` specifies how long we want to wait in seconds after checking the log file for errors before repeating the error checking process. This should also be fine for most applications.
   - Save the `config.ini` file and exit the text editor.
3. Run software
   - You are now ready to use the software.
   - This is done in the following way:
     - Start your measurements the usual way (i.e. in the “Star Software” and “Mass Hunter” software)
     - Make sure that the "Star Software" is run in full screen mode and is in the foreground. Additionally, ensure that no window is covering its `Reset` button.
     - Head to the `src` folder.
     - Run the `server.py` script.
     - Run the `client.py` script.
     - After the measurements are done or an error was detected and the "Star Software" was stopped, you can terminate both scripts again.


### Dual PC setup:
1. Network setup
   - We need to ensure that both computers are in the same network (i.e. the one running the “Star Software” (from now on called PC1) and the one running the “Mass Hunter” software (from now on called PC2)). If they are not, please contact your IT department for help.
   - Now we want to ensure that PC1 and PC2 can talk to one another. To do so, we first need to find out their local IP addresses.
   - For both PC1 and PC2 open Windows’ search bar in the lower left corner of their screen.
   - Type “cmd” and hit “Enter” which opens up a command prompt session.
   - In this black session window, type “ipconfig” and hit `Enter`.
   - Depending on whether your PC is connected via Ethernet or Wifi, look for the respective table.
   - It should contain a line called “IPv4 Address”.
   - Note down the numbers in that line, including the dots (Example: PC1: 192.168.0.150; PC2: 192.168.0.155).
   - On PC1 type "ping 192.168.0.155" (replace the IP address with the IP address of PC2 that you have found out for your setup).
   - If it does not reach the other computer, contact your IT department for help and continue after this has been fixed.
   - We can now forget about the IP address of PC1).
2. Python installation
   - There are various ways to install Python on your computers. We will be using Miniconda in this demonstration. If you want to go a different way (e.g. using the Microsoft store or Anaconda), continue with step 2 after you have installed Python 3.8 or later on both PC1 and PC2 as well as pip. Otherwise continue with the next bullet point.
   - Repeat the following process on both PC1 and PC2:
     - Head to `https://docs.conda.io/en/latest/miniconda.html#windows-installers`
     - Download Python 3.8 or later. Earlier versions like Python 2.7 might work as well but have not been tested.
     - Install Python by following the installation instructions.
3. Download and configure software
   - Now we need to install the software that will allow the two computers/two softwares to talk to one another.
   - Repeat the following tasks on both PC1 and PC2:
     - Download this Github repository to a location that suits you (e.g. your Desktop).
     - Install the required Python packages that are specified in the `requirements.txt` file. You can use pip to do this automatically by running `pip3 install -r requirements.txt` in the downloaded folder.
     - We will now need to edit the `config.ini` file. We will do this on PC1 first and copy the edited file to PC2 afterwards.
       - Head into its "config" folder.
       - Open the `config.ini` file.
       - We need to first figure out where the mouse is supposed to click when we want it to terminate the "Star Software":
         - Skip this bullet point for PC2: Open the "Star Software" on PC1 and make sure that it is in full screen mode. It must be run in full screen mode from now on to ensure proper functionality of this project's scripts.
         - Run the `get_mouse_positions.py` script inside the config folder and follow the instructions to get both the supposed mouse location for pressing the `Reset` button in the "Star Software".
         - Place the mouse in the middle of the `Reset` button before pressing `Enter` on your keyboard to get the x- and y-position.
         - Note down the shown coordinates.
         - Press the `Reset` button.
         - Place the mouse in the middle of the `Confirm reset` button before pressing `Enter` again.
         - Note down the shown shown coordinates again.
       - Inside the previously opened `config.ini` file edit the `reset_x_pos`, `reset_y_pos`, `confirm_reset_x_pos` and `confirm_reset_y_pos` values to the ones that you have just noted down.
       - Change the `ip_address` to that of PC2 that you have found out previously. This is used to indicate the local IP address of the server script's PC (i.e. PC2).
       - Leave the `port` as is ("8765") unless you know what you are doing and need to change it.
       - The `log_file_path` specifies where the “Mass Hunter” software saves its log files. Once you have found this folder on your computer, copy its path and repplace the default value here. You need to make sure to only use forward slashes ("/") instead of back slashes ("\\") in the path.
       - The `log_file_name` is mostly used for debugging purposes and can be left as is.
       - The `triggers` specifies which words in the log file indicate to us that we want to shut down the "Star Software". Please note that some words in the log file might indicate a critical error only in some occasions but are not critical in other occasions. Therefore make sure that a trigger word is "safe" to be used here. Also ensure that you separate trigger words by comma but without spaces.
       - The `client_shutdown_delay_mins` specifies how long we want to wait in minutes before shutting down the "Star Software" after detecting an error in the log file. By default this is set to "2" which should be fine for most applications.
       - The `server_repeat_delay_secs` specifies how long we want to wait in seconds after checking the log file for errors before repeating the error checking process. This should also be fine for most applications.
     - Save the `config.ini` file and exit the text editor.
     - Copy the `config.ini` file to PC2 (e.g. using a USB stick) and replace the default `config.ini` file with the edited version in the `config` folder.
4. Run software
   - You are now ready to use the software.
   - This is done in the following way:
     - Start your measurements the usual way (i.e. in the “Star Software” and “Mass Hunter” software on the respective computers)
     - Make sure that the "Star Software" is run in full screen mode and is in the foreground. Additionally, ensure that no window is covering its `Reset` button.
     - Head to the `src` folder on each computer.
     - Run the `server.py` script on PC2.
     - Run the `client.py` script on PC1.
     - After the measurements are done or an error was detected and the "Star Software" was stopped, you can terminate both scripts again.

