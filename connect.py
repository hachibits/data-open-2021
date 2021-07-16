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
CREATE TABLE IF NOT EXISTS listings(
    accommodates INTEGER NOT NULL,
    amenities TEXT ARRAY NOT NULL,
    availability_30 INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    bed_type VARCHAR(20) NOT NULL,
    bedrooms INTEGER NOT NULL,
    beds INTEGER NOT NULL,
    cancellation_policy VARCHAR(10) NOT NULL,
    city VARCHAR(20) NOT NULL,
    has_availability BOOLEAN NOT NULL,
    host_id INTEGER NOT NULL,
    id INTEGER PRIMARY KEY NOT NULL,
    instant_bookable BOOLEAN NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    metropolitan VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL,
    property_type VARCHAR(20) NOT NULL,
    review_scores_checkin INTEGER,
    review_scores_cleanliness INTEGER,
    review_scores_communication INTEGER,
    review_scores_location INTEGER,
    review_scores_rating INTEGER,
    review_scores_value INTEGER,
    room_type VARCHAR(20) CHECK(room_type in ('Entire home/apt', 'Private room', 'Shared room')),
    state VARCHAR(20) NOT NULL,
    weekly_price FLOAT NOT NULL,
    zipcode INTEGER NOT NULL
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS calendar(
    listing_id INTEGER NOT NULL,
    date DATE NOT NULL,
    available BOOLEAN NOT NULL,
    price FLOAT NOT NULL,
    metropolitan VARCHAR(20) NOT NULL,
    PRIMARY KEY(listing_id)
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS real_estate(
    type VARCHAR(4) CHECK(type in ('ZHVI', 'ZRI')),
    zipcode INTEGER NOT NULL,
    city VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    metro VARCHAR(20) NOT NULL,
    county VARCHAR(20) NOT NULL,
    size_rank INTEGER NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY(size_rank)
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS venues(
    city VARCHAR(20) NOT NULL,
    id VARCHAR(40) PRIMARY KEY NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    name VARCHAR(50) NOT NULL,
    rating FLOAT NOT NULL,
    types TEXT ARRAY NOT NULL
);
""")

conn.commit()
conn.close()