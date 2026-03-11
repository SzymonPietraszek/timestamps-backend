from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta
import boto3
import os

router = APIRouter(prefix="/timestamps")

TABLE_NAME = os.getenv("TABLE_NAME", "timestamps")
VALID_ACTIONS = ["l", "p", "lek"]
VALID_DELAYS = [0, 5, 10, 15, 20, 25, 30]

BLOCK_SECONDS = 60

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


class TimestampRequest(BaseModel):
    action: str
    delay: int


@router.post("/")
def add_timestamp(data: TimestampRequest):

    if data.action not in VALID_ACTIONS:
        raise HTTPException(status_code=400, detail="Nieprawidłowa akcja")

    if data.delay not in VALID_DELAYS:
        raise HTTPException(status_code=400, detail="Nieprawidłowy delay")

    now = datetime.now()

    table.put_item(
        Item={
            "pk": data.action,
            "timestamps": create_timestamp_list(now, data.action, data.delay),
            "last_write_at": now.isoformat(),
        }
    )

    return {"status": "ok"}


def create_timestamp_list(now: datetime, action: str, delay: int) -> List[str]:
    new_timestamp = (now - timedelta(minutes=delay)).isoformat(timespec="seconds")

    item = table.get_item(Key={"pk": action}).get("Item")

    if not item:
        return [new_timestamp]

    timestamps = item.get("timestamps")
    last_write_at = datetime.fromisoformat(item.get("last_write_at"))

    if (now - last_write_at).total_seconds() < BLOCK_SECONDS:
        timestamps[0] = new_timestamp
    else:
        timestamps.insert(0, new_timestamp)

    if len(timestamps) > 1 and timestamps[0] < timestamps[1]:
        raise HTTPException(
            status_code=400,
            detail="Nowy wpis musi być nowszy niż ostatni",
        )

    return timestamps[:5]


@router.get("/")
def get_all() -> Dict[str, List[str]]:
    result = {}

    for action in VALID_ACTIONS:
        item = table.get_item(Key={"pk": action}).get("Item")
        if item:
            result[action] = item.get("timestamps", [])

    return result
