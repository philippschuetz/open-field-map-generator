#!/bin/env python
from csv import excel
from email.utils import collapse_rfc2231_value
from multiprocessing.sharedctypes import Value
from attr import field
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
from sys import argv

if "-h" in argv or "--help" in argv:
    print("Usage: main.py [-h] [FILE]")
    quit()

if argv[1]:
    used_workbook = argv[1]
else:
    # user input
    used_workbook = input("name of the file (data.xlsx): ")
    if used_workbook == "":
        used_workbook = 'data.xlsx'

if used_workbook.endswith(".xlsx"):
    # parsing exel file
    from openpyxl import Workbook, load_workbook

    used_sheet = input("name of the sheet to use (data): ")
    if used_sheet == "":
        used_sheet = 'data'

    used_column = input("used column letter (A): ")
    if used_column == "":
        used_column = 'A'

    row_count = input("number of used rows (60): ")
    if row_count == "":
        row_count = 60

    border_config = input("used border type (inner (default): 0, outer: 1, none: 3): ")
    if border_config == "":
        border_config = 0

    raw_data_list = []
    wb = load_workbook(used_workbook)
    sheet = wb[used_sheet]

    for i in range(1, len(raw_data_list)):
        cell = str(used_column) + str(i)
        raw_data_list.append(sheet[cell].value)

elif used_workbook.endswith(".json"):
    # parsing json file
    from json import load

    with open(used_workbook, 'r') as json_in:
        raw_data_list = load(json_in)

else:
    print("assuming the data is in a csv format")
    with open(used_workbook, 'r') as csv_in:
        raw_data_list = []
        for line in csv_in.readlines():
            raw_data_list.append(int(line))

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
    i = i / max(frequency_dict)
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
    if frequency_list_p[i] > 0.5:
        text_color = 0
    else:
        text_color = 255
    color = int(frequency_list_p[i] * 255)

    if i in [8, 16, 24, 32, 40, 48, 56]:
        x1 = 0
        y1 += 64
        x2 = 64
        y2 += 64

    d.rectangle([(x1, y1), (x2, y2)], (color, color, color))
    d.text((x1 + 10, y1 + 10), str(i + 1), fill=(text_color, text_color, text_color))
    x1 += 64
    x2 += 64
    i += 1

# draw borders
if int(border_config) == 0:
    # delete four middle fields
    d.rectangle([(192, 192), (320, 320)], (0, 0, 0))
    # draw lines
    d.line([(192, 192), (320, 192)], (106, 153, 85), 8)
    d.line([(320, 192), (320, 320)], (106, 153, 85), 8)
    d.line([(320, 320), (192, 320)], (106, 153, 85), 8)
    d.line([(192, 320), (192, 192)], (106, 153, 85), 8)

if int(border_config) == 1:
    d.line([(0, 0), (512, 0)], (106, 153, 85), 8)
    d.line([(512, 0), (512, 512)], (106, 153, 85), 8)
    d.line([(512, 512), (0, 512)], (106, 153, 85), 8)
    d.line([(0, 512), (0, 0)], (106, 153, 85), 8)

out.show()
