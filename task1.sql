-- task1
SELECT COUNT(*) AS num_of_missions, Customers.name as customer_name
from Missions
    JOIN Customers
    ON Missions.customer_id = Customers.customer_id
GROUP BY Customers.name
ORDER BY num_of_missions DESC;

-- task2

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

-- task3

SELECT COUNT(*) AS num_of_missions,  EXTRACT(YEAR FROM missions.launch_date) as launch
FROM Missions
GROUP BY EXTRACT(YEAR FROM missions.launch_date)
ORDER BY launch;
