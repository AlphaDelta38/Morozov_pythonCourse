from homework3.part1.orm_constants_templates import *
from homework3.part2.db_connect_decorator import db_connector


class Sqlite_ORM:
    """
    description:
    converts input data to SQL command and execute them ,that means of realize ORM system

    :return: --> instance of static methods
    """

    @staticmethod
    @db_connector
    def init_table(table_name, fields, add, connector):
        """
        description:
        connect with db, transform data to SQL command and execute them

        :param table_name: name table for create
        :param fields: list of column data
        :param add: additional table settings
        :param connector: db connection

        :return: --> void
        """

        connector.execute(f'''
            {CREATE_TEMPLATE} {table_name.lower()} 
            ({", ".join([f"{key} {" ".join(value)}" for key, value in fields.items()])}
             {", ".join(add)}
            )
        ''')

    @staticmethod
    @db_connector
    def create(table_name, data, connector):
        """
        description:
        connect with db, transform data to SQL command and execute them
        create row in table

        :param table_name: name table for create
        :param data: data for create row in table
        :param connector: db connection

        :return: --> void
        """

        connector.execute(f'''
            {INSERT_TEMPLATE} {table_name.lower()} ({", ".join(data.keys())}) VALUES ({", ".join(["?"] * len(data.keys()))})
        ''', list(data.values()))

    @staticmethod
    @db_connector
    def create_many(table_name, data, connector):
        """
        description:
        connect with db, transform data to SQL command and execute them
        create many row in table with list of data

        :param table_name: name table for create
        :param data: list of data for create row in table
        :param connector: db connection

        :return: --> void
        """

        connector.executemany(f'''
            {INSERT_TEMPLATE} {table_name.lower()} ({", ".join(data[0].keys())}) VALUES ({", ".join(["?"] * len(data[0].keys()))})
        ''', list(list(row.values()) for row in data))

    @staticmethod
    @db_connector
    def update(table_name, new_date, search_by, connector):
        """
        description:
        connect with db, transform data to SQL command and execute them
        update row in table

        :param table_name: name table where will be updated row
        :param new_date:  data for update certain row in table
        :param search_by: condition for search certain row in table
        :param connector: db connection

        :return: --> void
        """

        connector.execute(f'''
               {UPDATE_TEMPLATE} {table_name.lower()} SET {", ".join(f"{key} = {f"\"{value}\""}" for key, value in new_date.items())}
               WHERE {search_by}
            '''
        )

    @staticmethod
    @db_connector
    def delete(table_name, search_by, connector):
        """
        description:
        connect with db, transform data to SQL command and execute them
        delete row in table

        :param table_name: name table from will be deleted row
        :param search_by: condition for search certain row in table
        :param connector: db connection

        :return: --> void
        """

        connector.execute(f'''
                {DELETE_TEMPLATE} {table_name.lower()} WHERE {search_by}
            '''
        )

    @staticmethod
    @db_connector
    def get_one(table_name, search_by, connector):
        """
        description:
        connect with db, transform data to SQL command and execute them
        get one  row from table by condition

        :param table_name: name table for get one
        :param search_by: condition for search certain row in table
        :param connector: db connection

        :return: --> one row from table by condition
        """

        connector.execute(f'''
                {SELECT_TEMPLATE} {table_name.lower()} WHERE {search_by}
            '''
        )
        return dict(connector.fetchone())

    @staticmethod
    @db_connector
    def get_many(table_name, connector, search_by="", limit = 0, ):
        """
        description:
        connect with db, transform data to SQL command and execute them
        get many row from table by condition

        :param table_name: name table for get one
        :param search_by: condition for search certain row in table
        :param limit: limit of return rows
        :param connector: db connection


        :return: --> many rows from table by condition
        """

        connector.execute(f'''
                {SELECT_TEMPLATE} {table_name.lower()} {f"WHERE {search_by}" if search_by != "" else ""}
                {f"LIMIT {limit}" if not limit else ""}
            '''
        )

        return dict(connector.fetchall())



