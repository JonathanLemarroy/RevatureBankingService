from daos.accountholderdao import AccountHolderDAO, AccountHolderDAOInterface
from entities.accountholder import AccountHolder
from util.nosuchelementerror import NoSuchElementError
from util.postgresdb import PostgresDB

database = PostgresDB("revaturedb.cw0dgbcoagdz.us-east-2.rds.amazonaws.com", "revature", "revature")
client_dao: AccountHolderDAOInterface = AccountHolderDAO(database, "test_account_holders", "test_accounts")


def test_create_client_success():
    client = AccountHolder("John", "Doe")
    client = client_dao.create_record(client)
    assert client.get_user_id() != 0
    assert client.get_first_name() == "John"
    assert client.get_last_name() == "Doe"
    assert len(client.get_accounts()) == 0
    

def test_load_client_success():
    client = AccountHolder("John1", "Doe2")
    client = client_dao.create_record(client)
    new = client_dao.load_object(client.get_user_id())
    assert new.get_user_id() != 0
    assert new.get_first_name() == "John1"
    assert new.get_last_name() == "Doe2"
    assert len(client.get_accounts()) == 0


def test_load_client_failure():
    try:
        new = client_dao.load_object(10000)
        assert False
    except NoSuchElementError as e:
        assert True
    except Exception as e:
        assert False


def test_save_client_success():
    client = AccountHolder("John3", "Doe4")
    client = client_dao.create_record(client)
    new = client_dao.load_object(client.get_user_id())
    assert new.get_user_id() != 0
    assert new.get_first_name() == "John3"
    assert new.get_last_name() == "Doe4"
    assert len(client.get_accounts()) == 0


def test_delete_client_success():
    client = AccountHolder("John1", "Doe2")
    client = client_dao.create_record(client)
    client_dao.delete_record(client.get_user_id())
    try:
        client_dao.load_object(client.get_user_id())
        assert False
    except NoSuchElementError as e:
        assert True
    except Exception as e:
        assert False


def test_delete_client_failure():
    try:
        client_dao.delete_record(1000)
        assert False
    except NoSuchElementError as e:
        assert True
    except Exception as e:
        assert False
