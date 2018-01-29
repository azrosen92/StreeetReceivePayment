import os
import dwollav2
import secrets

def run(json_input, context):
  print(json_input)
  message_data = [record["Sns"]["MessageAttributes"] for record in json_input["Records"]]

  for message in message_data:
    payer_id = message["PayerIdentifier"]["Value"]
    funding_source = message["PayerFundingSource"]["Value"]
    performer_id = message["PerformerIdentifier"]["Value"]
    payment_amount = int(message["PaymentAmount"]["Value"])

    # TODO: Record this somewhere.
    print("%s pays %s $%.2f" % (payer_id, performer_id, payment_amount/100))

    client = dwollav2.Client(
      key = os.environ['DWOLLA_APP_KEY'],
      secret = os.environ['DWOLLA_APP_SECRET'],
      environment = 'sandbox'
    )

    app_token = client.Auth.client()

    # Send Transaction
    request_body = {
      '_links': {
        'source': {
          'href': funding_source
        },
        'destination': {
          'href': __dwolla_url('accounts', os.environ['DWOLLA_PAYMENT_DESTINATION'])
        }
      },
      'amount': {
        'currency': 'USD',
        'value': "%.2f" % payment_amount/100
      },
      'metadata': {}
    }

    transfer = app_token.post('transfers', request_body)
    return transfer.headers['location']

def __dwolla_url(resource, resource_id):
  return "%s/%s/%s" % (os.environ['DWOLLA_BASE_URL'], resource, resource_id)

if __name__ == "__main__":
  json_input = {
    "Records": [{
      "Sns": {
        "MessageAttributes": {
          "PayerIdentifier": {
            "Value": "Alice"
          },
          "PerformerIdentifier": {
            "Value": "Bob"
          },
          "PaymentAmount": {
            "Value": "150"
          },
          "PayerFundingSource": {
            "Value": ""
          },
        }
      }
    }]
  }

  run(json_input, None)
