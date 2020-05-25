from fakeredis import FakeRedis

redis_conn = FakeRedis()

# Set Add
v1 = 'dimensions/gameiq_taxonomy_level/genre_id.csv.gz'
v2 = 'dimensions/gameiq_taxonomy_level/unified_product_taxonomy.csv.gz'
redis_conn.sadd('a_set', v1)
redis_conn.sadd('a_set', v2)
print(redis_conn.sismember('a_set', v1))
print(redis_conn.smembers('a_set'))

# Pipeline Execute
# ...
