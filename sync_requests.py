import datetime

import requests


def get_people(people_id):
    return requests.get(f'https://swapi.py4e.com/api/people/{people_id}/').json()


def main():
    responce_1 = get_people(1)
    responce_2 = get_people(2)
    responce_3 = get_people(3)
    responce_4 = get_people(4)
    print(responce_1, responce_2, responce_3, responce_4)



start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)