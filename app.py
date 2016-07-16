from chalice import Chalice
import requests
import urllib

GATHERER_TYPEAHEAD_URI = 'http://gatherer.wizards.com/Handlers/InlineCardSearch.ashx?nameFragment=%s'
GATHERER_URI = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card'

app = Chalice(app_name='magiccardbot')
app.debug = True

@app.route('/magic-cards', methods=['GET'])
def magic_cards():
  json = app.current_request.query_params
  # retrieve card information
  card_name = urllib.quote_plus(json['text'])
  # try to derive the card name from a fragment
  cards_json = requests.get(GATHERER_TYPEAHEAD_URI % card_name).json()
  if json['token'] == '5B4t9yJ044hLrDBYDKq8xK3A' and len(cards_json['Results']) > 0:
    card_name = cards_json['Results'][0]['Name']
    # Get card image uri
    response = '{}&name={}'.format(GATHERER_URI, urllib.quote_plus(card_name))
    out_json = {
      "response_type": "in_channel",
      "attachments": [
        {
          "text": json['text'],
          "image_url": response,
        }
      ]
    }
    return out_json
  else:
    return {"text": "Card not found"}