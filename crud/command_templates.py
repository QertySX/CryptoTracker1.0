class Command:
    async def execute(self, *args, **kwargs):
        raise NotImplementedError()