from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# 爬取新闻函数
def get_ltn_news():
    url = "https://news.ltn.com.tw/list/breakingnews/world"
    response = requests.get(url)
    if response.status_code != 200:
        return "❌ 无法访问自由时报新闻网站。"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = soup.find_all('h3')
    link = news_list[0].find_previous('a')['href']
    news_data = ""
    for news in news_list[:20]:  # 只取前 5 条新闻
        title = news.text.strip()
        news_data += f"🔹 {title}\n {link}\n\n"
    
    return news_data

# 处理 /start 命令
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    news = get_ltn_news()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=news)

# 主函数
if __name__ == '__main__':
    app = ApplicationBuilder().token("7635177967:AAF7rlTudsp_CjZWtV4SJVK5-CDUudJfBDo").build()
    
    app.add_handler(CommandHandler("news", news))
    
    print("🤖 Bot 正在运行...")
    app.run_polling()
