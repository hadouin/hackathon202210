import json
import os
import time
import shutil
import asyncio
from tkinter import W
from fact import cmd_fact
from decrypt_frame import decode_frame
from generateDLMSCMD import templating_dlms 
from x_max import get_x_max

from store_price import clone_product, sum_of_prices, delete_product
from prime_numbers import prime_numbers, sum_prime_numbers
from transport_stream import parse_transport_stream
from sink_aggregation import sink_aggregation

# See README.md for details

# Don't forget to relaod the service after any code change: 
#   ./app1_connect.sh
#   sudo systemctl restart app1.service
# 
# To see the errors:
#   ./app1_connect.sh
#   journalctl -u app1.service

# DO NOT CHANGE THESE CONSTANTS
INPUT_FOLDER = "/data/input" 
OUTPUT_FOLDER = "/data/output"

def main():
  while True:
    # List files under the input folder
    files = os.listdir(INPUT_FOLDER)
    # if no files wait and trya again later
    if not files: 
      time.sleep(5)
      continue
    file = files[0] #take the first file 
    with open(os.path.join(INPUT_FOLDER, file), 'r') as f: # load the file as json object if there is an error just continue            
      try:
        commands = json.load(f)
      except Exception as e:
        print(e)
        continue
    # temporary path the time we process the file
    tmp_path = f"/tmp/{os.path.splitext(file)[0]}.txt"
    print("tmp_path:", tmp_path)

    # Find commands of the file and create a task for each 
    with open(tmp_path, 'w') as f: 
      for id, command in commands.items():
        print(f"id: {id}, command: {command}")
        command_type = command.get("type")

    asyncio.create_task