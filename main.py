import boto3

from typing import Optional as O

from pydantic import BaseSettings, BaseConfig, Field

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request, Response, File, UploadFile, HTTPException

from fastapi.staticfiles import StaticFiles

from aiohttp import ClientSession

from aiofauna import *

from aioboto3 import Session



class Env(BaseSettings):

    class Config(BaseConfig):

        env_file = ".env"

        env_file_encoding = "utf-8"


    AUTH0_DOMAIN: str = Field(..., env="AUTH0_DOMAIN")

    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")

    AWS_SECRET_ACCESS_KEY: str = Field(default="2de26e97e07ca6eb3759f9d59d87dc07aff462bd62a9f2ace9c2d6c9f9beb8b6")

    AWS_ENDPOINT_URL: str = Field(..., env="AWS_ENDPOINT_URL")

    AWS_S3_BUCKET: str = Field(..., env="AWS_S3_BUCKET")

    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")

    FAUNA_SECRET: str = Field(..., env="FAUNA_SECRET")



env = Env()



class HUser(AioModel):

    email: str = Field(default=None, index=True)

    email_verified: bool = Field(default=False)

    family_name: O[str] = Field(default=None)

    give_name: O[str] = Field(default=None)

    locale: O[str] = Field(default=None)

    name: str = Field(..., index=True)

    nickname: O[str] = Field(default=None)

    picture: O[str] = Field(default=None)

    sub: str = Field(..., unique=True)

    updated_at: O[str] = Field(default=None)


class Record(AioModel):

    user: int = Field(..., index=True)

    key: str = Field(..., unique=True)

    duration: O[int] = Field(default=None, index=True)

    url: str = Field(..., unique=True)

    content_type: str = Field(..., index=True)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["http://localhost:3000"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)



@app.get("/api/auth")

async def authorize(token: str):
    """

    Temporary endpoint to authorize users
    """

    async with ClientSession() as session:

        async with session.get(

            f"https://{env.AUTH0_DOMAIN}/userinfo",

            headers={"Authorization": f"Bearer {token}"},
        ) as response:

            user = HUser(**await response.json())

            return await user.create()

@app.get("/api/records/delete")
async def delete_record(key: str):
    """

    Deletes a record by key
    """
    instance = await Record.find_unique("key",key)
    if instance is not None and isinstance(instance.ref, int):
        return await Record.delete(instance.ref)
    raise HTTPException(status_code=404, detail="Record not found")

@app.get("/api/records")
async def get_records(uid: int):
    """

    Get a list of records for a user
    """

    return await Record.find_many("user",uid)


@app.post("/api/upload")
async def upload_sample(uid: int, file: UploadFile = File(...)):
    """

    Upload a sample to S3 and create a record in FaunaDB
    """
    session = Session()

    async with session.client(

        "s3",

        endpoint_url=env.AWS_ENDPOINT_URL,

        aws_access_key_id=env.AWS_ACCESS_KEY_ID,

        aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
        
        config=boto3.session.Config(signature_version="s3v4", region_name=env.AWS_REGION)) as client:

        _file = await file.read()

        _key = f"{uid}/{str(uuid4())}/{file.filename}"
        
        await client.put_object(

            Bucket=env.AWS_S3_BUCKET, Key=_key, Body=_file
        )

        url = await client.generate_presigned_url(

            "get_object",

            Params={"Bucket": env.AWS_S3_BUCKET, "Key": _key},

            ExpiresIn=3600 * 24 * 7,
        )

        if file.content_type is not None:
            sample = Record(
                user=uid,

                key=_key,
                url=url,

                content_type=file.content_type,
            )

            return await sample.create()
        sample = Record(
            user=uid,

            key=_key,
            url=url,

            content_type="application/octet-stream",
        )

        return await sample.create()


app.mount("/", StaticFiles(directory="static",html=True), name="static")


#@app.on_event("startup")
async def startup():

    await HUser.provision()

    await Record.provision()


if __name__ == "__main__":

    import uvicorn


    uvicorn.run(app, host="0.0.0.0", port=8080)

