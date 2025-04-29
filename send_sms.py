import africastalking

username='sandbox'
api_key='atsk_9399b61cc1618bcaca93799482ba793a7cf3192f203b7751febf6aebd8504b16314f3585'
africastalking.initialize(username, api_key)

sms =  africastalking.SMS

def send_sms(event_name, phone_number):
        sms.send(event_name, [phone_number])    
        