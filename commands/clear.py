from utilities.dependencies import *

@tree.command(
    name="clear",
    description="clears the current queue",
    guild=discord.Object(id=1101666836690505819),
)
async def comm_clear(interaction: discord.Interaction):
    global guild_data

    caller: discord.Member              = interaction.user
    guild: discord.Guild                = interaction.guild

    if not guild.id in guild_data.keys():
        guild_data[guild.id]            = GuildData(client)

    data: GuildData                     = guild_data[guild.id]

    await interaction.response.defer(thinking=True)
    await interaction.followup.send(content=data.audio_queue.clear_queue())