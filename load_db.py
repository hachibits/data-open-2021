import psycopg2
import argparse
import os
import pandas as pd

def loadDatabase(conn, path, schema):
    c = conn.cursor()
    df =  pd.read_csv(path, compression='gzip') if path[-3:] == ".gz" else pd.read_csv(path)

    for i, row in df.iterrows():
        for key in df.columns.values:
            if str(row[key]) == "nan":
                row[key] = psycopg2.extensions.AsIs('NULL')
            if isinstance(row[key], str):
                row[key] = f"'{row[key]}'"
        c.execute("""
        INSERT INTO %(table)s VALUES(
            %(row)s
        );
        """ % {
            "table": schema,
            #"row" : ", ".join(map(lambda x: f"'{str(x)}'" if isinstance(x, str) else str(x), row.values))
            "row": ", ". join(map(str, row))
        })

    conn.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--host", nargs='?', action="store", dest="host", default="localhost")
    parser.add_argument("-p", "--port", nargs='?', action="store", dest="port", default="5432")
    parser.add_argument("-d", "--dbname", nargs='?', action="store", dest="dbname", default="postgres")
    parser.add_argument("-U", "--username", nargs='?', action="store", dest="username", default="postgres")
    #parser.add_argument("-w", "--no-password", action="store_true")
    parser.add_argument("-W", "--password", nargs='?', action="store", dest="password", default=None)
    parser.add_argument("--listings", action="store_true", default=False)
    parser.add_argument("--calendar", action="store_true", default=False)
    parser.add_argument("--real_estate", action="store_true", default=False)
    parser.add_argument("--venues", action="store_true", default=False)

    args = parser.parse_args()

    conn = psycopg2.connect(
        host = args.host,
        port = args.port,
        database = args.dbname,
        user = args.username,
        password = args.password
    )

    path = "./data"
    if args.listings:
        listings_path = os.path.join(path, "listings.csv")
        loadDatabase(conn, listings_path, "listings")
    if args.calendar:
        calendar_path = os.path.join(path, "calendar.csv.gz")
        loadDatabase(conn, calendar_path, "calendar")
    if args.real_estate:
        real_estate_path = os.path.join(path, "real_estate.csv.gz")
        loadDatabase(conn, real_estate_path, "real_estate")
    if args.venues:
        venues_path = os.path.join(path, "venues.csv.gz")
        loadDatabase(conn, venues_path, "venues")

    conn.close()
