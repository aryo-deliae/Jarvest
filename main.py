import discord
from discord.ext import commands
from commandes import upload_image, medias_pdf_to_manifest
import time
import arvestapi
from commandes import upload_image, medias_pdf_to_manifest
from pdf2image import convert_from_path
import os
from dotenv import load_dotenv

load_dotenv()
key_bot = os.getenv('BOT_KEY')

mail = os.getenv('MAIL')
password = os.getenv('PASS')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
racine = (os.getcwd())




#UPLOADER UNE IMAGE SUR ARVEST

@bot.tree.command()
async def image(interaction: discord.Interaction):

    await interaction.response.defer()
    time.sleep(10)

    @bot.event
    async def on_message(message):

           lien_brut = str(message.attachments)
           upload_image(mail, password, lien_brut)
           await message.channel.send("image uploaded !")

    await interaction.followup.send("time out")



#CONVERTIR UN PDF EN MANIFEST

@bot.tree.command()
async def pdf(interaction: discord.Interaction):

    #Mise en attente du bot le temps de l'envoi du pdf
    await interaction.response.defer()
    time.sleep(10)

    # Upload et conversion du pdf envoyé
    @bot.event
    async def on_message(message):
        ar = arvestapi.Arvest(mail, password)

        #Recuperation de la piece jointe 

        fichier = message.attachments
        chemin = os.path.join(racine,"img")

        for attachment in fichier :
            await attachment.save(attachment.filename)
            name = attachment.filename

        file_name = name.replace('.pdf', '')
        chemin = os.path.join(racine,name)

        # Conversion en JPEG
        image = convert_from_path(chemin, 72)
        os.remove(chemin)

        #Upload des medias sur Arvest
        num_page = 0

        for i, page in enumerate(image):
            img_name = f"{file_name}_page_{i + 1}.jpeg"
            output_path = os.path.join("file", img_name)
            page.save(output_path, 'JPEG')
            added_media = ar.add_media(path = output_path)
            os.remove(output_path)
            num_page += 1

        await message.channel.send(f"upload the pdf as {num_page} medias")
        
        #Creation et upload du manifest
        medias = ar.get_medias()
        nom_manifest = file_name
        medias_pdf_to_manifest(medias, nom_manifest, racine, ar)

        await message.channel.send("le pdf est devenu un manifest !")

    await interaction.followup.send("time out")

#Syncronisation des commandes de bot 

@bot.event
async def on_ready():
   print(f"Connecté en tant que {bot.user}")
   sync = await bot.tree.sync()
   print(f"{len(sync)} commandes syncronisées")    


if __name__ == '__main__':
    bot.run(token=key_bot)
