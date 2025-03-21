from telethon import TelegramClient, events
import json
import logging
from datetime import datetime

# 初始化日志
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 加载配置文件
with open('config.json') as f:
    config = json.load(f)

# 创建Telegram客户端
client = TelegramClient(
    session='telegram_monitor',
    api_id=config['api_id'],
    api_hash=config['api_hash']
)

# 定义消息处理器
@client.on(events.NewMessage)
async def message_handler(event):
    try:
        chat = await event.get_chat()
        message = event.message
        
        # 记录消息信息
        log_data = {
            "时间": message.date.strftime("%Y-%m-%d %H:%M:%S"),
            "群组": chat.title if hasattr(chat, 'title') else "私聊",
            "发送者": message.sender_id,
            "内容": message.text,
            "关键词匹配": [kw for kw in config['keywords'] if kw in message.text]
        }
        
        # 打印日志到控制台
        logger.info(f"收到消息: {log_data}")
        
        # 写入文件
        with open('monitor.log', 'a', encoding='utf-8') as f:
            f.write(f"{json.dumps(log_data, ensure_ascii=False)}\n")
            
    except Exception as e:
        logger.error(f"处理消息出错: {str(e)}")

# 主程序
async def main():
    await client.start()
    logger.info("监控系统已启动...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
