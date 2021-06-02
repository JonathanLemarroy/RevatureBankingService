import json
from abc import ABC, abstractmethod
from typing import Optional, Union

from daos.accountholderdao import AccountHolderDAO
from daos.bankaccountdao import BankAccountDAO
from entities.accountholder import AccountHolder
from entities.bankaccount import BankAccount
from util.nosuchelementerror import NoSuchElementError
from util.postgresdb import PostgresDB


class BankingServiceInterface(ABC):

    @abstractmethod
    def create_client(self, first_name: str, last_name: str) -> tuple[str, int]:
        pass

    @abstractmethod
    def get_client(self, client_id: int) -> tuple[str, int]:
        pass

    @abstractmethod
    def get_all_clients(self) -> tuple[str, int]:
        pass

    @abstractmethod
    def update_client(self, client_id: int, first_name: str, last_name: str) -> tuple[str, int]:
        pass

    @abstractmethod
    def remove_client(self, client_id: int) -> tuple[str, int]:
        pass

    @abstractmethod
    def create_account(self, client_id: int, account_type: str) -> tuple[str, int]:
        pass

    def get_accounts(self, client_id: int, min_balance: float, max_balance: float) -> tuple[str, int]:
        pass

    @abstractmethod
    def get_account(self, client_id: int, account_id: int) -> tuple[str, int]:
        pass

    @abstractmethod
    def update_account(self, client_id: int, account_id: int,
                       account_type: Optional[str] = None,
                       balance: Optional[Union[float, int]] = None) -> tuple[str, int]:
        pass

    @abstractmethod
    def remove_account(self, client_id: int, account_id: int) -> tuple[str, int]:
        pass

    @abstractmethod
    def update_balance(self, client_id: int, account_id: int, funds_transferred: float) -> tuple[str, int]:
        pass

    @abstractmethod
    def transfer_funds(self, client_id: int, transfer_from: int, transfer_to: int, amount: float) -> tuple[str, int]:
        pass


class BankingService(BankingServiceInterface):

    def __init__(self):
        self.__pg = PostgresDB("revaturedb.cw0dgbcoagdz.us-east-2.rds.amazonaws.com", "revature", "revature")
        self.user_dao = AccountHolderDAO(self.__pg, "account_holders", "accounts")
        self.account_dao = BankAccountDAO(self.__pg, "accounts")

    def create_client(self, first_name: str, last_name: str) -> tuple[str, int]:
        if first_name is None or last_name is None:
            return f"""Client must have a first and last name, 
                   first name given {first_name}, last name given {last_name}""", 422
        return json.dumps(self.user_dao.create_record(AccountHolder(first_name, last_name)).to_json_dict()), 201

    def get_client(self, client_id: int) -> tuple[str, int]:
        try:
            return json.dumps(self.user_dao.load_object(client_id).to_json_dict()), 200
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return f"A server side error occurred {client_id}", 500

    def get_all_clients(self) -> tuple[str, int]:
        return json.dumps([account.to_json_dict() for account in self.user_dao.load_all_objects().values()]), 200

    def update_client(self, client_id: int, first_name: str, last_name: str) -> tuple[str, int]:
        try:
            client = self.user_dao.load_object(client_id)
            if first_name is not None:
                client.set_first_name(first_name)
            if last_name is not None:
                client.set_last_name(last_name)
            self.user_dao.save_record(client)
            return json.dumps(client.to_json_dict()), 200
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return f"A server side error occurred", 500

    def remove_client(self, client_id: int) -> tuple[str, int]:
        try:
            self.user_dao.delete_record(client_id)
            return f"Successfully deleted client {client_id} and all accounts associated with it", 205
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500

    def create_account(self, client_id: int, account_type: str) -> tuple[str, int]:
        try:
            client = self.user_dao.load_object(client_id)
            if account_type.lower() != "savings" and account_type.lower() != "checking":
                return f"Account type must be either checking or savings, type received {account_type}", 422
            account_init = BankAccount(client.get_user_id(), account_type)
            account = self.account_dao.create_record(account_init)
            client.add_account(account.get_account_id())
            return json.dumps(client.to_json_dict()), 201
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500

    def get_accounts(self, client_id: int, min_balance: float, max_balance: float) -> tuple[str, int]:
        try:
            self.user_dao.load_object(client_id)
            accounts = self.account_dao.load_objects(client_id)
            account_list_dict = []
            for account in accounts.values():
                if min_balance <= account.get_balance() <= max_balance:
                    account_list_dict.append(account.to_json_dict())
            return json.dumps(account_list_dict), 200
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500

    def get_account(self, client_id: int, account_id: int) -> tuple[str, int]:
        try:
            account = self.account_dao.load_object(account_id)
            if account.get_owner_id() != client_id:
                return f"This client does not own account {account_id}", 404
            return json.dumps(account.to_json_dict()), 200
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500

    def update_account(self, client_id: int, account_id: int,
                       account_type: Optional[str] = None,
                       balance: Optional[Union[float, int]] = None) -> tuple[str, int]:
        try:
            account = self.account_dao.load_object(account_id)
            if account.get_owner_id() != client_id:
                return f"This client does not own account {account_id}", 404
            if account_type is not None:
                account.set_account_type(account_type)
            if balance is not None:
                account.set_balance(balance)
            self.account_dao.save_record(account)
            return json.dumps(account.to_json_dict()), 200
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500

    def remove_account(self, client_id: int, account_id: int) -> tuple[str, int]:
        try:
            account = self.account_dao.load_object(account_id)
            if account.get_owner_id() != client_id:
                return f"This client does not own account {account_id}", 404
            self.account_dao.delete_record(account_id)
            return f"Account {account_id} deleted successfully", 205
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500

    def update_balance(self, client_id: int, account_id: int, funds_transferred: float) -> tuple[str, int]:
        try:
            account = self.account_dao.load_object(account_id)
            new_balance = account.get_balance()
            if account.get_owner_id() != client_id:
                return f"This client does not own account {account_id}", 404
            new_balance += funds_transferred
            if new_balance < 0:
                return f"Insufficient funds transfer to/from account {account_id}", 422
            account.set_balance(new_balance)
            self.account_dao.save_record(account)
            return json.dumps(account.to_json_dict()), 200
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500

    def transfer_funds(self, client_id: int, transfer_from: int, transfer_to: int, amount: float) -> tuple[str, int]:
        try:
            account_from = self.account_dao.load_object(transfer_from)
            account_to = self.account_dao.load_object(transfer_to)
            if account_from.get_owner_id() != client_id:
                return f"This client does not own account {transfer_from}", 404
            if account_to.get_owner_id() != client_id:
                return f"This client does not own account {transfer_from}", 404
            if account_from.get_balance() - amount < 0:
                return f"Insufficient funds transfer from account {transfer_from}", 422
            account_from.set_balance(account_from.get_balance() - amount)
            account_to.set_balance(account_to.get_balance() + amount)
            self.account_dao.save_record(account_from)
            self.account_dao.save_record(account_to)
            return json.dumps([account_from.to_json_dict(), account_to.to_json_dict()]), 200
        except NoSuchElementError as e:
            return str(e), 404
        except Exception as e:
            print(str(e))
            return "A server side error occurred", 500
