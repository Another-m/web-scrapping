import telegram
from data import TOKEN, ChatID



def send_to_tg(all_news, TOKEN=TOKEN, ChatID=ChatID):
    bot = telegram.Bot(token=TOKEN)
    for news in all_news["Интересные статьи"]:
        message = '{}\n{}\nСсылка на статью: {}'.format(news['Дата'], news['Заголовок'], news['Ссылка'])
        bot.send_message(chat_id=ChatID, text=message)

