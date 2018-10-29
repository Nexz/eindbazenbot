#!/usr/bin/python3
import discord
import aiohttp
import json
import requests
import giphypop
import random
import shutil
import configparser
from discord.ext.commands import Bot

config = configparser.ConfigParser()
config.read("eindbazen.ini")

TOKEN = config['Tokens']['discord']
GIFTOKEN = config['Tokens']['gif']
VERSION = "0.0.2"

client = Bot(command_prefix="!")
gapi = giphypop.Giphy(GIFTOKEN)

def removeCommand(messageContent):
    retMsg = messageContent.split(' ', 1)
    if len(retMsg) > 1:
        return retMsg[1]
    else:
        return ''

@client.event
async def on_message(message):
        
    if message.content.startswith('!'): 
        print(message.author.name+" requested:\n"+message.content)

    if message.content.startswith('kut bot'):
        await client.send_message(message.channel, "Je bent zelf een kutbot "+message.author.name)

    if "dan weet u dat" in message.content:
        with open('./gifjes/dan-weet-u-dat.png', 'rb') as picture:
             await client.send_file(message.channel, picture)

    if message.author == client.user:
        return

    if message.content.startswith('!koopdan'):
        msg = 'WANNEER GA JE KOPEN '+removeCommand(message.content)+'?'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!partyhard'):
        with open('./gifjes/party.gif', 'rb') as picture:
             await client.send_file(message.channel, picture)

    if message.content.startswith('!bitcoin'):
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            currentUSD = response['bpi']['USD']['rate'].replace(".", "|").replace(",", ".").replace("|", ",")
            await client.send_message(message.channel, "1 BTC gaat momenteel voor $" + currentUSD)

    if message.content.startswith('!bittrexusd'):
        market = removeCommand(message.content).upper()
        if 'BTC' not in market:
            await client.send_message(message.channel, "Market status opvragen in het volgende format: !bittrex BTC-<coin>")
        else:
            url = 'https://bittrex.com/api/v1.1/public/getticker?market='+market
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(url)
                response = await raw_response.text()
                response = json.loads(response)
                if (response['success'] == True):
                    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
                    async with aiohttp.ClientSession() as session:  # Async HTTP request
                        rawr_response = await session.get(url)
                        responsea = await rawr_response.text()
                        responsea = json.loads(responsea)
                        currentUSD = float(responsea['bpi']['USD']['rate'].replace(",", ""))

                        resultBid = str(response['result']['Bid'] * currentUSD).replace(".", "|").replace(",", ".").replace("|", ",")
                        resultAsk = str(response['result']['Ask'] * currentUSD).replace(".", "|").replace(",", ".").replace("|", ",")
                        resultLast = str(response['result']['Last'] * currentUSD).replace(".", "|").replace(",", ".").replace("|", ",")
                        resultReturn = "Momenteel $"+resultBid+" bid, $"+resultAsk+" ask en $"+resultLast + " last."
                        await client.send_message(message.channel, resultReturn)
                else:
                    await client.send_message(message.channel, "Ongeldige market")

    if message.content.startswith('!bittrex '):
        market = removeCommand(message.content).upper()
        if 'BTC' not in market:
            await client.send_message(message.channel, "Market status opvragen in het volgende format: !bittrex BTC-<coin>")
        else:
            url = 'https://bittrex.com/api/v1.1/public/getticker?market='+market
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(url)
                response = await raw_response.text()
                response = json.loads(response)
                if (response['success'] == True):
                    resultBid = str(response['result']['Bid']).replace(".", "|").replace(",", ".").replace("|", ",")
                    resultAsk = str(response['result']['Ask']).replace(".", "|").replace(",", ".").replace("|", ",")
                    resultLast = str(response['result']['Last']).replace(".", "|").replace(",", ".").replace("|", ",")
                    resultReturn = "Momenteel BTC"+resultBid+" bid, BTC"+resultAsk+" ask en BTC"+resultLast + " last."
                    await client.send_message(message.channel, resultReturn)
                else:
                    await client.send_message(message.channel, "Ongeldige market")

    if message.content.startswith('!mogge'):
        msg = 'Mogge {0.author.mention}, hoe ist nou?'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!versie'):
        await client.send_message(message.channel, "EindbazenBot v"+VERSION+" rev 1337")

    if message.content.startswith('!gifje'):
        zoekGifje = removeCommand(message.content)
        foundGif = gapi.search_list('', zoekGifje)
        if len(foundGif) < 10:
            randPos = random.randint(0, len(foundGif))
        else:
            randPos = random.randint(0, 10)
        rgif = requests.get(foundGif[randPos].media_url, stream=True)
        if rgif.status_code == 200:
            with open('./gifjes/temp.gif', 'wb') as f:
                rgif.raw.decode_content = True
                shutil.copyfileobj(rgif.raw, f)
            with open('./gifjes/temp.gif', 'rb') as picture:
                await client.send_file(message.channel, picture)
        else:
            await client.send_message(message.channel, "Geen GIFje gevonden :-(")

    if message.content.startswith('!belike'):
        poppetje = removeCommand(message.content).replace(' ', '%20')
        if poppetje == '':
            await client.send_message(message.channel, "Wel een naampje opgeven neh.")   
        else:
            url = 'https://belikebill.ga/billgen-API.php?default=1&name='+poppetje+'&sex=m'
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                async with session.get(url) as resp:
                    if resp.status == 200:
                        with open('./gifjes/temp.jpg', 'wb') as f:
                            f.write(await resp.read())
                        with open('./gifjes/temp.jpg', 'rb') as picture:
                            await client.send_file(message.channel, picture)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
