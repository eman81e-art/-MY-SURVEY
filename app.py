import streamlit as st
import requests
import json
import uuid
import time
from extra_streamlit_components import CookieManager

st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# 1. إعداد مدير الكوكيز
cookie_manager = CookieManager()

# انتظار بسيط لضمان توافق المتصفح مع المكون
time.sleep(0.8) 

USER_ID_COOKIE = "user_id_v11"
SUBMIT_COOKIE = "submitted_v11"

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 2. محاولة جلب المعرف بأمان
try:
    user_id = cookie_manager.get(USER_ID_COOKIE)
except:
    user_id = None

# إذا فشل المتصفح في دعم الكوكيز، نستخدم معرفاً للجلسة الحالية فقط
if not user_id:
    if "fallback_id" not in st.session_state:
        st.session_state.fallback_id = f"guest_{str(uuid.uuid4())[:6]}"
    
    # محاولة حفظه في الكوكيز للمرات القادمة (إن أمكن)
    try:
        cookie_manager.set(USER_ID_COOKIE, st.session_state.fallback_id, key="save_uid")
    except:
        pass
    
    user_id = st.session_state.fallback_id

# 3. فحص حالة الإرسال
try:
    already_submitted = cookie_manager.get(SUBMIT_COOKIE)
except:
    already_submitted = "false"

if already_submitted == "true":
    st.success("✅ شكرًا لك! لقد تم استلام تقييمك مسبقًا.")
    st.stop()

# --- واجهة الاستبيان ---
st.markdown("""
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى التطوير الذاتي وتحسين بيئة العمل. 
**الردود سرية تماماً.**
<hr>
""", unsafe_allow_html=True)

script_url = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

with st.form(key="survey_form"):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

if submit_button:
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "notes": notes,
        "user_id": user_id
    }
    
    try:
        # رفع مهلة الانتظار لضمان وصول البيانات حتى لو المتصفح بطيء
        response = requests.post(script_url, data=json.dumps(payload), timeout=15)
        
        if response.status_code == 200:
            try:
                cookie_manager.set(SUBMIT_COOKIE, "true", key="save_submit")
            except:
                pass
            
            st.success("تم إرسال تقييمك بنجاح! شكراً لك.")
            st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"خطأ في استجابة السيرفر (كود: {response.status_code})")
    except Exception as e:
        # هنا أضفنا تفاصيل أكثر لنعرف سبب "الخطأ الفني"
        if "Rerun" in str(type(e)):
            raise e
        else:
            st.error(f"حدث خطأ أثناء الإرسال. يرجى التأكد من استقرار الإنترنت.")
            # طباعة الخطأ في سجلات الموقع عندك (لا يراها المستخدم)
            print(f"DEBUG: {e}")
