file = [("access.log", ['%h', '%t', '%r', '%>s', '%b'])]
db_info = {
    #параметр : ваше значение
    'database': 'logdate',
    'user': 'postgres',
    'password': 'qwerty',
    'host': '127.0.0.1',
    'port': '5432'
}

create_table_query = '''
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(255),
    timestamp TIMESTAMP,
    method VARCHAR(255),
    url VARCHAR(255),
    status VARCHAR(255),
    user_agent VARCHAR(255)
);
'''