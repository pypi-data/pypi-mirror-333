import asyncio
from freeapihub import get_all_users, get_user_by_id

async def test():
    users = await get_all_users()
    print(users)

    user = await get_user_by_id("123")
    print(user)

asyncio.run(test())
