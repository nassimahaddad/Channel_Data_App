import streamlit as st

# --- Streamlit App Layout ---
def main():
    st.set_page_config(
        page_title="برامج NITRO QASAR الاحترافية 🚀",
        page_icon="✨",
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
            color: #FF4B4B; /* لون أحمر جذاب */
            text-align: center;
            font-weight: bold;
            margin-bottom: 0.5em;
            text-shadow: 3px 3px 8px rgba(0,0,0,0.2);
            line-height: 1.2;
            padding: 10px;
            background: linear-gradient(45deg, #FFD700, #FF4B4B); /* تدرج ذهبي-أحمر */
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
        .program-card {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            height: 100%; /* لضمان نفس الارتفاع في الأعمدة */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .program-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
        }
        .program-icon {
            font-size: 3.5em;
            margin-bottom: 0.5em;
            color: #007BFF; /* أزرق جذاب */
        }
        .program-title {
            font-size: 1.6em;
            font-weight: bold;
            color: #333;
            margin-bottom: 0.5em;
        }
        .program-description {
            font-size: 1em;
            color: #555;
            line-height: 1.5;
            flex-grow: 1; /* لجعل الوصف يملأ المساحة المتاحة */
        }
        .program-button {
            background-color: #28A745; /* أخضر للنجاح */
            color: white;
            font-size: 1.1em;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            margin-top: 1.5em;
            width: 100%;
        }
        .program-button:hover {
            background-color: #218838;
            transform: translateY(-2px);
        }
        .encouragement-text {
            font-size: 1.3em;
            color: #FF8C00;
            text-align: center;
            margin-top: 3em;
            font-weight: bold;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>برامج NITRO QASAR الاحترافية 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>اكتشف مجموعتنا المتكاملة من الحلول الذكية لنمو قناتك على يوتيوب!</p>", unsafe_allow_html=True)

    st.markdown("---")

    # برامج التبادل (الاشتراك، المشاهدات، اللايكات)
    st.subheader("برامج تضخيم التفاعل")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="program-card">
            <div class="program-icon">🤝</div>
            <div class="program-title">برنامج تبادل الاشتراكات</div>
            <div class="program-description">
                انضم إلى شبكة قوية من صناع المحتوى لزيادة عدد المشتركين في قناتك بشكل حقيقي ومتبادل. كل اشتراك تحصل عليه يأتيك من مستخدم حقيقي مهتم بالنمو!
            </div>
            <button class="program-button" onclick="alert('هذا البرنامج قيد التطوير حالياً وسيكون متاحاً قريباً جداً!')">اكتشف المزيد</button>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="program-card">
            <div class="program-icon">👁️</div>
            <div class="program-title">برنامج تبادل المشاهدات</div>
            <div class="program-description">
                اجعل فيديوهاتك تحصد آلاف المشاهدات الحقيقية من مجتمعنا المتنامي. عزز ظهور فيديوهاتك في نتائج البحث والمقترحات على يوتيوب!
            </div>
            <button class="program-button" onclick="alert('هذا البرنامج قيد التطوير حالياً وسيكون متاحاً قريباً جداً!')">اكتشف المزيد</button>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="program-card">
            <div class="program-icon">👍</div>
            <div class="program-title">برنامج تبادل الإعجابات</div>
            <div class="program-description">
                زيد من تفاعل فيديوهاتك واحصل على عدد كبير من الإعجابات الحقيقية. الإعجابات تزيد من مصداقية محتواك وتدفعه للخوارزميات!
            </div>
            <button class="program-button" onclick="alert('هذا البرنامج قيد التطوير حالياً وسيكون متاحاً قريباً جداً!')">اكتشف المزيد</button>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # برامج التفاعل والتحليل
    st.subheader("أدوات التفاعل والتحليل المتقدمة")
    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="program-card">
            <div class="program-icon">💬</div>
            <div class="program-title">نشر والرد على التعليقات</div>
            <div class="program-description">
                عزز التفاعل في قناتك من خلال نشر تعليقات ذات صلة والردود الذكية. تفاعل نشط يعني مجتمعاً حيوياً وقناة مزدهرة!
            </div>
            <button class="program-button" onclick="alert('هذا البرنامج قيد التطوير حالياً وسيكون متاحاً قريباً جداً!')">اكتشف المزيد</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="program-card">
            <div class="program-icon">🔍</div>
            <div class="program-title">تحليل المنافسين واستخراج الكلمات المفتاحية</div>
            <div class="program-description">
                اكتشف استراتيجيات منافسيك الناجحين واستخرج الكلمات المفتاحية الأكثر بحثاً في مجالك. خطط لمحتواك بذكاء وتفوق على الجميع!
            </div>
            <button class="program-button" onclick="alert('هذا البرنامج قيد التطوير حالياً وسيكون متاحاً قريباً جداً!')">اكتشف المزيد</button>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # نص تشجيعي عام
    st.markdown("""
    <p class='encouragement-text'>
        🌟 **كل برنامج مصمم خصيصاً ليمنح قناتك الدفعة التي تستحقها.** <br>
        سواء كنت تبحث عن زيادة التفاعل، أو فهم أفضل لسوقك، أو مجرد توفير الوقت، فإن حلول NITRO QASAR هنا لمساعدتك على تحقيق أهدافك. <br>
        **اكتشف قوة النمو الحقيقي معنا!**
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #888; font-size: 0.9em;'>&copy; 2025 NITRO QASAR. جميع الحقوق محفوظة.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
