from typing import Optional
import psycopg2


class PostgresDB:

    def __init__(self, host: str, username: str, password: str, port: Optional[int] = 5432,
                 database: Optional[str] = "postgres") -> None:
        self.__host = host
        self.__username = username
        self.__password = password
        self.__port = port
        self.__database = database
        self.__pg = psycopg2.connect(host=host, port=port, user=username, password=password, database=database)

    def execute(self, sql_statement: str, variables: Optional[list] = None) -> Optional[list[tuple]]:
        try:
            if self.__pg.closed != 0:
                self.__pg = psycopg2.connect(host=self.__host,
                                             port=self.__port,
                                             user=self.__username,
                                             password=self.__password,
                                             database=self.__database)
            cursor = self.__pg.cursor()
            if variables is None:
                cursor.execute(sql_statement)
            else:
                cursor.execute(sql_statement, variables)
            return cursor.fetchall()
        except Exception as e:
            print("Postgres Error: " + str(e))
            return []

    def commit(self) -> None:
        self.__pg.commit()

    def rollback(self) -> None:
        self.__pg.rollback()
