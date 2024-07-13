import random
import os
import json
import pygame
import tkinter as tk
import threading
import classes

music_player_window = None

def generateIP():
    octet1 = random.randint(1, 254)
    octet2 = random.randint(0, 255)
    octet3 = random.randint(0, 255)
    octet4 = random.randint(1, 254)
    IP = f"{octet1}.{octet2}.{octet3}.{octet4}"
    return IP

def loadData():
    import data as dataPY
    standard_data = dataPY.standard_data
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            loadedData = json.loads(file.read())
            if loadedData["dataVersion"] and loadedData["dataVersion"] == dataPY.standard_data["dataVersion"]:
                return loadedData
            else:
                return None
    else:
        with open("data.json", "w") as file:
            json.dump(standard_data, file)
            return standard_data

def saveData(data : dict):
    with open("data.json", "w") as file:
        json.dump(data, file)

def listServers(include_local : bool):
    servers = []
    for filename in os.listdir("./servers"):
        if filename.endswith(".json"):
            file_path = os.path.join("./servers", filename)
            with open(file_path, 'r') as file:
                server_info = json.load(file)
                servers.append(server_info)

    if include_local:
        with open("./local.json", 'r') as file:
            server_info = json.load(file)
            servers.append(server_info)

    return servers

def getServerInfo(server_id : str, server_ip : str):
    servers = listServers(True)
    for file in servers:
        if server_id == False:
            if file['ip'] == server_ip:
                return file
        else:
            if file['id'] == server_id:
                return file
    return

def randomizeServerIPs():
    for filename in os.listdir("./servers"):
        if filename.endswith(".json"):
            file_path = os.path.join("./servers", filename)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    if not content.strip():
                        print(f"File {filename} is empty.")
                        continue
                    server_info = json.loads(content)
                server_info['ip'] = generateIP()
                with open(file_path, 'w') as file:
                    json.dump(server_info, file, indent=4)
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")

def generateBinary(length="VERYLONG"):
    string = ""
    if length == "VERYLONG":
        for i in range(40):
            binary = ""
            for i2 in range(6):
                if random.random() > 0.5:
                    binary += "0"
                else:
                    binary += "1"
            string += (" " + binary)
    elif length == "LONG":
        for i in range(30):
            binary = ""
            for i2 in range(6):
                if random.random() > 0.5:
                    binary += "0"
                else:
                    binary += "1"
            string += (" " + binary)
    elif length == "MEDIUM":
        for i in range(20):
            binary = ""
            for i2 in range(6):
                if random.random() > 0.5:
                    binary += "0"
                else:
                    binary += "1"
            string += (" " + binary)
    elif length == "SHORT":
        for i in range(10):
            binary = ""
            for i2 in range(6):
                if random.random() > 0.5:
                    binary += "0"
                else:
                    binary += "1"
            string += (" " + binary)
    return string

def checkContents(contents : dict, file_system : classes.FileSystem, directory : classes.Directory):
    for content in contents:
        if file_system:
            if content['type'] == 'file':
                fileContent = ""
                executable = ""
                if content.get('specialType'):
                    if content['specialType'] == '#BINARY_VERYLONG#':
                        fileContent = generateBinary("VERYLONG")
                    elif content['specialType'] == '#BINARY_LONG#':
                        fileContent = generateBinary("LONG")
                    elif content['specialType'] == '#BINARY_MEDIUM#':
                        fileContent = generateBinary("MEDIUM")
                    elif content['specialType'] == '#BINARY_SHORT#':
                        fileContent = generateBinary("SHORT")
                else:
                    fileContent = content['content']
                if content.get('executable'):
                    executable = content['executable']
                file_system.makeFile(content['name'], fileContent, content['core'], executable)
            elif content['type'] == 'dictionary':
                if content.get('specialType'):
                    tag = content['specialType']
                    Dir = file_system.makeDir(content['name'], content['core'], tag)
                    checkContents(content['contents'], None, Dir)
                else:
                    Dir = file_system.makeDir(content['name'], content['core'])
                    checkContents(content['contents'], None, Dir)
        else:
            if content['type'] == 'file':
                fileContent = ""
                executable = ""
                if content.get('specialType'):
                    if content['specialType'] == '#BINARY_VERYLONG#':
                        fileContent = generateBinary("VERYLONG")
                    elif content['specialType'] == '#BINARY_LONG#':
                        fileContent = generateBinary("LONG")
                    elif content['specialType'] == '#BINARY_MEDIUM#':
                        fileContent = generateBinary("MEDIUM")
                    elif content['specialType'] == '#BINARY_SHORT#':
                        fileContent = generateBinary("SHORT")
                else:
                    fileContent = content['content']
                if content.get('executable'):
                    executable = content['executable']
                directory.add(classes.File(content['name'], fileContent, content['core'], executable))
                
            elif content['type'] == 'dictionary':
                if content.get('specialType'):
                    tag = content['specialType']
                    Dir = directory.add(classes.Directory(content['name'], content['core'], tag))
                    checkContents(content['contents'], None, Dir)
                else:
                    Dir = directory.add(classes.Directory(content['name'], content['core']))
                    checkContents(content['contents'], None, Dir)

def loadFilesystems():
    file_systems = []
    servers = listServers(True)
    for server in servers:
        file_system = classes.FileSystem(server['name'])
        checkContents(server['contents'], file_system, None)
        file_systems.append(file_system)
    return file_systems