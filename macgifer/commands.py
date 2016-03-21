import hashlib
import random
import tempfile
import uuid

import click
import dropbox
import requests
import xerox

from .config import (
    get_base_path, get_gif_path, get_gif_url, get_base_url, read_config
)
from .dropbox import get_metadata, update_metadata


@click.group()
@click.pass_context
def cli(ctx):
    """
    Base parent comment. Not directly invoked, it is used for initialization
    purposes.
    """
    config = read_config(click.get_app_dir('macgifer'))

    ctx.obj = {
        'dropbox': dropbox.Dropbox(config['default.dropbox_api_key']),
        'config': config,
    }


@cli.command()
@click.argument('url', type=str)
@click.argument('tags', type=str, nargs=-1)
@click.pass_context
def add(ctx, url, tags):
    """
    Add the gif at the given URL to your Dropbox and assign it the given tags.
    """
    gif_id = hashlib.sha1(str(uuid.uuid4()).encode('ascii')).hexdigest()

    metadata = get_metadata(
        ctx.obj['dropbox'], get_base_path(ctx.obj['config'])
    )
    r = requests.get(url, stream=True)

    _, tmp = tempfile.mkstemp()
    with open(tmp, 'wb') as temp_gif_file:
        for chunk in r.iter_content(chunk_size=1024):
            temp_gif_file.write(chunk)

    with open(tmp, 'rb') as temp_gif_file:
        ctx.obj['dropbox'].files_upload(
            temp_gif_file,
            get_gif_path(get_base_path(ctx.obj['config']), gif_id),
            mute=True
        )

    metadata[gif_id] = set(tags)
    update_metadata(
        ctx.obj['dropbox'], metadata, get_base_path(ctx.obj['config'])
    )


@cli.command()
@click.argument('tags', type=str, nargs=-1)
@click.pass_context
def get(ctx, tags):
    """
    Get a gif matching the given set of tags and copy its URL to the clipboard.
    """
    tags = set(tags)
    metadata = get_metadata(
        ctx.obj['dropbox'], get_base_path(ctx.obj['config'])
    )
    matches = [
        item for item, item_tags in metadata.items()
        if item_tags >= tags
    ]

    if matches:
        gif = random.choice(matches)
        gif_url = get_gif_url(get_base_url(ctx.obj['config']), gif)
        xerox.copy(gif_url)
