import csv
import pyautogui
import time
import argparse

pyautogui.FAILSAFE = True


Parser = argparse.ArgumentParser()
Parser.add_argument(
    "-F", help="Pass the csv file that stores the HID data.", required=True, type=str)
Parser.add_argument(
    "-I", help="Passing the interactive flag allows for evaluation of text via PyAutoGUI", type=int)
Args = Parser.parse_args()


def InteractiveAnalysis(KeyboardInput):
    'Uses PyAutoGui to evaluate sequence interactively'
    print("[*] Sleeping for 5 Seconds, Open Leafpad.")
    time.sleep(5)

    for key in KeyboardInput:
        if key == "RightArrow" or key == ">":
            pyautogui.press("right")
        elif key == "LeftArrow" or key == "<":
            pyautogui.press("left")
        elif key == "enter":
            pyautogui.press("enter")
        else:
            pyautogui.press(key)



def CapitalizationHandler(ToProcess, CapsLock=False):
    'Correcly capitalizes the string'

    ReturnArr = []
    i = 0
    for Sig in ToProcess:
        CounterObs = ToProcess[i]

        if Sig == "CapsLock":
            CapsLock = not CapsLock
            i += 1
            continue

        else:
            if CapsLock:
                ReturnArr.append(ToProcess[i].capitalize())
            else:
                ReturnArr.append(ToProcess[i])

            i += 1

    return(ReturnArr)


def HID2KEY(HID, ShiftPresence):
    'Converts HIDs to their keys by using the MappingN dictionary'
    if (4 <= HID < 99):
        if ShiftPresence:
            return(MappingS.get(HID))
        else:
            return(MappingN.get(HID))
    else:
        return("")


Filename = Args.F
Rows = []
HIDs = []
KeyboardInput = []

# reading csv file
with open(Filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        Rows.append(row)
        HIDs.append(row[6]) #! Look Into 
# This line works on the idea that the CSV file included a table header value. 
HIDs.pop(0) 

# Working HIDs



# MappingN Accounts for Normal Mappings whilst MappingS accounts for MappingN with Shift
MappingN = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 40: 'Enter', 41: 'esc',
            42: 'del', 43: 'tab', 44: 'space', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 50: ' ', 51: ';', 52: "'", 53: '`', 54: ',', 55: '.', 56: '/', 57: 'CapsLock', 79: 'RightArrow', 80: 'LeftArrow', 84: '/', 85: '*', 86: '-', 87: '+', 88: 'Enter', 89: '1', 90: '2', 91: '3', 92: '4', 93: '5', 94: '6', 95: '7', 96: '8', 97: '9', 98: '0', 99: '.'}
MappingS = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*',
            38: '(', 39: ')', 40: 'Enter', 41: 'esc', 42: 'del', 43: 'tab', 44: 'space', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 50: ' ', 51: (':',), 52: '\\', 53: '~', 54: '<', 55: '>', 56: '?', 57: 'CapsLock', 79: 'RightArrow', 80: 'LeftArrow', 84: '/', 85: '*', 86: '-', 87: '+', 88: 'Enter', 89: '1', 90: '2', 91: '3', 92: '4', 93: '5', 94: '6', 95: '7', 96: '8', 97: '9', 98: '0', 99: '.'}
ShiftKeys = ["02", "20"]


# Works on the assumption all HIDs are of length 16
for HID in HIDs:
    if HID == "0" * 16:
        HIDs.remove(HID)

i = 0
# Find and Generate List of mappings
for HID in HIDs:
    i += 1
    # print(i)
    ShiftBits = str(HID[0:2])
    ContentBytes = bytearray.fromhex(HID[2:16])
    ShiftPresence = (ShiftBits in ShiftKeys)

    for Byte in ContentBytes:
        # print(Byte)
        if Byte != 0:
            Key = HID2KEY(int(Byte), ShiftPresence)
            if Key != None:
                KeyboardInput.append(Key)
                # print(f"Appending {Key},{Byte},{ShiftPresence},{len(KeyboardInput)-1}")
            else:
                print(f"[-] No Mapping Found for {Byte}")

# Remove Duplicate CapsLock
for Sig in KeyboardInput:
    i = 0
    if Sig == "CapsLock" and KeyboardInput[i+1] == "CapsLock":
        KeyboardInput.pop(i+1)
        KeyboardInput.pop(i)
        print("[+] Removed Duplicated CapsLock")
    i += 1

if "CapsLock" in KeyboardInput:
    KeyboardInput = CapitalizationHandler(KeyboardInput)

KeyboardInput = list("".join(KeyboardInput).split("Enter")[
                     2].replace("RightArrow", ">").replace("LeftArrow", "<"))
print("[+] Payload Generated", "".join(KeyboardInput))

