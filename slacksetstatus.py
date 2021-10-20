import slack, argparse, datetime
from pathlib import Path

# Terminal arguments
my_parser = argparse.ArgumentParser()
my_parser.add_argument('-input', action='store', type=str, required=True)
args = my_parser.parse_args()

parameters = (args.input).replace(", ","").replace(" ,","")
parameters = parameters.split(",")
if len(parameters) not in [3,4]:
    raise Exception("Needs at least 3 or 4 arguments. (Member ID, Status Text, Status Emoji, (Optional) Status Expiration)")

client_id = parameters[0]
status_text = parameters[1]
status_emoji = parameters[2]

try:
    status_expiration = parameters[3]
except Exception as e:
    status_expiration = 0

# If not 0 ensure proper datetime input 
if status_expiration != 0:
    date = status_expiration.split("/")
    now_time = (datetime.datetime.now())
    if len(date[2]) == 2:
        date[2] = "20"+date[2]
    set_time = (datetime.datetime(int(date[2]),int(date[0]),int(date[1])))
    status_expiration = set_time.timestamp()

    time_diff = set_time - now_time 
    if "-" in str(time_diff):
        raise Exception("You cannot choose a date that has already passed.")


USER_TOKEN = "xoxp-13881559250-2180207628595-2608320044581-bdcf75c1fe6f2eadac0c725587722538"
client = slack.WebClient(token=USER_TOKEN)
client.users_profile_set(user=client_id, profile={"status_text": status_text, "status_emoji": status_emoji,"status_expiration": status_expiration})