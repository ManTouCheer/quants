from setting import LogCfg
import time

def log_message(msg):
    log_file_name = f"log_{time.time()}.txt"
    with open(f".\log_files\{log_file_name}", "a") as log_file:
        log_file.write(f"{msg}\n")
