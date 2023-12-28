from ..handler import HashHandler
from model import DATABASE_ENGINE, AccountTable, AccountEntity


class AccountManager:
    @staticmethod
    def sign_up(account_id: str, raw_password: str) -> bool:
        hashed_password = HashHandler.hash(raw_contents=raw_password)
        new_account_entity = AccountEntity(account_id=account_id, hashed_password=hashed_password)
        new_account_table = AccountTable.load_from_entities(entities=[new_account_entity])
        try:
            new_account_table.save_to_database(database_engine=DATABASE_ENGINE)
            return True
        except:
            return False

    @staticmethod
    def sign_in(account_id: str, raw_password: str) -> bool:
        target_account_table = AccountTable.load_specified_account_from_database(database_engine=DATABASE_ENGINE, account_id=account_id)
        try:
            target_account_entity = target_account_table.get_entity(column_name="account_id", value=account_id)
        except ValueError:
            return False
        return HashHandler.verify(raw_contents=raw_password, hashed_contents=target_account_entity.hashed_password)
