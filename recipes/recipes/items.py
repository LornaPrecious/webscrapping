# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipesItem(scrapy.Item):
   title = scrapy.Field()
   subheading = scrapy.Field()
   image = scrapy.Field()

   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   total_time = scrapy.Field()
   servings = scrapy.Field()
   yield_result = scrapy.Field()

   ingredients_list = scrapy.Field()

   directions_steps = scrapy.Field()

   recipe_tip = scrapy.Field()

   calories = scrapy.Field()
   fat = scrapy.Field()
   carbs = scrapy.Field()
   protein = scrapy.Field()