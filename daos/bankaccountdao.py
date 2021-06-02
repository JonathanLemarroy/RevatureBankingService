from abc import ABC, abstractmethod
from entities.bankaccount import BankAccount
from util.dataerror import DataError
from util.nosuchelementerror import NoSuchElementError
from util.postgresdb import PostgresDB


class BankAccountDAOInterface(ABC):

    @abstractmethod
    def create_record(self, account: BankAccount) -> BankAccount:
        pass

    @abstractmethod
    def save_record(self, account: BankAccount) -> None:
        pass

    @abstractmethod
    def delete_record(self, account_id: int) -> None:
        pass

    @abstractmethod
    def load_object(self, account_id: int) -> BankAccount:
        pass

    @abstractmethod
    def load_objects(self, owner_id: int) -> dict[int, BankAccount]:
        pass

    @abstractmethod
    def load_all_objects(self) -> dict[int, BankAccount]:
        pass


class BankAccountDAO(BankAccountDAOInterface):

    def __init__(self, database: PostgresDB, table_name: str):
        self.__database: PostgresDB = database
        self.__table_name = table_name

    def create_record(self, account: BankAccount) -> BankAccount:
        sql = f"INSERT INTO {self.__table_name} " \
              f"(owner_id, account_type, balance) VALUES (%s, %s, %s) RETURNING account_id"
        result = self.__database.execute(sql, [account.get_owner_id(),
                                               account.get_account_type(),
                                               account.get_balance()])
        if len(result) == 0:
            self.__database.rollback()
            raise DataError(f"Failed creating account in database with id {account.get_account_id()}")
        else:
            self.__database.commit()
        return self.load_object(result[0][0])

    def save_record(self, account: BankAccount) -> None:
        sql = f"UPDATE {self.__table_name} " \
              f"SET account_type = %s, balance = %s WHERE account_id = %s RETURNING account_id"
        result = self.__database.execute(sql, [account.get_account_type(),
                                               account.get_balance(),
                                               account.get_account_id()])
        if len(result) == 0:
            self.__database.rollback()
            raise DataError(f"Failed creating account in database with id {account.get_account_id()}")
        else:
            self.__database.commit()

    def delete_record(self, account_id: int) -> None:
        sql = f"DELETE FROM {self.__table_name} WHERE account_id = %s RETURNING account_id"
        results = self.__database.execute(sql, [account_id])
        if len(results) == 0:
            self.__database.rollback()
            raise NoSuchElementError(f"Couldn't find account with id {account_id}")
        else:
            self.__database.commit()

    def load_object(self, account_id: int) -> BankAccount:
        sql = f"SELECT * FROM {self.__table_name} WHERE account_id = %s"
        results = self.__database.execute(sql, [account_id])
        if len(results) == 0:
            raise NoSuchElementError(f"No accounts found for query on account id {account_id}")
        result = results[0]
        return BankAccount(result[0], result[1], result[2], result[3])

    def load_objects(self, owner_id: int) -> dict[int, BankAccount]:
        sql = f"SELECT * FROM {self.__table_name} WHERE owner_id = %s"
        sql_results = self.__database.execute(sql, [owner_id])
        accounts = {}
        for result in sql_results:
            account = BankAccount(result[0], result[1], result[2], result[3])
            accounts[account.get_account_id()] = account
        return accounts

    def load_all_objects(self) -> dict[int, BankAccount]:
        sql = f"SELECT * FROM {self.__table_name}"
        sql_results = self.__database.execute(sql)
        accounts = {}
        for result in sql_results:
            account = BankAccount(result[0], result[1], result[2], result[3])
            accounts[account.get_account_id()] = account
        return accounts
