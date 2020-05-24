import pandas as pd
import csv
import cx_Oracle

username = "dummy"
password = "dummy"
database = "localhost:1521/ORCLCDB.localdomain"

connection = cx_Oracle.connect(username, password, database)


data = pd.read_csv("space_x_database.csv")
countries_list = data["Customer Country"].ffill().unique()


def quote(x):

    if isinstance(x, str):
        return "'" + x + "'"  # quote all strings in quotes
    else:
        if str(x) == "nan":
            return "''"  # for nan
        else:
            return "'" + str(x) + "'"  # for digits


def gen_type_sql(table_name, columns_list, values_list, id_offset=0):
    res_dict = {}
    for row_n in range(len(values_list)):
        uid = id_offset + row_n

        cursor = connection.cursor()
        try:
            ##insert_query = '''INSERT INTO COUNTRYREGION (country, region) VALUES (:country, :region)'''
            insert_query = (
                f"INSERT INTO {table_name}({','.join(columns_list)})"
                + "VALUES("
                + ", ".join([str(uid)] + [quote(values_list[row_n])])
                + " );"
            )
            print(insert_query)
            cursor.execute(insert_query)
        except:
            print("already in database")

        connection.commit()
        cursor.close()

        res_dict[values_list[row_n]] = str(uid)
    return res_dict


countries_dict = gen_type_sql("Country", ["CountryID", "Name"], countries_list, 31)

customer_types_list = data["Customer Type"].ffill().unique()
customer_types_dict = gen_type_sql(
    "CustomerType", ["CustomerTypeId", "Name"], customer_types_list
)
landing_types_list = data["Landing Type"].ffill().unique()
landing_types_dict = gen_type_sql(
    "LandingType", ["LandingTypeId", "Name"], landing_types_list
)

vehicle_types_list = data["Vehicle Type"].ffill().unique()
vehicle_types_dict = gen_type_sql(
    "VehicleType", ["VehicleTypeId", "Name"], vehicle_types_list
)

payload_types_list = data["Payload Type"].ffill().unique()
payload_types_dict = gen_type_sql(
    "PayloadType", ["PayloadTypeId", "Name"], payload_types_list
)
table_name = "Customer"

row_map = {
    "CustomerId": lambda row, cnt, val: str(cnt),
    "Name": lambda row, cnt, val: quote(row["Customer Name"]),
    "CustomerType_CustomerTypeId": lambda row, cnt, val: str(
        customer_types_dict[row["Customer Type"]]
    ),
    "Country_CountryId": lambda row, cnt, val: str(
        countries_dict[row["Customer Country"]]
    ),
}

df = (
    data[["Customer Name", "Customer Type", "Customer Country"]]
    .ffill()
    .drop_duplicates()
)


def gen_table_inserts(
    table_name, df, row_map, unique_identifier_name="Name", default_val=""
):
    cnt = 0
    res_dict = {}  # store mapping of name => id

    cursor = connection.cursor()
    for index, row in df.iterrows():

        try:
            insert_query = (
                f"INSERT INTO {table_name}({','.join(row_map.keys())}) VALUES("
                + ", ".join([l(row, cnt, default_val) for k, l in row_map.items()])
                + " );"
            )
            print(insert_query)
            cursor.execute(insert_query)
        except:
            print("already in database")

        connection.commit()

        res_dict[row_map[unique_identifier_name](row, cnt, default_val)] = str(cnt)
        cnt += 1
        # except Exception as e:
        #    print(f"-- Oups:: {row} + {e}")
    cursor.close()
    return res_dict


customer_names_dict = gen_table_inserts(
    table_name, df, row_map, unique_identifier_name="Name", default_val=""
)

table_name = "Payload"

row_map = {
    "PayloadId": lambda row, cnt, val: str(cnt),
    "Name": lambda row, cnt, val: quote(row["Payload Name"]),
    "MassKg": lambda row, cnt, val: quote(row["Payload Mass (kg)"]),
    "PayloadType_PayloadTypeId": lambda row, cnt, val: str(
        payload_types_dict[row["Payload Type"]]
    ),
}

df = (
    data[["Payload Name", "Payload Mass (kg)", "Payload Type"]]
    .ffill()
    .drop_duplicates()
)


payload_names_dict = gen_table_inserts(
    table_name, df, row_map, unique_identifier_name="Name", default_val=""
)

table_name = "Mission"


def month2num(m):
    return str(
        {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12,
        }[m]
    )


def double_digit(d):
    return d if len(d) > 1 else "0" + d


def convert_oracle_date(d):
    # -- INSERT INTO my_table (my_date) VALUES ( TO_DATE( '11-13-2012', 'MM-DD-YYYY' ) );
    # -- SELECT TO_CHAR( my_date, 'MM-DD-YYYY' ) FROM my_table;
    # d="3 August 2008"
    dd = d.split(" ")
    oracle_date = "-".join([double_digit(d) for d in [dd[0], month2num(dd[1]), dd[2]]])
    return f"TO_DATE( '{oracle_date}', 'DD-MM-YYYY' )"


row_map = {
    "MissionId": lambda row, cnt, val: str(cnt),
    "LaunchDate": lambda row, cnt, val: convert_oracle_date(row["Launch Date"]),
    "LaunchSite": lambda row, cnt, val: quote(row["Launch Site"]),
    "MissionOutcome": lambda row, cnt, val: quote(row["Mission Outcome"]),
    "FailureReason": lambda row, cnt, val: quote(row["Failure Reason"]),
    "LandingOutcome": lambda row, cnt, val: quote(row["Landing Outcome"]),
    "FlightNumber": lambda row, cnt, val: quote(row["Flight Number"]),
    "Orbit": lambda row, cnt, val: quote(row["Payload Orbit"]),
    # -- FKs
    "Payload_PayloadId": lambda row, cnt, val: str(
        payload_types_dict[row["Payload Type"]]
    ),
    "LandingType_LandingTypeId": lambda row, cnt, val: str(
        landing_types_dict[row["Landing Type"]]
    ),
    "VehicleType_VehicleTypeId": lambda row, cnt, val: str(
        vehicle_types_dict[row["Vehicle Type"]]
    ),
    "Customer_CustomerId": lambda row, cnt, val: str(
        customer_names_dict[quote(row["Customer Name"])]
    ),
}

df_cols = [
    "Launch Date",
    "Launch Site",
    "Mission Outcome",
    "Failure Reason",
    "Landing Outcome",
    "Flight Number",
    "Payload Orbit",
    "Payload Type",
    "Landing Type",
    "Vehicle Type",
    "Customer Name",
]
df = data[df_cols].ffill().drop_duplicates()
missions_names_dict = gen_table_inserts(
    table_name, df, row_map, unique_identifier_name="FlightNumber", default_val=""
)


connection.close()
