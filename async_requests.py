import asyncio
import aiohttp
import datetime

from more_itertools import chunked
from models import init_orm, close_orm, Session, SwapiPeople


MAX_COROS = 5

async def get_people_info(people_id, session):
    response = await session.get(f'https://swapi.py4e.com/api/people/{people_id}/')
    json_data = await response.json()
    films_list = []
    species_list = []
    starships_list = []
    vehicles_list = []
    for item in json_data:
        if 'name' in item:
            for i in json_data['films']:
                response = await session.get(i)
                json_data_film = await response.json()
                json_data['films'] = json_data_film['title']
                films_list.append(json_data['films'])
            json_data['films'] = films_list
            for i in json_data['species']:
                response = await session.get(i)
                json_data_species = await response.json()
                json_data['species'] = json_data_species['name']
                species_list.append(json_data['species'])
            json_data['species'] = species_list
            for i in json_data['starships']:
                response = await session.get(i)
                json_data_starships = await response.json()
                json_data['starships'] = json_data_starships['name']
                starships_list.append(json_data['starships'])
            json_data['starships'] = starships_list
            for i in json_data['vehicles']:
                response = await session.get(i)
                json_data_vehicles = await response.json()
                json_data['vehicles'] = json_data_vehicles['name']
                vehicles_list.append(json_data['vehicles'])
            json_data['vehicles'] = vehicles_list
    return json_data


async def insert_to_database(list_json: list[dict]):
    async with Session() as session:
        for item in list_json:
            objects = []
            if 'name' in item:
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
