import configparser
import logging
import sqlalchemy.ext.declarative as sed
import sqlalchemy
import sqlalchemy.orm
from telethon.sync import TelegramClient, events

# Импортируем конфигурационный файл
from telethon.tl import types

import database as db
import strings

config = configparser.ConfigParser()
config.read("config.ini")
log = logging.getLogger("core")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# Создаем подключение к базе данных
log.debug("Creating the sqlalchemy engine...")
engine = sqlalchemy.create_engine(config["Database"]["engine"])
log.debug("Binding metadata to the engine...")
db.TableDeclarativeBase.metadata.bind = engine
log.debug("Creating all missing tables...")
db.TableDeclarativeBase.metadata.create_all()
log.debug("Preparing the tables through deferred reflection...")
sed.DeferredReflection.prepare(engine)

# Создание объекта клиента Telegram
client = TelegramClient(username, int(api_id), api_hash)

# Запуск клиента
client.start()


# Событие на новое входящее сообщение
@client.on(events.NewMessage(incoming=True, forwards=None))
async def handler(event):
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    users = session.query(db.User).all()
    sender = await event.get_input_sender()
    entity = await client.get_entity(sender.user_id)
    if isinstance(event.original_update, types.UpdateShortMessage):
        if sender.user_id not in [user.user_id for user in users]:
            await event.reply(strings.greeting, parse_mode='html')
            new_user = db.User(
                user_id=entity.id,
                first_name=entity.first_name,
                last_name=entity.last_name,
                username=entity.username,
                phone_number=entity.phone
            )
            session.add(new_user)
            session.commit()
            session.close()

client.run_until_disconnected()
