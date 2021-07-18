import psycopg2
import argparse
import csv

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--host", nargs='?', action="store", dest="host", default="localhost")
parser.add_argument("-p", "--port", nargs='?', action="store", dest="port", default="5432")
parser.add_argument("-d", "--dbname", nargs='?', action="store", dest="dbname", default="postgres")
parser.add_argument("-U", "--username", nargs='?', action="store", dest="username", default="postgres")
#parser.add_argument("-w", "--no-password", action="store_true")
parser.add_argument("-W", "--password", nargs='?', action="store", dest="password", default=None)

args = parser.parse_args()

conn = psycopg2.connect(
    host = args.host,
    port = args.port,
    database = args.dbname,
    user = args.username,
    password = args.password
)
c = conn.cursor()

def extract():
    def getMonthlyListings():
        return c.execute("""
            SELECT l.id, l.longitude, l.latitude, c.date
            FROM listings l, calendar c
            WHERE l.id = c.listing_id
            ORDER BY c.date ASC
        """).fetchall()
    def write(path, m_dict):
        with open("./data/{}".format(path), "wb") as f:
            w = csv.DictWriter(f, m_dict[0].keys())
            w.writerow(dict((fn,fn) for fn in m_dict[0].keys()))
            w.writerows(m_dict)
    write("l_by_month.csv", getMonthlyListings())

try:
    extract()
except psycopg2.DatabaseError as e:
    if e.pgcode != None: print(e)
conn.commit()