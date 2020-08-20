from knockknock import email_sender

@email_sender(recipient_email="aggarwalpiushdocs@gmail.com", sender_email="aggarwalpiushdocs@gmail.com")
def train_your_nicest_model(your_nicest_parameters):
    import time
    print('hello')
    time.sleep(1)
    return {'loss': 0.9} # Optional return value

train_your_nicest_model('a')
