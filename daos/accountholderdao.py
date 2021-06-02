from abc import ABC, abstractmethod

from daos.bankaccountdao import BankAccountDAO
from entities.accountholder import AccountHolder
from util.dataerror import DataError
from util.nosuchelementerror import NoSuchElementError
from util.postgresdb import PostgresDB


class AccountHolderDAOInterface(ABC):

    @abstractmethod
    def create_record(self, user: AccountHolder) -> AccountHolder:
        pass

    @abstractmethod
    def save_record(self, user: AccountHolder) -> None:
        pass

    @abstractmethod
    def delete_record(self, client_id: int) -> None:
        pass

    @abstractmethod
    def load_object(self, client_id: int) -> AccountHolder:
        pass

    @abstractmethod
    def load_all_objects(self) -> dict[int, AccountHolder]:
        pass


class AccountHolderDAO(AccountHolderDAOInterface):

    def __init__(self, database: PostgresDB, table_name_p: str, table_name_s):
        self.__database: PostgresDB = database
        self.__table_name = table_name_p
        self.__table_name_s = table_name_s
        sql = f"CREATE TABLE IF NOT EXISTS {self.__table_name} ( " \
              f"first_name varchar(50), " \
              f"last_name varchar(50), " \
              f"user_id int primary key generated always as identity );"
        self.__database.execute(sql)
        self.__database.commit()
        self.__account_dao = BankAccountDAO(self.__database, self.__table_name_s)

    def create_record(self, user: AccountHolder) -> AccountHolder:
        sql = f"INSERT INTO {self.__table_name} (first_name, last_name) values (%s, %s) returning user_id;"
        result = self.__database.execute(sql, [user.get_first_name(), user.get_last_name()])
        if len(result) == 0:
            self.__database.rollback()
            raise DataError(f"Failed creating client in database with id {user.get_user_id()}")
        else:
            self.__database.commit()
        return self.load_object(result[0][0])

    def save_record(self, user: AccountHolder) -> None:
        sql = f"UPDATE {self.__table_name} SET first_name = %s, last_name = %s WHERE user_id = %s returning user_id;"
        results = self.__database.execute(sql, [user.get_first_name(), user.get_last_name(), user.get_user_id()])
        if len(results) == 0:
            self.__database.rollback()
            raise DataError(f"Failed updating client in database with id {user.get_user_id()}")
        else:
            self.__database.commit()

    def delete_record(self, client_id: int) -> None:
        client = self.load_object(client_id)
        for account in client.get_accounts():
            self.__account_dao.delete_record(account)
        sql = f"DELETE FROM {self.__table_name} WHERE user_id = %s returning user_id;"
        results = self.__database.execute(sql, [client_id])
        if len(results) == 0:
            self.__database.rollback()
            raise NoSuchElementError(f"Failed deleting client {client_id}")
        else:
            self.__database.commit()

    def load_object(self, client_id: int) -> AccountHolder:
        sql = f"SELECT * FROM {self.__table_name} WHERE user_id = %s;"
        results = self.__database.execute(sql, [client_id])
        if len(results) == 0:
            raise NoSuchElementError(f"No clients found for query on client id {client_id}")
        result = results[0]
        accounts = self.__account_dao.load_objects(result[2])
        return AccountHolder(result[0], result[1], result[2], [account.get_account_id()
                                                               for account in accounts.values()
                                                               if account.get_owner_id() == result[2]])

    def load_all_objects(self) -> dict[int, AccountHolder]:
        sql = f"SELECT * FROM {self.__table_name};"
        sql_results = self.__database.execute(sql)
        account_holders = {}
        for result in sql_results:
            account_holders[result[2]] = self.load_object(result[2])
        return account_holders
