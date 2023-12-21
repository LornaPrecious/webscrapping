import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from recipes.items import RecipesItem
from w3lib.html import remove_tags


class AllrecipesSpider(CrawlSpider):
    name = "allrecipes"  # The name of the Spider, it will be used to create unique requests and identify the spider
    allowed_domains = ['allrecipes.com']
    start_urls =['https://www.allrecipes.com/', 
                 'https://www.allrecipes.com/recipes/17562/dinner/', 
                 'https://www.allrecipes.com/recipes-a-z-6735880', 
                 'https://www.allrecipes.com/ingredients-a-z-6740416', 
                 'https://www.allrecipes.com/recipes/85/holidays-and-events/', 
                 'https://www.allrecipes.com/cuisine-a-z-6740455']

    rules = (
        Rule(LinkExtractor(restrict_xpaths= ["//section[@id='taxonomysc_1-0']", "//section[@id='mntl-sc-block_2-0']", "//div[@class='loc article-content']", "//div[@class='loc fixedContent']", "//div[@class='loc recirc-content']"], allow ='/recipe/'), callback='parse', follow=True),
    )
    #Extract, Transform and load - request, parse, output

    def parse(self, response):
        
       
        for articles in response.xpath('//article[@id="allrecipes-article_1-0"]'):

            recipe_loader = ItemLoader(item = RecipesItem(), selector=articles)
            recipe_loader.default_input_processor = MapCompose(remove_tags)
            
            #TITLE
            recipe_loader.add_xpath("title", "//h1[@id='article-heading_1-0']"), 
            # SUBHEADING - DESCRIPTION     
            recipe_loader.add_xpath("subheading",'//p[@id="article-subheading_1-0"]'),    
            # IMAGES 
            recipe_loader.add_xpath("image",'//div[@class="primary-image__media"]/div[@class="img-placeholder"]'),  


            #************ ADDING PREP, COOK, TOTAL TIME and SERVINGS ***************

            recipe_details = response.xpath('//div[@class="mntl-recipe-details__item"]')

            for detail in recipe_details:
                # recipe_loader = ItemLoader(item = RecipesItem(), response=response)
                # recipe_loader.default_input_processor = MapCompose(remove_tags)
            
                label = detail.xpath('.//div[@class="mntl-recipe-details__label"]/text()').get()
                value = detail.xpath('.//div[@class="mntl-recipe-details__value"]/text()').get()

                # Extracting data based on label
                if label == 'Prep Time:':
                    recipe_loader.add_value('prep_time', value.strip())
                elif label == 'Cook Time:':
                    recipe_loader.add_value('cook_time', value.strip())
                elif label == 'Total Time:':
                    recipe_loader.add_value('total_time', value.strip())
                elif label == 'Servings:':
                    recipe_loader.add_value('servings', value.strip())
                elif label == 'Yield:':
                    recipe_loader.add_value('yield_result', value.strip())

        #******************************** INGREDIENTS ********************************

            ingredients = response.xpath('//ul[@class="mntl-structured-ingredients__list"]/li')

            ingredients_list = [] 

            for ingredient in ingredients:
                # Extract the text of each list item (ingredient)
                ingredient_text = ' '.join(ingredient.xpath('./p/span/text()').getall())
                
                # Append each ingredient to a list
                ingredients_list.append(ingredient_text.strip() if ingredient_text else '')

            # Store the list of ingredients in the item
            recipe_loader.add_value('ingredients_list', ingredients_list)

       
        #*************************** COOKING DIRECTIONS *******************      
            cooking_directions = response.xpath("//ol[@id='mntl-sc-block_2-0']/li")

            directions_steps = []

            for direction in cooking_directions:
                # Extract the text of each list item (cooking step)
                step_text = direction.xpath('./p[@class="comp mntl-sc-block mntl-sc-block-html"]/text()').get()
        
                # Append each cooking step to a list
                directions_steps.append(step_text.strip() if step_text else '')

            # Store the list of cooking directions in the item
            recipe_loader.add_value('directions_steps', directions_steps)

            
            
        # RECIPE TIP
            recipe_loader.add_xpath( "recipe_tip",'//div[@id="mntl-sc-block-callout-body_1-0"]'),

        #********************* NUTRITION TIPS*************************************
           
            recipe_loader.add_xpath("calories",'//table[@class="mntl-nutrition-facts-summary__table"]/tr[1]/td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]'),
            recipe_loader.add_xpath("fat",'//table[@class="mntl-nutrition-facts-summary__table"]/tr[2]/td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]')
            recipe_loader.add_xpath("carbs",'//table[@class="mntl-nutrition-facts-summary__table"]/tr[3]/td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]')
            recipe_loader.add_xpath("protein",'//table[@class="mntl-nutrition-facts-summary__table"]/tr[4]/td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]')

            # 'Nutrition facts': articles.xpath('//table[@class="mntl-nutrition-facts-label__table"]').get()
            

            loaded_item = recipe_loader.load_item()
            yield loaded_item
    


   


#//ol[@class="comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup"]/li           
#Running spider - recipes scrapy crawl allrecipes -o allrecipes.csv(.json)) (o -for output, capital o (O) overides what was previously saved in the json/csv files)
#