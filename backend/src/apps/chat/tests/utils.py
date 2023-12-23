def tp_to_unaccurate(json: dict) -> dict:
    """ timestamp to unaccurate format """

    json['timestamp'] = str(json['timestamp'])[:8]
    return json