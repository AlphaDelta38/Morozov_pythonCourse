from threading import Lock
import sqlite3
import os


class DBConnectController:
    """
    description:
    implements of singleton logic,manages db connection with Thread and async check (delay_disconnect)
    which checking for using this class, if class has been using, connection has still open

    :return: --> unified instance
    """

    _instance = None
    _lock = Lock()
    _in_use = 0
    _disconnect_flag = False

    def __init__(self):
        self.conn = None
        self.cursor = None

    def __new__(cls):
        """
        description:
        create instance of DBConnectController, if that has been not created,
        also call function for db connect

        :return: --> unified instance
        """

        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._connect()
        return cls._instance

    def _connect(self):
        """
        description:
        install connect with db,and set curso

        :return: --> void
        """

        current_dir = os.path.dirname(__file__)
        db_path = os.path.join(current_dir, '../part1/default.db')
        db_path = os.path.abspath(db_path)

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        """
        description:
        get cursor from db connection

        :return: --> cursor
        """

        with self._lock:
            if self.conn is None:
                self._connect()

        return self.conn.cursor()

    def commit(self):
        """
        description:
        commit db connection

        :return: --> void
        """

        with self._lock:
            self.conn.commit()

    def close(self):
        """
        description:
        if one of using elements stop using the instance, then if in_use > 0, minus 1, if 0 ,
        call delay_disconnect for check maybe someone function will be use the instance

        :return: --> void
        """

        with self._lock:
            self.conn.close()
            self.conn = None
