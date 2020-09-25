from pyrogram import Client, filters

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import json


@Client.on_message(filters.command(['emtia'], ['!','.', '/']) & filters.me)
async def emtia(client, message): 

    istek = requests.get("https://www.doviz.com/emtialar")
    corba = BeautifulSoup(istek.content, 'lxml')
    tablo = corba.find('table', id='commodities')

    pandaVeri = pd.read_html(str(tablo))[0]
    # print(pandaVeri)

    jsonVeri = json.loads(pandaVeri.to_json(orient='records'))
    #print(jsonVeri)

    jsonCikti = json.dumps(jsonVeri, indent=2, sort_keys=False, ensure_ascii=False)
    
    mesaj = ""
    
    for say in range(len(jsonVeri)):
        mesaj += f"**Emtia Verileri**\n\n"
        mesaj += f"**{jsonVeri[say]['Emtia']}**\n"
        mesaj += f"**Son :**  `{jsonVeri[say]['Son']}`\n"
        mesaj += f"**En Düşük :**  `{jsonVeri[say]['En Düşük']}`\n"
        mesaj += f"**En Yüksek :**  `{jsonVeri[say]['En Yüksek']}`\n"
        mesaj += f"**Değişim :**  `{jsonVeri[say]['Değişim']}`\n\n"
        
        #mesaj += f"__{bak['Emtia']}__ | `{bak['Son']}` | {bak['En Düşük']}** | {bak['En Yüksek']} | {bak['Değişim']}\n"
    
    await message.edit(mesaj)