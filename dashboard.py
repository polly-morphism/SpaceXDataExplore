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


chart_studio.tools.set_credentials_file(username='pollymorphism', api_key='c7t1ak32dm')

home_team = list(map(lambda x: x[0], result1))
matches = list(map(lambda x: x[1], result1))
bar = go.Bar(x=home_team, y=matches, marker_color='lightsalmon', name="Кількість запусків")
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



city = list(map(lambda x: x[0], result3))
tournament = list(map(lambda x: x[1], result3))
bar = go.Bar(x=city, y=tournament, marker_color='lightsalmon', name="Кількість запусків по рокам")
layout = go.Layout(
    title=
'Кількість успішних запусків',
    xaxis=dict(
        title='Рік',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Запуск',
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
launches_by_year = py.plot(fig, filename='City and Tournament')




success_percent = float(result2[0][0])
rest = 100 - neutral_percent
pie = go.Pie(labels=['Neutral', 'NonNeutral'], values=[success_percent, rest],
             textinfo='percent', title="Кількість успішних запусків")
success_percent = py.plot([pie], filename='Pie')


def fileId_from_url(url):
    fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1:]
    return fileId.replace('/', ':')
my_dboard = dashboard.Dashboard()
home_team_matches_id = fileId_from_url(home_team_matches)
away_team_matches_id = fileId_from_url(away_team_matches)
count_tournament_id = fileId_from_url(count_tournament)
neutral_matches_percent_id = fileId_from_url(neutral_matches_percent)
box1= {
    'type': 'box',
    'boxType': 'plot',
    'fileId': launches,
    'title': 'Кількість домашніх матчів'
}

box2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': launches_by_year,
    'title': 'Кількість виїздних матчів'
}

box3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': success_percent,
    'title': 'Кількість прийнятих турнірів містом'
}


my_dboard.insert(box3, 'below', 1)
my_dboard.insert(box2, 'right', 2)
my_dboard.insert(box1, 'left', 3)

py.dashboard_ops.upload(my_dboard, 'Lab_2')
