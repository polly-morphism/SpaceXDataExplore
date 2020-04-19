CREATE TABLE Customers
(
  customer_id integer,
  name char(20),
  type char(20),
  country char(20) 

);

ALTER TABLE Customers
ADD CONSTRAINT customer_pk 
    PRIMARY KEY (customer_id);


CREATE TABLE Payloads
(
  payload_id integer,
  name char(40),
  type char(35),
  mass_kg  REAL
);

ALTER TABLE Payloads
ADD CONSTRAINT payload_pk 
    PRIMARY KEY (payload_id);




CREATE TABLE Missions
(
  mission_id integer,
  payload_id integer,
  customer_id integer,
  vehicle_type char(40),
  mission_outcome char(20),
  failure_reason char(40),
  landing_type char(20),
  landing_outcome char(20),
  flight_number char(5),
  launch_date date,
  launch_site char(40),
  orbit char(40)
);

ALTER TABLE Missions
ADD CONSTRAINT mission_pk 
    PRIMARY KEY (mission_id);


ALTER TABLE Missions
ADD CONSTRAINT payload_fk
  FOREIGN KEY (payload_id)
  REFERENCES Payloads (payload_id);


ALTER TABLE Missions
ADD CONSTRAINT customer_fk
  FOREIGN KEY (customer_id)
  REFERENCES Customers (customer_id);
