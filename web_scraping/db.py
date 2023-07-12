import sqlite3

import pandas as pd
from sqlalchemy import create_engine

DB_NAME = "competitors.db"
TABLE_NAME = "products_data"


def add_to_db(df: pd.DataFrame) -> None:
    """Append a dataframe to the SQL table"""

    # Create a connection to the SQL database
    engine = create_engine("sqlite:///" + DB_NAME)

    # Save the dataframe to an SQL table
    df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)


def website_names() -> list[str]:
    """Get the websites of all accounts with media data"""

    with sqlite3.connect("competitors.db") as conn:
        # create a cursor object
        cursor = conn.cursor()

        # execute a SELECT query to retrieve all distict websites
        cursor.execute(f"SELECT DISTINCT website FROM {TABLE_NAME}")

        # fetch all websites as a list of tuples
        websites = cursor.fetchall()

        # unpack each tuple into a list
        return [website[0] for website in websites]


def delete_website(website) -> None:
    """Delete a website from the SQL table"""

    with sqlite3.connect("competitors.db") as conn:
        # create a cursor object
        cursor = conn.cursor()

        # execute a DELETE query to delete the website
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE website = ?", (website,))

        # commit the changes
        conn.commit()
