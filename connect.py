import psycopg2
import argparse

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

c.execute("""
DROP TABLE IF EXISTS listings;

CREATE TABLE listings(
    accommodates INTEGER,
    amenities TEXT ARRAY,
    availability_30 INTEGER,
    bathrooms INTEGER,
    bed_type VARCHAR(20),
    bedrooms INTEGER,
    beds INTEGER,
    cancellation_policy VARCHAR(20),
    city VARCHAR(50),
    has_availability BOOLEAN,
    host_id INTEGER,
    id INTEGER PRIMARY KEY,
    instant_bookable BOOLEAN,
    latitude FLOAT,
    longitude FLOAT,
    metropolitan VARCHAR(20),
    price FLOAT,
    property_type VARCHAR(20),
    review_scores_checkin INTEGER,
    review_scores_cleanliness INTEGER,
    review_scores_communication INTEGER,
    review_scores_location INTEGER,
    review_scores_rating INTEGER,
    review_scores_value INTEGER,
    room_type VARCHAR(20) CHECK(room_type in ('Entire home/apt', 'Private room', 'Shared room')),
    state VARCHAR(20),
    weekly_price FLOAT,
    zipcode INTEGER
);
""")

c.execute("""
DROP TABLE IF EXISTS calendar;

CREATE TABLE calendar(
    listing_id INTEGER,
    date DATE,
    available BOOLEAN,
    price FLOAT,
    metropolitan VARCHAR(20)
);
""")

c.execute("""
DROP TABLE IF EXISTS real_estate;

CREATE TABLE real_estate(
    type VARCHAR(4) CHECK(type in ('ZHVI', 'ZRI')),
    zipcode INTEGER,
    city VARCHAR(20),
    state VARCHAR(20),
    metro VARCHAR(20),
    county VARCHAR(20),
    size_rank INTEGER,
    date DATE,
    PRIMARY KEY(size_rank)
);
""")

c.execute("""
DROP TABLE IF EXISTS venues;

CREATE TABLE venues(
    city VARCHAR(20),
    id VARCHAR(40) PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    name VARCHAR(50),
    rating FLOAT,
    types TEXT ARRAY
);
""")

conn.commit()
conn.close()
