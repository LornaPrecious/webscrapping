import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from recipes.items import RecipesItem, AfriRecipeItem, WeeatatlastRecipesItem
from w3lib.html import remove_tags


# class AllrecipesSpider(CrawlSpider):
#     name = "allrecipes"  # The name of the Spider, it will be used to create unique requests and identify the spider
#     allowed_domains = ['allrecipes.com']
#     start_urls =['https://www.allrecipes.com/', 
#                  'https://www.allrecipes.com/recipes/17562/dinner/', 
#                  'https://www.allrecipes.com/recipes-a-z-6735880', 
#                  'https://www.allrecipes.com/ingredients-a-z-6740416', 
#                  'https://www.allrecipes.com/recipes/85/holidays-and-events/', 
#                  'https://www.allrecipes.com/cuisine-a-z-6740455']

#     rules = (
#         Rule(LinkExtractor(restrict_xpaths= ["//section[@id='taxonomysc_1-0']", "//section[@id='mntl-sc-block_2-0']", "//div[@class='loc article-content']", "//div[@class='loc fixedContent']", "//div[@class='loc recirc-content']"], allow ='/recipe/'), callback='parse', follow=True),
#     )
#     #Extract, Transform and load - request, parse, output

#     def parse(self, response):

#         for articles in response.xpath('//article[@id="allrecipes-article_1-0"]'):

#             recipe_loader = ItemLoader(item = RecipesItem(), selector=articles)
#             recipe_loader.default_input_processor = MapCompose(remove_tags)
            
#             #TITLE
#             recipe_loader.add_xpath("title", "//h1[@id='article-heading_1-0']")
#             # SUBHEADING - DESCRIPTION     
#             recipe_loader.add_xpath("subheading",'//p[@id="article-subheading_1-0"]')    
#             # IMAGES 
#             recipe_loader.add_xpath("image",'//div[@class="primary-image__media"]//div[@class="img-placeholder"]')  


#             #************ ADDING PREP, COOK, TOTAL TIME and SERVINGS ***************

#             recipe_details = response.xpath('//div[@class="mntl-recipe-details__item"]')

#             for detail in recipe_details:
#                 # recipe_loader = ItemLoader(item = RecipesItem(), response=response)
#                 # recipe_loader.default_input_processor = MapCompose(remove_tags)
            
#                 label = detail.xpath('.//div[@class="mntl-recipe-details__label"]/text()').get()
#                 value = detail.xpath('.//div[@class="mntl-recipe-details__value"]/text()').get()

#                 # Extracting data based on label
#                 if label == 'Prep Time:':
#                     recipe_loader.add_value('prep_time', value.strip())
#                 elif label == 'Cook Time:':
#                     recipe_loader.add_value('cook_time', value.strip())
#                 elif label == 'Total Time:':
#                     recipe_loader.add_value('total_time', value.strip())
#                 elif label == 'Servings:':
#                     recipe_loader.add_value('servings', value.strip())
#                 elif label == 'Yield:':
#                     recipe_loader.add_value('yield_result', value.strip())

#         #******************************** INGREDIENTS ********************************

#             ingredients = response.xpath('//ul[@class="mntl-structured-ingredients__list"]/li')

#             ingredients_list = [] 

#             for ingredient in ingredients:
#                 # Extract the text of each list item (ingredient)
#                 ingredient_text = ' '.join(ingredient.xpath('./p/span/text()').getall())
                
#                 # Append each ingredient to a list
#                 ingredients_list.append(ingredient_text.strip() if ingredient_text else '')

#             # Store the list of ingredients in the item
#             recipe_loader.add_value('ingredients_list', ingredients_list)

       
#         #*************************** COOKING DIRECTIONS *******************      
#             cooking_directions = response.xpath("//ol[@id='mntl-sc-block_2-0']/li")

#             directions_steps = []

#             for direction in cooking_directions:
#                 # Extract the text of each list item (cooking step)
#                 step_text = direction.xpath('./p[@class="comp mntl-sc-block mntl-sc-block-html"]/text()').get()
        
#                 # Append each cooking step to a list
#                 directions_steps.append(step_text.strip() if step_text else '')

#             # Store the list of cooking directions in the item
#             recipe_loader.add_value('directions_steps', directions_steps)

            
            
#         # RECIPE TIP
#             recipe_loader.add_xpath( "recipe_tip",'//div[@id="mntl-sc-block-callout-body_1-0"]')

#         #********************* NUTRITION TIPS*************************************

#             recipe_loader_nutrition = ItemLoader(item = RecipesItem(), selector=articles)

#             nutrition_facts_list = []
#             rows = response.xpath('//table[@class="mntl-nutrition-facts-summary__table"]/tbody/tr')
            
#             for row in rows:
#                 nutrition_facts = {}
             
#                 label = row.xpath('./td[@class="mntl-nutrition-facts-summary__table-cell type--dog"]/text()').get()
#                 value = row.xpath('./td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]/text()').get()

#                 if label and value:
#                     nutrition_facts[label.strip()] = value.strip()
#                     nutrition_facts_list.append(nutrition_facts)
                   
                   
#             recipe_loader_nutrition.add_value('nutrition_facts', nutrition_facts_list)
#             yield recipe_loader_nutrition.load_item()


#             #CALORIES
#             recipe_loader.add_xpath("calories",'//table[@class="mntl-nutrition-facts-summary__table"]/tbody/tr[1]/td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]'),
    
#             loaded_item = recipe_loader.load_item()
#             yield loaded_item

