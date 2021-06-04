import os
import gc
import asyncio
import threading
import constants
import command
import utils
from datetime import datetime
from snekcord import EmbedBuilder
from snekcord.clients.wsevents import MessageCreateEvent

commands = constants.loader.get_global('commands')
client = constants.loader.get_global('client')
ICON_URL = 'https://cdn.discordapp.com/icons/%s/%s.png'


@command.doc(
    'Sends this guild\'s shard id and the shard\'s websocket latency'
)
@commands.command
async def ping(evt: MessageCreateEvent) -> None:
    shard = evt.shard
    embed = EmbedBuilder(
        title=':ping_pong: Ping',
        description=(
            f'**Shard {shard.id}**\n'
            f'Websocket Latency: {(shard.latency * 1000):.2f}ms'
        ),
        color=constants.BLUE
    )
    await embed.send_to(evt.channel)


@command.doc(
    'Sends info about the bot\'s Python process'
)
@commands.command
async def info(evt: MessageCreateEvent) -> None:
    threads = threading.active_count()
    tasks = asyncio.all_tasks()
    collected = sum(gen['collected'] for gen in gc.get_stats())
    delta = datetime.now() - client.started_at
    embed = EmbedBuilder(
        title='Info',
        description=(
            f'**Process ID**: {os.getpid()}\n'
            f'**Active Threads**: {threads}\n'
            f'**Asyncio Tasks**: {len(tasks)}\n'
            f'**Garbage Collected Objects**: {collected}\n'
            f'**Started**: {utils.humanize(delta)}'
        ),
        color=constants.BLUE
    )
    await embed.send_to(evt.channel)


@command.doc(
    'Sends the bot\'s github repository'
)
@commands.command
async def source(evt: MessageCreateEvent) -> None:
    await evt.channel.messages.create(content=constants.REPOSITORY)