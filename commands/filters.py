from utilities.dependencies import *

@tree.command(
    name="filters",
    description="modifies the audio filters",
    guild=discord.Object(id=1101666836690505819),
)
async def comm_filters(interaction: discord.Interaction, pitch: float = None, tempo: float = None, bass: int = None):
    global guild_data

    caller: discord.Member              = interaction.user
    guild: discord.Guild                = interaction.guild

    if not guild.id in guild_data.keys():
        guild_data[guild.id]            = GuildData(client)

    data: GuildData                     = guild_data[guild.id]

    await interaction.response.defer(thinking=True)
    
    data.audio_queue.update_filters(pitch, tempo, bass)

    await interaction.followup.send(content=(await data.audio_queue.output_filters()))