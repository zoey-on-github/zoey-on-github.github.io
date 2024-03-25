fom bs4 import BeautifulSoup
import os

directory = os.fsdecode("blog")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    with open("wallpapers/" + filename) as fp2:
        soup2 = BeautifulSoup(fp2, 'html.parser')
    f.write("<a href=\"" + "blog/" + filename + "\">" + str(soup2.h1.text) + "</a>"+"<br>\n")
#f.write(str(soup.h1))
f.close()