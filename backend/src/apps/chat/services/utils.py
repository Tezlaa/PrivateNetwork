
from datetime import datetime


def receive_json_to_needed_fields(receive_json: dict, search_fields: tuple) -> dict:
    fields = {}
    for needed_field in search_fields:
        data_from_recive = receive_json.get(needed_field)
        if data_from_recive is None:
            continue
        fields[needed_field] = data_from_recive
        
    return fields


def get_path_for_voice_message(obj, filename: str) -> str:
    return f'voice_messages/{obj.user.username}/{filename}'


def get_path_for_file_message(obj, filename: str) -> str:
    return f'files/{datetime.now().strftime("%m.%d.%Y")}/{filename}'
