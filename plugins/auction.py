from disco.bot import Plugin
import requests
import json

class AuctionPlugin(Plugin):

  @Plugin.command('search', '[item_name:str...]')
  def on_auction_Search(self, event, item_name):
    r = requests.post('https://na.nasomi.com/auctionhouse/data/ah-data/searchItemByName.php',
                      data={
                        'itemname': item_name
                      })


    search_response = r.json()
    if not search_response['list']:
      event.msg.reply('Could not find listings for {}'.format(item_name))
      return

    item_id = search_response['list'][0]['itemid']
    data_params = {
      'itemid': item_id
    }

    stack = search_response['list'][0]['stackSize']

    if int(stack) != 1:
      data_params['stack'] = 1

    r = requests.post('https://na.nasomi.com/auctionhouse/data/ah-data/searchItem.php',
                      data=data_params)

    price_response = r.json()
    items = price_response['sale_list']
    total = 0
    count = 0
    for price in items:
      total += int(price['price'])
      count += 1
    total = total / count

    event.msg.reply('Current {} price: {} gil'.format(item_name, total))
