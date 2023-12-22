from pathlib import Path

from fastapi import FastAPI, Depends
import psycopg2
import uvicorn
import os
import yaml
from dotenv import load_dotenv
from src.crud import get_feed, get_user

app = FastAPI()


def config():
    with open(Path(__file__).parent.parent / 'params.yaml', 'r') as f:
        return yaml.safe_load(f)


def get_db():
    with psycopg2.connect(
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"]
    ) as conn:
        return conn


@app.get("/user/feed")
def get_user_feed(user_id: int, limit: int = 10, conn=Depends(get_db), config: dict = Depends(config)):
    return get_user(user_id, limit, conn, config)


@app.get("/user/")
def get_all_users(limit: int = 10, conn=Depends(get_db)):
    return get_feed(limit, conn)


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run(app)
