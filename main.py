import time
import random
import math
import os
import functions
#import classes # for later file system
import data
import pygame
import threading

pygame.mixer.init()
standard_data = data.standard_data
color_map = data.color_map
current_data = {}
file_systems = []

username = ""
password = ""
connected_ip = ""
connected_id = ""
connected_file_system = None

boot_sequence = data.boot_sequence
BOOT_ENABLED = True

def convertColor(code : str):
    if code.upper() in color_map:
        return color_map[code.upper()]
    else:
        print("  Invalid color code!")
        return None

def boot():
    clearScreen()
    if not BOOT_ENABLED:
        return
    boot_time = 0.0
    time_threshold_high = 0.1
    time_threshold_low = 0.3
    estimated_time = sum(delay for _, delay in boot_sequence)
    print("--// Estimated boot time:", math.ceil(estimated_time * 10 ** 2) / 10 ** 2, "seconds")
    for message, delay in boot_sequence:
        print(message)
        random_delay = random.uniform(delay - time_threshold_low, delay + time_threshold_high)
        boot_time += random_delay
        time.sleep(random_delay)
    print("--// Boot time:", math.ceil(boot_time * 10 ** 2) / 10 ** 2, "seconds")

def firstBoot():
    functions.randomizeServerIPs()

def typewrite(message: str, delay: float):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def login():
    data = functions.loadData()
    input_username = input("username: ")
    input_password = input("password: ")
    if data["firstBoot"] == "true":
        data["username"] = input_username
        data["password"] = input_password
        username = input_username
        password = input_password
        functions.saveData(data)
        return
    else:
        if input_username == data["username"] and input_password == data["password"]:
            username = input_username
            password = input_password
            return
        else:
            print("Incorrect username/password.")
            login()

def handleHelp(args):
    if len(args) == 1:
        pass
    elif len(args) == 0:
        print("  --// System Commands")
        print("  help <(command)> - Displays all available commands or specific information about a command.")
        print("  color <color_code> - Changes the terminal color to the selected color.")
        print("  colors - Displays all color codes.")
        print("  echo <string> - prints any string given.")
        print("  ipconfig - prints your currently connected IP address.")
        print("  exit - Exits the terminal.")
        print("  scan <(ip)>- shows all ips available from the current device or specific info about a server")
        print("  netscan - scans for any open ports")
        print("  clear - clears the screen")
        print("  --// Executables")
        for executable in executables:
            print("  " + str(executable))
    else:
        print(f"  help.py - Too many arguments ({str(len(args))})")

def handleEcho(args):
    if len(args) != 0:
        print(" ".join(args))
    else:
        print("  Missing 1 argument: <string>")

def handleIPConfig(args):
    if len(args) != 0:
        print(f"  ip_config.cpp - Too many arguments ({str(len(args))}")
    else:
        print(f"  You are currently connected to: {connected_ip}")

def handleColor(args):
    if len(args) == 1:
        if len(args[0]) == 1:
            if os.name == 'nt':
                if args[0].upper() in color_map:
                    os.system(f'color {args[0]}')
                else:
                    print("  Invalid color code!")
            elif os.name == 'posix':
                color_code = convertColor(args[0])
                if color_code:
                    os.system(f'\033[38;5;{color_code}m')
        else:
            print(f"  Invalid color code: {str(args[0])}")
    elif len(args) == 0:
        print("  Missing 1 argument: <color_code>")
    else:
        print(f"  color.sh - Too many arguments ({str(len(args))})")

def handleExit(args=None):
    os._exit(0)

def handleScan(args):
    if len(args) >= 2:
        print(f"  scan.c - Too many arguments ({str(len(args))})")
    elif len(args) == 1:
        message = ""
        info = functions.getServerInfo(False, args[0])
        if info:
            print(f"  name: {info['name']}")
            print(f"  ip: {info['ip']}")
            print(f"  status: {info['status']}")
            print(f"  type: {info['type']}")
            print(f"  ports: {len(info['ports'])}")
            print(f"  firewall: {info['firewall']}")
        else:
            print("  Invalid IP address.")
    else:
        message = ""
        current_server = functions.getServerInfo(connected_id, False)
        for server in current_server['connected']:
            info = functions.getServerInfo(server, False)
            if info:
                message = message + "  " + server + " " + info['ip'] + "\n"
        print(message)

