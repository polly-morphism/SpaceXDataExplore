import cx_Oracle
import pandas as pd

username = "dummy"
password = "dummy"

connection = cx_Oracle.connect(username, password)

cursor = connection.cursor()


def execute_query_via_pd(query):
    SQL_Query = pd.read_sql_query(query, connection)
    return SQL_Query


def execute_query_via_cur(query):
    cursor.execute(query)
    data = pd.DataFrame(cursor.fetchall())
    return data


query1 = """
        SELECT num_of_missions, customer_name FROM missions_per_customer;
        """
print(query1)
data = execute_query_via_pd(query1)
print(data)


query2 = """
        SELECT all_missions, success_percentage, customer_name FROM all_missions_success_percentage;
"""
print(query2)
data = execute_query_via_pd(query2)
print(data)


query3 = """
        SELECT num_of_missions, launch FROM num_of_missions_per_year;
"""
print(query3)
data = execute_query_via_pd(query3)
print(data)


cursor.close()

connection.close()
