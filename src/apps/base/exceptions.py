class UserLimitError(Exception):
    def __init__(self, limit: int) -> None:
        super().__init__(f'Out of limit in {limit} user!')
        

class LobbyNotFound(Exception):
    def __init__(self, lobby_name: str) -> None:
        super().__init__(f'Lobby {lobby_name} not found in the database or password doesn`t match.')
        

class OwnerError(Exception):
    def __init__(self):
        super().__init__("You are not the owner of this lobby.")
    