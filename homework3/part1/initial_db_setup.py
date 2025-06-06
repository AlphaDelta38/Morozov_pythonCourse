from dataclasses import asdict
import os
from schemas.db_schemas import DB_SCHEMAS
from sqlite3_orm import SQLite3ORM


def initial_db_setup(unique_user_fullname_flag):
    """
    description:
    with Sqlite_ORM, initialize database tables by schemas

    :param unique_user_fullname_flag: flag for turn off unique user fullname, (Default = False)

    :return: --> void
    """

    if os.path.exists("default.db"):
        os.remove("default.db")

    for schema in DB_SCHEMAS:
        dict_schema = asdict(schema)

        if not unique_user_fullname_flag and schema.table_name == "User":
            dict_schema.popitem()

        SQLite3ORM.init_table(*dict_schema)
