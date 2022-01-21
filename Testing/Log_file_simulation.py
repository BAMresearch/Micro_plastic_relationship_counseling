import random
import time

log_file_name = "20220121-1443-3-TGATDU_error_simulation.log"

normal_log_messages =   ["Moving motor Motor Z relative -2.0mm",\
                        "Moving to TDUP:1",\
                        "Release Needle Guide",\
                        "Updating TDUI2"]

error_log_messages =    ["Error: Exception while cleaning up for entry 2: Aborted",\
                        "Critical Error: Controller State FAULT",\
                        "Error while moving to TDUI2:1: 147: Unexpected Z-Axis Collision at 161.4mm",\
                        "Critical Error: Controller State FAULT"]

for _ in range(100):
    with open(log_file_name, "a") as f:
        f.write("21-Jan-22 14:43:00\t\t")
        
        rnd_num_error = random.random()

        if rnd_num_error < 0.1:
            rnd_num_message = random.randint(0, len(error_log_messages) - 1)
            f.write(error_log_messages[rnd_num_message])
        else:
            rnd_num_message = random.randint(0, len(normal_log_messages) - 1)
            f.write(normal_log_messages[rnd_num_message])
        
        f.write("\n")
    
    time.sleep(0.5)