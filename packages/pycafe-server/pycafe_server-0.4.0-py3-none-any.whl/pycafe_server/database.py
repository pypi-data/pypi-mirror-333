import datetime
import logging
import threading
import time
import uuid
from sqlalchemy import func

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from . import config

logger = logging.getLogger(__name__)
use_database = True
instance_id: str | None = None


class Base(DeclarativeBase):
    pass


engine = create_engine(config.PYCAFE_SERVER_DATABASE_URL, echo=True)
Session = sessionmaker(engine, expire_on_commit=False)

from sqlalchemy import Column, String, Boolean, DateTime, JSON, Integer


class Login(Base):
    __tablename__ = "logins"

    user_id = Column(String, primary_key=True)
    datetime = Column(DateTime, primary_key=True)
    email = Column(String)
    userinfo = Column(JSON)
    is_editor = Column(Boolean)
    is_admin = Column(Boolean)


class InstanceTable(Base):
    __tablename__ = "instance_id"

    # a unique column, so we can easily only store 1 row
    id = Column(Integer, primary_key=True, default=1)
    unique_id = Column(String, unique=True)  # Stores a unique UUID


def create_and_get_instance_id():
    session = Session()
    with session.begin():
        # Generate a new UUID
        unique_id = str(uuid.uuid4())

        # Try to insert the row with the default id=1
        singleton_row = InstanceTable(unique_id=unique_id)
        try:
            session.add(singleton_row)
            session.commit()
        except Exception:
            # Roll back the transaction if row already exists
            session.rollback()
            print("Row already exists; skipping insert.")
    with session.begin():
        # get the unique number
        rows = session.query(InstanceTable).all()
        assert len(rows) == 1
        unique_id = rows[0].unique_id
        return unique_id


last_cleanup = datetime.datetime.now()
# max 3 month log retention
max_log_age = datetime.timedelta(weeks=4 * 3)
cleanup_interval = datetime.timedelta(hours=1)
# useful for testing:
# max_log_age = datetime.timedelta(seconds=10)
cleanup_lock = threading.Lock()


def cleanup():
    global last_cleanup
    session = Session()
    with session:
        with session.begin():
            should_be_deleted_datetime = datetime.datetime.now() - max_log_age
            session.query(Login).filter(
                Login.datetime < should_be_deleted_datetime
            ).delete()
            last_cleanup = datetime.datetime.now()
            logger.info("Cleaned up login database")


def cleanup_task():
    global last_cleanup
    while True:
        try:
            cleanup()
        except Exception:
            logger.exception("Failed to cleanup database, trying again in 1 minute")
            time.sleep(60)
        else:
            sleep_time_seconds = cleanup_interval.total_seconds()
            time.sleep(sleep_time_seconds)


threading.Thread(target=cleanup_task, daemon=True).start()


def log_login(id: str, email: str, is_editor: bool, is_admin: bool, userinfo: dict):
    if not use_database:
        return
    session = Session()
    with session:
        with session.begin():
            login = Login(
                user_id=id,
                email=email,
                # we do not store userinfo for now
                # userinfo=userinfo,
                userinfo={},
                datetime=datetime.datetime.now(),
                is_editor=is_editor,
                is_admin=is_admin,
            )
            session.add(login)


def get_all_logins():
    session = Session()
    with session:
        with session.begin():
            logins = session.query(Login).all()
            return logins


def get_logins():
    session = Session()
    with session:
        with session.begin():
            # Subquery to find the latest datetime per day for each user_id
            subquery = (
                session.query(
                    Login.user_id,
                    func.date(Login.datetime).label("login_date"),
                    func.max(Login.datetime).label("max_datetime"),
                )
                .group_by(Login.user_id, func.date(Login.datetime))
                .subquery()
            )

            # Join the Login table with the subquery on user_id and datetime
            logins = (
                session.query(Login)
                .join(
                    subquery,
                    (Login.user_id == subquery.c.user_id)
                    & (Login.datetime == subquery.c.max_datetime),
                )
                .all()
            )

            return logins


def init():
    Base.metadata.create_all(bind=engine)


try:
    init()
    instance_id = create_and_get_instance_id()
    print("Instance ID:", instance_id)
except Exception:
    use_database = False
    logger.exception("Failed to initialize database")
