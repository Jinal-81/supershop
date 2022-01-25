"""
Establish connection and perform curd operation using postgresql
"""
import psycopg2

DATABASE_CREATED = "Database Created Successfully"
TABLE_CREATED = "Table created Successfully"
UPDATE_STATEMENT = "Record Updated Successfully.."
DATABASE_NAME = "Enter Database name:"
MAIN_DATABASE_NAME = "Enter Main Database name:"
TABLE_NAME = "Enter Table Name:"
BUILDING_NAME = "Enter Building name:"
OWNER_ID = "Enter Owner ID:"
OWNER_FNAME = "Enter Owner Fname:"
YEAR = "Enter Built in Year:"
BUILDING_CAPACITY = "Enter new building capacity:"
ROW_TABLE = "How many Row you want to create:"
ROW_NAME = "Enter Row Name:"
ROW_DATA_TYPE = "Enter Row datatype:"
MENU = "1.Database\n2.table\n3.InsertRecord\n4.ShowRecords\n5.BuildingName\n6.BuildingName and Capacity\n7.Update " \
       "Building Capacity\n8.BuildingID and BuildingName\n9.Apartment Details by ownerID\n10.Unique Building address" \
       "\n11.Building name and building year by builtin 2003\n12.Building capacity between query\n13.Total Number of " \
       "Apartments\n14.Count total apartments and owner\n15.Delete by owner Fname\n16.Apartment detail by owner fname" \
       "\n17.All  building name and apartment details\n18.Apartments details by building name OceanBlue\n19.owner_id " \
       "and owner_name which is Unique\n20.lowest weekly rent\n21Building name have more than 5 apartments\n22.Rent " \
       "Greater than 600\n23.Increase by 2%"
CHOICE = "Enter Your Choice:"
DEFAULT_STATEMENT = "select between 1-15"
FIRST_RANGE = "Enter first range for between query:"
SECOND_RANGE = "Enter second range for between query:"
DEFAULT_TABLE_STATEMENT = "Enter Valid Table name.."
TABLE_RECORDS = "Enter the list of tuples for table:\n"
RECORD_INSERTED = "Record Inserted Successfully.."
BUILDING_TABLE_COLUMN = "building_id, building_name, building_address, built_year, building_capacity"
OWNER_TABLE_COLUMN = "owner_id, owner_fname, owner_lname, owner_email, owner_phone"
APARTMENT_TABLE_COLUMN = "apartment_id, total_rooms, apartment_rent, building_id, owner_id"


