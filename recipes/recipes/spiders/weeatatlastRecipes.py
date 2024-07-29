import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from items import WeeatatlastRecipesItem
from w3lib.html import remove_tags

# ******************************************************************************************************************************
# KENYAN, african RECIPES  && others

# Can get cuisine country from the name
class WeeatatlastRecipeSpider(CrawlSpider):
    name = "weeatatlast"  # The name of the Spider, it will be used to create unique requests and identify the spider
    allowed_domains = ['weeatatlast.com']
    start_urls =['https://weeatatlast.com/',
                 'https://weeatatlast.com/20-plus-top-kenyan-food-recipes/',
                 'https://weeatatlast.com/category/international-cuisine-recipes/',
                 'https://weeatatlast.com/category/kenyan-and-other-african-dishes/',
                 'https://weeatatlast.com/category/ninja-foodi-recipes/'
                 ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths= ["//div[@id='genesis-content']"]), callback='parse', follow=True),
    )
    #Extract, Transform and load - request, parse, output

    def parse(self, response):

        for articles in response.xpath("//div[@class='wprm-recipe wprm-recipe-template-template-kate']"):

            weeatatlastrecipe_loader = ItemLoader(item = WeeatatlastRecipesItem(), selector=articles)
            weeatatlastrecipe_loader.default_input_processor = MapCompose(remove_tags)
            
            #TITLE
            weeatatlastrecipe_loader.add_xpath("title", "//h2[@class ='wprm-recipe-name wprm-block-text-bold']") 
            # SUBHEADING - DESCRIPTION     
            weeatatlastrecipe_loader.add_xpath("subheading", "//div[@class='wprm-recipe-summary wprm-block-text-normal']/span")  
            # IMAGES 
            weeatatlastrecipe_loader.add_xpath("image",'//div[@class="primary-image__media"]//div[@class="img-placeholder"]/img/@src')  


#************ ADDING PREP, COOK, TOTAL TIME and SERVINGS ***************

            prep_time = articles.xpath("//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-prep_time wprm-recipe-prep_time-minutes']").get()

            weeatatlastrecipe_loader.add_value('prep_time', prep_time)

            cook_time = articles.xpath("//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-cook_time wprm-recipe-cook_time-minutes']").get()
           
            weeatatlastrecipe_loader.add_value('cook_time', cook_time)

            total_time = articles.xpath("//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes']").get()
           
            weeatatlastrecipe_loader.add_value('total_time', total_time)
             
            weeatatlastrecipe_loader.add_xpath("course", "//span[@class='wprm-recipe-course wprm-block-text-normal']")
            weeatatlastrecipe_loader.add_xpath("cuisine", "//span[@class='wprm-recipe-cuisine wprm-block-text-normal']")
            weeatatlastrecipe_loader.add_xpath("servings", "//span[@aria-label='Adjust recipe servings']")
            weeatatlastrecipe_loader.add_xpath("calories", "//span[@class='wprm-recipe-details wprm-recipe-nutrition wprm-recipe-calories wprm-block-text-normal']")
      
        #******************************** INGREDIENTS ********************************

            ingredients = response.xpath("//ul[@class='wprm-recipe-ingredients']/li")

            ingredients_list = [] 

            for ingredient in ingredients:
                # Extract the text of each list item (ingredient)
                ingredient_text = ' '.join(ingredient.xpath('.//span[contains(@class, "wprm-recipe-ingredient")]/text()').getall())
                
                # Append each ingredient to a list
                ingredients_list.append(ingredient_text.strip() if ingredient_text else '')

            # Store the list of ingredients in the item
            weeatatlastrecipe_loader.add_value('ingredients_list', ingredients_list)

       
        #*************************** COOKING DIRECTIONS *******************      
            cooking_directions = response.xpath("//ul[@class='wprm-recipe-instructions']/li")

            directions_steps = []

            for direction in cooking_directions:
                # Extract the text of each list item (cooking step)
                step_text = direction.xpath('./div[@class="wprm-recipe-instruction-text"]/span/text()').get()
        
                # Append each cooking step to a list
                directions_steps.append(step_text.strip() if step_text else '')

            # Store the list of cooking directions in the item
            weeatatlastrecipe_loader.add_value('directions_steps', directions_steps)

    #***************************** NUTRITION FACTS *********************************************************************

            nutrition_facts_list = []
            rows = response.xpath('//div[@class="wprm-nutrition-label-container wprm-nutrition-label-container-grouped wprm-block-text-normal"]/span')
            
            for row in rows:
                nutrition_facts = {}
             
                label = row.xpath('./span[@class="wprm-nutrition-label-text-nutrition-label  wprm-block-text-faded"]/text()').get()
                value = row.xpath('./span[contains(@class,"wprm-nutrition-label-text-nutrition-value")]/text()').get()

                if label and value:
                    nutrition_facts[label.strip()] = value.strip()
                    nutrition_facts_list.append(nutrition_facts)
                   
                nutrition_facts_list_string = str(nutrition_facts_list)  
            weeatatlastrecipe_loader.add_value('nutrition_facts', nutrition_facts_list_string)
          

            loaded_item = weeatatlastrecipe_loader.load_item()
            yield loaded_item

        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page is not None:
            yield scrapy.Request(url = next_page, callback=self.parse)
        