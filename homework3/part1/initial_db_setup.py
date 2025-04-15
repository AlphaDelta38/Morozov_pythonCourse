from schemas.db_schemas import DB_SCHEMAS
from sqlite3_orm import Sqlite_ORM
import os


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
        if not unique_user_fullname_flag and schema[0] == "User":
            Sqlite_ORM.init_table(schema[0], schema[1], [])
        else:
            Sqlite_ORM.init_table(*schema)
