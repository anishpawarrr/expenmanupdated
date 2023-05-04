from twilio.rest import Client

account_sid = 'ACe37218c83a39cb303ac1a46bff38a56f'
auth_token = 'fc2cfa34e3ee784d5d6a7c3b854f212f'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Hi bro',
  to='whatsapp:+919325588724'
)
# http://wa.me/+14155238886?text=join%20breath-forth
print(message.sid)
