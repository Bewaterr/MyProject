import mysql.connector.pooling

__config = {
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"wq123",
    "database":"vege"
}
try:
    pool = mysql.connector.pooling.MySQLConnectionPool(
        **__config,
        pool_size=10
    )
except Exception as e:
    print(e)

