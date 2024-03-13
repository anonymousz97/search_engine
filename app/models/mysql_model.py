class MySQLModel:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='password',
            db='mydb'
        )
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns={}):
        query = f'CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, '
        for key, value in columns.items():
            query += f'{key} {value}, '
        query = query[:-2] + ')'
        self.cursor.execute(query)

    def get_articleId(self, table_name, article_id):
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE article_id={article_id}')
        return self.cursor.fetchone()

    def get_all_article(self, table_name='default'):
        self.cursor.execute(f'SELECT * FROM {table_name}')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def insert(self, table_name, data_list):
        columns = data_list[0].keys()
        values = [tuple(data.values()) for data in data_list]
        placeholders = ', '.join(['%s'] * len(columns))
        query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
        self.cursor.executemany(query, values)
        self.connection.commit()
        return self.cursor.rowcount

    def update(self, table_name, data_list):
        for data in data_list:
            query = f'UPDATE {table_name} SET '
            for key, value in data.items():
                query += f'{key} = {value}, '
            query = query[:-2] + f' WHERE id = {data["id"]}'
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.rowcount
    
    