#WORK ON IMAGES
#WORK ON CUISINES, GETTING RECIPES ACCORDING TO CUISINES

#***************************************************************************************************************************************


# class AfrifoodNetworkSpider(CrawlSpider):
#     name = "afrifoodnetwork"  
#     allowed_domains = ['afrifoodnetwork.com']
#     start_urls =['https://afrifoodnetwork.com/', 
#                  'https://afrifoodnetwork.com/recipes/'
#                  'https://afrifoodnetwork.com/recipes/breakfast-recipes/', 
#                  'https://afrifoodnetwork.com/recipes/chicken-beef-recipes/', 
#                  'https://afrifoodnetwork.com/recipes/condiment/', 
#                  'https://afrifoodnetwork.com/recipes/dessert-recipes/'
#                 ]

#     rules = (
#         Rule(LinkExtractor(allow ='recipes/'), callback='parse', follow=True),
#     )
   
#     def parse(self, response):
           
#         for articles in response.xpath("//article[@id='template-id-14295']"):
            
#             afriRecipe_loader = ItemLoader(item = AfriRecipeItem(), selector=articles)
#             afriRecipe_loader.default_input_processor = MapCompose(remove_tags)
            
#             #TITLE
#             afriRecipe_loader.add_xpath("title", "//h2[@class='wprm-recipe-name wprm-block-text-bold']")
#             # SUBHEADING - DESCRIPTION     
#             afriRecipe_loader.add_xpath("subheading","//div[contains(@class,'wprm-recipe-summary wprm-block-text-normal')]/span")   
#             # IMAGES 
#             afriRecipe_loader.add_xpath("image","//div[@class='wprm-recipe-image wprm-block-image-rounded']/img")


#             #************ ADDING PREP, COOK, TOTAL TIME and SERVINGS ***************

#             prep_time = articles.xpath("//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-prep_time wprm-recipe-prep_time-minutes']").get()

#             afriRecipe_loader.add_value('prep_time', prep_time)

#             cook_time = articles.xpath("//span[contains(@class,'wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-cook_time wprm-recipe-cook_time-minutes')]").get()
           
#             afriRecipe_loader.add_value('cook_time', cook_time)

#             total_time = articles.xpath("//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes']").get()
           
#             afriRecipe_loader.add_value('total_time', total_time)
             
#             afriRecipe_loader.add_xpath("course", "//span[@class='wprm-recipe-course wprm-block-text-normal']")
#             afriRecipe_loader.add_xpath("cuisine", "//span[@class='wprm-recipe-cuisine wprm-block-text-normal']")
#         #******************************** INGREDIENTS ********************************

#             ingredients = response.xpath("//ul[@class='wprm-recipe-ingredients']/li")

#             ingredients_list = [] 

#             for ingredient in ingredients:
#                 # Extract the text of each list item (ingredient)
#                 ingredient_text = ' '.join(ingredient.xpath('./span/text()').getall())
                
#                 # Append each ingredient to a list
#                 ingredients_list.append(ingredient_text.strip() if ingredient_text else '')

#             # Store the list of ingredients in the item
#             afriRecipe_loader.add_value('ingredients_list', ingredients_list)
  
#         #*************************** COOKING DIRECTIONS *******************      
#             cooking_directions = response.xpath("//ul[@class='wprm-recipe-instructions']/li")

#             directions_steps = []

#             for direction in cooking_directions:
#                 # Extract the text of each list item (cooking step)
#                 step_text = direction.xpath('./div[@class="wprm-recipe-instruction-text"]/span/text() | ./div[@class="wprm-recipe-instruction-text"]/text()').get()
        
#                 # Append each cooking step to a list
#                 directions_steps.append(step_text.strip() if step_text else '')

#             # Store the list of cooking directions in the item
#             afriRecipe_loader.add_value('directions_steps', directions_steps)  
            
        
#             loaded_item = afriRecipe_loader.load_item()
#             yield loaded_item

#         next_page = response.xpath("//a[@aria-label='next-page']").attrib['href']
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)

#WORK ON IMAGES 
            

#******************************************************************************************************************************
#KENYAN, african RECIPES  && others

#Can get cuisine country from the name
class weeatatlastRecipeSpider(CrawlSpider):
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
            weeatatlastrecipe_loader.add_xpath("image",'//div[@class="primary-image__media"]//div[@class="img-placeholder"]')  


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
            recipe_loader_nutrition = ItemLoader(item = WeeatatlastRecipesItem(), selector=articles)

            nutrition_facts_list = []
            rows = response.xpath('//div[@class="wprm-nutrition-label-container wprm-nutrition-label-container-grouped wprm-block-text-normal"]/span')
            
            for row in rows:
                nutrition_facts = {}
             
                label = row.xpath('./span[@class="wprm-nutrition-label-text-nutrition-label  wprm-block-text-faded"]/text()').get()
                value = row.xpath('./span[contains(@class,"wprm-nutrition-label-text-nutrition-value")]/text()').get()

                if label and value:
                    nutrition_facts[label.strip()] = value.strip()
                    nutrition_facts_list.append(nutrition_facts)
                   
                   
            recipe_loader_nutrition.add_value('nutrition_facts', nutrition_facts_list)
            yield recipe_loader_nutrition.load_item()


            loaded_item = weeatatlastrecipe_loader.load_item()
            yield loaded_item

        next_page = response.xpath("//a[@class='next page-numbers']/@href").extract()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

#********************************************************************************************************************************

