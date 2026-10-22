import subprocess
import sys
filename = sys.argv[1].split("/")[1].split(".")[0]
subprocess.run(["pandoc", "-s", sys.argv[1], "--syntax-highlighting=breezedark", "--css=/styling.css", "-t", "html", "-o", "blog/" + filename + ".html"])
