import os

f = open("wallpapers.html", "w", encoding="utf-8")
f.write("    <link rel=\"stylesheet\" href=\"styling.css\">"+"\n")
directory = os.fsdecode("wallpapers")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    # with open("wallpapers/" + filename) as fp2:
    f.write("<img src=\"" + "wallpapers/" + filename + "\">" + "\n")
f.close()
