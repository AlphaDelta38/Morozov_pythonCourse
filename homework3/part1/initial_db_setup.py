from schemas.db_schemas import DB_SCHEMAS
from sqlite3_orm import Sqlite_ORM


def initial_db_setup():
    """
    description:
    with Sqlite_ORM, initialize database tables by schemas

    :return: --> void
    """

    for schema in DB_SCHEMAS:
        Sqlite_ORM.init_table(*schema)









