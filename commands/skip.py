from utilities.dependencies import *

@tree.command(
    name="skip",
    description="skips current song",
    guild=discord.Object(id=1101666836690505819),
)
async def comm_skip(interaction: discord.Interaction):
    global guild_data

    caller: discord.Member              = interaction.user
    guild: discord.Guild                = interaction.guild

    if not guild.id in guild_data.keys():
        guild_data[guild.id]            = GuildData(client)

    data: GuildData                     = guild_data[guild.id]

    await interaction.response.defer(thinking=True)

    response = (await data.audio_queue.skip())
    if response:
        await interaction.followup.send(content=response)
    else:
        await interaction.followup.send(content='skipped')
