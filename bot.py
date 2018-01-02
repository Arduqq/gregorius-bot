#!/usr/env python3

import discord
import asyncio
import datetime
import random
# create config.py with a dictionary of important credentials
import config
import birthday
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

imgurclient_id = config.BOT_CONFIG['imgur_client']
imgurclient_secret = config.BOT_CONFIG['imgur_secret']


imgurclient = ImgurClient(imgurclient_id, imgurclient_secret)
client = discord.Client()

quotes = []

def printRoll(dices):
    text = ""
    for dice in dices:
        if dice > 4:
            text += " **" + str(dice) + "** ";
        elif dice < 2:
            text += " *" + str(dice) + "* "
        else:
            text += " " + str(dice) + " "
    return text

def passedRoll(dices):
    passed = 0
    for dice in dices:
        if dice > 4:
            passed += 1;
    return passed

def failedRoll(dices):
    failed = 0
    for dice in dices:
        if dice < 2:
            failed += 1;
    return failed

def lovecheck(s1, s2):
    a = (len(s1))
    b = (len(s2))
    result = 0
    if a > b:
        a, b = b, a
    s = s1 + s2
    for letter in s:
        result += ord(letter)
    return result % 101

def check_quotes():
    global quotes
    with open('quotes') as f:
        for line in f:
            if '\n' == line[-1]:
                line = line[:-1]
            quotes.append(line)

def save_quotes():
    global quotes
    f = open('quotes','w')
    for item in quotes:
        f.write("%s\n" % item)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='invictus.cool'))
    check_quotes()


