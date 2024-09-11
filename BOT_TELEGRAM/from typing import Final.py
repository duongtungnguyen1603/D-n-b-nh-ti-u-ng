from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes

TOKEN:  Final = '7043867128:AAFi597ufAipT2ijkvekwxTkw8i_aWxAIK4'
BOT_USERNAME: Final = '@Meleegoo_Jun_bot'

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, Tôi là Meleegoo. Tôi có thể giúp gì cho bạn ?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Vui lòng nhập nội dung phía dưới mà bạn cần hỏi để tôi đưa ra câu trả lời bạn muốn!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Lệnh chỉnh sửa.')

#Reponses
def handle_reponse(text: str) -> str:  #Hàm phản hồi xử lí văn bản chuỗi trả về chuỗi văn bản
    processed: str = text.lower() #Thay đổi chữ hoa thường trong python
    
    if 'xin chào' in processed:
        return 'tôi ở đây'
    
    if 'bạn khỏe không' in processed:
        return 'tôi ổn'
    
    return 'tôi không hiểu những gì bạn viết' #Trong trường hợp không chứa lựa chọn nào ở trên

#Xử lí việc người dùng liên hệ với bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #Cho biết là cuộc trò chuyện nhóm hay tiêng tư
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"') #Lấy mã Id người trò chuyện để xem đó là cuộc trò chuyện riêng hay nhóm

    #Cấm bot trả lời trừ khi gọi đến tên bot trong cuộc trò chuyện nhóm
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_reponse(new_text)
        else:
            return #Trả về việc bot ko trả lời trừ khi gọi tên của bot
    else:
        response: str = handle_reponse(text)

    print('Bot:',response)
    await update.message.reply_text(response)

#Chức năng ghi lại các lỗi 
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ ==  '__main__':
    print('Starting bot....')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #Messges
    app.add_handler(MessageHandler(filters.TEXT, handle_message)) #Trình xử lí thông báo tin nhắn

    #Error
    app.add_error_handler(error)

    #Update tín nhắn liên tục 
    print('Polling...')
    app.run_polling(poll_interval=3) #Kiểm tra tin nhắn 3s 1 lần 


