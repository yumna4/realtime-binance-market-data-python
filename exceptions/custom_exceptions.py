from fastapi import status


class CustomAPIException(Exception):
    def __init__(self, name, message, stack_trace=None):
        self.name = name
        self.message = message
        self.stack_trace = stack_trace
        super().__init__(message)


class DatabaseException(CustomAPIException):
    def __init__(self, message="Database transaction error has occurred.", status_code=status.HTTP_400_BAD_REQUEST):
        self.name = "DatabaseException"
        self.message = message
        self.status_code = status_code
        super().__init__(self.name, self.message)


class DatabaseIntegrityException(CustomAPIException):
    def __init__(self, message="The specified reference key does not exist or one or more of the input values are "
                               "duplicate", delete=False, db_model=None):
        self.name = "DatabaseIntegrityException"
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message
        if db_model:
            self.message = f'The {db_model.__name__} specified by this ID already exists'
        super().__init__(self.name, self.message)


class ItemNotFoundException(CustomAPIException):
    def __init__(self, db_id=None, db_model=None):
        self.name = "ItemNotFoundException"
        self.status_code = status.HTTP_404_NOT_FOUND
        id_string = "the given id(s) do"
        if db_id is not None:
            id_string = f'id {db_id} does'
        item_string = "database item"
        if db_model:
            item_string = db_model.__name__

        self.message = f"The {item_string} specified by {id_string} not exist"
        super().__init__(self.name, self.message)


class ItemsNotFoundException(CustomAPIException):
    def __init__(self, ids):
        self.name = "ItemsNotFoundException"
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"The database items specified by ids {ids} are not found"
        super().__init__(self.name, self.message)


class InvalidTimestampException(CustomAPIException):
    def __init__(self, timestamp=None, message=None):
        self.name = "InvalidTimestampException"
        if message is None:
            self.message = f"Timestamp {timestamp if timestamp is not None else ''} cannot be converted to a valid " \
                           f"datetime object."
        else:
            self.message = message
        super().__init__(self.name, self.message)


class ConfigNotFoundException(CustomAPIException):
    def __init__(self, message):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.name = "ConfigNotFoundException"
        self.message = message
        super().__init__(self.name, self.message)


class InvalidTimeFormat(CustomAPIException):
    def __init__(self):
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.name = "InvalidTimeFormat"
        self.message = "Invalid time format"
        super().__init__(self.name, self.message)