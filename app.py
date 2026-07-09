import streamlit as st
import requests
import json

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# رابط الويب أب الخاص بك من جوجل (تأكد أنه ينتهي بـ /exec)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

# نظام حماية داخلي: منع التكرار في نفس الجلسة
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# المنطق: إذا تم الإرسال، اظهر الرسالة وأوقف كل شيء
if st.session_state.submitted:
    st.success("✅ شكرًا لك! تم استلام تقييمك بنجاح.")
    st.balloons()
    st.info("ملاحظة: لضمان دقة النتائج، يُسمح بإرسال الرد مرة واحدة في كل جلسة.")
    st.stop()

# --- واجهة الاستبيان ---
st.markdown("""
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى التطوير الذاتي. 
**الردود سرية تماماً ولن يتم جمع أي بيانات شخصية.**
<hr>
""", unsafe_allow_html=True)

with st.form(key="survey_form"):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    # عند الضغط على هذا الزر، ستريم ليت يقوم بمعالجة البيانات مرة واحدة فقط
    submit_button = st.form_submit_button(label="إرسال التقييم")

if submit_button:
    # القفل الفوري للجلسة
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "notes": notes
    }
    
    try:
        # إرسال البيانات
        response = requests.post(SCRIPT_URL, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            st.session_state.submitted = True
            st.rerun() # تحديث الصفحة لإظهار رسالة النجاح فقط
        else:
            st.error("فشل الإرسال، يرجى المحاولة مرة أخرى.")
    except:
        st.error("حدث خطأ في الاتصال بالسيرفر.")
