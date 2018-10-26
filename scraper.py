import requests
from bs4 import BeautifulSoup
import datetime
import scraperwiki
import csv

linkliste = list(csv.reader(open("skigebiete_linkliste.csv")))

skigebiete_final = []
for gebiet_link in linkliste:
    print(gebiet_link)
    website = requests.get("https://www.bergfex.ch"+gebiet_link).text
    soup = BeautifulSoup(website, "html.parser")

    # Titel des Skigebiets
    titel = soup.find('h1', {"class": "has-sup"})
    titel = (titel.text.replace("Skigebiet ", ""))
    # Offene Skilifte auslesen
    for skigebiet in soup.find_all('table', class_="schneewerte"):
        offenelifte = (skigebiet.find_all('td')[-1].text).split(" von ") # Auslesen im Format "12 von 24" (offene Lifte sind immer das letzte TD, deshalb -1)
        total = offenelifte[1].strip()
        offen = offenelifte[0].strip()
        now = datetime.datetime.now()
        scraperwiki.sqlite.save(unique_keys=['name'], data={"zeit": now.strftime("%Y-%m-%d_%H-%M"), "titel": titel, "totallifte": total, "offen": offen})
        #skigebiete_final.append({"titel": titel, "totallifte": total, "offen": offen}) # In die finale Liste laden

