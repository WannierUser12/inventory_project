import os
import environ


@environ.config(prefix="HP")
class InventoryConfig:
    @environ.config(prefix="DB")
    class Database:
        host = environ.var("localhost", help="Database host")
        port = environ.var(5432, int, help="Database port")
        name = environ.var("inventory", help="Database name")
        user = environ.var("postgres", help="Database username")
        password = environ.var("0210", help="Database password")
        name_test = environ.var("inventory_ci", help="Test database name")
        statement_timeout = environ.var(
            1 * 60 * 1000,
            int,
            help="Database statement timeout in milliseconds",
        )

    database = environ.group(Database)


def get_config() -> InventoryConfig:
    return InventoryConfig.from_environ(os.environ)  # noqa
