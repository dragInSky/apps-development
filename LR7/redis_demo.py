from __future__ import annotations

import os

import redis


def main() -> None:
    client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        db=int(os.getenv("REDIS_DB", "0")),
        decode_responses=True,
    )

    try:
        client.ping()
        print("Успешное подключение к Redis")
    except redis.ConnectionError:
        print("Ошибка подключения к Redis")
        return

    print("\n== Строки ==")
    client.set("user:name", "Иван")
    print("user:name =", client.get("user:name"))

    client.setex("session:123", 3600, "active")
    print("session:123 =", client.get("session:123"), "(TTL:", client.ttl("session:123"), ")")

    client.set("counter", 0)
    client.incr("counter")
    client.incrby("counter", 5)
    client.decr("counter")
    print("counter =", client.get("counter"))

    print("\n== Списки ==")
    client.delete("tasks")
    client.lpush("tasks", "task1", "task2")
    client.rpush("tasks", "task3", "task4")
    print("tasks =", client.lrange("tasks", 0, -1))
    print("lpop =", client.lpop("tasks"))
    print("rpop =", client.rpop("tasks"))
    print("len =", client.llen("tasks"))

    print("\n== Множества ==")
    client.delete("tags", "languages")
    client.sadd("tags", "python", "redis", "database")
    client.sadd("languages", "python", "java", "javascript")
    print("tags has python =", client.sismember("tags", "python"))
    print("tags =", sorted(client.smembers("tags")))
    print("intersection =", sorted(client.sinter("tags", "languages")))
    print("union =", sorted(client.sunion("tags", "languages")))
    print("diff tags-languages =", sorted(client.sdiff("tags", "languages")))

    print("\n== Хэши ==")
    client.delete("user:1000")
    client.hset(
        "user:1000",
        mapping={
            "name": "Иван",
            "age": "30",
            "city": "Москва",
        },
    )
    print("user:1000 name =", client.hget("user:1000", "name"))
    print("user:1000 all =", client.hgetall("user:1000"))
    print("user:1000 has email =", client.hexists("user:1000", "email"))
    print("keys =", client.hkeys("user:1000"))
    print("values =", client.hvals("user:1000"))

    print("\n== Упорядоченные множества ==")
    client.delete("leaderboard")
    client.zadd(
        "leaderboard",
        {
            "player1": 100,
            "player2": 200,
            "player3": 150,
        },
    )
    print("top =", client.zrange("leaderboard", 0, 2, withscores=True))
    print("by_score 100..200 =", client.zrangebyscore("leaderboard", 100, 200))
    print("rank player1 =", client.zrank("leaderboard", "player1"))


if __name__ == "__main__":
    main()

