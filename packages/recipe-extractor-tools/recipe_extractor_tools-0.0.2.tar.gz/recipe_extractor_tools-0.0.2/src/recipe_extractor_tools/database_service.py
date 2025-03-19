import os
from typing import List

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

from recipe_extractor_tools.database_tables import Listing as ListingRow
from recipe_extractor_tools.modes import Mode

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable cannot be found.")


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_database():
    """
        Creates a database connection. Should be used with an iterator:
        
        with (next(get_database())) as database:
            ...
    """
    database = SessionLocal()

    try:
        yield database
    
    finally:
        database.close()

def is_listing_complete():
    """
        Returns true if all listing rows have been processed. 

        A complete listing mode is seen as:
        - There is more than 0 rows in the listings table
        - The count of *not* RECIPE_LINKS with successful = 1 == the count of *not* RECIPE_LINKS
    
    """
    database = SessionLocal()

    try:
        return database.query(ListingRow).filter(
            ListingRow.mode.__ne__(Mode.RECIPE_LINKS)).count() == database.query(ListingRow).filter(
            and_(
                ListingRow.mode.__ne__(Mode.RECIPE_LINKS),
                ListingRow.successful.__eq__(1)
            )
        ).count() and database.query(ListingRow).count() > 0
    
    finally:
        database.close()

def is_detail_complete():
    """
        Returns true if all detail rows have been processed. 

        A complete detail mode is seen as:
        - There is more than 0 rows with mode = RECIPE_LINKS in the listings table
        - The count of RECIPE_LINKS with successful = 1 == the count of RECIPE_LINKS
    
    """


    database = SessionLocal()

    try:
        return database.query(ListingRow).filter(
            and_(
                ListingRow.mode.__eq__(Mode.RECIPE_LINKS), 
                ListingRow.successful.__eq__(1)
            ) #number of successful = true == number of recipe links -> The details is complete.
        ).count() == database.query(ListingRow).filter(
            ListingRow.mode.__eq__(Mode.RECIPE_LINKS)).count() and database.query(ListingRow).filter(
                ListingRow.mode.__eq__(Mode.RECIPE_LINKS)).count() > 0 #There are recipe links present
    finally:
        database.close()

def get_listing_to_process(limit:int) -> List[ListingRow]:
    """
        Returns Listing rows with mode != RECIPE_LINKS needing to be processed. 

        A row needing to be processed is:
        - successful = None or False

        Your code should manage the maximum number of attempts since this function doesn't.

        Params:
            limit (int): the maximum number of rows to be returned by the function.
    
    """
    database = SessionLocal()

    try:
        return database.query(ListingRow).filter(and_(or_(ListingRow.successful.is_(None), ListingRow.successful.is_(False)), ListingRow.mode.__ne__(Mode.RECIPE_LINKS))).limit(limit).all()
    
    finally:
        database.close()


def get_details_to_process(limit:int) -> List[ListingRow]:
    """
        Returns Listing rows with mode = RECIPE_LINKS needing to be processed. 

        A row needing to be processed is:
        - successful = None or False

        Your code should manage the maximum number of attempts since this function doesn't.

        Params:
            limit (int): the maximum number of rows to be returned by the function.
    """
    database = SessionLocal()

    try:
        return database.query(ListingRow).filter(and_(or_(ListingRow.successful.is_(None), ListingRow.successful.is_(False)), ListingRow.mode.__eq__(Mode.RECIPE_LINKS))).limit(limit).all()
    
    finally:
        database.close()


def update_listing(listing:ListingRow):
    """
        Updates a listing row. 

        Params:
            listing (Listing): a listing row to be updated.
    """
    database = SessionLocal()
    
    try:
        database.query(ListingRow).where(ListingRow.id == listing.id).update({
            "attempts": listing.attempts, 
            "enddate": listing.enddate,
            "successful": listing.successful,
            "startdate": listing.startdate
        })
        database.commit()
    
    finally:
        database.close()
