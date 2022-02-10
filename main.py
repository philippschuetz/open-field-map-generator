from csv import excel
from email.utils import collapse_rfc2231_value
from multiprocessing.sharedctypes import Value
from typing import Counter
from attr import field
from openpyxl import Workbook, load_workbook
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

# user input
used_workbook = 'data.xlsx'
used_sheet = 'data'
used_column = 'A'
row_count = 60
border_config = 0

used_workbook = input("name of the excel table: ")
used_sheet = input("name of the sheet to use: ")
used_column = input("used column letter: ")
row_count = input("number of used rows: ")
border_config = input("used border type (inner(0), outer(1), none(3)): ")


excel_data_list = []
wb = load_workbook(used_workbook)
sheet = wb[used_sheet]

for i in range(1, int(row_count) + 1):
    cell = str(used_column) + str(i)
    excel_data_list.append(sheet[cell].value)

frequency_dict = Counter(excel_data_list)
frequency_list = []

for i in range(1, 65):
    if i in frequency_dict:
        frequency_list.append(frequency_dict[i])
    else:
        frequency_list.append(0)

frequency_list_p = []

# get percentage for each value
for i in frequency_list:
    i = i / 60
    frequency_list_p.append(i)


# background creation
out = Image.new("RGB", (520, 520), (0, 0, 0))
d = ImageDraw.Draw(out)

# green lines
# i = 65
# while i < 519:
#     d.line([(0, i), (519, i)], (106, 153, 85), 1)
#     d.line([(i, 0), (i, 519)], (106, 153, 85), 1)
#     i += 65

i = 0
x1 = 4
y1 = 4
x2 = 68
y2 = 68

for i in range(0, len(frequency_list_p)):
    if frequency_list_p[i] > 0.5:
        text_color = 0
    else:
        text_color = 255
    color = int(frequency_list_p[i] * 255)

    if i in [8, 16, 24, 32, 40, 48, 56]:
        x1 = 4
        y1 += 64
        x2 = 64
        y2 += 64
        
    d.rectangle([(x1, y1), (x2, y2)], (color, color, color))
    d.text((x1 + 5, y1 + 5), str(i+1), fill=(text_color, text_color, text_color))
    x1 += 64
    x2 += 64
    i += 1

# draw borders
if int(border_config) == 0:
    # delete four middle fields
    d.rectangle([(196, 196), (324, 324)], (0, 0, 0))
    # draw lines
    d.line([(196, 196), (324, 196)], (106, 153, 85), 4)
    d.line([(324, 196), (324, 324)], (106, 153, 85), 4)
    d.line([(324, 324), (196, 324)], (106, 153, 85), 4)
    d.line([(196, 324), (196, 196)], (106, 153, 85), 4)

if int(border_config) == 1:
    d.line([(0, 0), (520, 0)], (106, 153, 85), 4)
    d.line([(520, 0), (520, 520)], (106, 153, 85), 4)
    d.line([(520, 520), (0, 520)], (106, 153, 85), 4)
    d.line([(0, 520), (0, 0)], (106, 153, 85), 4)

out.show()