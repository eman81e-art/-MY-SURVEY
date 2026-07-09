import streamlit as st
import requests
import json
from extra_streamlit_components import CookieManager

# إعدادات الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# مدير الكوكيز لمنع التكرار
cookie_manager = CookieManager()

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# فحص إذا كان الزميل قد أرسل رداً مسبقاً
# ملاحظة: الكوكيز قد تحتاج لجزء من الثانية للتحميل عند فتح الصفحة
submission_status = cookie_manager.get("survey_v2_status")

if submission_status == "submitted":
    st.success("✅ شكرًا لك! لقد قمت بإرسال تقييمك مسبقًا.")
    st.info("لضمان دقة النتائج، يُسمح بإرسال الرد مرة واحدة فقط لكل جهاز.")
    st.balloons()
else:
    st.markdown("""
    ### مادة توضيحية:
    عزيزي الزميل/ة، تحية طيبة وبعد،
    يهدف هذا الاستطلاع إلى قياس مدى رضاكم عن أسلوبي في العمل وكفاءتي المهنية وطريقة تعاملي الشخصية معكم. 
    أؤكد لكم أن هذا الاستبيان **سري تماماً** ولا يتم فيه جمع أي بيانات شخصية، والنتائج ستُستخدم فقط لأغراض التحسين والتطوير ولن تُستخدم في أي خلافات.
    شكراً لوقتكم وصراحتكم التي أقدرها عالياً.
    <hr>
    """, unsafe_allow_html=True)

    # الرابط الخاص بك (Web App URL) من Google Apps Script
    script_url = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

    with st.form(key="survey_form"):
        work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
        efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
        interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
        notes = st.text_area("ملاحظات إضافية أو نصائح للتطوير (اختياري):")
        
        submit_button = st.form_submit_button(label="إرسال التقييم")

    if submit_button:
        payload = {
            "work_style": str(work_style),
            "efficiency": str(efficiency),
            "interaction": str(interaction),
            "notes": notes
        }
        
        try:
            # محاولة إرسال البيانات
            response = requests.post(script_url, data=json.dumps(payload))
            
            # إذا نجح الإرسال
            if response.status_code == 200:
                # زرع بصمة في المتصفح لمنع التكرار مستقبلاً
                cookie_manager.set("survey_v2_status", "submitted", key="cookie_tracker")
                st.success("تم إرسال تقييمك بنجاح! شكراً لك.")
                st.balloons()
                # إعادة تحميل الصفحة لتفعيل المنع وإخفاء النموذج
                st.rerun()
            else:
                st.error("فشل الإرسال، يرجى التأكد من إعدادات الوصول في جوجل شيت.")

        except Exception as e:
            # استثناء خاص بـ Streamlit لتفادي رسالة الخطأ الوهمية
            if "RerunException" in str(type(e)):
                raise e
            else:
                st.error("حدث خطأ تقني، يرجى المحاولة مرة أخرى.")
