
import datetime
from common.database.base import SessionLocal

start_timestamp = datetime.datetime(2020, 7, 20, 0, 0)
end_timestamp = datetime.datetime(2020, 7, 23, 0, 0)

db = SessionLocal()
