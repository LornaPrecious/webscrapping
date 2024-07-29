import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from items import DessertfortwoRecipeItem
from w3lib.html import remove_tags


class DessertForTwoSpider(CrawlSpider):
    name = "dessertfortwo"  # The name of the Spider, it will be used to create unique requests and identify the spider
    allowed_domains = ['dessertfortwo.com']
    start_urls =['https://www.dessertfortwo.com/', 
                 'https://www.dessertfortwo.com/recipes/', 
                 'https://www.dessertfortwo.com/category/breakfast/', 
                 'https://www.dessertfortwo.com/category/bread-2/', 
                 'https://www.dessertfortwo.com/category/donuts-2/', 
                 'https://www.dessertfortwo.com/category/muffins-scones/',
                 'https://www.dessertfortwo.com/category/chocolate-2/',
                 'https://www.dessertfortwo.com/category/brownies-2/',
                 'https://www.dessertfortwo.com/category/candy-2/',
                 'https://www.dessertfortwo.com/category/peanut-butter/',
                 'https://www.dessertfortwo.com/category/cupcakes/',
                 'https://www.dessertfortwo.com/category/cakes/',
                 'https://www.dessertfortwo.com/category/pies-and-cobblers/',
                 'https://www.dessertfortwo.com/category/cookies-and-bars/',
                 'https://www.dessertfortwo.com/category/dinners-for-two/',
                 'https://www.dessertfortwo.com/category/pasta-2/',
                 'https://www.dessertfortwo.com/category/meat-seafood/',
                 'https://www.dessertfortwo.com/category/drinks-for-two/',
                 'https://www.dessertfortwo.com/category/egg-white-only/',
                 'https://www.dessertfortwo.com/category/egg-yolk-only/',
                 'https://www.dessertfortwo.com/category/egg-free/',
                 'https://www.dessertfortwo.com/category/no-bake-2/',
                 'https://www.dessertfortwo.com/category/christmas/',
                 'https://www.dessertfortwo.com/category/apples/',
                 'https://www.dessertfortwo.com/category/pumpkin/',
                 'https://www.dessertfortwo.com/category/frozen-treats/',
                 'https://www.dessertfortwo.com/category/vegan/',
                 'https://www.dessertfortwo.com/category/paleo/',
                 'https://www.dessertfortwo.com/category/keto/',
                 'https://www.dessertfortwo.com/category/whole30/',
                 'https://www.dessertfortwo.com/category/dairy-free/',
                 'https://www.dessertfortwo.com/category/gluten-free-2/',
                 'https://www.dessertfortwo.com/category/healthy/',
                 'https://www.dessertfortwo.com/category/egg-free/',
                 'https://www.dessertfortwo.com/category/instant-pot/',
                 'https://www.dessertfortwo.com/category/crockpot/',
                 'https://www.dessertfortwo.com/category/freezer-meals/',
                 'https://www.dessertfortwo.com/category/baby-food/',
                 'https://www.dessertfortwo.com/category/fancy/',
                 'https://www.dessertfortwo.com/category/frosting-recipes/',
                 'https://www.dessertfortwo.com/category/party-food-ideas/',
                 'https://www.dessertfortwo.com/category/videos/'
                 
                 ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths= ["//main[@id='genesis-content']", "//div[@class='feast-category-index']", "//div[@class='feast-recipe-index']"]), callback='parse_item', follow=True),
    )
    #Extract, Transform and load - reque st, parse, output
    #post-42907 post type-post status-publish format-standard has-post-thumbnail category-breakfast category-egg-free mv-content-wrapper grow-content-body entry
    def parse_item(self, response): # div[@class='wp-block-mv-recipe']
        # div[@class='wp-block-mv-recipe']
        for articles in response.xpath(".//main[@class='content']/article/div[@class='entry-content']/section/div[@class='mv-create-wrapper'] | .//main[@class='content']/article/div[@class='entry-content']/div[@class='wp-block-mv-recipe']/section/div[@class='mv-create-wrapper']"):

            recipe_loader = ItemLoader(item = DessertfortwoRecipeItem(), selector=articles)
            recipe_loader.default_input_processor = MapCompose(remove_tags)
            
            #TITLE
            recipe_loader.add_xpath("title", "//div[@class='mv-create-title-wrap']/h2")
            # SUBHEADING - DESCRIPTION    *********  
            recipe_loader.add_xpath("subheading",'//div[@class="mv-create-description"]/p')    
            # IMAGES 
            recipe_loader.add_xpath("image_url", '//div[@class="mv-create-image-container"]/img/@src')

            #recipe_loader.add_css('div.mv-create-image-container img::attr(src)').get()

            
            #************ ADDING PREP, COOK, TOTAL TIME and SERVINGS ***************

            prep_time = articles.xpath("//div[@class='mv-create-time mv-create-time-prep']/span/span[@class='mv-time-part mv-time-minutes']/text()").get()

            recipe_loader.add_value('prep_time', prep_time)

            cook_time = articles.xpath("//div[@class='mv-create-time mv-create-time-active']/span/span[@class='mv-time-part mv-time-minutes']/text()").get()
           
            recipe_loader.add_value('cook_time', cook_time)

            total_time = articles.xpath("//div[@class='mv-create-time mv-create-time-total']/span/span[@class='mv-time-part mv-time-minutes']/text()").get()
           
            recipe_loader.add_value('total_time', total_time)
             
            recipe_loader.add_xpath("yield_result", "//span[@class='mv-create-yield mv-create-uppercase']")
           
        #******************************** INGREDIENTS ********************************

            ingredients = response.xpath('//div[@class="mv-create-ingredients"]/ul/li')

            ingredients_list = [] 

            for ingredient in ingredients:
                # Extract the text of each list item (ingredient)
                ingredient_text = ingredient.xpath('./text()').get()
                
                # Append each ingredient to a list
                ingredients_list.append(ingredient_text.strip() if ingredient_text else '')

            # Store the list of ingredients in the item
            recipe_loader.add_value('ingredients_list', ingredients_list)

       
        #*************************** COOKING DIRECTIONS *******************      
            cooking_directions = response.xpath("//div[@class='mv-create-instructions mv-create-instructions-slot-v2']/ol/li | //div[@class='mv-create-instructions mv-create-instructions-slot-v2']/ol/p")

            directions_steps = []

            for direction in cooking_directions:
                # Extract the text of each list item (cooking step)
                step_text = direction.xpath('./text()').get() 
        
                # Append each cooking step to a list
                directions_steps.append(step_text.strip() if step_text else '')

            # Store the list of cooking directions in the item
            recipe_loader.add_value('directions_steps', directions_steps)
            
        # RECIPE TIP
            recipe_loader.add_xpath( "recipe_tip",'//div[@class="mv-create-notes-content"]/p/text()')


        #********************* NUTRITION TIPS*************************************

            serving_size = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-serving-size']/text()").get()
            recipe_loader.add_value('serving_size', serving_size)
            total_fat= articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-total-fat']/text()").get()
            recipe_loader.add_value('total_fat_value', total_fat)
            saturated_fat_value = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-saturated-fat mv-create-nutrition-indent']/text()").get()
            recipe_loader.add_value('saturated_fat_value', saturated_fat_value)
            trans_fat_value = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-trans-fat mv-create-nutrition-indent']/text()").get()
            recipe_loader.add_value('trans_fat_value', trans_fat_value)
            unsaturated_fat_value = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-unsaturated-fat mv-create-nutrition-indent']/text()").get()
            recipe_loader.add_value('unsaturated_fat_value', unsaturated_fat_value)
            cholesterol_value = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-cholesterol']/text()").get()
            recipe_loader.add_value('cholesterol_value', cholesterol_value)
            sodium_value = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-sodium']/text()").get()
            recipe_loader.add_value('sodium_value', sodium_value)
            carbohydrates_value = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-carbohydrates']/text()").get()
            recipe_loader.add_value('carbohydrates_value', carbohydrates_value)
            fiber_value = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-fiber mv-create-nutrition-indent']/text()").get()
            recipe_loader.add_value('fiber_value', fiber_value)
            protein = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-protein']/text()").get()
            recipe_loader.add_value('protein', protein)
            calories = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-calories']/text()").get()
            recipe_loader.add_value('calories', calories)
            sugar = articles.xpath("//span[@class='mv-create-nutrition-item mv-create-nutrition-sugar mv-create-nutrition-indent']/text()").get()
            recipe_loader.add_value('sugar_value', sugar)
            

            loaded_item = recipe_loader.load_item()
            yield loaded_item

        # Follow pagination links
        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page is not None:
            yield scrapy.Request(url = next_page, callback=self.parse)
            
    #     next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
    #    # if next_page is not None:
    #     yield response.follow(next_page, callback=self.parse_item)
# WORK ON IMAGES
# WORK ON CUISINES, GETTING RECIPES ACCORDING TO CUISINES
