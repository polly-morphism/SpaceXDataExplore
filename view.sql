CREATE VIEW missions_per_customer AS
    SELECT COUNT(*) AS num_of_missions, Customer.Name as customer_name
    from Mission
        JOIN Customer
        ON Mission.Customer_CustomerId = Customer.CustomerId
    GROUP BY Customer.Name
    ORDER BY num_of_missions DESC;




CREATE VIEW missions_view AS
        SELECT COUNT(*) AS all_missions, Customer.Name as customer_name, Customer.CustomerId as cust_id
        FROM Mission
            JOIN Customer
            ON Mission.Customer_CustomerId = Customer.CustomerId
        WHERE Mission.MissionOutcome <> 'Success'
        GROUP BY Customer.CustomerId, Customer.Name ;

CREATE VIEW success_missions_view AS
    SELECT COUNT(*) AS successfull_missions, Customer.Name as customer_name, Customer.CustomerId as cust_id
    FROM Mission
            JOIN Customer
            ON Mission.Customer_CustomerId = Customer.CustomerId
    WHERE Mission.MissionOutcome = 'Success'
    GROUP BY Customer.CustomerId, Customer.Name;


CREATE VIEW all_missions_success_percentage AS
    SELECT all_missions, COALESCE((successfull_missions/all_missions)*100, 0) as success_percentage, missions_view.customer_name 
    FROM
        missions_view
    LEFT JOIN 
        success_missions_view
    ON missions_view.cust_id =success_missions_view.cust_id;


CREATE VIEW num_of_missions_per_year AS
    SELECT COUNT(*) AS num_of_missions,  EXTRACT(YEAR FROM Mission.LaunchDate) as launch
    FROM Mission
    GROUP BY EXTRACT(YEAR FROM Mission.LaunchDate)
    ORDER BY launch;
