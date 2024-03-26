'''
curl -X POST -H "Content-Type: application/json" -d '{"username":"Alice"}' http://localhost:5000/add
To view the updated list of users, access http://localhost:5000 in your browser or use a GET request:curl http://localhost:5000
'''
import asyncio
import aiohttp

async def add_user(session, username):
    url = 'http://localhost:5000/add'
    data = {'username': username}
    async with session.post(url, json=data) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        users = ['messi']
        tasks = [add_user(session, user) for user in users]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)

if __name__ == '__main__':
    asyncio.run(main())
