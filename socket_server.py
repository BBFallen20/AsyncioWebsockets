import asyncio
import websockets


USERS = set()


async def addUser(websocket):
    # Метод добавления пользователя в глобальный список
    USERS.add(websocket)


async def removeUser(websocket):
    # Метод удаления пользователя(при окончании работы сервера)
    USERS.remove(websocket)


async def socket(websocket, path):
    # При подключении пользователя добавляем его в глобальный список
    await addUser(websocket)

    try:
        while True:
            # Создаем так называемый POLLING - бесконечный цикл, который слушает сообщения по порту и отсылает
            # их всем записаным пользователям
            message = await websocket.recv()

            await asyncio.wait([user.send(f"{message}") for user in USERS])
    finally:
        await removeUser(websocket)


start_server = websockets.serve(socket, '127.0.0.1', 8001)

# Зацыкливаем работу сервера с помощью asyncio
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
