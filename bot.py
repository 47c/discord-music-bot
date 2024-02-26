from utilities.dependencies import *

@client.event
async def on_ready():
    await tree.sync()

    print('ready')
    log(f'{client.user} ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

@tree.command(
    name="connect",
    description="connects to caller voice channel"
)
async def connect_command(interaction: discord.Interaction):
    caller: discord.Member = interaction.user
    voice_channel: discord.VoiceChannel = caller.voice.channel

    if not voice_channel:
        await interaction.response.send_message(content="you're not in any voice channel")
        return

    if client_status.connected_to_channel:
        await interaction.response.send_message(content="currently busy")
        return

    await voice_channel.connect()


if __name__ == '__main__':
    logger_thread.start()
    timeout_thread.start()

    client.run(BOT_TOKEN)

    GLOBAL_KILLTHREADS = True

    print(f'{GLOBAL_KILLTHREADS}')

    logger_thread.join()
    timeout_thread.join()