import argparse
import logging

from constants import BASE_URL, top_munch
from spiders import RestaurantSpider
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher


def create_argument_parser():
    """Parse all the command line arguments for scraping."""

    parser = argparse.ArgumentParser(description='Scrape TripAdvisor')
    parser.add_argument('id', help='the geolocation id of the city')
    parser.add_argument('name', help='the name of the city')
    return parser


def create_tripadvsior_urls(city_id, city_name):
    """Creates the relevant urls for attractions and restaurants."""

    attractions = '/Attractions-g{}-Activities-{}.html'.format(city_id,
                                                               city_name)
    city_attractions = BASE_URL + attractions

    restaurants = '/Restaurants-g{}-{}.html'.format(city_id, city_name)
    city_restaurants = BASE_URL + restaurants

    return city_restaurants, city_attractions


# TODO: Make async
def crawl_tripadvisor(url):
    """Starts crawling process and returns results as a dict."""
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})

    process.crawl(RestaurantSpider(),
                  start_urls=[url])
    process.start()
    return results


if __name__ == "__main__":
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()

    logger = logging.getLogger(__name__)
    logging.getLogger().addHandler(logging.StreamHandler())

    restaurants_url, attractions_url = create_tripadvsior_urls(args.id,
                                                               args.name)
    results = crawl_tripadvisor(restaurants_url)

    # TODO: Make pretty output
    place_names = [place.get("name") for place in results]
    logger.info('The top {} restaurants in {} are: {}'.format(top_munch,
                                                              args.name,
                                                              place_names))
