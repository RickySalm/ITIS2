import psycopg2


connection = psycopg2.connect(
    host='localhost',
    database='CRUD',
    user='postgres',
    password='BARSIKETOZLO'
)

cur = connection.cursor()

"INSERT INTO posts (title, content) VALUES (?, ?)"
"alter table"
"alter column"
"updates"
"select"

cur.execute('CREATE TABLE products ('
            'id serial PRIMARY KEY,'
            'uploaded time with time zone DEFAULT CURRENT_TIMESTAMP,'
            'name varchar NOT NULL,'
            'description varchar NOT NULL,'
            'price int NOT NULL'
            ');'
            )

sql_command = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
data = ('banana', 'bananaaaa', 100)

cur.execute(sql_command, data)

connection.commit()
connection.close()
