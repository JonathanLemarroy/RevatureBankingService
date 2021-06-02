from typing import Optional, Union


class BankAccount:

    def __init__(self, owner_id: int, account_type: str,
                 balance: Optional[Union[float, int]] = 0.0, account_id: Optional[int] = 0) -> None:
        self.__owner_id: int = owner_id
        self.__account_type: str = account_type.lower()
        self.__balance: float = float(balance)
        self.__account_id: int = account_id

    def get_owner_id(self) -> int:
        return self.__owner_id

    def get_account_type(self) -> str:
        return self.__account_type

    def set_account_type(self, account_type: str) -> None:
        self.__account_type = account_type

    def get_balance(self) -> float:
        return self.__balance

    def set_balance(self, new_balance: Union[int, float]) -> None:
        self.__balance = float(new_balance)

    def get_account_id(self) -> int:
        return self.__account_id

    def to_json_dict(self) -> dict:
        return {"ownerId": self.__owner_id, "accountType": self.__account_type,
                "balance": self.__balance, "accountId": self.__account_id}
