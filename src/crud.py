def get_feed(limit, conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * 
            FROM "user"
            LIMIT %(limit_user)s
            """, {'limit_user': limit})
        return cursor.fetchall()


def get_user(user_id, limit, conn, config):
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
