import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging
from api.howlongtobeat import HowLongToBeatAPI

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
GUILD_ID2 = os.getenv('GUILD_ID2')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.d ', intents=intents)

hltb_api = HowLongToBeatAPI()

# on ready command
@bot.event
async def on_ready():
    print('The bot is ready!')
    print(f"Commands in tree: {[cmd.name for cmd in bot.tree.get_commands()]}")
    
@bot.command(description="Sync slash commands with Discord")
async def sync(ctx) -> None:
        try:
            fmt = await bot.tree.sync()
            await ctx.send(f"Synced {len(fmt)} commands.")
        except Exception as e:
            print(e)


#hell command
@bot.hybrid_command(description="Say hello and introduce the bot")
async def hello(ctx):
    await ctx.send("Wasup! It's me Daoud!")

#godrick incident
@bot.hybrid_command(description="Tell the legendary tale of the Godrick Incident")
async def godrick_incident(ctx):
    await ctx.send("Ah. The Godrick Incident. I spent so many nights staying up fighting him. It took me a long time. A part of my soul. A part of my essence. And in the end, the only one who prevailed was me. The most time it ever took me to fight a beast. I will never forget you Godrick, for as long as I live.")

# always watching command
@bot.hybrid_command(description="I am always watching you.")
async def iamwatching(ctx):
    async for message in ctx.channel.history(limit=10):
        if message.author == ctx.author and message.id != ctx.message.id:
            await ctx.send(f'I am watching you. You just said "{message.content}"')
            return

    await ctx.send("I couldn't find any previous messages from you!")

# game data
@bot.hybrid_command(description="Get completion times and info for any video game")
async def howlongtobeat(ctx, *, game_name: str):    
    thinking_embed = discord.Embed(
        title="Searching...",
        description=f"Looking up completion times for **{game_name}**",
        color=0x3498db
    )
    message = await ctx.send(embed=thinking_embed)
    
    try:
        game_data = await hltb_api.search_and_get_first(game_name)
        
        if not game_data:
            error_embed = discord.Embed(
                title="Game Not Found",
                description=f"Sorry, I couldn't find any results for **{game_name}**.\n\nTry checking the spelling or using a different search term.",
                color=0xe74c3c
            )
            await message.edit(embed=error_embed)
            return
        
        embed = discord.Embed(
            title=f"🎮 {game_data['name']}",
            url=f"https://howlongtobeat.com/game/{game_data['id']}",
            color=0x2ecc71
        )
        
        if game_data.get('image_url'):
            embed.set_thumbnail(url=game_data['image_url'])
        
        if game_data.get('summary'):
            summary = game_data['summary']
            if len(summary) > 1000:
                summary = summary[:997] + "..."
            embed.add_field(name="Description", value=summary, inline=False)
        
        times = game_data.get('times', {})
        time_text = ""
        
        if times.get('main_story', 0) > 0:
            time_text += f"**Main Story:** {times['main_story']} hours\n"
        
        if times.get('main_plus_extras', 0) > 0:
            time_text += f"**Main + Extras:** {times['main_plus_extras']} hours\n"
        
        if times.get('completionist', 0) > 0:
            time_text += f"**Completionist:** {times['completionist']} hours\n"
        
        if times.get('all_styles', 0) > 0:
            time_text += f"**All PlayStyles:** {times['all_styles']} hours\n"
        
        if time_text:
            embed.add_field(name="Completion Times", value=time_text, inline=False)
        else:
            embed.add_field(name="Completion Times", value="No timing data available", inline=False)
        
        details_left = ""
        details_right = ""
        
        if game_data.get('developer'):
            details_left += f"**Developer:** {game_data['developer']}\n"
        
        if game_data.get('publisher'):
            details_left += f"**Publisher:** {game_data['publisher']}\n"
        
        if game_data.get('release_date'):
            details_right += f"**Released:** {game_data['release_date']}\n"
        
        if game_data.get('genre'):
            details_right += f"**Genre:** {game_data['genre']}\n"
        
        if details_left:
            embed.add_field(name="Studio Info", value=details_left, inline=True)
        
        if details_right:
            embed.add_field(name="Game Info", value=details_right, inline=True)
        
        if game_data.get('platforms'):
            platforms = game_data['platforms']
            if len(platforms) > 100:  
                platforms = platforms[:97] + "..."
            embed.add_field(name="🖥️ Platforms", value=platforms, inline=False)
        
        if game_data.get('review_score'):
            score = game_data['review_score']
            if score > 0:
                stars = "⭐" * min(5, int(score / 20)) 
                embed.add_field(name="🏆 User Score", value=f"{score}/100 {stars}", inline=True)
        
        embed.set_footer(
            text="Data from HowLongToBeat.com • Times are community averages",
            icon_url="https://howlongtobeat.com/img/hltb_brand.png"
        )
        
        await message.edit(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="Error",
            description=f"Something went wrong while fetching data for **{game_name}**.\n\nError: `{str(e)}`",
            color=0xf39c12
        )
        await message.edit(embed=error_embed)
        print(f"HowLongToBeat command error: {e}")

# info
@bot.hybrid_command(description="Display all available commands and their descriptions")
async def info(ctx):
    embed = discord.Embed(
        title="Game Bot - Available Commands",
        description="Here are all the commands you can use with this bot:",
        color=0x9b59b6,
        timestamp=ctx.message.created_at
    )
    
    embed.set_author(name="Daoud Bot", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    
    commands_info = [
        ("`.d hello`", "Say hello and introduce the bot"),
        ("`.d info`", "Display this help message"),
        ("`.d howlongtobeat [game name]`", "Get completion times and info for any video game"),
        ("`.d godrick_incident`", "Tell the legendary tale of the Godrick Incident"),
        ("`.d iamwatching`", "Shows your most recent message (I'm watching you!)"),
    ]
    
    for command, description in commands_info:
        embed.add_field(
            name=command,
            value=description,
            inline=False
        )
    
    embed.add_field(
        name="Usage Notes",
        value="• Commands can be used as slash commands (/) or with prefix `.d`\n• For `howlongtobeat`, just type the game name after the command\n• All commands work in any channel where the bot has permissions",
        inline=False
    )

    embed.set_footer(
        text=f"Requested by {ctx.author.display_name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )

    await ctx.send(embed=embed)

# edit fun
@bot.event
async def on_message_edit(before, after):
    if after.author.bot:
        return
    await after.channel.send("ayyyy you just changed your message i love one piece but dont do that okay?")

bot.run(DISCORD_TOKEN)