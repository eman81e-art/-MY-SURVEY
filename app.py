import streamlit as st
import requests
import json
import uuid
import extra_streamlit_components as stx

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# فرض اتجاه الكتابة من اليمين إلى اليسار على كامل الصفحة
st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        direction: rtl;
    }
    .stMarkdown, .stCaption, .stTextArea textarea, label, .stSlider {
        text-align: right;
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# --- إدارة رمز عشوائي غير مرتبط بأي هوية، لمنع التكرار فقط ---
cookie_manager = stx.CookieManager()
respondent_token = cookie_manager.get(cookie="survey_token")
if respondent_token is None:
    respondent_token = str(uuid.uuid4())
    cookie_manager.set("survey_token", respondent_token)

if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني (زميلكم طارق البلاسمة)")

if st.session_state.submitted:
    st.success("✅ شكراً لك! تم استلام تقييمك بنجاح.")
    st.stop()

# --- واجهة الاستبيان ---
st.markdown("""
عزيزي الزميل/ة، هذا الاستطلاع **مجهول بالكامل بالنسبة لي**؛ لا أستطيع ولا أرغب
بمعرفة هويتك أو ربط إجابتك باسمك. يُخزَّن في متصفحك رمز عشوائي (لا يحمل أي معلومة
عنك) هدفه الوحيد منع تكرار التعبئة أكثر من مرة. هدف الاستبيان تحسين الأداء والتعامل المهني.
<hr>
""", unsafe_allow_html=True)

# ضع الرابط الخاص بك هنا (تأكد أنه بين علامتي التنصيص "")
script_url = "https://script.google.com/macros/s/AKfycbxLsDcgEpWtw0sPNTsLdjILT099ElJzeEoyP6PvANFnbVJtLiDBlrnz-6EFbKShpAuB/exec"

with st.form(key="survey_form"):
    st.caption("مقياس التقييم: 1 = ضعيف  ←  →  5 = قوي")
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
        "dedup_token": respondent_token,  # رمز عشوائي فقط لفلترة التكرار، لا يحمل أي هوية
    }

    try:
        requests.post(script_url, data=json.dumps(payload), timeout=15)
    except Exception:
        pass

    st.session_state.submitted = True
    st.rerun()

