from daos.accountholderdao import AccountHolderDAO, AccountHolderDAOInterface
from daos.bankaccountdao import BankAccountDAO, BankAccountDAOInterface
from services.bankingservice import BankingServiceInterface, BankingService
from util.postgresdb import PostgresDB

database = PostgresDB("revaturedb.cw0dgbcoagdz.us-east-2.rds.amazonaws.com", "revature", "revature")
client_dao: AccountHolderDAOInterface = AccountHolderDAO(database, "test_account_holders2", "test_accounts2")
bank_account_dao: BankAccountDAOInterface = BankAccountDAO(database, "test_accounts2")
banking_service: BankingServiceInterface = BankingService()
banking_service.account_dao = bank_account_dao
banking_service.user_dao = client_dao


def test_banking_create_client_success():
    result = banking_service.create_client("John", "Doe")
    assert result[1] == 201


def test_banking_get_client_success():
    result = banking_service.get_client(1)
    assert result[1] == 200


def test_banking_get_client_failure():
    result = banking_service.get_client(10000)
    assert result[1] == 404


def test_banking_get_all_clients_success():
    result = banking_service.get_all_clients()
    assert result[1] == 200


def test_banking_update_client_success():
    result = banking_service.update_client(1, "RedBull", "Monster")
    assert result[1] == 200


def test_banking_update_client_failure():
    result = banking_service.update_client(10000, "RedBull", "Monster")
    assert result[1] == 404


def test_banking_remove_client_success():
    result = banking_service.create_client("John2", "Doe2")
    result = banking_service.create_client("John3", "Doe3")
    result = banking_service.remove_client(2)
    assert result[1] == 205


def test_banking_remove_client_failure():
    result = banking_service.remove_client(10000)
    assert result[1] == 404


def test_banking_create_account_success():
    result = banking_service.create_account(1, "checking")
    assert result[1] == 201


def test_banking_create_account_failure1():
    result = banking_service.create_account(10000, "checking")
    assert result[1] == 404


def test_banking_create_account_failure2():
    result = banking_service.create_account(1, "check")
    assert result[1] == 422


def test_banking_get_accounts_success():
    result = banking_service.get_accounts(1, 0, 10000)
    assert result[1] == 200


def test_banking_get_accounts_failure():
    result = banking_service.get_accounts(10000, 0, 10000)
    assert result[1] == 404


def test_banking_get_account_success():
    result = banking_service.create_account(1, "checking")
    result = banking_service.get_account(1, 1)
    assert result[1] == 200


def test_banking_get_account_failure1():
    result = banking_service.create_account(1, "checking")
    result = banking_service.get_account(10000, 1)
    assert result[1] == 404


def test_banking_get_account_failure2():
    result = banking_service.create_account(1, "checking")
    result = banking_service.get_account(1, 10000)
    assert result[1] == 404


def test_banking_update_account_success():
    result = banking_service.create_account(1, "checking")
    result = banking_service.update_account(1, 1, "savings", 1000)
    assert result[1] == 200


def test_banking_update_account_failure1():
    result = banking_service.create_account(1, "checking")
    result = banking_service.update_account(1000, 1, "savings", 1000)
    assert result[1] == 404


def test_banking_update_account_failure2():
    result = banking_service.create_account(1, "checking")
    result = banking_service.update_account(1, 1000, "savings", 1000)
    assert result[1] == 404


def test_banking_remove_account_success():
    result = banking_service.create_account(1, "checking")
    result = banking_service.remove_account(1, 3)
    assert result[1] == 205


def test_banking_remove_account_failure1():
    result = banking_service.create_account(1, "checking")
    result = banking_service.remove_account(1000, 3)
    assert result[1] == 404


def test_banking_remove_account_failure2():
    result = banking_service.create_account(1, "checking")
    result = banking_service.remove_account(1, 3000)
    assert result[1] == 404


def test_banking_dp_or_wd_account_success():
    result = banking_service.update_balance(1, 1, 1000)
    assert result[1] == 200


def test_banking_dp_or_wd_account_failure1():
    result = banking_service.update_balance(1000, 1, 1000)
    assert result[1] == 404


def test_banking_dp_or_wd_account_failure2():
    result = banking_service.update_balance(1, 1000, 1000)
    assert result[1] == 404


def test_banking_dp_or_wd_account_failure3():
    result = banking_service.update_balance(1, 1, -10000)
    assert result[1] == 422


def test_banking_transfer_success():
    result = banking_service.transfer_funds(1, 1, 4, 100)
    assert result[1] == 200


def test_banking_transfer_failure1():
    result = banking_service.transfer_funds(1000, 1, 4, 100)
    assert result[1] == 404


def test_banking_transfer_failure2():
    result = banking_service.transfer_funds(1, 1000, 4, 100)
    assert result[1] == 404


def test_banking_transfer_failure3():
    result = banking_service.transfer_funds(1, 1, 4000, 100)
    assert result[1] == 404


def test_banking_transfer_failure4():
    result = banking_service.transfer_funds(1, 1, 4, 1000000)
    assert result[1] == 422
