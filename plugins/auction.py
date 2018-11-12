from disco.bot import Plugin
import requests
import json
import math
import urllib

SEARCH_URL = 'http://classicffxi.com/ajax/'

class AuctionPlugin(Plugin):

  @Plugin.command('search', '[item_name:str...]')
  def on_auction_Search(self, event, item_name):
    formatted_item_name = item_name.lower().replace(' ', '_')
    qs = {
      'name': item_name
    }
    r = requests.get('{}items'.format(SEARCH_URL), params=qs)

    search_response = r.json()
    if not search_response:
      event.msg.reply('Could not find listings for {}'.format(item_name))
      return

    real_item = [obj for obj in search_response if obj['name'] == formatted_item_name][0]
    item_id = real_item['id']
    payload = {
      'id': item_id
    }

    r = requests.get('{}item'.format(SEARCH_URL), params=payload)

    price_response = r.json()
    items = price_response['ahhistory']
    if not items:
      event.msg.reply('No price history found for {}'.format(item_name))
      return
    total = []
    for price in items:
      total.append(int(price['sale']))
    total.sort()
    median = total[int(math.floor(len(total)/2))]

    event.msg.reply('Median {} price: {} gil'.format(item_name, median))
