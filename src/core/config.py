from dataclasses import dataclass
from os import environ


@dataclass(frozen=True)
class Config:
    DB_CONNECTION_STRING: str

    @staticmethod
    def get_config():
        db_connection_string = environ.get(
            "DB_CONNECTION_STRING",
            "postgres://user:password@localhost:5432/test_database"
        )

        return Config(db_connection_string)


config = Config.get_config()
