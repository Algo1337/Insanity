import enum

from utils import *

class ops_t(enum.Enum):
    __read_db__ = "read"
    __add_row__ = "add"
    __rm_row__ = "rm"

class dbs_t(enum.Enum):
    __EVENT_LOGS__             : str = "assets/logs/events.log"
    __MESSAGE_LOGS__            : str = "assets/logs/messages.log"

def database(db: db_t, op: op_t, query: int | str) -> bool | str:
    if op == op_t.__read_db__:
        """ Read Database """
        file = open(db, "r")
        data = file.read().split("\n")
        file.close()

        return data
    elif op == op_t.__add_id__:
        """ Add Query to File """
        file = open(db, "a")
        file.write(f"{query}\n")
        file.close()

        return True
    elif op == op_t.__rm_id__:
        """ Remove Query from file """
        lines: list[str] = []
        file = open(db, "r")
        lines = file.read().split("\n")
        for line in lines:
            if query not in line:
                lines.append(line)

        file.close()
        file = open(db, "w")
        file.write("\n".join(lines))
        file.close()

        return True
    
    return False