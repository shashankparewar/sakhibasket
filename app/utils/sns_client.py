import boto3



class SNSClient:
    message_template = "Hi {}, Thank you for booking with SakhiBasket\n" + \
                       "Your Booking Reference is: {}\n" + \
                        "Access Link: http://sakhibasket.com:8000/app/app#!/order/{}"

    @classmethod
    def send_sms(cls, phone, name, booking_id):
        client = boto3.client('sns')
        phone_number = "+91{}".format(phone)
        message = cls.message_template.format(name, booking_id, booking_id)
        client.publish(PhoneNumber=phone_number,  Message=message)

