import boto3
import os
from fastapi import APIRouter

router = APIRouter()

TABLE_NAME = os.environ["TABLE_NAME"]
TABLE_PK = os.environ["TABLE_PK"]
TABLE_PK_VALUE = "data"
TABLE_DATA_VALUE = "value"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


@router.get("/dynamo")
async def read_dynamo():
    item = table.get_item(Key={TABLE_PK: TABLE_PK_VALUE})
    return {
        "message": "Hello World from Dynamo!",
        "data": item.get("Item", {}).get(TABLE_DATA_VALUE, "Not set"),
    }


@router.post("/dynamo")
async def write_dynamo(value: str):
    table.put_item(
        Item={
            TABLE_PK: TABLE_PK_VALUE,
            TABLE_DATA_VALUE: value,
        }
    )
    return {"message": f"Value set successfully to {value}"}
