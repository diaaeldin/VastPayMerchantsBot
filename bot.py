import telebot
import openai
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime, timedelta
import re

TELEGRAM_BOT_TOKEN = '*************' 
TELEGRAM_CHAT_ID = -********35
OPENAI_API_KEY = 'sk-proj-78V********'

DB_HOST = '********ws.com'
DB_USER = 're********er'   
DB_PASSWORD = 'h********.&q' 
DB_NAME = 'pro********tion'  

RESTAURANT_ID = '88********8'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

def create_db_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as e:
        print("DB Error:", e)
        return None

def execute_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    return cursor.fetchall()

def get_date_filter_sql(date_range):
    if not date_range:
        return ""
    
    date_range = date_range.replace("آخر", "").replace("من", "").strip()
    match = re.search(r'(\d+)\s*(يوم|أسبوع|شهر|ساعة)', date_range)
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        
        if unit == "يوم":
            return f"AND created_at >= NOW() - INTERVAL {num} DAY"
        elif unit == "أسبوع":
            return f"AND created_at >= NOW() - INTERVAL {num * 7} DAY"
        elif unit == "شهر":
            return f"AND created_at >= NOW() - INTERVAL {num * 30} DAY"
        elif unit == "ساعة":
            return f"AND created_at >= NOW() - INTERVAL {num} HOUR"
    
    if "يومين" in date_range:
        return "AND created_at >= NOW() - INTERVAL 2 DAY"
    elif "أسبوع" in date_range:
        return "AND created_at >= NOW() - INTERVAL 7 DAY"
    elif "٣٠" in date_range or "30" in date_range or "شهر" in date_range:
        return "AND created_at >= NOW() - INTERVAL 30 DAY"
    elif "يوم" in date_range:
        return "AND created_at >= NOW() - INTERVAL 1 DAY"
    
    return ""

def extract_intent_from_openai(question):
    prompt = f"""
أنت مساعد ذكاء اصطناعي لمطعم سعودي اسمه "أصياخ".
حدد التالي من سؤال المستخدم:
- intent: واحدة من:
  top_products, top_branches, avg_delivery_time,
  payment_methods, online_customers_count,
  orders_count, online_total, delayed_orders,
  product_sales_by_name, product_count, branch_sales_for_product
- product_name: إن وُجد اسم منتج محدد
- date_range: مثل "آخر يومين"، "أسبوع"، "30 يوم" أو None
- branch_name: إن وُجد اسم فرع محدد

السؤال: {question}

أعد الرد بصيغة JSON فقط.
"""
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return json.loads(res.choices[0].message["content"])
    except Exception as e:
        print(f"Error in extract_intent_from_openai: {e}")
        return {"intent": "unknown"}

