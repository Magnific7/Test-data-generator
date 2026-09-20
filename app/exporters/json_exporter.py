import json

def export_to_json(data, file_path):
    """
    Exports the given data to a JSON file.

    Args:
        data (dict): The data to be exported.
        file_path (str): The path to the output JSON file.
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)