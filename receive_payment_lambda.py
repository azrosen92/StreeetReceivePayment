import os
import dwollav2
import secrets

def run(json_input, context):
  message_data = [record["Sns"]["MessageAttributes"] for record in json_input["Records"]]

  for message in message_data:
    payer_id = message["PayerIdentifier"]["Value"]
    funding_source = message["PayerFundingSource"]["Value"]
    performer_id = message["PerformerIdentifier"]["Value"]
    payment_amount = int(message["PaymentAmount"]["Value"])
    
    print("%s pays %s $%.2f" % (payer_id, performer_id, payment_amount/100))

    client = dwollav2.Client(
      key = os.environ['DWOLLA_APP_KEY'],
      secret = os.environ['DWOLLA_APP_SECRET'],
      environment = 'sandbox'
    )

    app_token = client.Auth.client()

    # # Get funding source
    # funding_source_url = __dwolla_url('funding-sources', '')
    # funding_source = app_token.get(funding_source_url)
    # print("Name:", funding_source.body['name'])
    # print("Bank:", funding_source.body['bankName'])
    # print("Account Type:", funding_source.body['bankAccountType'])
    # print("Status:", funding_source.body['status'])

    # # Send Transaction
    # request_body = {
    #   '_links': {
    #     'source': {
    #       'href': funding_source
    #     },
    #     'destination': {
    #       'href': __dwolla_url('accounts', os.environ['DWOLLA_PAYMENT_DESTINATION'])
    #     }
    #   },
    #   'amount': {
    #     'currency': 'USD',
    #     'value': "%.2f" % payment_amount/100
    #   },
    #   'metadata': {}
    # }

    # transfer = app_token.post('transfers', request_body)
    # return transfer.headers['location']

    # # Create a customer.
    # customer_data = {
    #   'firstName': 'Joe',
    #   'lastName': 'Buyer',
    #   'email': 'joe.buyer%s@gmail.com' % secrets.token_hex(16),
    #   'ipAddress': '69.202.208.40'
    # }
    # new_customer = app_token.post('customers', customer_data)
    # customer_url = new_customer.headers['location']
    # print("Customer initialized: %s" % customer_url)

    # # Attach a funding source to the customer.
    # # IAV: 
    # customer = app_token.post('%s/iav-token' % customer_url)
    # iav_token = customer.body['token']
    # print("IAV Token: %s" % iav_token)

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