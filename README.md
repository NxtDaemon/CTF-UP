# CTF-UP (CTF USB-Parser)

```
Python3 -F data.csv -I
```

```
usage: Parse.py [-h] -F F [-I] [-NH]

options:
  -h, --help  show this help message and exit
  -F F        Pass the csv file that stores the HID data.
  -I          Passing the interactive flag allows for evaluation of text via PyAutoGUI
  -NH         Use this argument if the CSV file has no Header Row
```

The program is written to process CSV files and build the input of the keyboard found in the `usb.capdata` variable within wireshark captures, the responsibility of collecting the data in a usable form is directed to the user, the program expects a comma seperated .CSV with the given option to select the column to scape data from.
