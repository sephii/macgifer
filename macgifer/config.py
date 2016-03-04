import configparser
import os


def get_base_path(config):
    return config['default.gifs_path']


def get_base_url(config):
    return config['default.gifs_url']


def get_metadata_path(base_path):
    return base_path + '/metadata.json'


def get_gif_path(base_path, gif_hash):
    return '{}/{}.gif'.format(base_path, gif_hash)


def get_gif_url(base_url, gif_hash):
    return '{}/{}.gif'.format(base_url, gif_hash)


def read_config(app_dir):
    cfg = os.path.join(app_dir, 'config.ini')
    parser = configparser.RawConfigParser()
    parser.read([cfg])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value

    return rv
