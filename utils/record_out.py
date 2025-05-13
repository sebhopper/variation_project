#Standard imports
import os
import json
from pathlib import Path


def create_output_folder(base_dir, folder_name):
    """
    Create a folder named `folder_name` inside `base_dir`.
    Returns the full path to the created folder.
    """
    output_path = Path(base_dir) / folder_name
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path

def write_json_file(data, folder_path, filename):
    """
    Write `data` as a JSON file named `filename` inside `folder_path`.
    """
    file_path = Path(folder_path) / filename
    if not file_path.suffix:
        file_path = file_path.with_suffix('.json')  # ensure .json extension

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
