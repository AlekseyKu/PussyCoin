import requests

# Замените YOUR_BOT_TOKEN и YOUR_CHANNEL_ID на соответствующие значения
bot_token = 'YOUR_BOT_TOKEN'
channel_id = 'YOUR_CHANNEL_ID'

# Функция для проверки подписки пользователя на канал
def check_subscription(user_id):
    url = f'https://api.telegram.org/bot{bot_token}/getChatMember?chat_id={channel_id}&user_id={user_id}'
    response = requests.get(url)
    data = response.json()
    return data['result']['status'] == 'member'

# Функция для обновления кнопки
def update_button(user_id):
    is_subscribed = check_subscription(user_id)
    button_text = 'Join us for 1000 Pussies' if not is_subscribed else 'Join us'
    # Обновите базу данных и установите/снимите соответствующий тумблер
    return button_text

# Пример использования функции update_button
user_id = 'USER_ID'
button_text = update_button(user_id)
print(button_text)