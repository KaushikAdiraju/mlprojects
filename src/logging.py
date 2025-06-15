import logging
from datetime import datetime
import os
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"   #Month day year and Hour-Minute-Second Format
log_path = os.path.join(os.getcwd(),"logs",LOG_FILE) #cwd is Desktop/MLProjects  --> Desktop/MLProjects/logs
os.makedirs(log_path,exist_ok=True)      # Example --> 04_10_2025_11_53_55.log
LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)  

logging.basicConfig(                          #Basic configuration for logging the logs
    filename= LOG_FILE_PATH,
    level= logging.INFO
)