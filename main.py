import cx_Oracle
import pandas as pd

username = 'dummy'
password = 'dummy'

connection = cx_Oracle.connect(username, password)

cursor = connection.cursor()


def execute_query_via_pd(query):
    SQL_Query = pd.read_sql_query(query, connection)
    return SQL_Query

def execute_query_via_cur(query):
    cursor.execute(query)
    cursor.execute(query)
    data = pd.DataFrame(cursor.fetchall())
    return data


query1 = '''
SELECT COUNT(*) AS num_of_missions, Customers.name as customer_name
from Missions
    JOIN Customers
    ON Missions.customer_id = Customers.customer_id
GROUP BY Customers.name
ORDER BY num_of_missions DESC;
'''
print(query1)
data = execute_query_via_pd(query1)
print(data)


query2 = '''
SELECT all_missions, COALESCE((successfull_missions/all_missions)*100, 0) as success_percentage, missions_table.customer_name FROM
    (SELECT COUNT(*) AS all_missions, Customers.name as customer_name, customers.customer_id as cust_id
    FROM Missions
        JOIN Customers
        ON Missions.customer_id = Customers.customer_id
--        WHERE missions.mission_outcome <> 'Success'
    GROUP BY customers.customer_id, customers.name
    ) missions_table
    LEFT JOIN 
    (SELECT COUNT(*) AS successfull_missions, Customers.name as customer_name, customers.customer_id as cust_id
    FROM Missions
        JOIN Customers
        ON Missions.customer_id = Customers.customer_id
        WHERE missions.mission_outcome = 'Success'
    GROUP BY customers.customer_id, customers.name) success_missions_table
    ON missions_table.cust_id = success_missions_table.cust_id;

'''
print(query2)
data = execute_query_via_pd(query2)
print(data)



query3 = '''
SELECT COUNT(*) AS num_of_missions,  EXTRACT(YEAR FROM missions.launch_date) as launch
FROM Missions
GROUP BY EXTRACT(YEAR FROM missions.launch_date)
ORDER BY launch;
'''
print(query3)
data = execute_query_via_pd(query3)
print(data)


cursor.close()

connection.close()
