from datetime import datetime
from pydantic import BaseModel, Field

from recipe_extractor_tools.modes import Mode

class Listing(BaseModel):
    """
    Represents the listing item for a scraper.
    """
    id: int|None = Field(init = False, default = None, description="The database id.")
    link: str = Field(description="The url of the recipe.")
    mode: Mode = Field(description="The listing mode for a listing item.")
    startdate: datetime|None = Field(init = False, default = None, description="When the url scraping was started.")
    enddate: datetime|None = Field(init = False, default = None, description="When the url scraping was finished.")
    successful: bool = Field(default = False, description="True if the scraping of the item finished without error.")
    attempts: int = Field(init = False, default = 0, description="Number of scraping attempts.")
    