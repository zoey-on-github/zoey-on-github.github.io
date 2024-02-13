from bs4 import BeautifulSoup
import os

with open("blog/a_blog.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
f = open("blog_index.html","w")
f.write("<head>"+"\n")
f.write("    <title>gay raccoon girl on the web</title>"+"\n")
f.write("    <link rel=\"stylesheet\" href=\"styling.css\">"+"\n")
f.write("</head>"+"\n")
f.write("<h1> here are all of my blog posts</h1>")

directory = os.fsdecode("blog")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    with open("blog/" + filename) as fp2:
        soup2 = BeautifulSoup(fp2, 'html.parser')
    f.write("<a href=\"" + "blog/" + filename + "\">" + str(soup2.h1.text) + "</a>"+"<br>")
#f.write(str(soup.h1))
f.close()
