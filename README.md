# Sales Insight Generator for Merchants

##  Overview
This Python script provides smart sales analytics for merchants by connecting to a MySQL database and using OpenAI to summarize and interpret sales data. It helps the store owner understand total sales, buyer count, and top-performing branches.

##  Features
- Retrieves and analyzes sales data.
- Calculates total sales, number of buyers, top-selling branches.
- Uses AI to summarize performance insights.
- Helps merchants improve strategic decisions.

##  Data Sources
- Sales transactions from MySQL database.
- Buyer IDs, amounts, branch names.

##  Preprocessing
- Removal of incomplete or null sales entries.
- Grouping and aggregation by branch and date.
- Handling currency formats and date parsing.

##  Tech Stack
- **Language**: Python
- **AI Model**: OpenAI GPT API
- **Database**: MySQL
- **Libraries**: `pymysql`, `pandas`, `openai`

##  How to Run
1. Install dependencies:
   ```bash
   pip install openai pymysql pandas
   ```
2. Configure your database credentials and OpenAI key.
3. Run the script:
   ```bash
   python sales_insights.py
   ```

## 📈 Output
- Printed or exported summary of:
  - Total sales
  - Number of unique buyers
  - Top-performing branches
  - AI-generated performance report
 # مولّد تقارير ذكية للمبيعات للتجار

##  نظرة عامة
يقدم هذا السكربت تحليلاً ذكياً لمبيعات التاجر من خلال الاتصال بقاعدة بيانات MySQL واستخدام OpenAI لتلخيص البيانات وتفسيرها. يساعد التاجر على فهم إجمالي المبيعات وعدد المشترين والفروع الأكثر مبيعًا.

##  المميزات
- استخراج وتحليل بيانات المبيعات.
- حساب إجمالي المبيعات وعدد المشترين وأعلى الفروع أداءً.
- استخدام الذكاء الاصطناعي لتوليد تقارير ملخصة.
- دعم اتخاذ القرار لدى التاجر.

## مصادر البيانات
- بيانات المعاملات المخزنة في MySQL.
- معرفات المشترين، مبالغ الشراء، أسماء الفروع.

## المعالجة المسبقة
- حذف الإدخالات الناقصة أو غير الصالحة.
- التجميع حسب الفرع والتاريخ.
- تنسيق العملات والتواريخ.

##  التقنيات المستخدمة
- **اللغة**: Python
- **النموذج الذكي**: OpenAI GPT API
- **قاعدة البيانات**: MySQL
- **المكتبات**: `pymysql`, `pandas`, `openai`

## طريقة التشغيل
1. تثبيت المتطلبات:
   ```bash
   pip install openai pymysql pandas
   ```
2. إعداد الاتصال بقاعدة البيانات ومفتاح OpenAI.
3. تشغيل السكربت:
   ```bash
   python sales_insights.py
   ```

## الناتج
- ملخص مطبوع أو محفوظ يحتوي على:
  - إجمالي المبيعات
  - عدد المشترين الفريدين
  - الفروع الأعلى مبيعًا
  - تقرير ذكاء اصطناعي عن أداء المتجر
