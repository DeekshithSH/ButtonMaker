import asyncio
import motor.motor_asyncio
from bson import ObjectId

from Bot.vars import Var
# from vars import Var
con= motor.motor_asyncio.AsyncIOMotorClient(Var.DATABASE_URL)
db=con["ButtonMaker"]
ObjectId().generation_time.isoformat

async def add_user(user_id: int):
    await db.user.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}},upsert=True)

async def save_button(id: str, user_id: int, msg_id: int):
    if not id:
        id=ObjectId()
    else:
        id=ObjectId(id)
    return (await db.button.update_one({"_id": id}, {"$set": {"_id": id, "user_id": user_id, "msg_id": msg_id}},upsert=True)).upserted_id

async def get_button(id: str=None, msg_id: int=None):
    if id:
        return await db.button.find_one({"_id": ObjectId(id)})
    elif msg_id:
        return await db.button.find_one({"msg_id": msg_id})
