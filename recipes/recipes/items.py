# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipesItem(scrapy.Item):
   title = scrapy.Field()
   image_url = scrapy.Field()
   image = scrapy.Field()
   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   total_time = scrapy.Field()
   additional_time = scrapy.Field()
   servings = scrapy.Field()
   yield_result = scrapy.Field()
   ingredients_list = scrapy.Field()
   directions_steps = scrapy.Field()
   nutrition_facts = scrapy.Field()
   recipe_details_list = scrapy.Field()
 

class AfriRecipeItem(scrapy.Item):
   title = scrapy.Field()
   subheading = scrapy.Field()
   image_url = scrapy.Field()
   image = scrapy.Field()
   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   total_time = scrapy.Field()
   course = scrapy.Field()
   cuisine = scrapy.Field()
   ingredients_list = scrapy.Field()
   directions_steps = scrapy.Field()


class WeeatatlastRecipesItem(scrapy.Item):
   title = scrapy.Field()
   subheading = scrapy.Field()
   image_url = scrapy.Field()
   image = scrapy.Field()
   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   total_time = scrapy.Field()
   course = scrapy.Field()
   cuisine = scrapy.Field()
   servings = scrapy.Field()
   calories = scrapy.Field()
   ingredients_list = scrapy.Field()
   directions_steps = scrapy.Field()
   nutrition_facts = scrapy.Field()


class Food24RecipeItem(scrapy.Item):
   title = scrapy.Field()
   subheading = scrapy.Field()
   image_url = scrapy.Field()
   image = scrapy.Field()
   servings = scrapy.Field()
   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   ingredients_list = scrapy.Field()
   directions_steps = scrapy.Field()


class DessertfortwoRecipeItem(scrapy.Item):
   title = scrapy.Field()
   subheading = scrapy.Field()
   image_url = scrapy.Field()
   image = scrapy.Field()
   yield_result = scrapy.Field()
   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   total_time = scrapy.Field()
   ingredients_list = scrapy.Field()
   directions_steps = scrapy.Field()
   recipe_tip = scrapy.Field() 
   serving_size = scrapy.Field() 
   calories = scrapy.Field() 
   total_fat_value = scrapy.Field() 
   saturated_fat_value = scrapy.Field() 
   trans_fat_value = scrapy.Field() 
   unsaturated_fat_value = scrapy.Field() 
   cholesterol_value = scrapy.Field() 
   sodium_value = scrapy.Field() 
   carbohydrates_value = scrapy.Field() 
   fiber_value = scrapy.Field() 
   sugar_value = scrapy.Field() 
   protein = scrapy.Field() 
   substitution_addition = scrapy.Field()
   video_url = scrapy.Field()
   video = scrapy.Field()

class BeanRecipeItem(scrapy.Item):
   title = scrapy.Field()
   subheading = scrapy.Field()
   image_url = scrapy.Field()
   image = scrapy.Field()
   yield_result = scrapy.Field()
   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   total_time = scrapy.Field()
   ingredients_list = scrapy.Field()
   directions_steps = scrapy.Field()
   recipe_tip = scrapy.Field() 
   serving_size = scrapy.Field() 
   calories = scrapy.Field() 
   total_fat_value = scrapy.Field() 
   saturated_fat_value = scrapy.Field() 
   trans_fat_value = scrapy.Field() 
   unsaturated_fat_value = scrapy.Field() 
   cholesterol_value = scrapy.Field() 
   sodium_value = scrapy.Field() 
   carbohydrates_value = scrapy.Field() 
   fiber_value = scrapy.Field() 
   sugar_value = scrapy.Field() 
   protein = scrapy.Field() 
   substitution_addition = scrapy.Field()
   video_url = scrapy.Field()
   video = scrapy.Field()


class VeganuaryRecipeItem(scrapy.Item):
   title = scrapy.Field()
   subheading = scrapy.Field()
   image_url = scrapy.Field()
   image = scrapy.Field()
   servings = scrapy.Field()
   prep_time = scrapy.Field()
   cook_time = scrapy.Field()
   ingredients_list = scrapy.Field()
   directions_steps = scrapy.Field()
