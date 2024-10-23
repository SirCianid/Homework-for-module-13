import asyncio

balls = 5


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования!')
    for balls_number in range(1, balls + 1):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {balls_number}-й шар!')
    print(f'Силач {name} закончил соревнования!')


async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Артур', 4))
    task2 = asyncio.create_task(start_strongman('Женя', 7))
    task3 = asyncio.create_task(start_strongman('Геракл', 15))
    await task1
    await task2
    await task3


asyncio.run(start_tournament())
