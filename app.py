from fastapi import FastAPI, Depends
import psycopg2
import uvicorn
from psycopg2.extras import RealDictCursor
import os
import yaml
from dotenv import load_dotenv

app = FastAPI()


def config():
    with open('params.yaml', 'r') as f:
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
    with conn.cursor() as cursor:
        cursor.execute("""
        SELECT *
        FROM feed_action
        WHERE user_id = %(user_id)s AND time >= %(start_date)s
        ORDER BY time
        LIMIT %(limit)s
        """,
                       {'user_id': user_id, 'limit': limit, 'start_date': config['feed_start_date']})
        return cursor.fetchall()


@app.get("/user/")
def get_all_users(limit: int = 10, conn=Depends(get_db)):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
        SELECT * 
        FROM "user"
        LIMIT %(limit_user)s
        """, {'limit_user': limit})
        return cursor.fetchall()


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run(app)
