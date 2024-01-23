"""DB module
"""
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''save the user to the database'''
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''Find and return the first user in the database
        based on input arguments'''
        try:
            query = self._session.query(User).filter_by(**kwargs)
            user = query.first()
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        '''Update user attributes based on input arguments
        and commit changes to the database'''
        try:
            user_to_update = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user_to_update, key):
                    setattr(user_to_update, key, value)
                else:
                    raise ValueError(f"Invalid argument: {key}")

            self._session.commit()
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise
