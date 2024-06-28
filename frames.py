import os

f = open("frames.html", "w", encoding="utf-8")
f.write("    <link rel=\"stylesheet\" href=\"wallpaper.css\">"+"\n")
directory = os.fsdecode("frames")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    # with open("wallpapers/" + filename) as fp2:
    f.write("<img src=\"" + "frames/" + filename + "\">" + "\n")
f.close()