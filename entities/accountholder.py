from typing import Optional
from json import dumps
from util.nosuchelementerror import NoSuchElementError


class AccountHolder:

    def __init__(self, first_name: Optional[str] = "N/A", last_name: Optional[str] = "N/A",
                 user_id: Optional[int] = 0, accounts: Optional[list[int]] = None) -> None:
        self.__first_name: str = first_name
        self.__last_name: str = last_name
        self.__user_id: int = user_id
        if accounts is None:
            self.__accounts: list[int] = []
        else:
            self.__accounts = accounts

    def add_account(self, account_id: int) -> None:
        self.__accounts.append(account_id)

    def remove_account(self, account_id: int) -> None:
        if self.__accounts is None or account_id not in self.__accounts:
            raise NoSuchElementError(f"Account with id {account_id} not found")
        self.__accounts.remove(account_id)

    def get_accounts(self) -> list[int]:
        return self.__accounts.copy()

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def get_user_id(self) -> int:
        return self.__user_id

    def to_json_dict(self) -> dict:
        return {"firstName": self.__first_name, "lastName": self.__last_name,
                "identification": self.__user_id, "accounts": dumps(self.__accounts)}
