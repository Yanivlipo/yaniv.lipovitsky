from flask import session


class SessionHelper:
    _SUCCESS_KEY = 'success'
    _FAILED_KEY = 'failed'

    @classmethod
    def clear_session_results(cls):
        session[cls._SUCCESS_KEY] = None
        session[cls._FAILED_KEY] = None

    @classmethod
    def set_result_in_session(cls, is_success: bool, message: str):
        session[cls._get_result_key_in_session(is_success)] = message

    @classmethod
    def _get_result_key_in_session(cls, is_success: bool):
        if is_success:
            return cls._SUCCESS_KEY
        return cls._FAILED_KEY
