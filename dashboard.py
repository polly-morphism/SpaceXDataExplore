import cx_Oracle
import re
import chart_studio
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio.dashboard_objs as dashboard

username = 'dummy'
password = 'dummy'
database = 'localhost:1521/xe'

connection = cx_Oracle.connect(username, password, database)

query1 = '''
SELECT COUNT(*) AS num_of_missions, Customers.name as customer_name
from Missions
    JOIN Customers
    ON Missions.customer_id = Customers.customer_id
GROUP BY Customers.name
ORDER BY num_of_missions DESC;
'''

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
query3 = '''
SELECT COUNT(*) AS num_of_missions,  EXTRACT(YEAR FROM missions.launch_date) as launch
FROM Missions
GROUP BY EXTRACT(YEAR FROM missions.launch_date)
ORDER BY launch;
'''
cursor = connection.cursor()
cursor.execute(query1)

result1 = cursor.fetchall()


cursor.execute(query2)
result2 = cursor.fetchall()

cursor.execute(query3)
result3 = cursor.fetchall()


chart_studio.tools.set_credentials_file(username='pollymorphism', api_key='uIgsM6xLSnTFjhoHpOVz')

launch_count= list(map(lambda x: x[0], result1))
customers = list(map(lambda x: x[1], result1))
bar = go.Bar(x=customers, y=launch_count, marker_color='blue', name="Кількість запусків")
layout = go.Layout(
    title='Кількість запусків',
    xaxis=dict(
        title='Компанія',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Запуски',
        rangemode='nonnegative',
        autorange=True,
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=bar, layout=layout)
launches = py.plot(fig, filename='launches')


count_lounches= list(map(lambda x: x[0], result3))
year = list(map(lambda x: x[1], result3))
bar = go.Bar(x=year, y=count_lounches, marker_color='red', name="Кількість запусків")
layout = go.Layout(
    title='Кількість запусків',
    xaxis=dict(
        title='Рік',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Запуски',
        rangemode='nonnegative',
        autorange=True,
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=bar, layout=layout)
launches_by_year = py.plot(fig, filename='launches_by_year')

sum_lounches = 37

count_lounches= list(map(lambda x: x[0], result2))
company = list(map(lambda x: x[2], result2))

sum_all = 37


pie = go.Pie(labels=company, values=[i/sum_all for i in count_lounches],
             textinfo='percent', title="Відсоток запусків по організаціям")
success_percent = py.plot([pie], filename='Pie')


def fileId_from_url(url):
    fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1:]
    print(url)
    return fileId.replace('/', ':')

my_dboard = dashboard.Dashboard()

launches_id = fileId_from_url(launches)
launches_by_year_id = fileId_from_url(launches_by_year)
success_percent_id = fileId_from_url(success_percent)

box1= {
    'type': 'box',
    'boxType': 'plot',
    'fileId': launches_id,
    'title': 'Кількість запусків'
}

box2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': launches_by_year_id,
    'title': 'Кілість запусків по роках'
}

box3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': success_percent_id,
    'title': 'Кількість прийнятих турнірів містом'
}


my_dboard.insert(box1)
my_dboard.insert(box2, 'below', 1)
my_dboard.insert(box3, 'left', 2)

py.dashboard_ops.upload(my_dboard, 'Dashboard')
