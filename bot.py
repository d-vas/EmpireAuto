from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
from telegram import ReplyKeyboardMarkup
import settings
from google_map_tolls import make_link_from_locations
# import tk_window


# BUTTONS
btn_fnd_ld = 'FIND LOAD'
btn_fnd_new_ld = 'FIND NEW LOAD'
btn_fnd_crt_ld = 'FIND CURRENT LOAD'
btn_snd_msg = 'SEND MESSAGE'
btn_snd_msg_ofc = 'SEND MESSAGE TO OFFICE'
btn_snd_msg_yrd = 'SEND MESSAGE TO YARD OFFICE'
btn_snd_msg_all = 'SEND MESSAGE TO ALL EMPLOYEES'
btn_snd_msg_all_drv = 'SEND MESSAGE TO ALL DRIVERS'
btn_snd_msg_3cd = 'SEND MESSAGE TO 3-CAR DRIVERS'
btn_snd_msg_9cd = 'SEND MESSAGE TO 9-CAR DRIVERS'
btn_snd_msg_acc = 'SEND MESSAGE TO ACCOUNTING'
btn_make_link = 'MAKE A LIST FROM LOCATIONS'


'''
main_menu_btn_list = [btn_fnd_ld, btn_snd_msg]
find_menu_btn_list = [btn_fnd_new_ld, btn_fnd_crt_ld]
msg_menu_btn_list = [[btn_snd_msg_ofc, ], [btn_snd_msg_yrd, ], [btn_snd_msg_all, ], [btn_snd_msg_all_drv, ], [btn_snd_msg_3cd, ], [btn_snd_msg_9cd, ], [btn_snd_msg_acc, ]]
'''

main_menu = [[btn_make_link], ]


TOKEN = settings.TOKEN


def msg_from_dict(dict_):
    msg = ''
    for i in dict_:
        msg = msg + f"{i} --- {dict_[i]}\n"
    return msg


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

    await update.message.reply_html(rf"Hi {user.mention_html()}!", reply_markup=reply_markup)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

    if text == btn_make_link:
        await update.message.reply_text('ВВЕДІТЬ СПИСОК ЛОКАЦІЙ', reply_markup=reply_markup, )
        new_text = update.message.text
        # print(new_text)
        # await update.message.reply_text(make_link_from_locations(update.message.text), reply_markup=reply_markup, )

    # await update.message.reply_text('hi message_handler', reply_markup=reply_markup)


def main():
    # headers_list_new_row(load)
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # application.add_handler(CommandHandler(btn_fnd_new_ld, tk_window))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.run_polling()


# if __name__ == "__main__":
main()

