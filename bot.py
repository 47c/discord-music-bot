from utilities.dependencies import *
import io

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=878425116009201704))

    log(f'{client.user} ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

@tree.command(
    name="join_voice",
    description="connects to caller voice channel",
    guild=discord.Object(id=878425116009201704),

)
async def comm_join_voice(interaction: discord.Interaction, query: str):
    global guild_data

    caller: discord.Member              = interaction.user
    guild: discord.Guild                = interaction.guild

    voice_channel: discord.VoiceChannel = None
    try:
        voice_channel: discord.VoiceChannel = caller.voice.channel
    except:
        pass

    if not guild.id in guild_data.keys():
        guild_data[guild.id]            = GuildData(client)

    data: GuildData                     = guild_data[guild.id]

    if not voice_channel:
        await interaction.response.send_message(content="you're not in any voice channel")
        return

    if data.status.connected_to_channel:
        await interaction.response.send_message(content="currently busy")
        return

    data.status.update_status(interaction, 
                              await voice_channel.connect())
    
    stream = YoutubeEntry()
    video_data = stream.search(query)
    if not video_data:
        await interaction.response.send_message(content="video not found")
        return

    log(f'playing {video_data.title}')

    data.status.voice_client.play(source=discord.FFmpegOpusAudio(video_data.buffer,
                                                                before_options='',#'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                                                options='-vn -filter:a "rubberband=pitch=1.25, rubberband=tempo=1.45, bass=gain=10"',
                                                                pipe=True, 
                                                                executable='ffmpeg/ffmpeg.exe'), 
                                        after=lambda e: log(f'done {e}'))

if __name__ == '__main__':
    logger_thread.start(); timeout_thread.start()

    client.run(BOT_TOKEN)

    GLOBAL_KILLTHREADS = logger.kill = True
    logger_thread.join(); timeout_thread.join()