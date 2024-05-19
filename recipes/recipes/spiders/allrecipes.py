import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from items import RecipesItem
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
        Rule(LinkExtractor(restrict_xpaths= ["//section[@id='taxonomysc_1-0']", "//section[@id='mntl-sc-block_2-0']", "//main[@id='main']", "//div[@class='loc article-content']", "//div[@class='loc fixedContent']", "//div[@class='loc recirc-content']"], allow ='/recipe/'), callback='parse', follow=True),
    )
    #Extract, Transform and load - request, parse, output

    def parse(self, response):

        for articles in response.xpath('//article[@id="allrecipes-article_1-0"]'):

            recipe_loader = ItemLoader(item = RecipesItem(), selector=articles)
            recipe_loader.default_input_processor = MapCompose(remove_tags)
            
            
            #TITLE loc article-post-header
            recipe_loader.add_xpath("title", "//div[@id='article-header--recipe_1-0']/h1")
            
            # # SUBHEADING - DESCRIPTION     
            # recipe_loader.add_xpath("subheading",'//p[@id="article-subheading"]')    
            # IMAGES 
            recipe_loader.add_xpath("image_url", '//div[@class="primary-image__media"]//div[@class="img-placeholder"]/img/@src')

            #recipe_loader.add_css('div.primary-image__media img::attr(src)').get()

            
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
            cooking_directions = response.xpath("//ol[@class='comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--OL']/li")

            directions_steps = []

            for direction in cooking_directions:
                # Extract the text of each list item (cooking step)
                step_text = direction.xpath('./p[@class="comp mntl-sc-block mntl-sc-block-html"]/text()').get()
        
                # Append each cooking step to a list
                directions_steps.append(step_text.strip() if step_text else '')

            # Store the list of cooking directions in the item
            recipe_loader.add_value('directions_steps', directions_steps)


        #********************* NUTRITION TIPS*************************************

            recipe_loader_nutrition = ItemLoader(item = RecipesItem(), selector=articles)

            nutrition_facts_list = []
            rows = response.xpath('//table[@class="mntl-nutrition-facts-summary__table"]/tbody/tr')
            
            for row in rows:
                nutrition_facts = {}
             
                label = row.xpath('./td[@class="mntl-nutrition-facts-summary__table-cell type--dog"]/text()').get()
                value = row.xpath('./td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]/text()').get()

                if label and value:
                    nutrition_facts[label.strip()] = value.strip()
                    nutrition_facts_list.append(nutrition_facts)
                   
                   
            recipe_loader_nutrition.add_value('nutrition_facts', nutrition_facts_list)
            yield recipe_loader_nutrition.load_item()


            #CALORIES
            recipe_loader.add_xpath("calories",'//table[@class="mntl-nutrition-facts-summary__table"]/tbody/tr[1]/td[@class="mntl-nutrition-facts-summary__table-cell type--dog-bold"]'),
    
            loaded_item = recipe_loader.load_item()
            yield loaded_item

# WORK ON IMAGES
# WORK ON CUISINES, GETTING RECIPES ACCORDING TO CUISINES
