# recipe_extractor_tools
## What is it?
This library is made to have some basic tools allowing you to manage scraping recipes on the back-end side. 
Originally, this was part of a [recipe scraping project](https://github.com/sebastienhamel/recipe_extractor), but you you can use it anyway you want. 

## What's in it?
### Details
In the context of scraping, this is the data found on the website you were scraping. This model includes meta-information about scraping and the recipes data found on the page.

### Recipes (details.data)
This field contains the recipe of the website scraped. 

### Ingredients (details.data.ingredients)
The ingredients field is an list of ingredients containing the name of the ingredient (ingredient.ingredient_name) and the quantity (ingredient.quantity_unit). Both are string. You should include the type of unit in the quantity_unit field for further analysis.

### Method (details.data.method)
The method field is a list of actions necessary to make the recipe. It contains the step number (method.step_number) and the instruction for the step (method.instruction). 
> Please be aware that this information is as is on the website and might not reflect how you want to analyze the data. For example, the instruction for a specific step might include two actions (preheat the oven and measure dry ingredients). You might want to normalize the data so the information used for further analysis.

### Listing
In the context of scraping, this is all the steps necessary to find the detail urls. In this tool, we must consider one table for the listing and each record will have it's own mode. Keep in mind that in the context of scraping, you want to have a preventative approach: **your script will fail**, that's a given. Dividing the listing in smaller modes will reduce the risk of losing data. 

The modes, in our case, are:
1. **CATEGORIES_LISTING**: the seeding of the start urls necessary to start the listing
2. **CATEGORIES_LISTING_PAGE**: each seperate page from the categories search
3. **RECIPE_LINKS**: the last listing mode; a detail link (this is a page where you can directly find the data you are scraping)
4. **RECIPE_DETAILS**: the data scraped from the details page


### Logger
Basic logging service using the loguru library.
