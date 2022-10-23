import discord
from discord.ext import commands, tasks

from datetime import datetime

import requests

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    #loop_task_test.start()   

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        print(f'chegou aqui!!!')
        await message.channel.send('Hello!')

    await bot.process_commands(message)

@bot.command("xau")
async def bye(ctx):
    await ctx.message.channel.send("ate a próxima")

@bot.command("lancamentos")
async def news(ctx):
    timestamp = str(datetime.now().timestamp()).split('.')[0]

    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    credenciais = {'client_id':'y3gnw6tnbrt0mp93wzefs23o37kwor', 'client_secret': 'nelemtids2479bayisq9056gldnrek', 'grant_type': 'client_credentials' }
    urlToken = 'https://id.twitch.tv/oauth2/token?client_id=y3gnw6tnbrt0mp93wzefs23o37kwor&client_secret=nelemtids2479bayisq9056gldnrek&grant_type=client_credentials'

    res = requests.post(urlToken, credenciais)
    token = res.json()['access_token']

    url_lancamentos = 'https://api.igdb.com/v4/release_dates/'
    headers_igdb_api = {'Client-ID': 'y3gnw6tnbrt0mp93wzefs23o37kwor', 'Authorization' : 'Bearer ' + token, 'content-type' : 'text/plain'}
    body_lancamentos = f'fields game, human; where date > {timestamp}; sort date asc; limit 10;'
    res_lancamentos = requests.post(url_lancamentos, data=body_lancamentos, headers=headers_igdb_api)

    res_lancamento_json = res_lancamentos.json()
    id_games = list(map(lambda x: str(x['game']), res_lancamento_json))

    url_games = 'https://api.igdb.com/v4/games/'
    body_games = 'fields name, first_release_date; where id = (' + ','.join(id_games) + ') ;'
    res_games = requests.post(url_games, headers=headers_igdb_api, data=body_games)

    message = ''
    contador = 0

    for game in res_games.json():
        lancamento_game = list(filter(lambda x : x['game'] == game['id'] ,res_lancamento_json))
        message += f'{reactions[contador]}  -  {game["name"]} - {lancamento_game[0]["human"]}\n'
        contador+=1

    await ctx.message.channel.send(message)

@bot.command("lancamentosplataforma")
async def news(ctx, platform):
    credenciais = {'client_id':'y3gnw6tnbrt0mp93wzefs23o37kwor', 'client_secret': 'nelemtids2479bayisq9056gldnrek', 'grant_type': 'client_credentials' }
    urlToken = 'https://id.twitch.tv/oauth2/token?client_id=y3gnw6tnbrt0mp93wzefs23o37kwor&client_secret=nelemtids2479bayisq9056gldnrek&grant_type=client_credentials'

    res = requests.post(urlToken, credenciais)
    token = res.json()['access_token']

    url_lancamentos = 'https://api.igdb.com/v4/release_dates/'
    headers_igdb_api = {'Client-ID': 'y3gnw6tnbrt0mp93wzefs23o37kwor', 'Authorization' : 'Bearer ' + token, 'content-type' : 'text/plain'}
    body_lancamentos = 'fields game; where date > 1667928683 & platform=' + platform + '; sort date asc; limit 10;'
    res_lancamentos = requests.post(url_lancamentos, data=body_lancamentos, headers=headers_igdb_api)
    res_lancamento_json = res_lancamentos.json()

    if(res_lancamentos.status_code == 200):
        id_games = list(map(lambda x: str(x['game']), res_lancamento_json))
    elif(res_lancamentos.status_code == 400):
        await ctx.message.channel.send("plataforma não existe!")
        return


    url_games = 'https://api.igdb.com/v4/games/'
    body_games = 'fields name,first_release_date; where id = (' + ','.join(id_games) + ') ;'
    res_games = requests.post(url_games, headers=headers_igdb_api, data=body_games)

    message = ''

    for game in res_games.json():
        message += game['name'] + '\n'


    await ctx.message.channel.send(message)


@bot.event
async def on_reaction_add(reaction, user):
    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣","8️⃣","9️⃣","🔟"]
    reactions_map = {"1️⃣":"1", "2️⃣":"2", "3️⃣":"3", "4️⃣":"4", "5️⃣":"5", "6️⃣":"6", "7️⃣":"7", "8️⃣":"8", "9️⃣":"9", "🔟":"10"}
    react_used = list(filter(lambda x: (x == reaction.emoji), reactions))
    posicao = reactions_map[react_used[0]]

    credenciais = {'client_id':'y3gnw6tnbrt0mp93wzefs23o37kwor', 'client_secret': 'nelemtids2479bayisq9056gldnrek', 'grant_type': 'client_credentials' }
    urlToken = 'https://id.twitch.tv/oauth2/token?client_id=y3gnw6tnbrt0mp93wzefs23o37kwor&client_secret=nelemtids2479bayisq9056gldnrek&grant_type=client_credentials'

    res = requests.post(urlToken, credenciais)
    token = res.json()['access_token']
    headers_igdb_api = {'Client-ID': 'y3gnw6tnbrt0mp93wzefs23o37kwor', 'Authorization' : 'Bearer ' + token, 'content-type' : 'text/plain'}

    message_content = reaction.message.content
    nome = message_content.split('\n')[int(posicao) - 1].split('-')[1]

    url_games = 'https://api.igdb.com/v4/games/'
    body_games = f'fields url; where name = "{nome.strip()}";'
    res_games = requests.post(url_games, headers=headers_igdb_api, data=body_games)
    await reaction.message.channel.send(res_games.json()[0]['url'])


# @tasks.loop(seconds=10)
# async def loop_task_test():

#     channel = bot.get_channel(1033528075666866176)

#     await channel.send("teste de task")


bot.run('')