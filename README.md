### โค้ด `README.md` สำหรับนำไปใช้งาน

```markdown
# 📈 Thai Stock Financial News Analyzer & Agentic RAG Assistant

ระบบวิเคราะห์ข่าวสารและผู้ช่วยลงทุนหุ้นไทยอัตโนมัติแบบครบวงจร (**End-to-End Financial News Pipeline**) ตั้งแต่การดึงข้อมูลข่าวสารจากเว็บการเงินชั้นนำ การประมวลผลคำและวิเคราะห์อารมณ์ตลาด (Market Sentiment) ด้วย AI (Gemini 2.5 Flash Lite) การทำ Vector Embedding เพื่อค้นหาเชิงความหมาย และการแสดงผลผ่าน Interactive Dashboard พร้อมระบบแชทอัจฉริยะ (Agentic RAG System)

---

## 🌟 คุณสมบัติเด่นของระบบ (System Features)

* **Asynchronous Web Scraping & AI Extraction:** ดึงข้อมูลหัวข้อข่าวและลิงก์จาก InfoQuest Stock แบบ Asynchronous ด้วย `crawl4ai` และใช้โครงสร้าง Pydantic ร่วมกับ `gemini-2.5-flash-lite` ในการสกัดข้อมูลข่าวออกมาในรูปแบบ JSON อัตโนมัติ
* **Smart Text Preprocessing:** ระบบทำความสะอาดข้อมูลข้อความ (Text Cleaning) ลบโค้ดส่วนเกิน, ลิงก์ และสัญลักษณ์ Markdown เพื่อเตรียมเนื้อหาข่าวให้พร้อมสำหรับการทำ NLP
* **Batch Sentiment Analysis & Multi-Key Rotation:** ส่งข้อมูลข่าวให้ AI วิเคราะห์อารมณ์ตลาด (Sentiment, Sector, Tickers, Summary) เป็นชุด (Batch) พร้อมระบบ **Auto-Retry & Key Rotation** สลับ API Key อัตโนมัติเมื่อคีย์ใดคีย์หนึ่งเต็มโควต้า (Rate Limit)
* **Dense Vector Embeddings:** แปลงหัวข้อ ข่าว และบทสรุปให้อยู่ในรูปของ Dense Vectors ความละเอียดสูงด้วยโมเดลสัญญะภาษาหลายภาษาชั้นนำอย่าง `BAAI/bge-m3` และจัดเก็บลงบน MongoDB Atlas
* **Interactive Financial Dashboard:** หน้าต่างสรุปผลข้อมูลเชิงสถิติ (KPIs, Market Sentiment Ratio, Sector Chart) พร้อมระบบค้นหาฟีดข่าวรายหุ้นรายเซกเตอร์ด้วย `Streamlit`
* **Agentic RAG Chat Assistant:** ระบบแชทผู้ช่วยลงทุนที่ใช้เทคนิค **Query Expansion** ร่วมกับ **MongoDB Atlas Vector Search** ค้นหาข่าวสารที่เกี่ยวข้องเชิงลึก แล้วส่งให้ Gemini สังเคราะห์คำตอบพร้อมแนบลิงก์อ้างอิงต้นฉบับเสมอ

---

## 🏗 สถาปัตยกรรมและการไหลของข้อมูล (Data Pipeline Architecture)

1. **ดึงข้อมูลหัวข้อข่าว (`db1_fetch_from_web.py`)** -> ดึงหัวข้อและลิงก์ข่าวอัปเดตล่าสุดลงฐานข้อมูล
2. **ดึงเนื้อหาข่าวฉบับเต็ม (`db2_fetch_content.py`)** -> เจาะลึกดึงเนื้อหาตามลิงก์ข่าวนั้นๆ พร้อม Clean ข้อมูล
3. **ส่งวิเคราะห์ข้อมูลด้วย AI (`db3_sent_content_to_gemini.py`)** -> สกัด Ticker หุ้น, อุตสาหกรรม, อารมณ์ข่าว (Sentiment) ลงในแต่ละ Document
4. **ทำ Vector Embedding (`embedding_env.py`)** -> สร้างเวกเตอร์จากหัวข้อและเนื้อหาข่าวด้วยโมเดล `bge-m3`
5. **แสดงผลและใช้งานห้องแชท (`Dashboard & Chat App`)** -> นำข้อมูลในฐานข้อมูลมาวิเคราะห์บน UI และใช้ค้นหาในระบบ RAG

---

## 🛠 เทคโนโลยีที่เลือกใช้ (Tech Stack & Libraries)

* **Core Language:** Python 3.9+
* **AI & LLM Provider:** Google GenAI SDK (`gemini-2.5-flash-lite`)
* **Web Crawler:** `crawl4ai` (Playwright-based Async Web Crawler)
* **Database & Vector Search:** MongoDB Atlas (MongoClient, Vector Search Index)
* **Embedding Model:** `sentence-transformers` (`BAAI/bge-m3`)
* **Frontend UI / Framework:** `Streamlit`
* **Data Manipulation:** `pandas`, `pydantic`

---

## 🚀 การติดตั้งและเตรียมสภาพแวดล้อม (Installation & Setup)

### 1. คลอนรีโพสิทอรี
```bash
git clone [https://github.com/S-Chatchai/R-Financial-news-analyzer.git](https://github.com/S-Chatchai/R-Financial-news-analyzer.git)
cd R-Financial-news-analyzer

```

### 2. ติดตั้งแพ็กเกจที่จำเป็น

```bash
pip install -r requirements.txt

```

### 3. ตั้งค่าไฟล์สภาพแวดล้อม (`.env`)

สร้างไฟล์ `.env` ไว้ที่โฟลเดอร์หลักของโปรเจกต์ และระบุคีย์ต่างๆ ดังนี้:

```env
# คีย์เชื่อมต่อฐานข้อมูล MongoDB Atlas
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"

# API Key ของ Gemini (รองรับการใส่หลายคีย์ คั่นด้วยเครื่องหมายจุลภาคเพื่อสลับคีย์อัตโนมัติ)
GEMINI_API_KEY="คีย์หลักสำหรับขั้นตอนการดึงข้อมูลสเต็ปที่ 1"
GEMINI_API_KEYS="คีย์ที่1, คีย์ที่2, คีย์ที่3"

```

### 4. การตั้งค่าบน MongoDB Atlas

* สร้าง Database ชื่อ `finance_db`
* สร้าง Collection ชื่อ `news_articles`
* สร้าง **Atlas Vector Search Index** บนคอลเลกชันชื่อ `vector_index` โดยกำหนด Schema ดังนี้:
```json
{
  "fields": [
    {
      "numDimensions": 1024,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "tickers",
      "type": "filter"
    }
  ]
}

```



---

## 💻 วิธีการรันระบบ (Execution Guide)

### 1. รัน Pipeline ข้อมูลข่าวสารแบบเป็นลำดับขั้น

คุณสามารถสั่งรัน Pipeline ทั้งหมดตั้งแต่เริ่มดึงข่าว ทำความสะอาด วิเคราะห์อารมณ์ จนถึงทำ Embedding ได้ในคำสั่งเดียวผ่านไฟล์ควบคุมหลัก:

```bash
python run_pipeline.py

```

*(ระบบจะเรียกทำงานเรียงลำดับ: `db1_fetch_from_web.py` -> `db2_fetch_content.py` -> `db3_sent_content_to_gemini.py` -> `embedding_env.py` ตามลำดับ)*

### 2. เปิดใช้งานหน้าจอ Dashboard สรุปผลข่าวสาร

```bash
streamlit run app_dashboard.py

```

### 3. เปิดใช้งานระบบแชทผู้ช่วยลงทุนอัจฉริยะ (RAG Assistant)

```bash
streamlit run app_rag_chat.py

```

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
R-Financial-news-analyzer/
│
├── db1_fetch_from_web.py        # สเต็ป 1: ดึงหัวข้อและลิงก์ข่าวดิบจากเว็บเข้าสู่ MongoDB
├── db2_fetch_content.py         # สเต็ป 2: ดึงเนื้อหาข่าวเต็มจากลิงก์และทำการ Clean Text
├── db3_sent_content_to_gemini.py# สเต็ป 3: ส่งเนื้อหาข่าวให้ Gemini ทำ Sentiment & Tagging ด้วยระบบ Multi-Key
├── embedding_env.py             # สเต็ป 4: ประมวลผลข้อความเป็น Vector ด้วย BAAI/bge-m3 ลงฐานข้อมูล
├── run_pipeline.py              # สคริปต์หลักสำหรับรันกระบวนการขั้นที่ 1-4 แบบอัตโนมัติ
│
├── app_dashboard.py             # หน้า Web UI Dashboard แสดง KPIs และสรุปสถิติตลาดทุน
├── app_rag_chat.py              # หน้า Web UI ระบบแชทถามตอบ RAG ค้นหาข้อมูลเชิงลึกรายหุ้น
│
├── requirements.txt             # รายชื่อไลบรารีและเวอร์ชันที่ระบบต้องการ
├── .env                         # ไฟล์สำหรับเก็บข้อมูลสำคัญแบบเป็นความลับ (สร้างเอง)
└── README.md                    # เอกสารประกอบการอธิบายโปรเจกต์นี้

```

---

## 🤝 การมีส่วนร่วมพัฒนาระบบ (Contributing)

ยินดีต้อนรับหากคุณต้องการร่วมพัฒนาฟีเจอร์หรือส่งข้อเสนอแนะเพื่อปรับปรุงตัวแบบ Pipeline ให้มีความเสถียรมากยิ่งขึ้น:

1. Fork รีโพสิทอรีนี้
2. สร้าง Branch สำหรับฟีเจอร์ของคุณ (`git checkout -b feature/AmazingFeature`)
3. Commit การแก้ไขของคุณ (`git commit -m 'Add some AmazingFeature'`)
4. Push สู่ Branch ปลายทาง (`git push origin feature/AmazingFeature`)
5. เปิด Pull Request

---

## 📄 สัญญาอนุญาต (License)

โปรเจกต์นี้ได้รับการคุ้มครองภายใต้สัญญาอนุญาตแบบ **MIT License** สามารถดูรายละเอียดเพิ่มเติมได้ที่ไฟล์ LICENSE

```

```
