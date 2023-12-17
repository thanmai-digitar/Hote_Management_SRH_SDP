import mysql.connector

class MySQLCRUD:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="krithicka",
            database='sdp_new'
        )
        self.mycursor = self.mydb.cursor()

    def create(self, table, columns, values):
        placeholders = ", ".join(["%s"] * len(values))
        column_names = ", ".join(columns)
        sql = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        # Convert values to a list
        values_list = list(values)
        self.mycursor.execute(sql, values_list)
        self.mydb.commit()
        return self.mycursor.lastrowid

    def read(self, table, columns="*", conditions=""):
        column_names = ", ".join(columns) if isinstance(columns, (list, tuple)) else columns
        sql = f"SELECT {column_names} FROM {table} {conditions}"
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def update(self, table, updates, conditions):
        update_string = ", ".join([f"{k} = %s" for k in updates])
        values = list(updates.values())
        sql = f"UPDATE {table} SET {update_string} WHERE {conditions}"
        self.mycursor.execute(sql, values)
        self.mydb.commit()
        return self.mycursor.rowcount

    def delete(self, table, conditions):
        sql = f"DELETE FROM {table} WHERE {conditions}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        return self.mycursor.rowcount

    def close(self):
        self.mycursor.close()
        self.mydb.close()