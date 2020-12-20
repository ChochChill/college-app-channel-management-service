from fastapi import FastAPI,APIRouter,HTTPException
from app.database.schema import Channel
# , Change_channel
from bson.objectid import ObjectId
channelsRouter = APIRouter() 
from app.config.config import channel_DB
from bson import ObjectId
import datetime

def fetch_channels():
    """
    Args : none

    Fetching all the channels from the database

    Return type : List
    """
    channels_list = []
    query = channel_DB().find({"type":"public"})
    for x in query:
        channels_list.append(Channel(**x))
        print(type(x))
        # x['id']=str(x['_id'])
        # x.pop("_id")
        print(x)
    return channels_list

# def fetch_channel(id):
#     req_channel=[]
#     query = channel_DB().find_one({"_id": ObjectId(id)})
#     for x in query:
#         req_channel.append(Channel(**x))
#         x.pop("_id")
#     return 

def create_channel(channel: Channel) -> Channel:
    """
    Args : channel -> Channel

    creates new channel in the database

    return type : list

    """
    if hasattr(channel, 'id'):
        delattr(channel, 'id')
    channel.created_at= datetime.datetime.now()
    # channel.id= str(uuid.uuid4())
    newChannel = channel_DB().insert_one(channel.dict(by_alias=True))
    channel.id = newChannel.inserted_id
    return {'channel': channel}    

# def update_channel(id: str, new_data: Change_channel) -> Channel:
#     print(new_data)
#     check_channel = channel_DB().find_one({"_id": ObjectId(id)})
#     print(check_channel)
#     updated_channel = channel_DB().update_one({"_id": ObjectId(id)}, {"$set": new_data})
#     return "channel is updated"

#custom exception 
#https://www.programiz.com/python-programming/user-defined-exception
class Error(Exception):
    """Base class for other exceptions"""
    pass

class RandomError(Error):
    """Raised when the channel is not found"""
    pass

def remove_channel(id: str):
    """
    Args:
    id -> string

    deletes a channel from the database

    return type: string
    """
    try:
        delChannel=channel_DB().delete_one({"_id":ObjectId(id)})
        if delChannel.deleted_count==0:
            raise  RandomError
        else:
            return("sueach_channelessfully deleted")

    except RandomError:
        print("Channel not found")
        return "channel not found"      

        