import os

f = open("wallpapers.html", "w")

directory = os.fsdecode("wallpapers")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    # with open("wallpapers/" + filename) as fp2:
    f.write("<img src=\"" + "wallpapers/" + filename + "\">" + "<br>\n")
f.close()
