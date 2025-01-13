from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# 获取每日新闻函数
def get_daily_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_NEWS_API_KEY"
    response = requests.get(url).json()
    articles = response.get('articles', [])
    
    # 格式化新闻内容
    news = ""
    for i, article in enumerate(articles[:5]):
        news += f"{i+1}. {article['title']}\n{article['url']}\n\n"
    
    return news if news else "今日无新闻更新。"

# 处理 /start 命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    news = get_daily_news()
    message = f"👋 你好 {user.first_name}！这是今日的新闻：\n\n{news}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# 主函数
if __name__ == '__main__':
    app = ApplicationBuilder().token("8197503885:AAEuf50LBEhRdb3UrR2bXvsI1RmNdK6HhYQ").build()
    
    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot 正在运行...")
    app.run_polling()
