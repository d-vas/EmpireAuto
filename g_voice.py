from googlevoice import Voice


def send_sms(phone_number, message):
    # Ініціалізуємо об'єкт Google Voice
    voice = Voice()

    voice.login('dzyadekvl@gmail.com', 'dzyadekvasyl551980GOOGLE_2023')

    voice.send_sms(phone_number, message)

send_sms('+13158983511', 'test message from vas')
