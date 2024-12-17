import asyncio
import aiohttp
import datetime

from more_itertools import chunked
from models import init_orm, close_orm, Session, SwapiPeople


MAX_COROS = 5

async def get_people_info(people_id, session):
    response = await session.get(f'https://swapi.py4e.com/api/people/{people_id}/')
    # print(response.status)
    if response.status == 200:
        json_data = await response.json()
        # print(json_data['url'])
        list = ['films', 'species', 'starships', 'vehicles']
        for i in list:
            json_data[i] = await get_people_description(json_data[i], session)
            # print(f'json_data["i"] = {json_data[i]}')
        return json_data


async def get_people_description(links, session):
    json_data_temp = []
    for i in links:
        response = await session.get(i)
        data = await response.json()
        if 'name' in data:
            json_data_temp.append(data['name'])
        else:
            json_data_temp.append(data['title'])
    json_data = ', '.join(json_data_temp)
    return json_data


async def insert_to_database(list_json: list[dict]):
    async with Session() as session:
        for item in list_json:
            objects = []
            if item is not None:
                objects = [SwapiPeople(name=item['name'],
                                       height=item['height'],
                                       mass=item['mass'],
                                       hair_color=item['hair_color'],
                                       skin_color=item['skin_color'],
                                       eye_color=item['eye_color'],
                                       birth_year=item['birth_year'],
                                       gender=item['gender'],
                                       homeworld=item['homeworld'],
                                       films=item['films'],
                                       species=item['species'],
                                       vehicles=item['vehicles'],
                                       starships=item['starships'],
                                       created=item['created'],
                                       edited=item['edited'],
                                       url=item['url'])]

            session.add_all(objects)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:
        for coros_chunk in chunked(range(1, 100), MAX_COROS):
            coros = [get_people_info(i, session) for i in coros_chunk]
            result = await asyncio.gather(*coros)
            asyncio.create_task(insert_to_database(result))
    tasks = asyncio.all_tasks()
    current_task = asyncio.current_task()
    tasks.remove(current_task)
    await asyncio.gather(*tasks)
    await close_orm()


start = datetime.datetime.now()
main_coro = main()
asyncio.run(main_coro)
print(datetime.datetime.now() - start)
