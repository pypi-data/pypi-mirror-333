from simple_blogger.reviewers.ReviewerBase import ReviewerBase
import os
import telebot

class TelegramReview(ReviewerBase):
    def __init__(self, channel_id=None, **kwargs):
        self.channel_id = channel_id if channel_id is not None else int(os.environ.get('TG_REVIEW_CHANNEL_ID'))
        super().__init__(**kwargs)

    def review(self, text_file_name=None, image_file_name=None):
        bot = telebot.TeleBot(os.environ.get("TG_REVIEW_BOT_TOKEN"))
        if os.path.exists(image_file_name) and os.path.exists(text_file_name):
            bot.send_photo(chat_id=self.channel_id
                            , photo=open(image_file_name, 'rb')
                            , caption=open(text_file_name, 'rt', encoding='UTF-8').read()
                            , parse_mode="Markdown")
        else:
            if os.path.exists(image_file_name):
                bot.send_photo(chat_id=self.channel_id
                                , photo=open(image_file_name, 'rb')
                                , disable_notification=True)

            if os.path.exists(text_file_name):
                bot.send_message(chat_id=self.channel_id
                                    , text=open(text_file_name, 'rt', encoding='UTF-8').read()
                                    , parse_mode="Markdown")