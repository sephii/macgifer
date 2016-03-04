from collections import defaultdict
import json

import dropbox

from .config import get_metadata_path


def get_metadata(dbx, base_path):
    try:
        _, metadata_file = dbx.files_download(get_metadata_path(base_path))
    except dropbox.exceptions.ApiError:
        metadata = defaultdict(set)
    else:
        metadata = {
            key: set(value)
            for key, value in metadata_file.json().items()
        }

    return metadata


def update_metadata(dbx, metadata, base_path):
    dumpable_metadata = {
        key: list(value)
        for key, value in metadata.items()
    }
    dbx.files_upload(
        json.dumps(dumpable_metadata), get_metadata_path(base_path),
        dropbox.files.WriteMode('overwrite')
    )
