from utilities.dependencies import *

@tree.command(
    name="leave",
    description="stops playback, clears queue and leaves the voice channel",
    guild=discord.Object(id=1101666836690505819),
)
async def comm_leave(interaction: discord.Interaction):
    global guild_data

    caller: discord.Member              = interaction.user
    guild: discord.Guild                = interaction.guild

    if not guild.id in guild_data.keys():
        guild_data[guild.id]            = GuildData(client)

    data: GuildData                     = guild_data[guild.id]

    await interaction.response.defer(thinking=True)

    response = (await data.audio_queue.leave())
    if response:
        await interaction.followup.send(content=response)
    else:
        await interaction.followup.send(content='left')