from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base
from recipe_extractor_tools.encoder import JSONEncodedRecipe

Base = declarative_base()
metadata = MetaData()

class Listing(Base):
    """
        Table model for listing objects.
    """

    __tablename__ = "listings"
    id = Column(Integer, primary_key = True, autoincrement = True, doc = "The listing row id.")
    link = Column(String(255), unique = True, nullable = False, doc = "The url of the row.") 
    mode = Column(String(255), nullable = False, doc = "The scraping mode of the row.")
    startdate = Column(DateTime, nullable = True, doc = "The datetime at which the scraping of the row was started.")
    enddate = Column(DateTime, nullable = True, doc = "The datetime at which the scraping of the row was finished.")
    successful = Column(Boolean, nullable = True, doc = "True if the scraping of the item finished without error.")
    attempts = Column(Integer, nullable = True, doc = "The current number of scraping attempts.")


class Detail(Base):
    """
        Detail model for listing objects.
    """

    __tablename__ = "details"
    id = Column(Integer, primary_key = True, autoincrement = True, doc = "The detail row id.")
    link = Column(String(255), unique = True, nullable = False, doc = "The url of the row.")
    timestamp = Column(DateTime, nullable=False, doc = "The datetime when the detail item was processed.")
    data = Column(JSONEncodedRecipe, nullable = True, doc = "The data scraped for this item.")


    