class DATABASE:
    """
    class for database operations
    """
    def print_statement(self, *args: str) -> str:
        """
        Print statement function
        """
        print(*args)

    def user_input(self, *args: str) -> str:
        """
        take input form the user
        """
        input_user = input(*args)
        return input_user

    def database_conn(self, db_name: str) -> str:
        """
        Establish connection
        """
        database_name = db_name
        my_conn = psycopg2.connect(
            database=f'{database_name}',
            user='myuser',
            password='mypass',
            host='localhost',
            port='5432'
        )
        my_conn.autocommit = True
        cursor = my_conn.cursor()
        return cursor

    def create_database(self):
        """
        create database
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        database_name = self.user_input(DATABASE_NAME)
        query = f'CREATE DATABASE {database_name}'
        cursor.execute(query)
        self.print_statement(DATABASE_CREATED)

    def create_table(self):
        """
        create table building,owner and apartment
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)

        if table_name == "Building":
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            Building_ID INTEGER PRIMARY KEY,
            Building_Name VARCHAR,
            Building_Address VARCHAR,
            Built_Year INTEGER,
            Building_Capacity INTEGER
            );
            """

            cursor.execute(create_table_query)
            self.print_statement(TABLE_CREATED)
        elif table_name == "Owner":
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            Owner_ID INTEGER PRIMARY KEY,
            Owner_Fname VARCHAR,
            Owner_Lname VARCHAR,
            Owner_email VARCHAR,
            Owner_Phone VARCHAR
            );
            """

            cursor.execute(create_table_query)
            self.print_statement(TABLE_CREATED)
        elif table_name == "Apartment":
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            Apartment_ID INTEGER PRIMARY KEY,
            Total_Rooms INTEGER,
            Apartment_Rent DECIMAL,
            building_id INTEGER REFERENCES building(building_id),
            owner_id INTEGER REFERENCES owner(owner_id)
            );
            """

            cursor.execute(create_table_query)
            self.print_statement(TABLE_CREATED)
        else:
            self.print_statement(DEFAULT_TABLE_STATEMENT)

    def insert_into_table(self):
        """
        insert records into table.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        if table_name == "Building":
            self.print_statement(BUILDING_TABLE_COLUMN)
            final_list = []
            line = self.user_input(TABLE_RECORDS)
            while line != '':
                final_list.append(tuple(line.split()))
                line = self.user_input()

            self.print_statement(final_list)

            car_records = ", ".join(["%s"] * len(final_list))

            insert_query = (
                f"INSERT INTO building (building_id, building_name, building_address, built_year, building_capacity) "
                f"VALUES {car_records}"
            )

            cursor.execute(insert_query, final_list)
            self.print_statement(RECORD_INSERTED)

        elif table_name == "Owner":
            self.print_statement(OWNER_TABLE_COLUMN)
            final_list = []
            line = self.user_input(TABLE_RECORDS)
            while line != '':
                final_list.append(tuple(line.split()))
                line = self.user_input()

            self.print_statement(final_list)

            table_records = ", ".join(["%s"] * len(final_list))

            insert_query = (
                f"INSERT INTO owner (owner_id, owner_fname, owner_lname, owner_email, owner_phone) "
                f"VALUES {table_records}"
            )

            cursor.execute(insert_query, final_list)
            self.print_statement(RECORD_INSERTED)
        elif table_name == "Apartment":
            self.print_statement(APARTMENT_TABLE_COLUMN)
            final_list = []
            line = self.user_input(TABLE_RECORDS)
            while line != '':
                final_list.append(tuple(line.split()))
                line = self.user_input()

            self.print_statement(final_list)

            table_records = ", ".join(["%s"] * len(final_list))

            insert_query = (
                f"INSERT INTO apartment (apartment_id, total_rooms, apartment_rent, building_id, owner_id) "
                f"VALUES {table_records}"
            )

            cursor.execute(insert_query, final_list)
            self.print_statement(RECORD_INSERTED)
        else:
            self.print_statement(DEFAULT_TABLE_STATEMENT)

    def show_table_data(self):
        """
        display table's data
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT * FROM {table_name}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()

        for value in values:
            self.print_statement(value)

    def building_name(self):
        """
        fetch data from the table by building name
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT building_name FROM {table_name}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def show_building_name_capacity(self):
        """
        fetch building name and building capacity from the table.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT building_name, building_capacity FROM {table_name}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def update_building_capacity(self):
        """
        update building capacity where building name is lillyplilly.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        new_building_capacity = self.user_input(BUILDING_CAPACITY)
        update_table_query = f"""UPDATE {table_name} SET building_capacity = {new_building_capacity} 
                                WHERE building_name = 'lillypilly'"""
        cursor.execute(update_table_query)
        self.print_statement(UPDATE_STATEMENT)

    def show_building_id_building_name(self):
        """
        fetch building id and building name where building capacity is greater than 3000.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        building_capacity = self.user_input(BUILDING_CAPACITY)
        select_table_query = f"SELECT building_id, building_name FROM {table_name} WHERE building_capacity > " \
                             f"{building_capacity}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def show_apartment_details_by_owner(self):
        """
        fetch all the data of apartment table where owner id is 2003.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        owner_id = self.user_input(OWNER_ID)
        select_table_query = f"SELECT * FROM {table_name} WHERE owner_id = {owner_id}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def unique_building_address(self):
        """
        fetch all the unique building address from the building table.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT DISTINCT building_address FROM {table_name}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def building_name_building_year_builtin(self):
        """
        fetch building name and built year from building table where built year is 2001.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        built_year = self.user_input(YEAR)
        select_table_query = f"SELECT building_name, built_year FROM {table_name} WHERE built_year = {built_year}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def between_query_for_building(self):
        """
        fetch building name where building capacity between 1000 to 2000 in descending order.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        first_range = self.user_input(FIRST_RANGE)
        second_range = self.user_input(SECOND_RANGE)
        select_table_query = f"SELECT building_name FROM {table_name} WHERE building_capacity BETWEEN {first_range} " \
                             f"AND {second_range} ORDER BY building_name DESC"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def total_apartments(self):
        """
        fetch total number of apartments into apartment table.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT count(*) FROM {table_name}"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def owner_id_total_owner(self):
        """
        fetch owner id and total number of apartments owned by each owner in ascending order.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT DISTINCT(count(owner_id)), apartment_id FROM {table_name} GROUP BY owner_id, " \
                             f"apartment_id"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def delete_owner_fname(self):
        """
        delete the record of the owners whose owner fname contains the word 'james'.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        delete_table_query = f"DELETE FROM {table_name} WHERE owner_fname = 'james'"
        cursor.execute(delete_table_query)

    def show_apartment_by_owner_fname(self):
        """
        display all the apartments owned by the owner 'hazel' as the owner fname.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT * FROM {table_name} INNER JOIN owner ON owner.owner_id=apartment.owner_id WHERE" \
                             f"owner.owner_fname = 'hazel'"
        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def all_apartment_with_building_name(self):
        """
        display all the apartments details and corresponding building name.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT apartment.*,building.building_name FROM {table_name} INNER JOIN building ON " \
                             f"building.building_id = apartment.building_id "

        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def all_apartment_by_building_name_ocean(self):
        """
        display all the apartment details in building 'OceanBlue'.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT apartment.*,building.building_name FROM {table_name} INNER JOIN building ON " \
                             f"building.building_id = apartment.building_id WHERE building.building_name = 'OceanBlue'"

        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def owner_id_and_owner_name_unique(self):
        """
        display owner in and owner fname of all the owners who do not any apartments.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT apartment.owner_id,owner.owner_id,owner.owner_fname FROM {table_name}" \
                             f" INNER JOIN owner ON owner.owner_id=apartment.owner_id WHERE" \
                             f" NOT(owner.owner_id = apartment.owner_id)"

        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def lowest_weekly_rent(self):
        """
        display the building name, which has the apartment with the lowest weekly rent.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT building.building_name FROM {table_name} INNER JOIN building ON " \
                             f"building.building_id = apartment.building_id WHERE apartment_rent = (select " \
                             f"MIN(apartment_rent) FROM apartment)"

        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def building_name_apartment_more_than_five(self):
        """
        display all the building names having more than 5 apartments.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT building.building_name FROM {table_name} " \
                             f"INNER JOIN building ON building.building_id = apartment.building_id GROUP BY " \
                             f"building.building_name,apartment.building_id HAVING COUNT(apartment.building_id) >= 2"

        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def rent_greater_600(self):
        """
        display apartment id,apartment rent and owner names of the apartments,which has a greater than 600 rent.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"SELECT owner.owner_name,MIN(apartment.apartment_rent),apartment.apartment_id FROM " \
                             f"{table_name} INNER JOIN building ON building.building_id = apartment.building_id " \
                             f"GROUP BY owner.owner_id HAVING apartment.apartment_rent > 600"

        cursor.execute(select_table_query)

        values = cursor.fetchall()
        self.print_statement(values)

    def increase_by_percentage(self):
        """
        increase rent value by 2% who have building name as 'OceanBlue'.
        """
        database_name = self.user_input(MAIN_DATABASE_NAME)
        cursor = self.database_conn(database_name)
        table_name = self.user_input(TABLE_NAME)
        select_table_query = f"UPDATE {table_name} SET apartment_rent = (1.02 * apartment_rent) WHERE (""building_id = " \
                             "(SELECT building_id FROM building WHERE ""building_name = 'OceanBlue' ))"
        cursor.execute(select_table_query)
        self.print_statement(UPDATE_STATEMENT)


database_operation = DATABASE()
while True:
    database_operation.print_statement(MENU)
    ch = database_operation.user_input(CHOICE)
    if ch == "1":
        database_operation.create_database()
    elif ch == "2":
        database_operation.create_table()
    elif ch == "3":
        database_operation.insert_into_table()
    elif ch == "4":
        database_operation.show_table_data()
    elif ch == "5":
        database_operation.building_name()
    elif ch == "6":
        database_operation.show_building_name_capacity()
    elif ch == "7":
        database_operation.update_building_capacity()
    elif ch == "8":
        database_operation.show_building_id_building_name()
    elif ch == "9":
        database_operation.show_apartment_details_by_owner()
    elif ch == "10":
        database_operation.unique_building_address()
    elif ch == "11":
        database_operation.building_name_building_year_builtin()
    elif ch == "12":
        database_operation.between_query_for_building()
    elif ch == "13":
        database_operation.total_apartments()
    elif ch == "14":
        database_operation.owner_id_total_owner()
    elif ch == "15":
        database_operation.delete_owner_fname()
    elif ch == "16":
        database_operation.show_apartment_by_owner_fname()
    elif ch == "17":
        database_operation.all_apartment_with_building_name()
    elif ch == "18":
        database_operation.all_apartment_by_building_name_ocean()
    elif ch == "19":
        database_operation.owner_id_and_owner_name_unique()
    elif ch == "20":
        database_operation.lowest_weekly_rent()
    elif ch == "21":
        database_operation.building_name_apartment_more_than_five()
    elif ch == "22":
        database_operation.rent_greater_600()
    elif ch == "23":
        database_operation.increase_by_percentage()
    else:
        database_operation.print_statement(DEFAULT_STATEMENT)
        break
