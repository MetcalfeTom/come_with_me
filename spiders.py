import scrapy
from bs4 import BeautifulSoup
from constants import top_munch, BASE_URL


class Restaurant(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()


class Attraction(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()


class RestaurantSpider(scrapy.spiders.CrawlSpider):
    """Spider which scrapes top Tripadvsior restaurants."""

    name = "restaurants"

    def parse(self, response):
        """Retrieve the URLs for top restaurants from the city."""

        soup = BeautifulSoup(response.text, 'html.parser')
        overview_box = soup.find(None, {'id': 'EATERY_OVERVIEW_BOX'})
        all_places = overview_box.find_all(None, {'class': 'property_title'})

        # filter out sponsored results
        top_places = []
        for place in all_places:
            review_link = place.attrs.get('href')

            if review_link:
                top_places.append(review_link)

            if len(top_places) == top_munch:
                break

        review_urls = ["{}{}".format(BASE_URL, rev) for rev in top_places]

        for url in review_urls:
            yield scrapy.Request(url, callback=self.parse_restaurant)

    @staticmethod
    def parse_restaurant(response):
        """Parse necessary information from the restaurant page."""

        soup = BeautifulSoup(response.text, 'html.parser')
        item = Restaurant()

        item['name'] = soup.find('h1', {'class': 'ui_header h1'}).text
        item['location'] = soup.find('span', {'class': 'detail'}).text

        yield item
