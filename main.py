from trello import TrelloApi

import discord
from discord.ext import commands
from discord import app_commands

TRELLO_API_KEY = "KEY"
TRELLO_TOKEN = "TOKEN"
cardPos = "bottom"
trello = TrelloApi(TRELLO_API_KEY, TRELLO_TOKEN)

bot = commands.Bot(command_prefix='idiot ', intents=discord.Intents.default())
loggingChannelID = 1165970854698553364
class ApplicationForm(discord.ui.Modal, title="Application form"):
    name_continent = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What is your username & continent?",
        max_length=50,
        required=True,
        placeholder="Name; Continent"
    )

    activity = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What would be your activity level?",
        max_length=10,
        required=True,
        placeholder="Your activity level, eg. 8/10"
    )

    warship = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What is your best warship?",
        max_length=100,
        required=True,
        placeholder="eg. Iver/DZP/OHP"
    )

    nmi_cash = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="What is your total nmi and cash in DSS3?",
        max_length=20,
        required=True,
        placeholder="eg. 200nmi & 500K cash"
    )

    link = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Please link your roblox profile below",
        required=True,
        placeholder="link to your profile: "
    )

    #timezone = discord.ui.TextInput(
    #    style=discord.TextStyle.short,
    #    label="What is your Timezone?",
    #    max_length=20,
    #    required=True,
    #    placeholder="example: IST, GMT+5, UTC-7 etc."
    #)

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(loggingChannelID)
        embed = discord.Embed(
            title=f'New application submitted by "{interaction.user.name}"',
            description=f"**Username & continent**: {self.name_continent} \n\n"
                        f"**Activity**: {self.activity} \n\n"
                        f"**Best warship**: {self.warship} \n\n"
                        f"**Nautical miles & cash**: {self.nmi_cash} \n\n"
                        f"**link to roblox profile**: {self.link}",
            colour=discord.Colour.random()
        )
        embed.set_thumbnail(url=interaction.user.avatar)

        await channel.send(embed=embed)
        await interaction.response.send_message(f'Thank you for applying {interaction.user.mention}!', ephemeral=True)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="Funny admin abuse")
async def ping(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message("Admin Aboose!!!", ephemeral=True)
    await interaction.channel.send(f"{user.mention} <:trololo:1026909534192681062>")

@bot.tree.command(name="apply", description="Our command to apply to the faction! fill out the form that shows up and wait before you get accepted.")
async def apply(interaction: discord.Interaction):
    form = ApplicationForm()
    verified = interaction.guild.get_role(1026838130101342278)
    try:
        if verified in interaction.user.roles:
            await interaction.response.send_modal(form)
        else:
            await interaction.response.send_message('Please verify yourself first before commissioning.', ephemeral=True)
    except Exception as e:
        print(e)

@bot.tree.command(name="accept_commission", description="used to accept commissioning applications found in commissioning logs")
async def accept_app(interaction: discord.Interaction, user_id: discord.Member, timezone: discord.Role):
    await interaction.response.send_message(f"Sending application result\nGiven role: {timezone}", ephemeral=True)

    app_channel = bot.get_channel(interaction.channel_id)
    await app_channel.send(f'<:WNF:1034607720541716531> | <@{user_id.id}> \n\n'
                               f'✅ ) **Your application has been approved.** Please read <#1027083382468902952>, <#1026852760840306768> & <#1026906637547622491> for more information about our faction and some of our guides.')

    await user_id.edit(nick=f"O-1 | {user_id.nick}")

    await user_id.remove_roles(interaction.guild.get_role(1057886765488296016), reason='Passed commissioning')
    await user_id.add_roles(interaction.guild.get_role(1026849103113629817), reason='Passed commissioning')
    await user_id.add_roles(interaction.guild.get_role(1026852084785614969), reason='Passed commissioning')
    await user_id.add_roles(interaction.guild.get_role(timezone.id), reason='Passed commissioning')

@bot.tree.command(name="register_ship", description="command to register ships on our trello/database, once registered your ship will go into a sorting list before getting qadded to the rest of the trello")
async def register_ship(interaction: discord.Interaction, owner: str, ship_name: str, ship_type: str, skin: str, image_link: str):
    try:
        embed = discord.Embed(
            title=ship_name,
            description=f"Owner: {owner}\nShip: {ship_type}\nSkin(s): {skin}",
            colour=discord.Colour.random()
        ).set_author(name=interaction.user, icon_url=interaction.user.avatar).set_image(url=image_link)
        newCard = trello.cards.new(name=ship_name,
                                   idList='65366720c6a01027e66f3761',
                                   desc=f"Owner: {owner}\nShip: {ship_type}\nSkin(s): {skin}",
                                   pos=cardPos)
        trello.cards.new_attachment(card_id_or_shortlink=newCard['id'],
                                    url=image_link)

        await interaction.response.send_message("Trello successfully updated.", ephemeral=True)
        await interaction.guild.get_channel(1165994826286772255).send(embed=embed)
    except Exception as error:
        await interaction.response.send_message("Error occurred, please try again.", ephemeral=True)
        await interaction.guild.get_channel(1060345512970166364).send(error)
        print(error)

@bot.tree.command(name="announce", description="announce something to a specific channel in the server")
async def announce(interaction: discord.Interaction, message: str, channel: discord.TextChannel, ping: bool):
    try:
        if ping:
            await interaction.response.send_message('Successfully announced your message to the server', ephemeral=True)
            await channel.send(f"{message}\n\n<@&1026838130101342278>")
        else:
            await interaction.response.send_message('Successfully announced your message to the server', ephemeral=True)
            await channel.send(message)
    except:
        await interaction.response.send_message("Error occurred, please try again.", ephemeral=True)
        await interaction.guild.get_channel(1060345512970166364).send(error)
        print(error)

bot.run('TOKEN')
