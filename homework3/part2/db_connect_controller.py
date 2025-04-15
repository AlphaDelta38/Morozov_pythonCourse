from threading import Lock, Thread
import sqlite3
import time
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
            self._in_use += 1

            self._disconnect_flag = False

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
            if self._in_use > 0:
                self._in_use -= 1
            if self._in_use == 0:
                self.delay_disconnect()
                self._disconnect_flag = True

    def delay_disconnect(self):
        """
        description:
        launches async await logic, for check if flag  is true, then db connection is closed

        :return: --> void
        """

        def delayed():
            time.sleep(5)
            if self._disconnect_flag:
                self.conn.close()

        Thread(target=delayed, daemon=True).start()
