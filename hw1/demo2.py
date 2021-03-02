import urllib.request
import sys

URL = sys.argv[1]
request = urllib.request.urlopen(URL)

list = []
resp = str(request.read())
resp.replace("\n", " ")
resp.replace("\r", " ")
resp.replace("\t", " ")
for part in resp.split(" "):
    if ".js'" in part or '.js"' in part:
        pos=1
        while not pos == -1:
            pos = part.find(".js")
            if not pos == -1:
                for i in range(pos+2,0,-1):
                    if part[i] == '"' or part[i]=="'":
                        if not (part[i+1:pos+3] in list):
                            list.append(part[i+1:pos+3])
                part = part[pos+3:]
for file in list:
    print(file)
print("JS Files found: " + str(len(list)))