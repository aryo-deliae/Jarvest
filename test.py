
from pdf2image import convert_from_path
import os
import arvestapi
import json
from PIL import Image
from urllib.request import urlopen
from iiif_prezi3 import Manifest, config

BOITE_IMG = os.path.join(os.getcwd(),'img')

MAIL_ARVEST = "aryodeliae@gmail.com"
PASSWORD_ARVEST = "Arvestmoon1203"


def pdf_to_image(mail, password, folder):

    #Connection a Arveste

    ar = arvestapi.Arvest(mail, password)
    print(ar.profile.name)


    #Nom du fichier
    file = "SS_DUBREUCQ_IVAN_RC.pdf"
    file_name = file.replace('.pdf', '')

    #PDF a utiliser 
    pdf_path = os.path.join(file)
        
    print(pdf_path)

    # Conversion en JPEG
    image = convert_from_path(pdf_path, 72)

    for i, page in enumerate(image):
        img_name = f"{file_name}_page_{i + 1}.jpeg"
        page.save(img_name)
        print(img_name)
        
pdf_to_image(MAIL_ARVEST, PASSWORD_ARVEST, BOITE_IMG)

#red = Image.new("RGB", (200, 200), "#f00")
#red.save("out.jpg", xmp=b"test")