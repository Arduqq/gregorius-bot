#!/usr/env python3

import discord
import asyncio
import datetime
import random
import json
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
broken_ribs = {}

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
    print('Fetched all of the quotes')
    global broken_ribs
    with open('broken_ribs.json') as json_data:
        broken_ribs = json.load(json_data)
    print('Opened broken_ribs.json')


@client.event
async def on_message(message):
    if message.content.startswith('!roll'):
        try:
          dices = []
          amount = int(message.content.split()[1])
          for i in range(1, amount):
            dices.append(random.randrange(1,6))
            text = '\n'.join(("**🎲 Wurf:** " + printRoll(dices),
                              "**:white_check_mark: Erfolge:** " + str(passedRoll(dices)),
                              "**:x: Misserfolge:** " + str(failedRoll(dices))))
          await client.send_message(message.channel, text)
        except IndexError:
          text = '\n'.join(("Ich brauche eine einzige Zahl als Input, Dummkopf.",
                            "`Usage: !roll [Anzahl der geworfenen D6-Würfel]`"))
          await client.send_message(message.channel, text)
    
    # !lovecheck
    # Überprüft, ob zwei Namen sich lieben sollten oder nicht
    elif message.content.startswith('!lovecheck'):
        try:
            lao = ("lao", "laomedeia", "laomedeiaTRX", "sonja", "mond", "münchnerin", "alte", "moon")
            dice = ("dice", "nicedice", "nicedice90", "christian", "chris", "chrissy", "kleiner", "würfel")
            laufi = ("Laufi", "Daniel", "Laufamholzer", "laufi", "daniel", "laufamholzer", "holzer", "Holzer")
            princess = message.content.split()[1]
            prince = message.content.split()[2]
            tmp = await client.send_message(message.channel, '**Analysiere Personen auf potenzielle Korpulationschancen:** :black_heart:')
            score = lovecheck(prince,princess)
            await asyncio.sleep(3)
            if prince.upper() == princess.upper():
                await client.send_message(message.channel, '**Liebe dich selbst und es ist egal wen du heiratest!**')
            else if prince in laufi or princess in laufi:
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** :pig:')
                await client.send_message(message.channel, 'Niemand mag Laufamholzer. Mach dir nichts vor.')                
            elif prince in dice + lao and princess in dice + lao:
                await client.edit_message(tmp, '**Keine Analyse nötig:** :heartpulse:')
                await client.send_message(message.channel, '**Heiratet endlich, danke!** *xoxo invictus*')
            elif prince in dice or princess in dice:
                await client.send_message(message.channel, '**Finger weg von meinem Stecher, du miese Snitch** *-Lao*')
            elif prince in lao or princess in lao:
                await client.send_message(message.channel, '**Finger weg von meiner Alten, du miese Snitch** *-Dice*')            
            elif score >= 75:
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** :heartpulse:')
                await client.send_message(message.channel, "**" + prince +"** und **" + princess + "** connecten zu **" + str(score) +"\%**!")
            elif score in range(25, 74):
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** :hearts:')
                await client.send_message(message.channel, "**" + prince +"** und **" + princess + "** connecten zu **" + str(score) +"\%**!")
            else:
                await client.edit_message(tmp, '**Analysiere Personen auf potenzielle Korpulationschancen:** ::broken_heart:')
                await client.send_message(message.channel, "**" + prince +"** und **" + princess + "** connecten zu **" + str(score) +"\%**!")
        except IndexError:
            text = '\n'.join(("Falscher Input, behinderter Spasti",
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

    # !paragon
    # Postet ein Todd Howard Meme aus Imgur
    elif message.content.startswith('!paragon'):
        try:
            paragon = imgurclient.subreddit_gallery('gayfortodd', sort='time', window='week', page=0)
            await client.send_message(message.channel, random.choice(paragon).link)
        except ImgurClientError:
            await client.send_message(message.channel, 'Imgur-Client spinnt. :(')
    
    # !shibe
    # Postet ein süßes Bild von einem Shiba Inu
    elif message.content.startswith('!shibe'):
        try:
            shibes = imgurclient.subreddit_gallery('shiba', sort='time', window='week', page=0)
            await client.send_message(message.channel, random.choice(shibes).link)
        except ImgurClientError:
            await client.send_message(message.channel, 'Imgur-Client spinnt. :(')

    # !puss
    # Postet ein süßes Bild von einem Kätzchen
    elif message.content.startswith('!puss'):
        try:
            cats = imgurclient.subreddit_gallery('cats', sort='time', window='week', page=0)
            await client.send_message(message.channel, random.choice(cats).link)
        except ImgurClientError:
            await client.send_message(message.channel, 'Imgur-Client spinnt. :(')
    # !capybara
    # Postet ein süßs Bild von einem Capybara
    elif message.content.startswith('!capybara'):
        try:
            baras = imgurclient.subreddit_gallery('capybara', sort='time', window='week', page=0)
            await client.send_message(message.channel, random.choice(baras).link)
        except ImgurClientError:
            await client.send_message(message.channel, 'Imgur-Client spinnt. :(')
    # !jews
    # Postet ein Bild von einem russischen Juden
    elif message.content.startswith('!jews'):
        try:
            jews = imgurclient.gallery_tag('ducklings', sort='viral', page=0, window='week')
            await client.send_message(message.channel, random.choice(jews).link)
        except ImgurClientError:
            await client.send_message(message.channel, 'Imgur-Client spinnt. :(')

    # !funnyAirplaneCrash
    # Postet ein Bild von einem lustigen Flugzeugabsturz
    elif message.content.startswith('!funnyairplanecrash'):
        try:
            funnyairplanecrash = imgurclient.subreddit_gallery('funnyairplanecrash', sort='time', window='week', page=0)
            await client.send_message(message.channel, random.choice(funnyairplanecrash).link)
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
    # !punch
    # Befehl zur ungerechten Diskriminierung von Laufi
    elif message.content.startswith('!punch'):
        try:
            feels = ['motiviert','energisch','energiegeladen','gewaltig','voller Elan','etwas','plötzlich','dramatisch','theatralisch']
            actions = ['**{}** haut **{}** eine rein.', 
                       '**{}** schlägt **{}** ins Gesicht.', 
                       '**{}** schlägt zu und tut **{}** ein bisschen weh.',
                       '**{}** konnte an **{}** einige Aggressionen auslassen.',
                       '**{}** haut **{}** kräftig auf die Nase.',
                       '**{}** schlägt **{}**.',
                       '**{}** gibt **{}** einen Schlag in die Magengrube.',
                       '**{}** hat **{}** satt und kann sich nicht mehr zurückhalten.',
                       '**{}** ist ein absoluter Neandertaler und haut **{}** eine rein.',
                       '**{}** MACHEN **{}** AUA!',
                       '**{}** klärt den Disput mit **{}** mithilfe eines Schlags in die Magengrube.']
            punched_member = message.mentions[0]
            laufi = False
            if (punched_member.name == 'Laufamholzer'):
                laufi = True
            await client.send_message(message.channel, '💢 **' + message.author.display_name + '** holt ' + random.choice(feels) + ' aus ...')

            if laufi == False:
                score_punched = random.randint(1,10)
            else:
                score_punched = 1

            score_puncher = random.randint(1,10)
            await asyncio.sleep(3)
            if (score_punched >= score_puncher):
                await client.send_message(message.channel, '💨 Und verfehlt miserabel.')
            else:
                await client.send_message(message.channel, '🥊' + random.choice(actions).format(message.author.display_name,punched_member.display_name))
                power = random.randint(1,1000)
                if (power > 700):
                    await client.send_message(message.channel, '🔨 ***' + punched_member.display_name + '** bricht sich eine Rippe!* Yay!')
                    if punched_member.id not in broken_ribs:
                        broken_ribs[punched_member.id] = 1
                        await client.send_message(message.channel, '🚑 ' + 
                            punched_member.display_name + ' hat nun offiziell die **erste** gebrochene Rippe! <3')

                    else:
                        broken_ribs[punched_member.id] += 1
                        await client.send_message(message.channel, '🚑 ' + punched_member.display_name + ' hat nun offiziell **' + str(broken_ribs[punched_member.id]) + '** gebrochene Rippen!')
                    with open('broken_ribs.json', 'w') as outfile:
                        json.dump(broken_ribs, outfile, ensure_ascii=False)

        except IndexError:
            text = '\n'.join((message.author.display_name + " schlägt in die Luft",
                              "`Usage: !punch @mention"))
            await client.send_message(message.channel, text)

        
    
    # !help
    # Verlinkung zur Website für alle nötigen Informationen
    elif message.content.startswith('!help'):
        await client.send_message(message.channel, "Alle Informationen zu den Bot-Commands findest du auf: http://invictus.cool/gregor")
    
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

    # !birthday (add)
    # Zeigt den Kalender für den entsprechenden Monat mit Geburtstagen
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
        elif message.content.startswith('!birthday'):
            birthday.initBirthdays()
            embed=discord.Embed(title="Aktuelle Geburtstage", description='```ml\n'+ birthday.createCalendar() +'\n```', color=0x67c7db)
            if birthday.getBirthdays():
              embed.add_field(name='🍬 Geburtstagskinder in diesem Monat', value=birthday.getBirthdays(), inline=False)
            else:
              embed.add_field(name='🍬 Geburtstagskinder in diesem Monat', value='Keine Geburtstage in diesem Monat :(', inline=False)
            await client.send_message(message.channel, embed=embed)

    elif message.content.startswith('!sr'):
      members = []
      try:
        with open('pnp') as f:
          lines = f.readlines()
        for line in lines:
          members.append(line)
      except FileNotFoundError:
        print("No pnp file found.")

      members_str = ''.join(members)
      em = discord.Embed(title='[SR5] Leviathan: Flügel', description='**Termin: ???** in #shadowrun', color=0x841d27)
      em.add_field(name='🏃‍ Runner', value=members_str, inline=True)
      em.add_field(name='👑 Spielleiter', value='Arduqq', inline=True)
      em.set_thumbnail(url='https://static.tumblr.com/640b093f45f7b5b330a371b1b5f15930/jdwgqx8/lVKn7ubmn/tumblr_static_c6bful52magc80wsg0g008csw.png')
      em.set_footer(text="!sr")
      await client.send_message(message.channel, embed=em)

    elif message.content.startswith('!movie add'):
      movie = message.content.split()[2]
      em = discord.Embed(title='Film erfolgreich erstellt!', description=movie + ' wurde erfolgreich in die Bewertung eingefügt!', color=0xf4d641)
      em.set_footer(text='Füge deine Bewertung mit !rate ' + movie.replace(' ','').lower() + ' [1-10] hinzu!')
      await client.send_message(message.channel, embed=em)

    elif message.content.startswith('!rate vertigo'):
      movie = message.content.split()[1]
      em = discord.Embed(title='Wertung erfolgreich gespeichert!', description='Die Bewertung für ' + movie + ' wurde aktualisiert.' , color=0xb3f442)
      em.set_author(name=message.author.nick + " (" + message.author.name + "@" + message.author.discriminator+ ")", icon_url=message.author.avatar_url)
      em.set_footer(text='(Irgendwann ist hier ein großartiger Link zur Übersicht)')
      await client.send_message(message.channel, embed=em)


    

# client.loop.create_task(check_reminders())
client.run(config.BOT_CONFIG['discord_token'])
