from daos.bankaccountdao import BankAccountDAOInterface, BankAccountDAO
from entities.bankaccount import BankAccount
from util.nosuchelementerror import NoSuchElementError
from util.postgresdb import PostgresDB

database = PostgresDB("revaturedb.cw0dgbcoagdz.us-east-2.rds.amazonaws.com", "revature", "revature")
bank_account_dao: BankAccountDAOInterface = BankAccountDAO(database, "test_accounts")


def test_create_record_success():
    original = BankAccount(100, "savings", 5)
    returned = bank_account_dao.create_record(original)
    assert original.get_owner_id() == returned.get_owner_id()
    assert original.get_balance() == returned.get_balance()
    assert original.get_account_type() == returned.get_account_type()
    assert returned.get_account_id() != 0


def test_load_record_success():
    original = BankAccount(100, "savings", 5)
    returned = bank_account_dao.create_record(original)
    returned = bank_account_dao.load_object(returned.get_account_id())
    assert returned.get_balance() == 5
    assert returned.get_account_type() == "savings"
    assert returned.get_owner_id() == 100


def test_load_record_failure():
    try:
        bank_account_dao.load_object(10000)
    except NoSuchElementError as e:
        assert True
    except Exception as e:
        assert False


def test_save_record_success():
    original = BankAccount(101, "savings", 5)
    original = bank_account_dao.create_record(original)
    original.set_balance(10)
    original.set_account_type("checking")
    bank_account_dao.save_record(original)
    modified = bank_account_dao.load_object(original.get_account_id())
    assert modified.get_balance() == 10
    assert modified.get_account_type() == "checking"


def test_delete_record_success():
    original = BankAccount(110, "savings", 6)
    original = bank_account_dao.create_record(original)
    bank_account_dao.delete_record(original.get_account_id())
    try:
        bank_account_dao.load_object(original.get_account_id())
        assert False
    except AssertionError:
        assert False
    except Exception as e:
        assert True


def test_delete_record_failure():
    try:
        bank_account_dao.delete_record(10000)
        assert False
    except AssertionError:
        assert False
    except Exception as e:
        assert True


def test_load_records_success():
    original1 = BankAccount(110, "savings", 6)
    original2 = BankAccount(110, "checking", 7)
    original1 = bank_account_dao.create_record(original1)
    original2 = bank_account_dao.create_record(original2)
    try:
        records = bank_account_dao.load_objects(110)
        assert records[original1.get_account_id()].get_account_type() == "savings"
        assert records[original1.get_account_id()].get_balance() == 6
        assert records[original1.get_account_id()].get_owner_id() == 110
        assert records[original2.get_account_id()].get_account_type() == "checking"
        assert records[original2.get_account_id()].get_balance() == 7
        assert records[original2.get_account_id()].get_owner_id() == 110
    except Exception as e:
        assert False
