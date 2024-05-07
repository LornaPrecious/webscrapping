import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from items import AfriRecipeItem
from w3lib.html import remove_tags


class AfrifoodNetworkSpider(CrawlSpider):
    name = "afrifoodnetwork"  
    allowed_domains = ['afrifoodnetwork.com']
    start_urls =['https://afrifoodnetwork.com/', 
                 'https://afrifoodnetwork.com/recipes/'
                 'https://afrifoodnetwork.com/recipes/breakfast-recipes/', 
                 'https://afrifoodnetwork.com/recipes/chicken-beef-recipes/', 
                 'https://afrifoodnetwork.com/recipes/condiment/', 
                 'https://afrifoodnetwork.com/recipes/dessert-recipes/'
                ]

    rules = (
        Rule(LinkExtractor(allow ='recipes/'), callback='parse', follow=True),
    )
   
    def parse(self, response):
           
        for articles in response.xpath("//article[@id='template-id-14295']"):
            
            afriRecipe_loader = ItemLoader(item = AfriRecipeItem(), selector=articles)
            afriRecipe_loader.default_input_processor = MapCompose(remove_tags)
            
            #TITLE
            afriRecipe_loader.add_xpath("title", "//h2[@class='wprm-recipe-name wprm-block-text-bold']")
            # SUBHEADING - DESCRIPTION     
            afriRecipe_loader.add_xpath("subheading","//div[contains(@class,'wprm-recipe-summary wprm-block-text-normal')]/span")   
            # IMAGES 
            afriRecipe_loader.add_xpath("image","//div[@class='wprm-recipe-image wprm-block-image-rounded']//img/@src")


            #************ ADDING PREP, COOK, TOTAL TIME and SERVINGS ***************

            prep_time = articles.xpath("//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-prep_time wprm-recipe-prep_time-minutes']").get()

            afriRecipe_loader.add_value('prep_time', prep_time)

            cook_time = articles.xpath("//span[contains(@class,'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-cook_time wprm-recipe-cook_time-minutes')]").get()
           
            afriRecipe_loader.add_value('cook_time', cook_time)

            total_time = articles.xpath("//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes']").get()
           
            afriRecipe_loader.add_value('total_time', total_time)
             
            afriRecipe_loader.add_xpath("course", "//span[@class='wprm-recipe-course wprm-block-text-normal']")
            afriRecipe_loader.add_xpath("cuisine", "//span[@class='wprm-recipe-cuisine wprm-block-text-normal']")
        #******************************** INGREDIENTS ********************************

            ingredients = response.xpath("//ul[@class='wprm-recipe-ingredients']/li")

            ingredients_list = [] 

            for ingredient in ingredients:
                # Extract the text of each list item (ingredient)
                ingredient_text = ' '.join(ingredient.xpath('./span/text()').getall())
                
                # Append each ingredient to a list
                ingredients_list.append(ingredient_text.strip() if ingredient_text else '')

            # Store the list of ingredients in the item
            afriRecipe_loader.add_value('ingredients_list', ingredients_list)
  
        #*************************** COOKING DIRECTIONS *******************      
            cooking_directions = response.xpath("//ul[@class='wprm-recipe-instructions']/li")

            directions_steps = []

            for direction in cooking_directions:
                # Extract the text of each list item (cooking step)
                step_text = direction.xpath('./div[@class="wprm-recipe-instruction-text"]/span/text() | ./div[@class="wprm-recipe-instruction-text"]/text()').get()
        
                # Append each cooking step to a list
                directions_steps.append(step_text.strip() if step_text else '')

            # Store the list of cooking directions in the item
            afriRecipe_loader.add_value('directions_steps', directions_steps)  
            
        
            loaded_item = afriRecipe_loader.load_item()
            yield loaded_item

        next_page = response.xpath("//a[@aria-label='next-page']").attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# WORK ON IMAGES 
            

