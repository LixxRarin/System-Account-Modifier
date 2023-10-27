#!/usr/bin/env python3

import os

c = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m'
}
print(f"-- {c['bold']}System-Account-Modifier{c['reset']} --\nHello, {os.getlogin()}...\n")

if os.geteuid() != 0:
    print("Please run as superuser.")
    exit()

directory = "/var/lib/AccountsService/users/"

if not os.path.isdir(directory):
    print("Directory not found.")
    exit()

print("Select one of the following users: ")
files = os.listdir(directory)

for index, filename in enumerate(files, start=1):
    with open(directory + filename, 'r') as file:
        for line in file:
            if 'SystemAccount' in line:
                current_value = line.split('=')[1].strip()

                if current_value == "true":
                    current_value = c['green'] + current_value + c['reset']
                elif current_value == "false":
                    current_value = c['red'] + current_value + c['reset']
                    
                break
    
    print(f"{index}. {c['bold']}{filename}{c['reset']} : {current_value}")

while True:
    try:
        selected_index = int(input(f"Enter the number corresponding to the {c['bold']}user{c['reset']}: "))
        if 1 <= selected_index <= len(files):
            break
        else:
            print(f"{c['red']}Invalid number{c['reset']}. Try again.")
    except ValueError:
        print(f"{c['red']}Invalid Input. Enter a number.{c['reset']}")

selected_file = os.path.join(directory, files[selected_index - 1])

with open(selected_file, 'r') as file:
    filedata = file.read()

if 'SystemAccount=true' in filedata:
    filedata = filedata.replace('SystemAccount=true', 'SystemAccount=false')
    new_value = f"{c['bold']}{c['red']}false{c['reset']}"
else:
    filedata = filedata.replace('SystemAccount=false', 'SystemAccount=true')
    new_value = f"{c['bold']}{c['green']}true{c['reset']}"

with open(selected_file, 'w') as file:
    file.write(filedata)

print(f"The {c['bold']}SystemAccount{c['reset']} variable in the file {c['bold']}{selected_file}{c['reset']} has been changed to {new_value}.")