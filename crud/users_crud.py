from create_db import async_session
from models.models import User
import bcrypt


class AddUserInDb:
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        

    async def execute(self):
        hashed_password = bcrypt.hashpw(
            self.password_hash.encode('utf-8'), 
            bcrypt.gensalt()
        )
        
        async with async_session() as session:
            new_user = User(
                username = self.username,
                email = self.email,
                password_hash = hashed_password
            )
            session.add(new_user)
            await session.commit()
            return new_user
