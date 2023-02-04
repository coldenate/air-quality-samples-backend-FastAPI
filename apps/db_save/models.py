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
    tvoc: int | None | str = None
    co2: int | None | str = None
    pm25: int | None = None
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
        self.tvoc = json_digest["tvoc"]
        self.co2 = json_digest["co2"]
        self.pm25 = json_digest["pm25"]
        self.room_location = room_dict[json_digest["room_num"]]
        self.temperature = json_digest["temperature"]
        self.humidity = json_digest["humidity"]


class ResponseModel(BaseModel):
    """A model for the responses to the survey questions. Example input:
    {
        "consent_question": "True",
        "email_address": "n8sol022@gmail.com",
        "room_num": "241",
        "fatigue": 3,
        "distractions": "True",
        "meds": "True",
        "subs": "True",
        "discomfort": "True",
        "sleep": "False",
        "reaction_time_ms": -8,
        "visual_mem_level": 12,
        "aiming_reaction_ms": 2,
        "chimp_score": 12
    }
    """

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    consent_question: bool = None  # type: ignore
    email_address: str = None  # type: ignore
    room_num: int = None  # type: ignore
    fatigue: int = None  # type: ignore
    distractions: bool = None  # type: ignore
    meds: bool = None  # type: ignore
    subs: bool = None  # type: ignore
    discomfort: bool = None  # type: ignore
    sleep: bool = None  # type: ignore
    reaction_time_ms: int = None  # type: ignore
    visual_mem_level: int = None  # type: ignore
    aiming_reaction_ms: int = None  # type: ignore
    chimp_score: int = None  # type: ignore

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
