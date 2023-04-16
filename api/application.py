import boto3
import asyncio
import os
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Depends,
    Request,
    Response,
    status,
)
from aiohttp import ClientSession
from aiofauna import AioModel, AioClient, q, Optional
from aioboto3 import Session
from sse_starlette import EventSourceResponse
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

FAUNA_SECRET = os.getenv("FAUNA_SECRET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


class App(FastAPI):
    """
    This is a custom FastAPI class that adds some extra functionality.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "HHMC Rest API"
        self.description = "Esta es la API REST para HHMC (Hip Hop Movimiento Cultural)"
        self.version = "0.0.1"
        self.db = AioClient(FAUNA_SECRET)

    async def fetch(
        self,
        url: str,
        method: str = "GET",
        headers: dict = {"Content-Type": "application/json"},
        json: Optional[dict] = None,
    ):
        if method in ["GET", "DELETE"]:
            async with ClientSession() as session:
                async with session.request(method, url, headers=headers) as response:
                    return await response.json()
        elif method in ["POST", "PUT", "PATCH"]:
            async with ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=json
                ) as response:
                    return await response.json()

    async def stream(
        self,
        url: str,
        method: str = "GET",
        headers: dict = {"Content-Type": "application/json"},
        json: Optional[dict] = None,
    ):
        if method in ["GET", "DELETE"]:
            async with ClientSession() as session:
                async with session.request(method, url, headers=headers) as response:
                    async for chunk in response.content.iter_chunked(1024):
                        yield chunk
        elif method in ["POST", "PUT", "PATCH"]:
            async with ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=json
                ) as response:
                    async for chunk in response.content.iter_chunked(1024):
                        yield chunk

    def sse(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return EventSourceResponse(func(*args, **kwargs))

        return wrapper

    async def uploadFile(self, key: str, file: UploadFile = File(...)):
        session = Session()
        async with session.client(
            "s3",
            endpoint_url=AWS_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version="s3v4"),
        ) as client:
            await client.put_object(
                Bucket=AWS_S3_BUCKET,
                Key=key,
                Body=await file.read(),
                ContentType=file.content_type,
                ACL="public-read",
                ContentDisposition="inline",
            )
            return await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": AWS_S3_BUCKET, "Key": key},
                ExpiresIn=3600,
            )

    async def deleteFile(self, key: str):
        session = Session()
        async with session.client(
            "s3",
            endpoint_url=AWS_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version="s3v4"),
        ) as client:
            await client.delete_object(Bucket=AWS_S3_BUCKET, Key=key)
            return True

    async def getFiles(self, prefix: str):
        session = Session()
        async with session.client(
            "s3",
            endpoint_url=AWS_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version="s3v4"),
        ) as client:
            response = await client.list_objects_v2(Bucket=AWS_S3_BUCKET, Prefix=prefix)
            files = []
            if "Contents" in response:
                for file in response["Contents"]:
                    files.append(file["Key"])
            return await asyncio.gather(
                *[
                    client.generate_presigned_url(
                        "get_object",
                        Params={"Bucket": AWS_S3_BUCKET, "Key": file},
                        ExpiresIn=3600,
                    )
                    for file in files
                ]
            )

    async def authorize(self, token: str):
        url = f"https://{AUTH0_DOMAIN}/userinfo"
        headers = {"Authorization": f"Bearer {token}"}
        return await self.fetch(url, headers=headers)

    async def auth(self, request: Request):
        token = request.headers.get("Authorization")
        if token:
            return await self.authorize(token)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided"
            )
