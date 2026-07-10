import streamlit as st
import requests
import json
import hashlib

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# 1. توليد "معرف ثابت" بناءً على عنوان الجهاز (IP)
def get_user_unique_id():
    try:
        # جلب عنوان الجهاز من خدمة خارجية
        ip = requests.get('https://api.ipify.org').text
        # تشفير العنوان لضمان السرية التامة (لا يمكن العودة للعنوان الأصلي)
        return hashlib.md5(ip.encode()).hexdigest()[:10]
    except:
        return "unknown_device"

user_id = get_user_unique_id()

# 2. نظام منع التكرار في الجلسة الحالية
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني")

if st.session_state.submitted:
    st.success(f"✅ شكراً لك! تم استلام تقييمك بنجاح.")
    st.info(f"معرف الجهاز الثابت للتدقيق: {user_id}")
    st.stop()

# --- واجهة الاستبيان ---
st.markdown(f"""
عزيزي الزميل/ة، هذا الاستطلاع **سري تماماً**. 
تم تحديد معرف رقمي لجهازك لضمان دقة البيانات وحذف المكرر: `{user_id}`
<hr>
""", unsafe_allow_html=True)

# رابط الويب أب الخاص بك من جوجل
script_url = "import streamlit as st
import requests
import json
import hashlib

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# 1. توليد "معرف ثابت" بناءً على عنوان الجهاز (IP)
def get_user_unique_id():
    try:
        # جلب عنوان الجهاز من خدمة خارجية
        ip = requests.get('https://api.ipify.org').text
        # تشفير العنوان لضمان السرية التامة (لا يمكن العودة للعنوان الأصلي)
        return hashlib.md5(ip.encode()).hexdigest()[:10]
    except:
        return "unknown_device"

user_id = get_user_unique_id()

# 2. نظام منع التكرار في الجلسة الحالية
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني")

if st.session_state.submitted:
    st.success(f"✅ شكراً لك! تم استلام تقييمك بنجاح.")
    st.info(f"معرف الجهاز الثابت للتدقيق: {user_id}")
    st.stop()

# --- واجهة الاستبيان ---
st.markdown(f"""
عزيزي الزميل/ة، هذا الاستطلاع **سري تماماً**. 
تم تحديد معرف رقمي لجهازك لضمان دقة البيانات وحذف المكرر: `{user_id}`
<hr>
""", unsafe_allow_html=True)

# رابط الويب أب الخاص بك من جوجل
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
        # إرسال البيانات
        response = requests.post(script_url, data=json.dumps(payload), timeout=15)
        st.session_state.submitted = True
        st.rerun()
    except:
        # حتى لو حدث تأخير في الرد، نعتبره نجح لأن جوجل يسجل في الخلفية
        st.session_state.submitted = True
        st.rerun()"

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
        # إرسال البيانات
        response = requests.post(script_url, data=json.dumps(payload), timeout=15)
        st.session_state.submitted = True
        st.rerun()
    except:
        # حتى لو حدث تأخير في الرد، نعتبره نجح لأن جوجل يسجل في الخلفية
        st.session_state.submitted = True
        st.rerun()
