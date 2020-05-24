import csv
import cx_Oracle

username = "dummy"
password = "dummy"
database = "localhost:1521/ORCLCDB.localdomain"

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

query = """
SELECT *
FROM
    country"""
cursor.execute(query)

with open("country.csv", "w", newline="\n") as file:
    writer = csv.writer(file)

    writer.writerow("countryid, name".split(","))

    for (countryid, name) in cursor:

        writer.writerow([countryid, name])

cursor.close()

cursor = connection.cursor()

query = """
SELECT *
FROM
    customertype"""
cursor.execute(query)

with open("customertype.csv", "w", newline="\n") as file:
    writer = csv.writer(file)

    writer.writerow("customertypeid, name".split(","))

    for (customertypeid, name) in cursor:

        writer.writerow([customertypeid, name])

cursor.close()
cursor = connection.cursor()

query = """
SELECT *
FROM
    landingtype"""
cursor.execute(query)

with open("landingtype.csv", "w", newline="\n") as file:
    writer = csv.writer(file)

    writer.writerow("landingtypeid, name".split(","))

    for (landingtypeid, name) in cursor:

        writer.writerow([landingtypeid, name])

cursor.close()

cursor = connection.cursor()

query = """
SELECT *
FROM
    mission"""
cursor.execute(query)

with open("mission.csv", "w", newline="\n") as file:
    writer = csv.writer(file)

    writer.writerow(
        """missionid,
        launchdate,
        launchsite,
        missionoutcome,
        failurereason,
        landingoutcome,
        flightnumber,
        orbit,
        payload_payloadid,
        landingtype_landingtypeid,
        vehicletype_vehicletypeid,
        customer_customerid""".split(
            ","
        )
    )

    for (
        missionid,
        launchdate,
        launchsite,
        missionoutcome,
        failurereason,
        landingoutcome,
        flightnumber,
        orbit,
        payload_payloadid,
        landingtype_landingtypeid,
        vehicletype_vehicletypeid,
        customer_customerid,
    ) in cursor:

        writer.writerow(
            [
                missionid,
                launchdate,
                launchsite,
                missionoutcome,
                failurereason,
                landingoutcome,
                flightnumber,
                orbit,
                payload_payloadid,
                landingtype_landingtypeid,
                vehicletype_vehicletypeid,
                customer_customerid,
            ]
        )

cursor.close()

cursor = connection.cursor()

query = """
SELECT *
FROM
    payload"""
cursor.execute(query)

with open("payload.csv", "w", newline="\n") as file:
    writer = csv.writer(file)

    writer.writerow(
        """payloadid,
        name,
        masskg,
        payloadtype_payloadtypeid""".split(
            ","
        )
    )

    for (payloadid, name, masskg, payloadtype_payloadtypeid) in cursor:

        writer.writerow([payloadid, name, masskg, payloadtype_payloadtypeid])

cursor.close()

cursor = connection.cursor()

query = """
SELECT *
FROM
    payloadtype"""
cursor.execute(query)

with open("payloadtype.csv", "w", newline="\n") as file:
    writer = csv.writer(file)

    writer.writerow(
        """payloadtypeid,
        name""".split(
            ","
        )
    )

    for (payloadtypeid, name) in cursor:

        writer.writerow([payloadtypeid, name])

cursor.close()
