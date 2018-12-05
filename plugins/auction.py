from disco.bot import Plugin
from disco.types.message import MessageEmbed
import requests
import json
import math
import urllib
from datetime import datetime

SEARCH_URL = 'http://classicffxi.com/ajax/'
WIKI_URL = 'https://www.bg-wiki.com/bg/'
IMAGE_URL = 'https://static.ffxiah.com/images/icon/'

class AuctionPlugin(Plugin):

  @Plugin.command('search', '[item_name:str...]')
  def on_auction_Search(self, event, item_name):
    formatted_item_name = item_name.lower().replace(' ', '_').replace('\'', '').replace(',', '')
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

    last_5 = price_response['ahhistory'][0:5]

    event.msg.reply(**self.create_embed(item_name, item_id, median, formatted_item_name, price_response['ahstock'], last_5))

  def create_embed(self, item_name, item_id, median_price, formatted_item_name, stock, last_5):
    print formatted_item_name
    formatted_item_name = urllib.quote_plus(formatted_item_name)

    embed = MessageEmbed()
    embed.set_author(name=item_name,
                     url='{}{}'.format(WIKI_URL, formatted_item_name),
                     icon_url='{}{}.png'.format(IMAGE_URL, item_id))

    five_price = five_date = ''
    for x in last_5:
      five_price += '\n{}'.format(x['sale'])
      five_date += '\n{}'.format(datetime.fromtimestamp(x['sell_date']))

    embed.add_field(name='Current Stock', value=stock, inline=False)
    embed.add_field(name='Last 5 Sold', value=five_price, inline=True)
    embed.add_field(name='Sell Date', value=five_date, inline=True)
    return {
      'embed': embed
    }
