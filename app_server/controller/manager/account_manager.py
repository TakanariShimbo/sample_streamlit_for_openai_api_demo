from ..handler import HashHandler, BaseResponse
from model import DATABASE_ENGINE, AccountTable, AccountEntity


class AccountResponse(BaseResponse[None]):
    pass


class AccountManager:
    @staticmethod
    def sign_up(account_id: str, raw_password: str) -> AccountResponse:
        hashed_password = HashHandler.hash(raw_contents=raw_password)
        new_account_entity = AccountEntity(account_id=account_id, hashed_password=hashed_password)
        new_account_table = AccountTable.load_from_entities(entities=[new_account_entity])
        try:
            new_account_table.save_to_database(database_engine=DATABASE_ENGINE)
            return AccountResponse(is_success=True)
        except:
            return AccountResponse(is_success=False, message=f"Account ID {account_id} has already signed up.")

    @staticmethod
    def sign_in(account_id: str, raw_password: str) -> AccountResponse:
        target_account_table = AccountTable.load_specified_account_from_database(database_engine=DATABASE_ENGINE, account_id=account_id)
        try:
            target_account_entity = target_account_table.get_entity(column_name="account_id", value=account_id)
        except ValueError:
            return AccountResponse(is_success=False, message=f"Account ID '{account_id}' hasn't signed up yet.")
        is_success =  HashHandler.verify(raw_contents=raw_password, hashed_contents=target_account_entity.hashed_password)
        if not is_success:
            return AccountResponse(is_success=False, message=f"Please input password correctly.")
        
        return AccountResponse(is_success=True)