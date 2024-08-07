import subprocess
import threading
import time
import os 

def run_process1(output_file):
    while True:
        # Start process1 and capture its output
        with open(output_file, 'a') as f:  
            process1 = subprocess.Popen(
                "kubectl get hpa php-apache",  #
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process1.communicate()
            
            # Write the output to the file
            if stdout:
                stringResponse = stdout.decode() 
                desired_string = stringResponse.split('\n')[1]
                print(desired_string)
            #if stderr:
            #    stringResponse = stderr.decode() + '\n'
            #    print('2',stringResponse)
        
            f.write(desired_string + '\n')
        time.sleep(2)  # Adjust this sleep interval as needed

# Define the output file for process1
start_string = 'NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE'
output_file = 'StressLog.log'
with open(output_file, 'a') as f:  
    f.write(start_string + '\n')

# Run process1 in a separate thread
process1_thread = threading.Thread(target=run_process1, args=(output_file,))
process1_thread.start()
