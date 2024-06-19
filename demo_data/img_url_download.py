import wget
import os 

os.system("clear")

print("Press ctrl+D to exit.")

while True:
    url = input("img_url_here: ")
    filename = wget.download(url)
    print(filename)
