from googlevoice import Voice


def send_sms(phone_number, message):
    # Ініціалізуємо об'єкт Google Voice
    voice = Voice()

    # Авторизація
    voice.login('empire120@gmail.com', 'TRANS@2018')

    # Надсилаємо SMS
    voice.send_sms(phone_number, message)


# Викликаємо функцію для надсилання SMS
send_sms('+13158983511', 'test message')