def handleConnect(args=None):
    global connected_id, connected_ip, connected_file_system
    if len(args) >= 2:
        print(f"  connect.c - Too many arguments ({str(len(args))})")
    elif len(args) == 1:
        info = functions.getServerInfo(False, args[0])
        if info:
            connected_ip = info['ip']
            connected_id = info['id']
            for fs in file_systems:
                if str(fs) == info['id']:
                    connected_file_system = fs
        else:
            print("  connect.c - Invalid IP address.")
    else:
        print("  connect.c - Missing 1 argument: <server_ip>")

def handleColors(args):
    if len(args) == 0:
        print(data.printed_color_map)
    else:
        print(f"  colors.py - Too many arguments ({str(len(args))})")

def handleNetscan(args):
    if len(args) == 0:
        current_server = functions.getServerInfo(connected_id, False)
        for number, port in current_server['ports'].items():
            print("    ", number, port)
    else:
        print(f"  netscan.cpp - Too many arguments ({len(args)})")

def clearScreen(args=None):
    if os.name == 'posix':
        _ = os.system('clear')
    elif os.name == 'nt':
        _ = os.system('cls')

commands = {
    "help": handleHelp,
    "echo": handleEcho,
    "ipconfig": handleIPConfig,
    "color": handleColor,
    "exit": handleExit,
    "scan": handleScan,
    "connect": handleConnect,
    "colors": handleColors,
    "netscan": handleNetscan,
    "clear": clearScreen,
}

executables = {
    "tunes": data.exes["%TUNES_EXE%"],
}

def processCommand(command : str):
    parts = command.strip().split()
    if not parts:
        return
    cmd_name = parts[0]
    args = parts[1:]

    if cmd_name in commands:
        commands[cmd_name](args)
    elif cmd_name in executables:
        thread = threading.Thread(target=executables[cmd_name], args=(args,))
        thread.start()
    else:
        typewrite(f"  Unknown command: {cmd_name}", 0.05)
        typewrite("Type 'help' to see a list of commands.", 0.05)

def askY_N(question : str):
    print(question)
    answer = input("(Y/N)\n")
    if answer.lower() == "y":
        return True
    elif answer.lower() == "n":
        return False
    else:
        print(answer)
        print(answer.lower())
        return askY_N(question)

file_systems = functions.loadFilesystems()
boot()
time.sleep(2)
clearScreen()
time.sleep(1)
current_data = functions.loadData()
if not current_data:
    answer = askY_N("Your data format is invalid and we currently cannot fix this automatically for you. Do you want to reset it?")
    if answer:
        functions.saveData(standard_data)
    else:
        print("Please contact anyone who knows about python like a developer to fix this error. This was probably caused by an update of the standard data format.")
        exit()
current_data = functions.loadData()
typewrite(data.ascii_intrudex, 0.001)
time.sleep(0.5)

if current_data["firstBoot"] == "true":
    typewrite("It seems you are new here. Please enter a username and a password to continue. (Write it down somewhere. You'll need it to reboot etc.)", 0.05)
else:
    typewrite("Please log in.", 0.05)
login()
current_data = functions.loadData()
typewrite("Welcome, " + current_data["username"] + "!", 0.05)
time.sleep(0.5)
handleConnect(["127.0.0.1"])
if current_data["firstBoot"] == "true":
    firstBoot()
    typewrite("Your job is to accept contracts and complete them for profit.", 0.05)
    time.sleep(1.5)
typewrite(f"You are currently connected to: {connected_ip}", 0.05)
time.sleep(0.5)
typewrite("Type 'help' to see a list of commands.", 0.05)
current_data["firstBoot"] = "false"
functions.saveData(current_data)
current_data = functions.loadData()

while True:
    command = input(connected_ip + " > ")
    processCommand(command)