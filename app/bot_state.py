from enum import IntEnum


class BotSate(IntEnum):
    START = 1
    PHONE = 2
    NO_PHONE = 3
    ADDRESS = 4
    PRESENT = 5
    ROOM_CHOICE = 6
    IN_ROOM_CREATOR = 7
    IN_ROOM_USER = 8
    IN_ROOM_USER_READY = 9



