from pyrogram import Client, filters
import asyncio


@Client.on_message(filters.command(['komut'], ['!','.', '/']) & filters.me)
async def komut(client, message): 
    await message.edit("Selamün Aleyküm Cümleten Gardaş.")