@client.event
async def on_message(message):
    if message.content.startswith('!roll'):
        try:
            first = int(message.content.split()[1])
            second = int(message.content.split()[2])
            val = loveCheck(first, second)
            await client.send_message(message.channel, text)
        except IndexError:
            text = '\n'.join(("Ich brauche eine einzige Zahl als Input, Dummkopf.",
                              "`Usage: !roll [Anzahl der geworfenen D6-Würfel]`"))
            await client.send_message(message.channel, text)
    
    # !lovecheck
    # Überprüft, ob zwei Namen sich lieben sollten oder nicht
    elif message.content.startswith('!lovecheck'):
        try:
            laufi = ("Laufi", "Daniel", "Laufamholzer", "laufi", "daniel", "laufamholzer", "holzer", "Holzer")
            princess = message.content.split()[1]
            prince = message.content.split()[2]
            tmp = await client.send_message(message.channel, '**Analysiere Personen auf potenzielle Korpulationschancen:** :black_heart:')
            score = lovecheck(prince,princess)
            await asyncio.sleep(3)
            if prince in laufi or princess in laufi:
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** :poop:')
                await client.send_message(message.channel, 'Niemand mag Laufamholzer. Mach dir nichts vor. :pig:')
            elif score >= 75:
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** :heartpulse:')
                await client.send_message(message.channel, "**" + prince +"** und **" + princess + "** haben zu **" + str(score) + "%** Sexytime.")
            elif score in range(25, 74):
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** :hearts:')
                await client.send_message(message.channel, "**" + prince +"** und **" + princess + "** haben zu **" + str(score) + "%** Sexytime.")
            else:
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** ::broken_heart:')
                await client.send_message(message.channel, "**" + prince +"** und **" + princess + "** haben zu **" + str(score) + "%** Sexytime.")
        except IndexError:
            text = '\n'.join(("Falscher Input, Dumpfbacke",
                              "`Usage: !loveCheck [Person1] [Person2]`"))
            await client.send_message(message.channel, text)
    
    # !meme
    # Postet ein zufälliges Meme aus Imgur
    elif message.content.startswith('!meme'):
        try:
            memes = imgurclient.memes_subgallery(sort='viral', page=0, window='week')
            await client.send_message(message.channel, random.choice(memes).link)
        except ImgurClientError:
            await client.send_message(message.channel, 'Imgur-Client spinnt. :(')
    
    # !shibe
    # Postet ein süßes Bild von einem Shiba Inus
    elif message.content.startswith('!shibe'):
        try:
            shibes = imgurclient.subreddit_gallery('shiba', sort='time', window='week', page=0)
            await client.send_message(message.channel, random.choice(shibes).link)
        except ImgurClientError:
            await client.send_message(message.channel, 'Imgur-Client spinnt. :(')
    
    # !choose
    # Wählt ein Element aus einer Auswahl von Elementen aus
    elif message.content.startswith('!choose'):
        try:
            l = message.content.split()[1:]
            tmp = await client.send_message(message.channel, ':four_leaf_clover: `[%s]`' % ' | '.join(map(str, l)))
            await asyncio.sleep(1)
            while len(l) != 1:
                l.pop(random.randrange(len(l)))
                await client.edit_message(tmp, ':four_leaf_clover: `[%s]`' % ' | '.join(map(str, l)))
                await asyncio.sleep(1)
            await client.edit_message(tmp, ':round_pushpin: **%s** wurde ausgewählt!' % ' | '.join(map(str, l)))
        except IndexError:
            text = '\n'.join(("Liste ist leer oder hier ist gerade die Hölle los",
                              "`Usage: !choose [Auswahlelement]*`"))
            await client.send_message(message.channel, text)
    
    # !coinflip
    # Wirft eine Münze
    elif message.content.startswith('!coinflip'):
        try:
            coin = random.randint(1,2)
            if coin == 1:
                await client.send_file(message.channel, 'heads.png')
            else:
                await client.send_file(message.channel, 'tails.png')
        except IndexError:
            text = '\n'.join(("Etzala a fail",
                              "`Usage: !coinflip`"))
            await client.send_message(message.channel, text)
    
    # !quote
    # Alle möglichen Commands in Bezug auf Zitate
    #     !quote add
    #     Fügt Zitate in eine Textdatei, die jederzeit mit !quote aufgerufen werden
    # 
    #     !quote id
    #     Zitiert eine Nachricht aus dem Channel mithilfe der Message-ID
    elif message.content.startswith('!quote'):
        await client.delete_message(message)
        try:
            global quotes
            if message.content.startswith('!quote add'):
                quote = message.content.split()[2:]
                if quote != []:
                    quotes.append(' '.join(quote))
                    save_quotes()
                    em = discord.Embed(title='Zitat gespeichert!', description=' '.join(quote), colour=0xffff00)
                    em.set_footer(text="!quote add [ZITAT]")
                    await client.send_message(message.channel, embed=em)
                else:
                    text = '\n'.join(("Korregation!",
                              "`Usage: !quote (add [Zitat] | id [ID])`"))

            elif message.content.startswith('!quote id'):
                quote_id = message.content.split()[2]
                if quote_id != None:
                    msg = await client.get_message(message.channel, quote_id)
                    em = discord.Embed(description=msg.content, colour=msg.author.color)
                    nick = msg.author.nick
                    if nick != None:
                        em.set_author(name=msg.author.nick + " (" + msg.author.name + "@" + msg.author.discriminator+ ")", icon_url=msg.author.avatar_url)
                    else:
                        em.set_author(name=msg.author.name + "@" + msg.author.discriminator, icon_url=msg.author.avatar_url)
                    if message.author.nick != None:
                        em.set_footer(text=msg.timestamp.strftime('%d.%m.%Y, %H:%M') + " - zitiert von: " + message.author.nick + " (" + message.author.name + "@" + message.author.discriminator + ")")
                    else:
                        em.set_footer(text=msg.timestamp.strftime('%d.%m.%Y, %H:%M') + " - zitiert von: " + message.author.name + "@" + message.author.discriminator)
                    if msg.attachments:
                        em.set_image(url=msg.attachments[0]["url"])
                    await client.send_message(message.channel, embed=em)
                else:
                    text = '\n'.join(("Korregation!",
                              "`Usage: !quote (add [Zitat]) | id [ID]`"))
            else:
                randquote = random.choice(quotes)
                randquote = randquote.split(' ')
                em = discord.Embed(description=' '.join(randquote[:-1]), colour=0xffff00)
                em.set_author(name=randquote[-1])
                await client.send_message(message.channel, embed=em)
        except IndexError:
            text = '\n'.join(("Korregation!",
                              "`Usage: !quote (add [Zitat] | id [ID])`"))
            await client.send_message(message.channel, text)
    
    # !dab
    # Lösch dich.
    elif message.content.startswith('!dab'):
        await client.send_message(message.channel, "Lösch dich.", tts=True)
    
    # !help
    # Verlinkung zur Website für alle nötigen Informationen
    elif message.content.startswith('!help'):
        await client.send_message(message.channel, "Alle Informationen zu den Bot-Commands findest du auf: http://gregorius.paperplane.io/")
    
    # !basterds
    # Postet Informationen zum kommenden Filmabend
    elif message.content.startswith('!basterds'):
        embed=discord.Embed(title="Victorurious Basterds", description="🎥 Der Filmabend findet jeden **Sonntag** um **20 Uhr** statt. Jeder bringt einen Film mit und wir würfeln einige Minuten vorher aus welchen davon wir uns anschauen werden, suchen einen passenden Stream heraus und lassen den Sonntag in Liebe ausklingen.", color=0xb14e38)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/clubpenguin/images/8/85/Popcorn.png/revision/latest/scale-to-width-down/363?cb=20161030050058")
        embed.add_field(name='Letterboxd-Liste:', value='https://letterboxd.com/arduqq/list/inivctus-classix/', inline=False)
        embed.add_field(name='Film-Spreadsheet:', value='https://goo.gl/DNGB5T', inline=True)
        embed.add_field(name='Trinkspiel-Prioritäten:', value='https://goo.gl/deJhD5', inline=True)
        embed.add_field(name='Cinesift:', value='https://www.cinesift.com/', inline=True)
        embed.add_field(name='Aktuelles Thema:', value='Freie Wahl', inline=True)
        embed.set_footer(text="#Liebe")
        await client.send_message(message.channel, embed=embed)

    elif message.content.startswith('!birthday'):
        if message.content.startswith('!birthday add'):
            await client.delete_message(message)
            name = message.author.name
            day = message.content.split()[2]
            month = message.content.split()[3]
            year = message.content.split()[4]
            birthday.addBirthday(name, day, month, year)
            em = discord.Embed(title='Erfolg!', description='Geburtstag von **' + message.author.name + ' (' + day + '.' + month + '.' + year + ')** hinzugefügt!', colour=0x80f442)
            em.set_thumbnail(url=message.author.avatar_url)
            em.set_footer(text="!birthday add TT MM YYYY")
            await client.send_message(message.channel, embed=em)
        else:
            birthday.initBirthdays()
            embed=discord.Embed(title="Aktuelle Geburtstage", description='```ml\n'+ birthday.createCalendar() +'\n```', color=0x67c7db)
            if 'Arduqq' in birthday.getBirthdays():
                embed.set_thumbnail(url='https://i.imgur.com/8RWMg8f.png')
            embed.add_field(name='🍬 Geburtstagskinder in diesem Monat', value=birthday.getBirthdays(), inline=False)
            await client.send_message(message.channel, embed=embed)

# client.loop.create_task(check_reminders())
client.run(config.BOT_CONFIG['discord_token'])