from ..base import BaseResponse
from ..handler import HashHandler
from model import DATABASE_ENGINE, AccountTable, AccountEntity


class SignUpResponse(BaseResponse[None]):
    pass

class SignInResponse(BaseResponse[AccountEntity]):
    pass


class AccountManager:
    @staticmethod
    def sign_up(account_id: str, raw_password: str) -> SignUpResponse:
        hashed_password = HashHandler.hash(raw_contents=raw_password)
        new_account_entity = AccountEntity(account_id=account_id, hashed_password=hashed_password)
        new_account_table = AccountTable.load_from_entities(entities=[new_account_entity])
        try:
            new_account_table.save_to_database(database_engine=DATABASE_ENGINE)
            return SignUpResponse(is_success=True, message=f"Account ID '{account_id}' signed up correctly.")
        except:
            return SignUpResponse(is_success=False, message=f"Account ID '{account_id}' has already signed up.")

    @staticmethod
    def sign_in(account_id: str, raw_password: str) -> SignInResponse:
        target_account_table = AccountTable.load_specified_account_from_database(database_engine=DATABASE_ENGINE, account_id=account_id)
        try:
            target_account_entity = target_account_table.get_specified_accout_entity(account_id=account_id)
        except ValueError:
            return SignInResponse(is_success=False, message=f"Account ID '{account_id}' hasn't signed up yet.")
        is_success =  HashHandler.verify(raw_contents=raw_password, hashed_contents=target_account_entity.hashed_password)
        if not is_success:
            return SignInResponse(is_success=False, message=f"Please input password correctly.")
        
        return SignInResponse(is_success=True, contents=target_account_entity)