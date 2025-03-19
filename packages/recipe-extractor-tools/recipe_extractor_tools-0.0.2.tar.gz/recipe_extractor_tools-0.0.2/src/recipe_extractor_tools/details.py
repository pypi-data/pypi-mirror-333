from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

class Ingredient(BaseModel):
    """
    Represents an ingredient in a recipe, including its quantity and name.
    """
    quantity_unit: str = Field(default="", description="The quantity of an ingredient including the unit (default value = '')")
    ingredient_name: str = Field(default="", description="The name of an ingredient (default value = '')")

class Method(BaseModel):
    """
    Represents a method step in a recipe.
    """
    step_number: int = Field(default=0, description="The integer of the step number of the method (default value = 0)")
    instruction: str = Field(default="", description="The string of instruction for the current step (default value = '')")

class Recipe(BaseModel):
    """
    Represents a recipe with its name, portions, time, and other details.
    """
    name: str = Field(default="", description="The name of the recipe on the website (default value = '')")
    portions: str = Field(default=0, description="The interger number of portions included in the recipe (default value = 0).") 
    preparation_time: str = Field(default="", description="The preparation time appearing on the website including the units (default value = '')")
    cooking_time: str = Field(default = "", description="The cooking time appearing on the website including the units (default value = '')")
    total_time: str = Field(default = "", description="The total time appearing on the website including the units (default value = '')")
    categories: List[str] = Field(default_factory=list, description="The recipe categories appearing on the website as a list of strings (default value = [])")
    keywords: List[str] = Field(default_factory=list, description="The recipe keywords appearing on the website as a list of strings (default value = [])")
    ingredients: List[Ingredient] = Field(default_factory=list, description="The ingredients list for the recipe (default value = [])")
    method: List[Method] = Field(default_factory=list, description="The method of the recipe (default_value = [])")

class Details(BaseModel):
    """
    Represents the details of a scraped recipe.
    """
    id: int = Field(description="The database id.")
    link: str = Field(description="The url of the recipe.")
    startdate: datetime = Field(description="When the url scraping was started.")
    enddate: datetime = Field(description="When the url scraping was finished.")
    successful: bool = Field(successful="True if the scraping was completed without issue.")
    data: Recipe = Field(description="The recipe data.")
    attempts: int = Field(description="Number of scraping attempts.")
