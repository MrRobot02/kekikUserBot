from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from tabulate import tabulate


@Client.on_message(filters.command(['doviz'], ['!','.','/']) & filters.me)
async def doviz(client, message):
    await message.edit("doviz")
    istek = requests.get("https://finans.haberler.com/doviz/")
    cobra = BeautifulSoup(istek.content, "html.parser")
    tablo = cobra.find("table", attrs={"width":"100%"})

    pandasVeri = pd.read_html(str(tablo))[0].drop(
        columns = {
            "Yön"
        }
    )
    #print(pandasVeri)

    jsonVeri = json.loads(pandasVeri.to_json(orient="records"))
    #print(jsonVeri)

    jsonCikti = json.dumps(jsonVeri, indent=2, sort_keys=False, ensure_ascii=False)
    #print(jsonCikti)

    gorselVeri = tabulate(pandasVeri, headers="keys", tablefmt="pretty")
    #print(gorselVeri)

    mesaj = ""

    for say in range(len(jsonVeri)):
        mesaj += f"**{jsonVeri[say]['Para Birimi']}**\n"
        mesaj += f"**Alış:** {jsonVeri[say]['Alış']}\n"
        mesaj += f"**Satış:** {jsonVeri[say]['Satış']}\n"
        mesaj += f"**% Fark:** {jsonVeri[say]['% Fark']}\n"
        mesaj += f"**Saat:** {jsonVeri[say]['Saat']}\n\n"

    await message.edit(mesaj)
#print(mesaj)