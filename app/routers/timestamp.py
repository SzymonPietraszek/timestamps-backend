from fastapi import APIRouter
from typing import List, Dict
import boto3
import os

router = APIRouter()

TABLE_NAME = os.getenv("TABLE_NAME", "timestamps")
VALID_ACTIONS = ["l", "p", "lek"]
VALID_DELAYS = [0, 5, 10, 15, 20, 25, 30]

BLOCK_SECONDS = 60

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


@router.get("/timestamp")
def get_all() -> Dict[str, List[str]]:
    result = {}

    for action in VALID_ACTIONS:
        item = table.get_item(Key={"pk": action}).get("Item")
        if item:
            result[action] = item.get("timestamps", [])

    return result
