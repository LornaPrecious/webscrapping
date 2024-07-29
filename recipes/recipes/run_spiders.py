from scrapy.crawler import CrawlerProcess
from spiders.allrecipes import AllrecipesSpider
from spiders.dessertfortwo import DessertForTwoSpider
from spiders.beans import BeansrecipeSpider
from spiders.vegan import VeganuarySpider
#from spiders.afrifood_network import AfrifoodNetworkSpider
from spiders.weeatatlastRecipes import WeeatatlastRecipeSpider
from scrapy.utils.project import get_project_settings

import settings

# Create a list of spider classes
spiders = [WeeatatlastRecipeSpider] #AllrecipesSpider, AfrifoodNetworkSpider, weeatatlastRecipeSpider]

# Create a CrawlerProcess with project settings
process = CrawlerProcess(settings=get_project_settings())

# Start each spider in the list
for spider in spiders:
    process.crawl(spider)

# Run the process (blocking call)
process.start()
