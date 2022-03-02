import shutil
import instaloader
import glob
import pytesseract
import os
import pandas as pd
from itertools import dropwhile, takewhile
from datetime import datetime, timedelta
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'

N_DAYS_AGO = 7
SINCE = datetime.now()
UNTIL = SINCE - timedelta(days=N_DAYS_AGO)
PROFILE = 'kutyakukkendare'
WORDS = ['kutyanév', 'kutyaneév']
LINES = []

ig = instaloader.Instaloader()
posts = instaloader.Profile.from_username(ig.context, PROFILE).get_posts()

def torol(): ## kitörli az egy hétnél régebbi fájlokat
    mydir = './kutyakukkendare'
    files = pd.Series(os.listdir(mydir))
    old_file = (datetime.utcnow() - timedelta(days=N_DAYS_AGO)).strftime('%Y-%m-%d %H:%M:%S')

    for d in pd.date_range('2022-02-01 10:00:00', str(old_file), freq='T').strftime('%Y-%m-%d%H-%M'):
        for file_name in files:
            if file_name.startswith(d):
                os.remove(os.path.join(mydir, file_name))

def heti_scrape(): ## lescrapeli az oldal elmúlt heti posztjait
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
        ig.download_post(post, PROFILE)

def keres(): ## kikeresi a megfelelő képet a kutyanévvel + a leírását

    images = glob.glob('./kutyakukkendare/*.webp')
    for image in images:
        with open(image, "rb") as file:
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
            res = any(ele in text for ele in WORDS)
            if res:
                new = './aktualis_kutya.jpg'
                new_txt = './leiras.txt'
                old = file.name
                old_txt = (os.path.splitext(file.name)[0] + ".txt")
                shutil.copy(old, new)
                shutil.copy(old_txt, new_txt)
        img.close()
    print(new)

def formaz(): #leírás formázása
    with open('./leiras.txt', "r") as f:
        lines = f.readlines()

    with open('./leiras.txt', "w") as f:
        lines = f.writelines(lines[:1])

#torol()
#heti_scrape()
#keres()
















