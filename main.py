#!/bin/env python3
from csv import excel
from email.utils import collapse_rfc2231_value
from multiprocessing.sharedctypes import Value
from attr import field
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
from sys import argv
import getopt

# define variables used in command line options
border_config = used_column = used_sheet = row_count = ""

# print help message
def print_help():
    print("Usage: main.py [OPTIONS] [FILE]")
    print("Generate analysation map for open-field-tests from data in .xlsx, .json or .csv file.\n")
    print("-b, --border     border type, accepted values are 0, 1, 2, 3")
    print("-s, --sheet      sheet from used .xlsx file")
    print("-c, --column     column letter used in .xlsx file")
    print("-r, --rows       number of rows used in .xlsx file")
    

# extract command line options
try:
    args, opts = getopt.getopt(argv[1:], "hb:s:c:r:", ["help", "border=", "sheet=", "column=", "rows="])
except getopt.GetoptError:
    print_help()
    quit(2)

for arg, opt in args:
    # print help and exit
    if arg in ["-h", "--help"]:
        print_help()
        quit(0)
    # set border style
    if arg in ["-b", "--border"]:
        try:
            border_config = int(opt)
            continue
        except ValueError:
            if opt == "inner":
                border_config = 0
                continue
            if opt == "outer":
                border_config = 1
                continue
            if opt == "both":
                border_config = 2
                continue
            if opt == "none":
                border_config = 3
                continue
    if arg in ["-s", "--sheet"]:
        used_sheet = opt
    if arg in ["-c", "--column"]:
        used_column = opt
    if arg in ["-r", "--rows"]:
        row_count = opt
        

# use command line argument as file name if given
if len(opts) > 0:
    used_workbook = opts[0]
# else use user input
else:
    used_workbook = input("path to and name of the file (data.csv): ")
    if used_workbook == "":
        used_workbook = 'example.csv'

# parsing exel file
if used_workbook.endswith(".xlsx"):
    from openpyxl import Workbook, load_workbook

    if used_sheet == "":
        used_sheet = input("name of the sheet to use (data): ")
        if used_sheet == "":
            used_sheet = 'data'

    if used_column == "":
        used_column = input("used column letter (A): ")
        if used_column == "":
            used_column = 'A'

    if row_count == "":
        row_count = input("number of used rows (60): ")
        if row_count == "":
            row_count = 60

    raw_data_list = []
    wb = load_workbook(used_workbook)
    sheet = wb[used_sheet]

    for i in range(1, int(row_count)):
        cell = str(used_column) + str(i)
        raw_data_list.append(sheet[cell].value)

# parsing json file
elif used_workbook.endswith(".json"):
    from json import load

    with open(used_workbook, 'r') as json_in:
        raw_data_list = load(json_in)

# default to csv format
else:
    if not used_workbook.endswith(".csv"):
        print("assuming the data is in a csv format")
    with open(used_workbook, 'r') as csv_in:
        raw_data_list = []
        for line in csv_in.readlines():
            raw_data_list.append(int(line))

# get border design if not set by command line options
if border_config == "":
    border_config = input("used border type (inner (default): 0, outer: 1, both: 2, none: 3): ")
    if border_config == "":
        border_config = 0

# calculate frequencies of values in raw_data_list
frequency_dict = Counter(raw_data_list)
frequency_list = []

for i in range(1, 65):
    if i in frequency_dict:
        frequency_list.append(frequency_dict[i])
    else:
        frequency_list.append(0)

frequency_list_p = []

# get percentage for each value
for i in frequency_list:
    i = i / max(frequency_list)
    frequency_list_p.append(i)

# background creation
out = Image.new("RGB", (512, 512), (0, 0, 0))
d = ImageDraw.Draw(out)

i = 0
x1 = 0
y1 = 0
x2 = 64
y2 = 64

for i in range(0, len(frequency_list_p)):
    # change text color depending on brightness of tile
    if frequency_list_p[i] > 0.5:
        text_color = 0
    else:
        text_color = 255
    # base brightness of tile on calculated value
    color = int(frequency_list_p[i] * 255)

    if i in [8, 16, 24, 32, 40, 48, 56]:
        x1 = 0
        y1 += 64
        x2 = 64
        y2 += 64

    d.rectangle(((x1, y1), (x2, y2)), (color, color, color))
    d.text((x1 + 10, y1 + 10), str(i + 1), fill=(text_color, text_color, text_color))
    x1 += 64
    x2 += 64
    i += 1

# draw inner border
if int(border_config) == 0:
    # delete four middle fields
    d.rectangle(((192, 192), (320, 320)),(0, 0, 0))
    # draw lines
    d.line([(192, 192), (320, 192)], (106, 153, 85), 8)
    d.line([(320, 192), (320, 320)], (106, 153, 85), 8)
    d.line([(320, 320), (192, 320)], (106, 153, 85), 8)
    d.line([(192, 320), (192, 192)], (106, 153, 85), 8)

# draw outer border
if int(border_config) == 1:
    d.line([(0, 0), (512, 0)], (106, 153, 85), 8)
    d.line([(512, 0), (512, 512)], (106, 153, 85), 8)
    d.line([(512, 512), (0, 512)], (106, 153, 85), 8)
    d.line([(0, 512), (0, 0)], (106, 153, 85), 8)

# draw both inner and outer border
if int(border_config) == 2:
    # draw outer border
    d.line([(0, 0), (512, 0)], (106, 153, 85), 8)
    d.line([(512, 0), (512, 512)], (106, 153, 85), 8)
    d.line([(512, 512), (0, 512)], (106, 153, 85), 8)
    d.line([(0, 512), (0, 0)], (106, 153, 85), 8)
        # delete four middle fields
    d.rectangle(((192, 192), (320, 320)),(0, 0, 0))
    # draw inner border
    d.line([(192, 192), (320, 192)], (106, 153, 85), 8)
    d.line([(320, 192), (320, 320)], (106, 153, 85), 8)
    d.line([(320, 320), (192, 320)], (106, 153, 85), 8)
    d.line([(192, 320), (192, 192)], (106, 153, 85), 8)

out.show()
