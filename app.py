import streamlit as st
import requests
import json
import time
from extra_streamlit_components import CookieManager

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# 1. استدعاء مدير الكوكيز
cookie_manager = CookieManager()

# ملاحظة تقنية: الكوكيز تحتاج ثانية للتحميل من المتصفح
time.sleep(0.5) 

# اسم البصمة (تغييره يصفر العداد للجميع)
COOKIE_NAME = "work_survey_final_lock_v10"

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 2. التحقق من وجود البصمة فوراً
already_submitted = cookie_manager.get(COOKIE_NAME)

if already_submitted == "true":
    st.success("✅ شكرًا لك! لقد تم استلام تقييمك مسبقًا.")
    st.info("لضمان دقة النتائج، يُسمح بإرسال الرد مرة واحدة فقط من هذا الجهاز.")
    st.stop() # إيقاف الكود هنا تماماً لمنع ظهور النموذج أو إرسال بيانات

# --- إذا وصل الكود هنا يعني أن الجهاز جديد ---

st.markdown("""
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى قياس مدى رضاكم عن أدائي المهني بكل شفافية.
**أؤكد لكم أن الردود سرية تماماً ولن يتم جمع أي بيانات شخصية.**
<hr>
""", unsafe_allow_html=True)

# الرابط الخاص بك من Google Apps Script (تأكد من أنه ينتهي بـ /exec)
script_url = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

with st.form(key="survey_form"):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

if submit_button:
    # قفل إضافي لحظي داخل الكود
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "notes": notes
    }
    
    try:
        # إرسال البيانات إلى جوجل
        response = requests.post(script_url, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            # زرع البصمة فوراً في متصفح الزميل
            cookie_manager.set(COOKIE_NAME, "true")
            st.success("تم إرسال تقييمك بنجاح! شكراً لك.")
            st.balloons()
            # التوقف قليلاً ثم إعادة التشغيل لتفعيل القفل العلوي
            time.sleep(1)
            st.rerun()
        else:
            st.error("فشل الإرسال، يرجى المحاولة لاحقاً.")
            
    except Exception as e:
        if "Rerun" in str(type(e)):
            raise e
        else:
            st.error("حدث خطأ في الاتصال.")
