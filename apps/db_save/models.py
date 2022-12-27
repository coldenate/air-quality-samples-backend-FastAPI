import datetime
import uuid
from pydantic import BaseModel, Field
from .values.locations import classes_values as room_dict


class EntryModel(BaseModel):
    """A class describing an object with the following attributes: room num, timestamp, raw VOC, raw PM2.5, and the Room Location, and temperature+humidity Room location will be a predefined environment variable."""

    # model for all data entries. Construct this class whenever a JSON is received at the route /entry
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    room_num: int = None  # type: ignore
    timestamp: str | datetime.datetime | None = None  # type: ignore
    raw_voc: int | None | str = None
    raw_pm25: int | None = None
    temperature: int | None = None
    humidity: int | None = None



    def digest_json(self, json_digest):
        """Digest the JSON and populate the fields"""
        # example json
        # {
        #     "room_num": ,
        #     "timestamp": "2020-10-10 10:10:10",
        #     "raw_voc": 100,
        #     "raw_pm25": 100,
        #     "temperature": 100, # in degrees celsius
        #     "humidity": 100,
        #
        # }
        self.room_num = json_digest["room_num"]
        self.timestamp = json_digest["timestamp"]
        self.raw_voc = json_digest["raw_voc"]
        self.raw_pm25 = json_digest["raw_pm25"]
        self.room_location = room_dict[json_digest["room_num"]]
        self.temperature = json_digest["temperature"]
        self.humidity = json_digest["humidity"]

    # class Config:
    #     allow_population_by_field_name = True


# class UpdateTaskModel(BaseModel):
#     name: Optional[str]
#     completed: Optional[bool]

#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "My important task",
#                 "completed": True,
#             }
#         }
