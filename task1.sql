SELECT COUNT(*) AS num_of_missions, Customers.name as customer_name
from Missions
    JOIN Customers
    ON Missions.customer_id = Customers.customer_id
GROUP BY Customers.name
ORDER BY num_of_missions DESC;
