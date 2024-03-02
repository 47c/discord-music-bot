from utilities.dependencies import *
from commands.commands      import *

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1101666836690505819))

    log(f'{client.user} ready')

if __name__ == '__main__':
    logger_thread.start(); timeout_thread.start()

    client.run(BOT_TOKEN, log_level=logging.NOTSET)

    GLOBAL_KILLTHREADS = logger.kill = True
    logger_thread.join(); timeout_thread.join()