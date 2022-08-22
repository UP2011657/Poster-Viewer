import json
import tkinter  as tk
from PIL import Image, ImageTk
from os import getenv

from urllib import response
#Allows for searching with the website
from urllib.request import Request, urlopen, urlretrieve

#Get api key from file
with open("APIKey.env") as file:
    apiKey = file.read()

#Getting the title of the movie to create the url
movieSearch = input("Enter a movie title: ")
movieSearch = movieSearch.replace(" ", "%20")
url = "https://imdb-api.com/en/API/SearchMovie/"+apiKey+"/"+movieSearch

#Getting the data from the url and loading it
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
data = urlopen(req,timeout=10).read()
jsonObject = json.loads(data)

#Outputs all movie titles matching the search
for i in jsonObject['results']:
    print(i['title'] + i['description'])

#Creating variables of the first results
title = jsonObject['results'][0]['title']
posterUrl = jsonObject['results'][0]['image']

currentTitleIndex = 0
def ChangeTitle(event):
    global title, posterUrl, currentTitleIndex
    if(event.keysym=='Right' and currentTitleIndex<len(jsonObject['results'])-1):
        currentTitleIndex += 1
    if(event.keysym=='Left' and currentTitleIndex != 0):
        currentTitleIndex -= 1
    title = jsonObject['results'][currentTitleIndex]['title']
    posterUrl = jsonObject['results'][currentTitleIndex]['image']
    ObtainPosterImg()
    clear_frame()
    displayPoster()
    print(title)

posterFound=True
def ObtainPosterImg():
    global posterUrl, posterFound
    try:
        urlretrieve  (
            posterUrl,
        "poster.jpg")
        posterFound=True
    except:
        print("#####ERROR##### \nFailed to load movie poster")
        posterFound=False
            

def clear_frame():
   global window
   for widgets in window.winfo_children():
      widgets.destroy()

ObtainPosterImg()
#create tkinter window
window = tk.Tk()
window.title("Movie Search")
#Display the poster.png image in the tkinter window
def displayPoster():
    if(posterFound):
        window.img = Image.open("poster.jpg")
    else:
        window.img = Image.open("nopicture.jpg")
    window.img = window.img.resize((416, 640), Image.Resampling.LANCZOS)
    window.img = ImageTk.PhotoImage(window.img)
    movieTitle = tk.Label(window, text=title+" ("+str(currentTitleIndex+1)+"/"+str(len(jsonObject['results']))+")")
    poster = tk.Label(window, image=window.img)
    movieTitle.pack()
    poster.pack()
displayPoster()
window.bind("<KeyRelease>", ChangeTitle)
window.mainloop()
