import json                                     # Used for storing individual user data
import discord                                  # Needed by discord.py
import asyncio                                  # Needed by discord.py
import AutoLibrary                              # Some of the nastier functions got moved here to keep the main file cleaner
from random import randint                      # Needed by the bot, used to play games of chance
from pathlib import Path                        # Used for error checking
from discord.voice_client import VoiceClient    # Needed by the bot, used only for audio playback

class TestClient(discord.Client):           
    async def on_ready(self):                           # This SHOULD be used to set up the bot, right now it just alerts you when the bot has finished booting
        pathToPet = Path('TextFiles/Pet.txt')
        if pathToPet.is_file():
            pass 
        else:
            petCountFile = open('TextFiles/Pet.txt', 'w+')
            petCountFile.write('0')
            petCountFile.close
            print ('works')

        pathToUserPetCount = Path ('TextFiles/PetCounter.json')
        if pathToUserPetCount.is_file():
            pass 
        else:
            pathToUserPetCount = open('TextFiles/PetCounter.json', 'w+')
            userPetCount = {"!Total": 0}
            jsonUserPetCount = json.dumps(userPetCount)
            pathToUserPetCount.write(jsonUserPetCount)
            pathToUserPetCount.close
           

        print('Logged in as user : ' + self.user.name)  
        print('with ID : ' + self.user.id)
        print('--------------------------------')

    async def on_message(self, message):                # Nasty uber function, it just reads a send message, matches the beginning of the message to a string and runs a corresponding function
        DiscMessage = message.content.casefold()        # This ensures case insensativity

        if message.author == self.user:                 # This just ensures that the bot doesnt get stuck in a feedback loop and reply to himself endlessly
            return
            
        if DiscMessage.startswith('Auto coin'):          # Flips a coin and replies with heads or tails
            print ('Flipping coin in server: ' + message.server.name)
            if randint(0,1):
                await client.send_message(discord.Object(id=message.channel.id), 'Heads')
            else:
                 await client.send_message(discord.Object(id=message.channel.id), 'Tails')
        
        if DiscMessage.startswith('Auto calc'):          # Allows for running native python code and having the bot execute it
            MathsToDo = DiscMessage.lstrip ('Auto calc')
            try:
                x = (eval (MathsToDo))                  
                await client.send_message(discord.Object(id=message.channel.id), x)
                print ('Calculating In channel :' + message.server.name)
            except Exception as errorInfo:
                await client.send_message(discord.Object(id=message.channel.id), 'Unable to process command')
                print ('Calculation error in channel : ' + message.server.name + str(errorInfo))
        
        if DiscMessage.startswith('Auto lookup'):        # Scrapes the runescape highscores, if no skill is specified just returns unformated data
            RsLookup = DiscMessage.replace('Auto lookup ', '')
            if len(RsLookup.split()) == 2:
                RsLookup = RsLookup.rsplit(' ', 1)
                RsLookupResults = AutoLibrary.runescapeLookup(RsLookup[0], RsLookup[1])
                if len(RsLookupResults) == 3:
                    if RsLookupResults[0] != '--':
                        await client.send_message(discord.Object(id=message.channel.id), RsLookup[0] + ' has a ' + RsLookup[1] + ' level of ' + RsLookupResults[2] + ', with ' + RsLookupResults[1] + ' xp, making him rank ' + RsLookupResults [0] )
                        print ('Looking up : ' + RsLookup[1] + 'for player :' + RsLookup[0] + 'in server :' + message.server.name)
            else:
                RsLookupResults = AutoLibrary.runescapeLookup(RsLookup, 0)
                await client.send_message(discord.Object(id=message.channel.id), RsLookup + str(RsLookupResults))
                print('looking up all stats for player : ' + RsLookup + 'in server : ' + message.server.name )

        if DiscMessage.startswith('Auto wiki'):          # Scrapes the runescape wiki search function and returns the top article, could be moddified to work with any wikia website
            WikiLookupTag = DiscMessage.replace('Auto wiki', '')
            RSWikiLookup = AutoLibrary.rsWikiLookup(WikiLookupTag)
            await client.send_message(discord.Object(id=message.channel.id), RSWikiLookup)
            print ('looking up article' + WikiLookupTag + 'in server : ' + message.server.name)
        
        if DiscMessage.startswith('Auto communism'):     # Nasty hacky audio player, currently just playes the soviet national anthem, 
            global AutoCffmpeg                           # Voice is handled by a voice object, the globals are "needed" so that other functions can work with the same voice object
            global AutoVoiceClient                       # There's definatly a nicer way to handle this, i'll get around to it eventualy
            if (AutoVoiceClient == 0):
                try:          
                    AutoVoiceClient = await client.join_voice_channel(message.author.voice.voice_channel)
                except discord.errors.InvalidArgument:
                    await client.send_message(discord.Object(id=message.channel.id), 'Error : User not in voice channel')

                else:
                    AutoCffmpeg = AutoVoiceClient.create_ffmpeg_player('Audio/Communism/Communism.mp3')
                    AutoCffmpeg.start()
                    print('Starting voice')

            else:
                try:
                    await AutoVoiceClient.move_to(message.author.voice.voice_channel)
                except discord.errors.InvalidArgument:
                    await client.send_message(discord.Object(id=message.channel.id), 'Error : User not in voice channel')
                else:
                    AutoCffmpeg.stop()
                    AutoCffmpeg = AutoVoiceClient.create_ffmpeg_player('Audio/Communism/Communism.mp3')
                    AutoCffmpeg.start()
                    print('Starting voice')
                
        if DiscMessage.startswith('Auto stop'):          # Stops the audio player, uses a nasty global for this
            AutoCffmpeg.stop()
            print ('Stopping voice')
            
        if DiscMessage.startswith('Auto yoink'):         # Grabs a random player from the message author's channel and throws him into the afk channel
            channelToYoinkFrom = message.author.voice.voice_channel.voice_members
            playerToYoink = channelToYoinkFrom [ randint(0,(len(channelToYoinkFrom)-1)) ]
            print (playerToYoink)
            await client.move_member(playerToYoink, message.server.afk_channel)

        if DiscMessage.startswith('Auto help'):          # Reads from a help file in the TextFiles directory
            helpFile = open('TextFiles/Help.txt','r') 
            helpLine = helpFile.read()
            await client.send_message(discord.Object(id=message.channel.id), helpLine)
            helpFile.close
      
        if DiscMessage.startswith('Auto pet'):
            petUser = message.author.name
            petCountPerUser = open('TextFiles/PetCounter.json', 'r')
            bankOfPets = json.load(petCountPerUser)
            petCountPerUser.close

            if petUser in bankOfPets:
                pathToUserPetCount = open('TextFiles/PetCounter.json', 'w+')
                bankOfPets[petUser] = (bankOfPets[petUser] + 1)
                bankOfPets['!Total'] = (bankOfPets['!Total'] + 1)
                json.dump(bankOfPets , pathToUserPetCount)
                pathToUserPetCount.close
                await client.send_message(discord.Object(id=message.channel.id), '<:Hypers:443914491294515200> Auto bot has been petted ' + str(bankOfPets['!Total']) + ' times <:Hypers:443914491294515200> \n <:Hypers:443914491294515200> You have ' + str(bankOfPets[petUser]) + ' pets in the bank of Auto <:Hypers:443914491294515200>' )

            else:
                pathToUserPetCount = open('TextFiles/PetCounter.json', 'w+')
                bankOfPets[petUser] = 1
                print (bankOfPets)
                json.dump(bankOfPets, pathToUserPetCount)
                pathToUserPetCount.close
                await client.send_message(discord.Object(id=message.channel.id), '<:Hypers:443914491294515200> Auto bot has been petted ' + str(bankOfPets['!Total']) + ' times <:Hypers:443914491294515200> \n <:Hypers:443914491294515200> You have ' + str(bankOfPets[petUser]) + ' pets in the bank of Auto <:Hypers:443914491294515200>' )

            
            
AutoCffmpeg = 0 #These global's are "needed" to get the voice functions working properly, They cause so many horrible errors, but i just pretend their not there
AutoVoiceClient = 0
discordTokenFile = open('TextFiles/Token.txt', 'r')
discordToken = discordTokenFile.read()

client = TestClient()
discord.opus.load_opus('opus')
client.run(discordToken)