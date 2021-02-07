import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix="prefix", case_insensitive=True) #change the prefix to whatever you want


check, online =False, False
servers = {1 : {'author': 1, 'channel': 1, 'waiting?': False, 'channel_2': 1}} #DO NOT remove the '1 : {'author': 1, 'channel': 1, 'waiting?': False, 'channel_2': 1}' as doing so will make the code not functional

@client.event
async def on_message(message):
    global servers, check 
    if (message.author.bot):
        pass
    else:
      if (check):
        servers[str(message.guild.id)]["waiting?"] = False

        rules = [
            message.author.id == servers[str(message.guild.id)]["author"],
            message.channel.id == servers[str(message.guild.id)]["channel"]
        ]

        if all(rules):
            msg = message.content.lower()
            if msg == f"{client.command_prefix}disconnect":
                channel = client.get_channel(servers[str(message.guild.id)]['channel_2'])
                for i in list(servers):
                    if servers[str(message.guild.id)]["channel"] == servers[i]["channel_2"]:
                        break
                servers.pop(i)
                servers.pop(str(message.guild.id))
                await message.channel.send("You have disconnected!")
                await channel.send(f"**`{message.author}`**` has disconnected with your server`")
                check=False
            else:
              channel = client.get_channel(servers[str(message.guild.id)]['channel_2'])
              await channel.send(f"**{message.author}**: {message.content}")


    await client.process_commands(message)

#use the command if something went wrong with the dict
@client.command()
async def clear(ctx):
    global servers
    servers = {1 : {'author': 1, 'channel': 1, 'waiting?': False, 'channel_2': 1}}

@client.command()
async def call(ctx):
    global check, servers
    await ctx.send("---- Calling someone ----")
    servers.update({str(ctx.guild.id) : {"author" : ctx.author.id, "channel" : int(ctx.channel.id), "waiting?" : True, "channel_2" : None}})
    t_c = 0
    while t_c <= 10:
        for i in list(servers):
            if i == str(ctx.guild.id):
                pass
            else:
              if servers[i]["waiting?"] == True and servers[str(ctx.guild.id)]["waiting?"] == True:
                servers.update({str(ctx.guild.id) : {"author" : ctx.author.id, "channel" : int(ctx.channel.id), "waiting?" : True, "channel_2" : int(servers[i]['channel'])}})
                member = client.get_user(servers[i]['author'])
                guild = client.get_guild(int(i))
                await ctx.send(f"**{member}** from **{guild.name}** has been reached!")
                check=True
                t_c=10002345839027534895
              else:
                await asyncio.sleep(1)
                t_c += 1
    if t_c == 11:
        await ctx.send("We couldn't find anyone to connect with your server")

client.run("TOKEN") #replace this with your token
