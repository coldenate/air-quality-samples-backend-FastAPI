import datetime
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .models import EntryModel  # pylint: disable=relative-beyond-top-level
from .models import ResponseModel  # pylint: disable=relative-beyond-top-level

from .models import EntryModel  # pylint: disable=relative-beyond-top-level

from .values.locations import classes_values as room_dict

entry_router = APIRouter()
response_router = APIRouter()


@response_router.post(
    "/create", response_description="Create a new response in the database"
)
async def create_response(request: Request, response: ResponseModel= Body(...)):
    """Create a new response in the database"""
    response_json = jsonable_encoder(response)
    new_response = await request.app.mongodb["surveys"].insert_one(response_json)
    created_response = await request.app.mongodb["surveys"].find_one(
        {"_id": new_response.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_response)


@entry_router.post("/entry", response_description="Add new entry to the database")
async def create_entry(request: Request, entry: EntryModel = Body(...)) -> JSONResponse:
    """Create a new entry in the database"""
    entry_json = jsonable_encoder(entry)
    # if isinstance(entry_json["timestamp"], str):
    #     # convert to datetime object
    #     entry_json["timestamp"] = datetime.datetime.strptime(
    #         entry_json["timestamp"], "%Y-%m-%d %H:%M:%S"
    #     )
    # we create our own timestamp
    entry_json["timestamp"] = datetime.datetime.now()
    entry_json["room_location"] = room_dict[entry_json["room_num"]]
    new_entry = await request.app.mongodb["measurements"].insert_one(entry_json)
    created_entry = await request.app.mongodb["measurements"].find_one(
        {"_id": new_entry.inserted_id}
    )
    created_entry["timestamp"] = str(created_entry["timestamp"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_entry)


@entry_router.get("/entries", response_description="List all entries")
async def list_entries(request: Request):
    """List all entries in the database"""
    entries = []
    for doc in await request.app.mongodb["measurements"].find().to_list(length=100):
        entries.append(doc)
    return entries


# @router.get("/{id}", response_description="Get a single task")
# async def show_task(id: str, request: Request):
#     if (task := await request.app.mongodb["tasks"].find_one({"_id": id})) is not None:
#         return task

#     raise HTTPException(status_code=404, detail=f"Task {id} not found")


# @router.put("/{id}", response_description="Update a task")
# async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
#     task = {k: v for k, v in task.dict().items() if v is not None}

#     if len(task) >= 1:
#         update_result = await request.app.mongodb["tasks"].update_one(
#             {"_id": id}, {"$set": task}
#         )

#         if update_result.modified_count == 1:
#             if (
#                 updated_task := await request.app.mongodb["tasks"].find_one({"_id": id})
#             ) is not None:
#                 return updated_task

#     if (
#         existing_task := await request.app.mongodb["tasks"].find_one({"_id": id})
#     ) is not None:
#         return existing_task

#     raise HTTPException(status_code=404, detail=f"Task {id} not found")


@entry_router.delete("/{id}", response_description="Delete Task")
async def delete_entry(id: str, request: Request) -> JSONResponse:
    delete_result = await request.app.mongodb["measurements"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
