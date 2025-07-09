import streamlit as st
import sqlite3
import uuid
from datetime import datetime
import re
from urllib.parse import urlparse, parse_qs
import base64
import pandas as pd
import os # استيراد os للتحقق من وجود الملف

# استيراد الإعدادات من config_likes.py
from config import CHANNEL_DATA_DATABASE_FILE # تم التعديل هنا
# --- Database Functions ---
def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول إذا لم تكن موجودة."""
    conn = sqlite3.connect(CHANNEL_DATA_DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registered_channels (
            id TEXT PRIMARY KEY,
            user_session_id TEXT NOT NULL,
            channel_url TEXT UNIQUE,
            channel_id TEXT UNIQUE,
            channel_name TEXT,
            registered_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_channel_to_db(user_session_id, channel_url, channel_id, channel_name):
    """يضيف قناة جديدة إلى قاعدة البيانات."""
    conn = sqlite3.connect(CHANNEL_DATA_DATABASE_FILE)
    cursor = conn.cursor()
    
    unique_id = str(uuid.uuid4())
    try:
        cursor.execute('INSERT INTO registered_channels (id, user_session_id, channel_url, channel_id, channel_name, registered_at) VALUES (?, ?, ?, ?, ?, ?)',
                       (unique_id, user_session_id, channel_url, channel_id, channel_name, datetime.now().isoformat()))
        conn.commit()
        st.success(f"🎉 تم تسجيل قناتك بنجاح: **{channel_name if channel_name else channel_id}**!")
        st.toast("تم تسجيل القناة!")
        return True
    except sqlite3.IntegrityError:
        st.error("⚠️ هذه القناة مسجلة بالفعل في قاعدة البيانات.")
        st.toast("القناة موجودة بالفعل!")
        return False
    finally:
        conn.close()

def get_registered_channels_count():
    """يعيد عدد القنوات المسجلة في قاعدة البيانات."""
    conn = sqlite3.connect(CHANNEL_DATA_DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM registered_channels')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_registered_channels_data():
    """يجلب جميع بيانات القنوات المسجلة من قاعدة البيانات."""
    conn = sqlite3.connect(CHANNEL_DATA_DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_url, channel_id, channel_name, registered_at FROM registered_channels')
    data = cursor.fetchall()
    conn.close()
    return data

def extract_channel_id(url):
    """
    يستخرج معرف القناة من رابط يوتيوب.
    يدعم روابط القنوات (channel, user, c) وروابط الـ @handle.
    لا يمكن استخراج معرف القناة من رابط الفيديو (watch?v=...) مباشرة بدون YouTube Data API.
    """
    # محاولة استخراج من روابط @handle
    match_handle = re.search(r"youtube\.com/@([a-zA-Z0-9_-]+)", url)
    if match_handle:
        return "@" + match_handle.group(1) # نرجع الـ handle مع علامة @

    # محاولة استخراج من روابط /channel/
    match_channel = re.search(r"youtube\.com/channel/([a-zA-Z0-9_-]+)", url)
    if match_channel:
        return match_channel.group(1)
    
    # محاولة استخراج من روابط /user/
    match_user = re.search(r"youtube\.com/user/([a-zA-Z0-9_-]+)", url)
    if match_user:
        return match_user.group(1)
    
    # محاولة استخراج من روابط /c/
    match_c = re.search(r"youtube\.com/c/([a-zA-Z0-9_-]+)", url)
    if match_c:
        return match_c.group(1)
    
    # إذا كان رابط فيديو أو أي صيغة أخرى لا يمكن استخراج معرف القناة منها مباشرة
    return None

# --- Streamlit App Layout ---
def main():
    init_db()

    if 'user_session_id' not in st.session_state:
        st.session_state.user_session_id = str(uuid.uuid4())

    st.set_page_config(
        page_title="انضم لمجتمع تبادل التفاعل! 🚀",
        page_icon="🤝",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Cairo', sans-serif;
            direction: rtl;
            text-align: right;
        }
        .main-header {
            font-size: 3.5em;
            color: #FF4B4B;
            text-align: center;
            font-weight: bold;
            margin-bottom: 0.5em;
            text-shadow: 3px 3px 8px rgba(0,0,0,0.2);
            line-height: 1.2;
            padding: 10px;
            background: linear-gradient(45deg, #FFD700, #FF4B4B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subheader {
            font-size: 1.8em;
            color: #333;
            text-align: center;
            margin-bottom: 1.5em;
            font-weight: 600;
        }
        .section-header {
            font-size: 2em;
            color: #007BFF;
            border-bottom: 2px solid #007BFF;
            padding-bottom: 10px;
            margin-top: 2em;
            margin-bottom: 1.5em;
            text-align: right;
        }
        .stTextInput > label {
            font-size: 1.1em;
            font-weight: bold;
            color: #555;
        }
        .stButton button {
            background-color: #28A745;
            color: white;
            font-size: 1.3em;
            font-weight: bold;
            padding: 12px 40px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            width: 100%;
            margin-top: 1.5em;
        }
        .stButton button:hover {
            background-color: #218838;
            transform: translateY(-2px);
        }
        .stButton button:active {
            transform: translateY(0);
            box-shadow: 1px 1px 4px rgba(0,0,0,0.2);
        }
        .info-box {
            background-color: #e0f7fa;
            border-left: 5px solid #00BCD4;
            padding: 15px;
            margin-bottom: 1.5em;
            border-radius: 8px;
            font-size: 1.1em;
            color: #006064;
            text-align: right;
        }
        .success-box {
            background-color: #e6ffe6;
            border-left: 5px solid #4CAF50;
            padding: 15px;
            margin-bottom: 1.5em;
            border-radius: 8px;
            font-size: 1.1em;
            color: #2E7D32;
            text-align: right;
        }
        .data-counter {
            font-size: 2.5em;
            color: #FF4B4B;
            font-weight: bold;
            text-align: center;
            margin-top: 2em;
            margin-bottom: 2em;
            padding: 20px;
            border: 3px dashed #FF4B4B;
            border-radius: 15px;
            background-color: #fffafa;
            box-shadow: 0px 0px 15px rgba(255,75,75,0.3);
        }
        .data-treasure-text {
            font-size: 1.8em;
            color: #FF8C00;
            font-weight: bold;
            text-align: center;
            margin-top: 1em;
            margin-bottom: 1em;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }
        .incentive-box {
            background-color: #ffe0b2;
            border-left: 5px solid #ff9800;
            padding: 20px;
            margin-top: 2em;
            margin-bottom: 2em;
            border-radius: 8px;
            font-size: 1.15em;
            color: #e65100;
            text-align: right;
            font-weight: 500;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
        .promotion-section {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 25px;
            margin-top: 3em;
            text-align: center;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        }
        .promotion-header {
            font-size: 2.2em;
            color: #FF0000;
            font-weight: bold;
            margin-bottom: 1em;
        }
        .promotion-text {
            font-size: 1.2em;
            color: #555;
            line-height: 1.6;
            margin-bottom: 1.5em;
        }
        .promotion-disclaimer {
            font-size: 1.1em;
            color: #006064;
            background-color: #e0f7fa;
            border-color: #00BCD4;
            font-weight: bold;
            margin-top: 1.5em;
            margin-bottom: 1.5em;
            padding: 10px;
            border: 1px solid #FFD700;
            background-color: #FFFACD;
            border-radius: 8px;
        }
        .promotion-button {
            background-color: #FF0000;
            color: white;
            font-size: 1.4em;
            font-weight: bold;
            padding: 15px 50px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        }
        .promotion-button:hover {
            background-color: #CC0000;
            transform: translateY(-3px);
        }
        .footer-text {
            font-size: 0.9em;
            color: #888;
            text-align: center;
            margin-top: 3em;
            padding-top: 1em;
            border-top: 1px solid #eee;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 2em;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- إضافة الشعار هنا ---
    try:
        st.markdown(
            f"<div class='logo-container'><img src='data:image/png;base64,{base64.b64encode(open('nassimacode.png', 'rb').read()).decode()}' alt='NITRO QASAR Logo' style='max-width: 200px; border-radius: 50%; box-shadow: 0px 0px 15px rgba(0,0,0,0.3);'></div>",
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("لم يتم العثور على ملف الشعار 'nitroqasar.png'. يرجى التأكد من وجوده في نفس مجلد التطبيق.")
    # --- نهاية إضافة الشعار ---

    st.markdown("<h1 class='main-header'>انضم لمجتمع تبادل التفاعل! 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>ساعد قناتك على النمو بمساعدة الآخرين، وساهم في بناء أكبر قاعدة بيانات للقنوات!</p>", unsafe_allow_html=True)

    st.markdown("<div class='info-box'>"
                "🌟 مرحباً بك في مبادرتنا المجانية لجمع بيانات القنوات! "
                "هنا، يمكنك تسجيل قناتك على يوتيوب لتصبح جزءًا من شبكة ضخمة من صناع المحتوى "
                "الذين يرغبون في تبادل الدعم والتفاعل. "
                "كلما زادت القنوات المسجلة، زادت قوة مجتمعنا وزادت فرص نمو قناتك وقنوات الآخرين!"
                "</div>", unsafe_allow_html=True)

    st.markdown("<h2 class='section-header'>سجل قناتك الآن مجاناً!</h2>", unsafe_allow_html=True)

    channel_url = st.text_input("رابط قناتك على يوتيوب (URL):", placeholder="مثال: https://www.youtube.com/channel/UC-... أو https://www.youtube.com/@اسم_قناتك")
    channel_name = st.text_input("اسم قناتك (اختياري، للمساعدة في التعرف):", placeholder="مثال: قناتي التعليمية")

    if st.button("سجل قناتي الآن!"):
        if channel_url:
            extracted_channel_id = extract_channel_id(channel_url)
            if extracted_channel_id:
                add_channel_to_db(st.session_state.user_session_id, channel_url, extracted_channel_id, channel_name)
            else:
                # رسالة تحذير معدلة لتكون أوضح وأكثر توجيهاً
                st.warning("⚠️ يبدو أن هذا ليس رابط قناة يوتيوب مباشر.")
                st.info("💡 يرجى إدخال رابط قناتك الرئيسي والمباشر (مثل: `youtube.com/channel/UC...`، `youtube.com/user/...`، `youtube.com/c/...`، أو `youtube.com/@اسم_قناتك`). لا يمكننا استخراج معرف القناة من روابط الفيديوهات.")
        else:
            st.error("الرجاء إدخال رابط قناتك على يوتيوب.")

    st.markdown("---")

    channels_count = get_registered_channels_count()
    st.markdown(f"<div class='data-counter'>"
                f"📊 عدد القنوات المسجلة حتى الآن: <br>"
                f"**{channels_count}** قناة!"
                f"<div class='data-treasure-text'>💎 الداتا كـ **ثروة**! 💎</div>"
                f"</div>", unsafe_allow_html=True)

    st.markdown("<div class='info-box'>"
                "✨ هذا الرقم ينمو باستمرار بفضل تعاونكم! "
                "كل قناة تضيفها تزيد من قوة شبكتنا وتوفر المزيد من فرص التفاعل للجميع."
                "</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='incentive-box'>
        🎁 **هدية التعاون: برنامج إدارة التفاعل!** 🎁<br>
        بمجرد انضمامكم وتعاونكم في بناء هذه القاعدة الضخمة من القنوات، سنقدم لكم برنامجاً خاصاً يقوم بإدارة هذه البيانات لكم. هذا البرنامج سيمكنكم من:
        <ul>
            <li>عمل **اشتراكات** تلقائية.</li>
            <li>عمل **إعجابات** تلقائية.</li>
            <li>تحقيق **مشاهدات** لقنواتكم.</li>
        </ul>
        ستحصلون على **نسخة مجانية** من هذا البرنامج لمساعدتكم في إشهار قنواتكم، وستتوفر أيضاً **نسخة متطورة ومدفوعة** لمن يرغب في تسريع النتائج وتحقيق أقصى استفادة!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-header'>لماذا يجب أن تشارك في مجتمعنا؟</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 1.1em; line-height: 1.6; text-align: right;">
    <ul>
        <li>🤝 <strong>التعاون قوة:</strong> انضم إلى مجتمع يدعم بعضه البعض لنمو مشترك.</li>
        <li>📈 <strong>زيادة التفاعل:</strong> كلما زادت القنوات، زادت فرص قناتك للحصول على مشاهدات، إعجابات، واشتراكات حقيقية.</li>
        <li>🆓 <strong>مجاني بالكامل:</b> تسجيل قناتك لا يكلفك شيئاً، فقط بضع ثوانٍ من وقتك.</li>
        <li>🚀 <strong>مستقبل قناتك:</strong> ساهم في بناء أكبر قاعدة بيانات لتبادل التفاعل، واستفد منها لاحقاً!</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- قسم جديد: استكشف بيانات المجتمع وحملها ---
    st.markdown("<h2 class='section-header'>استكشف بيانات المجتمع وحملها!</h2>", unsafe_allow_html=True)
    st.info("يمكنك الآن تحميل قائمة القنوات المسجلة لمشاهدة حجم مجتمعنا المتنامي!")

    channels_data = get_all_registered_channels_data()
    
    if channels_data: # هذا الشرط يضمن ظهور الأزرار فقط إذا كان هناك بيانات
        # 1. توفير تحميل بصيغة CSV
        df = pd.DataFrame(channels_data, columns=['Channel URL', 'Channel ID', 'Channel Name', 'Registered At'])
        csv_file = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="⬇️ تحميل بيانات القنوات (CSV)",
            data=csv_file,
            file_name="nitro_qasar_channels.csv",
            mime="text/csv",
            help="تحميل بيانات القنوات بصيغة CSV (متوافق مع Excel)."
        )

        # 2. توفير تحميل بصيغة TXT
        txt_content = ""
        for index, row in df.iterrows():
            txt_content += f"Channel URL: {row['Channel URL']}\n"
            txt_content += f"Channel ID: {row['Channel ID']}\n"
            txt_content += f"Channel Name: {row['Channel Name'] if pd.notna(row['Channel Name']) else 'N/A'}\n"
            txt_content += f"Registered At: {row['Registered At']}\n"
            txt_content += "-"*50 + "\n"
        
        st.download_button(
            label="⬇️ تحميل بيانات القنوات (TXT)",
            data=txt_content.encode('utf-8'),
            file_name="nitro_qasar_channels.txt",
            mime="text/plain",
            help="تحميل بيانات القنوات بصيغة نص عادي."
        )

        # 3. توفير تحميل قاعدة البيانات SQLite مباشرة (.db)
        # هذا الفحص يضمن أن زر تحميل DB يظهر فقط إذا كان الملف موجوداً
        if os.path.exists(CHANNEL_DATA_DATABASE_FILE):
            try:
                with open(CHANNEL_DATA_DATABASE_FILE, "rb") as f:
                    db_bytes = f.read()
                st.download_button(
                    label="⬇️ تحميل قاعدة البيانات (DB)",
                    data=db_bytes,
                    file_name="nitro_qasar_channels.db",
                    mime="application/octet-stream",
                    help="تحميل ملف قاعدة البيانات SQLite كاملاً."
                )
            except Exception as e:
                st.error(f"حدث خطأ أثناء محاولة تحميل ملف قاعدة البيانات: {e}. يرجى التأكد من الأذونات.")
        else:
            st.warning(f"ملف قاعدة البيانات '{CHANNEL_DATA_DATABASE_FILE}' غير موجود بعد. يرجى تسجيل قناة واحدة على الأقل لإنشائه وظهور زر التحميل.")
    else:
        st.info("لا توجد قنوات مسجلة بعد لتحميل بياناتها.")

    st.markdown("---")
    # --- نهاية قسم تحميل البيانات ---

    # قسم الترويج لبرامجك المدفوعة
    st.markdown("<div class='promotion-section'>"
                "<h3 class='promotion-header'>هل تبحث عن تسريع هائل لنمو قناتك؟</h3>"
                "<p class='promotion-text'>"
                "لقد قمنا ببناء هذه القاعدة الضخمة من القنوات الراغبة في التفاعل، والآن حان الوقت لترى كيف يمكن لبرامجنا الاحترافية أن تستغل هذه البيانات لتحقيق طفرة حقيقية لقناتك!"
                "<br><br>"
                "برامجنا المدفوعة لتبادل المشاهدات، الإعجابات، والاشتراكات تستخدم هذه البيانات لضمان تفاعل حقيقي ومستهدف."
                "انضم إلى آلاف القنوات الناجحة التي حققت أهدافها معنا!"
                "</p>"
                "<p class='promotion-disclaimer' style='color: #006064; background-color: #e0f7fa; border-color: #00BCD4;'>"
                "💡 هذه المبادرة المجانية هي نقطة انطلاق رائعة لنمو قناتك من خلال التعاون المجتمعي. "
                "أما برامجنا الاحترافية والمدفوعة، فهي مصممة خصيصًا لأصحاب المشاريع الجادة الذين يبحثون عن حلول قوية ونتائج مضمونة، وتوفر خدمات متقدمة تتجاوز التبادل اليدوي لنمو لا مثيل له."
                "</p>"
                "<a href='https://nassimacode-dashboard.streamlit.app' target='_blank' class='promotion-button' style='text-decoration: none;'>اكتشف برامجنا الاحترافية الآن!</a>"
                "</div>", unsafe_allow_html=True)

    st.markdown("<p class='footer-text'>&copy; 2025 جميع الحقوق محفوظة. بناء مجتمع قوي لنمو قناتك.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
