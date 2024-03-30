from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from exceptions.custom_exceptions import DatabaseException, DatabaseIntegrityException
from common.database.market_data import MarketData
created_date_col = "created_datetime"
modified_date_col = "modified_datetime"


def create(db, item):
    """
    Creates a new record in the database
    Args:
        db: database session
        item: values of attributes for new record

    Returns:
        primary key value of the newly created record
    """
    try:
        setattr(item, created_date_col, datetime.utcnow())
        setattr(item, modified_date_col, datetime.utcnow())
        db.add(item)
        db.commit()
        return item
    except IntegrityError as e:
        db.rollback()
        raise DatabaseIntegrityException(str(e))
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))

def bulk_create(db, db_model, item_data_list):
    """
    Creates new records in the database
    Args:
        db: database session
        db_model: ORM model of database table
        item_data_list: values of attributes for new records

    Returns:
        primary key value of the newly created record
    """
    try:

        objects_to_add = []
        for item_data in item_data_list:
            item = db_model()
            for attr in item_data.__dict__:
                setattr(item, attr, getattr(item_data, attr))
            if created_date_col not in item_data.__dict__:
                setattr(item, created_date_col, datetime.utcnow())
            if modified_date_col not in item_data.__dict__:
                setattr(item, modified_date_col, datetime.utcnow())
            objects_to_add.append(item)
        db.add_all(objects_to_add)
        db.commit()
        return objects_to_add
    except IntegrityError as e:
        db.rollback()
        raise DatabaseIntegrityException(str(e))
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))


def retrieve(db, filters, select_fields, joins=None, join_type="outerjoin"):
    """
    Retrieves record from database table
    Args:
        db: database session
        filters: database filters to apply
        select_fields: Fields to select
        joins: join attributes
        join_type: join type to use. Can be one of ["outerjoin", "join"]

    Returns:
        List of records, total number of database records
    """
    if joins is None:
        joins = []
    try:
        item_list = db.query(*select_fields)
        for join_args in joins:
            item_list = getattr(item_list, join_type)(*join_args)
        item_list = item_list.filter(filters).order_by(MarketData.timestamp.desc()).all()
        record_count = len(item_list)
        return item_list, record_count
    except SQLAlchemyError as e:
        raise DatabaseException(str(e))