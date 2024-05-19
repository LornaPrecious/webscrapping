import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from items import VeganuaryRecipeItem
from w3lib.html import remove_tags


class VeganuarySpider(CrawlSpider):
    name = "vegan"  # The name of the Spider, it will be used to create unique requests and identify the spider
    allowed_domains = ['veganuary.com']
    start_urls =['https://veganuary.com/', 
                 'https://veganuary.com/recipes/', 
                 'https://veganuary.com/recipes/meals/breakfast/', 
                 'https://veganuary.com/recipes/meals/lunch/', 
                 'https://veganuary.com/recipes/meals/dinner/', 
                 'https://veganuary.com/recipes/meals/snacks/',
                 'https://veganuary.com/recipes/meals/sweet-treats/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths= ["//div[@class='content-area js-push']", "//div[@class='section section--large section--light-gray section--ac']", "//div[@class='container']"], allow ='/recipes/'), callback='parse', follow=True),)
    #Extract, Transform and load - request, parse, output

    def parse(self, response):

        for articles in response.xpath('//div[@class="content-area js-push"]'):

            recipe_loader = ItemLoader(item = VeganuaryRecipeItem(), selector=articles)
            recipe_loader.default_input_processor = MapCompose(remove_tags)
            
            
            #TITLE loc article-post-header
            recipe_loader.add_xpath("title", "//div[@class='col-md-10 offset-md-1 col-lg-8 offset-lg-2 col-xl-6 offset-xl-3']/h1[@class='hero__title']")
            
        
            # IMAGES 
            recipe_loader.add_xpath("image_url", '//div[@class="hero__figure"]/picture[@class="hero__picture"]/img/@src | //div[@class="hero__figure"]/picture[@class="hero__picture"]/div[@class="hero__picture"]/img/@src')
            
            # ************ ADDING PREP, COOK, TOTAL TIME and SERVINGS ***************

            nutrition_facts = articles.xpath("//div[@class='tooltip-single']")

            nutrition_facts_dict = {
                "prep_time": "",
                "cook_time": "",
                "servings": ""
            }

            for fact in nutrition_facts:
                text = fact.xpath(".//div[@class='tooltip-text-recipe']/text()").get()
                if text:
                    if "Prep Time" in text:
                        nutrition_facts_dict["prep_time"] = text.split(":")[1].strip()
                    elif "Cooking Time" in text:
                        nutrition_facts_dict["cook_time"] = text.split(":")[1].strip()
                    elif "Serves" in text:
                        nutrition_facts_dict["servings"] = text.split(":")[1].strip()

            recipe_loader.add_value("prep_time", nutrition_facts_dict["prep_time"])
            recipe_loader.add_value("cook_time", nutrition_facts_dict["cook_time"])
            recipe_loader.add_value("servings", nutrition_facts_dict["servings"])

        #******************************** INGREDIENTS ********************************
            ingredients = response.xpath('//div[@class="recipe__ingredients"]/ul/li | //div[@class="recipe__ingredients"]/p')

            ingredients_list = [] 

            for ingredient in ingredients:
                # Extract the text of each list item (ingredient)
                ingredient_text = ' '.join(ingredient.xpath('./text()').getall())
                
                # Append each ingredient to a list
                ingredients_list.append(ingredient_text.strip() if ingredient_text else '')

            # Store the list of ingredients in the item
            recipe_loader.add_value('ingredients_list', ingredients_list)

       
        #*************************** COOKING DIRECTIONS *******************      
            cooking_directions = response.xpath("//div[@class='recipe__method']/ul | //div[@class='recipe__method']/ol | //div[@class='recipe__method'] ")

            directions_steps = []

            for direction in cooking_directions:
                # Extract the text of each list item (cooking step)
                step_text = ' ' .join(direction.xpath('./li/text() | ./p/text()').getall())
        
                # Append each cooking step to a list
                directions_steps.append(step_text.strip() if step_text else '')

            # Store the list of cooking directions in the item
            recipe_loader.add_value('directions_steps', directions_steps)
    
            loaded_item = recipe_loader.load_item()
            yield loaded_item

# WORK ON IMAGES
# WORK ON CUISINES, GETTING RECIPES ACCORDING TO CUISINES
