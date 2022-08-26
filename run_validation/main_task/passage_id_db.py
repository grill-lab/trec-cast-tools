import sys
import os
import sqlite3
import csv
import argparse
import logging

#
# Convert all_hashes.csv (or similarly formatted file) into an SQLite database,
# using a single table (passage_ids) and a single column (id). It provides a
# populate() method to copy IDs from the CSV and a validate() method to take
# a list of passage IDs and check if they appear in the table. 
#

DEFAULT_BATCH_SIZE = 20000
DEFAULT_PRINT_INTERVAL = 20

LOGLEVEL = logging.INFO

logger = logging.Logger(__file__)
logger.setLevel(LOGLEVEL)
# log to stdout and to file
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(logging.FileHandler(__file__ + '.log'))

class PassageIDDatabase:

    TABLE_NAME = 'passage_ids'
    COL_NAME = 'id'

    def __init__(self, path) -> None:
        self.path = path
        self.db = None

    def _init_database(self) -> bool:
        """
        (Re)create the database schema
        """
        try:
            self.cur.execute(f'DROP TABLE IF EXISTS {PassageIDDatabase.TABLE_NAME}')
            self.cur.execute(f'CREATE TABLE {PassageIDDatabase.TABLE_NAME} ({PassageIDDatabase.COL_NAME} TEXT PRIMARY KEY NOT NULL)')
        except sqlite3.Error as sqle:
            logger.error(f'Error initialising database: {sqle}')
            return False

        self.cur.execute('PRAGMA cache_size = 1000000')
        return True

    def open(self) -> bool:
        """
        Open a database file at the location given by self.path. If there's an 
        existing file there it will be opened, otherwise a new file is created.
        """
        try:
            # using check_same_thread=False should be safe here because the
            # database is either going to be populated or used for reads, not
            # both at the same time
            self.db = sqlite3.connect(self.path, check_same_thread=False)
            self.cur = self.db.cursor()
        except sqlite3.Error as sqle:
            logger.error(f'Error initialising database: {sqle}')
            return False

        return True

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def populate(self, hash_file: str, batch_size: int, print_interval: int) -> bool:
        """
        Populate the database from a .csv file with passage IDs in the first column.
        
        Inserts are done in transactions of batch_size rows. 
        """
        # assume we always want to completely repopulate here (alternatively
        # could check if table exists etc)
        if not self._init_database():
            logger.error('Failed to populate database')
            return False

        batch = []
        inserted = 0
        batch_count = 0
        with open(hash_file, 'r') as hf:
            rdr = csv.reader(hf)
            for row in rdr:
                batch.append((row[0], ))

                if len(batch) == batch_size:
                    self.cur.executemany(f'INSERT INTO {PassageIDDatabase.TABLE_NAME} VALUES (?)', batch)
                    self.db.commit()
                    inserted += len(batch)
                    batch_count += 1
                    batch = []

                    if batch_count % print_interval == 0:
                        logger.info(f'Inserted {inserted:9d} rows')

            # final partial batch
            self.cur.executemany(f'INSERT INTO {PassageIDDatabase.TABLE_NAME} VALUES (?)', batch)
            self.db.commit()
            inserted += len(batch)
            logger.info(f'Inserted {inserted:9d} rows')

        logger.info(f'Database populated with {inserted} rows, vacuuming...')
        self.db.execute('VACUUM')
        logger.info('Database population complete!')
        return True

    def validate(self, ids: [str]) -> [bool]:
        results = []
        for id in ids:
            self.cur.execute(f'SELECT {PassageIDDatabase.COL_NAME} FROM {PassageIDDatabase.TABLE_NAME} \
                    WHERE {PassageIDDatabase.COL_NAME} = ?', (id, ))
            result = self.cur.fetchone()
            results.append(False if result is None else True)
            logger.debug(f'Validate {id} = {result is not None}')

        return results

    def close(self) -> bool:
        if self.db is not None:
            self.db.commit()
            self.db.close()
        return True

    @property
    def rowcount(self) -> int:
        try:
            self.cur.execute(f'SELECT COUNT({PassageIDDatabase.COL_NAME}) FROM {PassageIDDatabase.TABLE_NAME}')
        except sqlite3.OperationalError:
            return -1
        return self.cur.fetchone()[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('hash_file')
    parser.add_argument('-b', '--batch_size', help='Number of rows in each insert transaction', 
                type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument('-i', '--print_interval', help='Display number of rows inserted after every <print_interval> batches', 
                type=int, default=DEFAULT_PRINT_INTERVAL)
    args = parser.parse_args()

    if not os.path.exists(args.hash_file):
        print(f'Error: {args.hash_file} does not exist!')
        sys.exit(255)

    # create database in same location as file with .sqlite3 extension
    db_name, db_ext = os.path.splitext(args.hash_file)
    db_name = db_name + '.sqlite3'
    print(f'Creating database at {db_name}')

    if os.path.exists(db_name):
        os.unlink(db_name)

    with PassageIDDatabase(db_name) as hdb:
        if not hdb.populate(args.hash_file, args.batch_size, args.print_interval):
            print('Error: failed to populate the database!')
            sys.exit(255)

        print(f'Database populated, row count is {hdb.rowcount}')
