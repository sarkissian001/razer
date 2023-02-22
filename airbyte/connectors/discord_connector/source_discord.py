import asyncio
from typing import Any, List, MutableMapping, Tuple
from airbyte_protocol import AirbyteStream
from airbyte_protocol import ConfiguredAirbyteStream
from airbyte_protocol import ConnectorSpecification
from airbyte_protocol import SyncMode
from airbyte_protocol import Type
import discord


async def read_from_discord(client, channel, state=None):
    messages = []
    async for message in channel.history(after=state):
        messages.append(message)
    return messages[-1].created_at.isoformat() if messages else state, [{'message': message.content} for message in messages]


async def get_messages(state):
    client = discord.Client()
    await client.login("<your discord bot token here>")
    await client.connect()

    # Replace this with the ID of the channel you want to extract messages from
    channel = client.get_channel(123456789)

    try:
        while True:
            state, messages = await read_from_discord(client, channel, state)
            for message in messages:
                yield message
    finally:
        await client.close()


def discover() -> ConnectorSpecification:
    return ConnectorSpecification(
        documentationUrl="<your documentation URL here>",
        changelogUrl="<your changelog URL here>",
        supportsIncremental=True,
        supportedDestinationSyncModes=[SyncMode.overwrite],
        connectionSpecification={
            "type": Type.OBJECT,
            "properties": {
                "discord_bot_token": {"type": Type.STRING},
            },
            "required": ["discord_bot_token"],
            "secretProperties": ["discord_bot_token"],
        },
        streamSpecifications={
            "messages": {
                "properties": {
                    "message": {"type": Type.STRING},
                },
            },
        },
    )

def check(client_config: MutableMapping[str, Any]) -> Tuple[bool, Optional[str]]:
    return True, None

def read(client_config: MutableMapping[str, Any], stream_name: str, sync_mode: SyncMode, cursor_field: List[str], stream_slice: Optional[Dict[str, any]] = None) -> ConfiguredAirbyteStream:
    if stream_name == "messages":
        state = cursor_field[0] if cursor_field else None
        stream = AirbyteStream(
            name=stream_name,
            json_schema=discover().streamSpecifications[stream_name],
            supported_sync_modes=[SyncMode.incremental],
            source_defined_cursor=True,
            source_defined_primary_key=[],
        )
        return ConfiguredAirbyteStream(
            stream=stream,
            sync_mode=SyncMode.incremental,
            cursor_field=[state],
            records=get_messages(state),
        )