def handle_intent(connection, intent_data):
    intent = intent_data.get("intent")
    date_filter = get_date_filter_sql(intent_data.get("date_range", ""))

    if intent == "top_products":
        query = f"""
        SELECT name_ar, sold FROM items
        WHERE restaurant_id = '{RESTAURANT_ID}'
        ORDER BY sold DESC LIMIT 10
        """
        results = execute_query(connection, query)
        if not results:
            return "📭 ما فيه بيانات حالياً عن أكثر الأصناف مبيعاً."
        res = "📊 أكثر المنتجات مبيعاً في أصياخ:\n"
        for i, row in enumerate(results, 1):
            res += f"{i}. {row['name_ar']} - {row['sold']} مبيعات\n"
        return res

    elif intent == "product_count":
        query = f"""
        SELECT COUNT(*) as count FROM items
        WHERE restaurant_id = '{RESTAURANT_ID}'
        """
        result = execute_query(connection, query)[0]
        return f"📦 عدد المنتجات المتوفرة في أصياخ: {result['count']} منتج."

    elif intent == "top_branches":
        query = f"""
        SELECT b.name_ar, COUNT(*) as total
        FROM orders o JOIN branches b ON o.branch_id = b.id
        WHERE o.restaurant_id = '{RESTAURANT_ID}' {date_filter}
        GROUP BY b.name_ar
        ORDER BY total DESC LIMIT 5
        """
        results = execute_query(connection, query)
        res = f"🏪 أكثر الفروع بيعاً في أصياخ {intent_data.get('date_range', '')}:\n"
        for i, row in enumerate(results, 1):
            res += f"{i}. {row['name_ar']} - {row['total']} طلب\n"
        return res

    elif intent == "avg_delivery_time":
        query = f"""
        SELECT AVG(TIMESTAMPDIFF(MINUTE, created_at, updated_at)) as avg_time
        FROM orders 
        WHERE restaurant_id = '{RESTAURANT_ID}' {date_filter}
        """
        result = execute_query(connection, query)[0]
        time = round(result["avg_time"], 2) if result["avg_time"] else 0
        return f"⏱️ متوسط وقت تنفيذ الطلبات في أصياخ {intent_data.get('date_range', '')}: {time} دقيقة."

    elif intent == "payment_methods":
        query = f"""
        SELECT payment_method, COUNT(*) as count FROM orders
        WHERE restaurant_id = '{RESTAURANT_ID}' {date_filter}
        GROUP BY payment_method ORDER BY count DESC
        """
        results = execute_query(connection, query)
        res = f"💳 أكثر وسائل الدفع استخداماً في أصياخ {intent_data.get('date_range', '')}:\n"
        for row in results:
            res += f"- {row['payment_method']}: {row['count']} طلب\n"
        return res

    elif intent == "orders_count":
        query = f"""
        SELECT COUNT(*) AS count FROM orders
        WHERE restaurant_id = '{RESTAURANT_ID}' {date_filter}
        """
        count = execute_query(connection, query)[0]["count"]
        return f"📦 عدد الطلبات في أصياخ خلال {intent_data.get('date_range', 'الفترة')} : {count} طلب."

    elif intent == "online_total":
        query = f"""
        SELECT SUM(total) AS total FROM orders
        WHERE restaurant_id = '{RESTAURANT_ID}' AND payment_method = 'online' {date_filter}
        """
        total = execute_query(connection, query)[0]["total"] or 0
        return f"💰 إجمالي المدفوعات أونلاين خلال {intent_data.get('date_range', 'الفترة')}: {round(total, 2)} ريال."

    return "🤷‍♂️ ما قدرت أفهم نوع السؤال، حاول تعيد صيغته."

# ✅ NEW: تحليل رسالة الرد الذكي من التقييم
def analyze_advice_message_with_openai(message_text):
    prompt = f"""
الرسالة التالية وصلتني كنصيحة من بوت تقييمي:

"{message_text}"

أريدك ترد على هذه الرسالة كأنك مساعد مدير ذكي.
- اسأله هل يحب تعرف تأثير القرار؟
- اقترح خطوات عملية بناءً على ما ورد.
- اعطيه شعور إنه في حوار ذكي مهني، لكن مختصر ولطيف.

رد باللهجة السعودية ولا تطول.
"""
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return res.choices[0].message["content"].strip()
    except Exception as e:
        print(f"❌ تحليل الرد الذكي فشل: {e}")
        return "🤖 فيه مشكلة في تحليل النص، جرب تعيد المحاولة."

# ✅ معالج الرسائل
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    if message.chat.id != TELEGRAM_CHAT_ID:
        bot.reply_to(message, "🚫 ما عندك صلاحية تستخدم البوت.")
        return

    user_question = message.text.strip()

    # ✅ كشف رسائل التقييم أو النصيحة الذكية
    if "نصيحة للمتجر" in user_question or "اقترح" in user_question or "خصم" in user_question:
        bot.send_message(message.chat.id, "🤖 أفكر معاك في الاقتراح...")
        advice_reply = analyze_advice_message_with_openai(user_question)
        bot.send_message(message.chat.id, advice_reply)
        return

    # 👇 باقي الرسائل تعامل كاستعلام على قاعدة البيانات
    bot.send_message(message.chat.id, "🧠 جارٍ فهم سؤالك...")
    intent_data = extract_intent_from_openai(user_question)
    if intent_data.get("intent") == "unknown":
        bot.send_message(message.chat.id, "❌ ما قدرت أفهم سؤالك، جرب تعيد صياغته.")
        return

    bot.send_message(message.chat.id, "📡 جاري جلب البيانات من قاعدة أصياخ...")
    conn = create_db_connection()
    if not conn:
        bot.send_message(message.chat.id, "❌ تعذر الاتصال بقاعدة البيانات.")
        return

    try:
        response = handle_intent(conn, intent_data)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ صار خطأ أثناء المعالجة: {str(e)}")
    finally:
        conn.close()

print("✅ البوت شغال في خدمة أصياخ...")
bot.polling()
