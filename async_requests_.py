import asyncio
from asyncio import current_task

import aiohttp
import datetime
from more_itertools import chunked
from models import init_orm, close_orm, Session, SwapiPeople


MAX_COROS = 5

async def get_people(people_id, session):
    # print(f'step_1 {people_id=}')
    response = await session.get(f'https://swapi.py4e.com/api/people/{people_id}/')
    if response.status == 200:
        json_data = await response.json()
    # print(f'step_3 {people_id=} {json_data=}')
    # print(f'step_4 {people_id=} session.close')
        return json_data


async def insert_to_database(list_json: list[dict]):
    async with Session() as session:
        objects = [SwapiPeople(json=item) for item in list_json]        # Вместо кода ниже
        # objects = []
        # for item in list_json:
        #     swapi = SwapiPeople(json=item)      # В поле json ложим item
        #     objects.append(swapi)
        session.add_all(objects)
        await session.commit()


async def main():
    await init_orm()        # Открытие ORM
    # *1 tasks = []
    async with aiohttp.ClientSession() as session:
        for coros_chunk in chunked(range(15, 26), MAX_COROS):       # Создать списки по MAX_COROS от 1 до 100
            coros = [get_people(i, session) for i in coros_chunk]        # get_people(i) for i in coros_chunk - Вместо цикла for ниже
            # for i in coros_chunk:
            #     coro = get_people(i)
            #     coros.append(coro)
            result = await asyncio.gather(*coros)
            # *1 task = asyncio.create_task(insert_to_database(result))     # Вместо кода строки ниже - позволяет продолжить выполнение кода не дожидаясь выполнения кода после await
            # *1 tasks.append(task)
            # await insert_to_database(result)        # Вставляем result в базу
            # print(result)
            asyncio.create_task(insert_to_database(result))     # Вместо *1
    tasks = asyncio.all_tasks()     # Вместо *1
    current_task = asyncio.current_task()       # Вместо *1  / Извлечение текущей задачи на базе main/ Для исключения рекурсии
    tasks.remove(current_task)      # Вместо *1  / Удаление текущей задачи из всех задач / Для исключения рекурсии
    await asyncio.gather(*tasks)
    await close_orm()       # Закытие ORM


    # coro_1 = get_people(1)
    # coro_2 = get_people(2)
    # coro_3 = get_people(3)
    # coro_4 = get_people(4)
    # result = await asyncio.gather(coro_1, coro_2, coro_3, coro_4)
    # print(result)
    # print(len(result))

    # responce_1 = await get_people(1)
    # responce_2 = await get_people(2)
    # responce_3 = await get_people(3)
    # responce_4 = await get_people(4)
    # print(responce_1, responce_2, responce_3, responce_4)


    # response = await get_people(4)         # get_people_coro = get_people(4)
    # # print(f'{get_people_coro=}')
    # # response = await get_people_coro
    # print(f'{response=}')


start = datetime.datetime.now()
main_coro = main()
asyncio.run(main_coro)
print(datetime.datetime.now() - start)