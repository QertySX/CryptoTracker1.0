from command_templates import Command

'''Доработать все crud-методы на основе паттерна Command'''

class AddUserCommand(Command):
    def __init__(self, session, username, email, password_hash):
        self.session = session
        self.username = username
        self.email = email
        self.password_hash = password_hash

    async def execute(self):
        new_user = User(
            username = self.username,
            email = self.email,
            password_hash = self.password_hash
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

        