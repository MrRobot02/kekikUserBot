from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import json



@Client.on_message(filters.command(['altin'], ['!','.','/']) & filters.me)
async def altin(client, message):
    await message.edit("altin")
    istek = requests.get("https://altin.doviz.com/")
    cobra = BeautifulSoup(istek.content, "lxml")
    tablo = cobra.find("table", id="golds")

    pandaVeri = pd.read_html(str(tablo))[0].rename(
        columns={
            "Unnamed: 0"    : "Altın Fiyatları",
            "Unnamed: 4"    : "Saat",
        }
    )
    #print(pandaVeri)

    jsonVeri = json.loads(pandaVeri.to_json(orient="records"))
    #print(jsonVeri)

    jsonCikti = json.dumps(jsonVeri, indent=2, sort_keys=False, ensure_ascii=False)
    #print(jsonCikti)
    mesaj = ""
    for say in range(len(jsonVeri)):
        mesaj += f"**{jsonVeri[say]['Altın Fiyatları']}**\n"
        mesaj += f"**Alış :**  `{jsonVeri[say]['Alış']}`\n"
        mesaj += f"**Satış :**  `{jsonVeri[say]['Satış']}`\n"
        mesaj += f"**Değişim :**  `{jsonVeri[say]['Değişim']}`\n"
        mesaj += f"**Saat :**  `{jsonVeri[say]['Saat']}`\n\n"

    await message.edit(mesaj)

    #gorselVeri = tabulate(pandaVeri, headers="keys", tablefmt="psql")
    #await message.edit(f"```{jsonCikti}```")

    #anahtarlar = [anahtar for anahtar in jsonVeri[0].keys()]
    #print(anahtarlar)