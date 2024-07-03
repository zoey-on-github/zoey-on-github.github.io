import os
import sys

f = open(sys.argv[1], "w", encoding="utf-8")
f.write("    <link rel=\"stylesheet\" href=\"wallpaper.css\">"+"\n")
directory = os.fsdecode("yuri")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    # with open("wallpapers/" + filename) as fp2:
    f.write("<img src=\"" + sys.argv[2] + "/" + filename + "\">" + "\n")
f.close()