from bs4 import BeautifulSoup
import os

with open("blog/a_blog.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
f = open("blog_index.html","w")
f.write(r"<head>")
f.write(r"    <title>gay raccoon girl on the web</title>")
f.write(r"    <link rel=\"stylesheet\" href=\"styling.css\">")
f.write(r"</head>")

directory = os.fsdecode("blog")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    with open("blog/" + filename) as fp2:
        soup2 = BeautifulSoup(fp2, 'html.parser')
    f.write("<a href=\"" + "blog/" + filename + str(soup2.h1) + "</a>")
#f.write(str(soup.h1))
f.close()
