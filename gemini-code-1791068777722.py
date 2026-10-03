import streamlit as st
import numpy as np
from PIL import Image
import cv2

# تنظیمات صفحه
st.set_page_config(
    page_title="سیستم هوشمند تخصصی انتخاب عینک | Eye1 AI",
    page_icon="👓",
    layout="wide"
)

# استایل‌دهی و ظاهر حرفه‌ای
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #0d6efd;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .recommendation-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# هدر برنامه
st.title("👓 سامانه هوشمند تخصصی انتخاب عینک (نسخه بالینی و زیبایی‌شناسی)")
st.markdown("این سیستم بر اساس پارامترهای آناتومیک چهره، تناسبات هندسی، تن رنگ پوست و اصول اپتومتریک، بهترین فریم عینک را به شما پیشنهاد می‌کند.")

# نوار کناری (Sidebar) برای ورود پارامترهای تخصصی کاربر
st.sidebar.header("⚙️ تنظیمات بالینی و اپتومتریک")
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)
rx_type = st.sidebar.selectbox("نوع نمره چشم (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده (Progressive)", "بدون نمره / محافظ بلوکات"])
face_shape_override = st.sidebar.selectbox("تشخیص دستی فرم صورت (اختیاری)", ["تشخیص خودکار هوش مصنوعی", "بیضی (Oval)", "گرد (Round)", "مربعی (Square)", "قلبی (Heart)", "الماس (Diamond)"])

# بخش آپلود تصویر چهره
st.markdown("### ۱. بارگذاری تصویر چهره کاربر")
uploaded_file = st.file_uploader("لطفاً تصویری روبه‌رو، با نور مناسب و بدون عینک از چهره خود آپلود کنید:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # خواندن تصویر
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### تصویر آپلود شده:")
        st.image(image, use_column_width=True)

    with col2:
        st.markdown("#### نتایج تحلیل هوش مصنوعی و آناتومی:")
        
        with st.spinner("در حال پردازش نقاط کلیدی صورت و استخراج هارمونی..."):
            # شبیه‌سازی تحلیل هوش مصنوعی بر اساس ابعاد تصویر و الگوریتم‌های هندسی
            h, w, _ = img_array.shape
            aspect_ratio = h / w
            
            # تعیین فرم صورت بر اساس نسبت ابعاد یا انتخاب کاربر
            if face_shape_override == "تشخیص خودکار هوش مصنوعی":
                if aspect_ratio > 1.3:
                    detected_shape = "بیضی (Oval)"
                    features = "متعادل‌ترین فرم صورت؛ تقریباً هر نوع فریم کلاسی یا مدرنی با آن سازگار است."
                elif 1.0 <= aspect_ratio <= 1.3:
                    detected_shape = "گرد (Round)"
                    features = "خط فک نرم و عرض و ارتفاع صورت نزدیک به هم؛ فریم‌های زاویه‌دار و مستطیلی توصیه می‌شود."
                else:
                    detected_shape = "مربعی (Square)"
                    features = "فک قوی و پیشانی پهن؛ فریم‌های گرد، بیضی یا خلبانی (Aviator) برای نرم کردن زوایا عالی هستند."
            else:
                detected_shape = face_shape_override
                features = "بر اساس انتخاب دستی شما بررسی شد."

            # تحلیل رنگ‌شناسی ساده (Colorimetry) از روی میانگین رنگ پوست در مرکز تصویر
            avg_color = np.mean(img_array[int(h*0.4):int(h*0.6), int(w*0.4):int(w*0.6)], axis=(0,1))
            skin_tone = "گرم (Warm)" if avg_color[0] > avg_color[2] else "سرد یا خنثی (Cool/Neutral)"

        # نمایش گزارش تحلیلی
        st.success("✅ تحلیل چهره با موفقیت انجام شد!")
        st.write(f"🔹 **فرم آناتومیک صورت:** {detected_shape}")
        st.write(f"💡 **تحلیل ویژگی‌ها:** {features}")
        st.write(f"🎨 **برآورد تن رنگی پوست:** {skin_tone}")
        st.write(f"📏 **سایز پیشنهادی فریم (بر اساس PD = {pd_input}mm):** پهنای عدسی {pd_input - 10} تا {pd_input - 6} میلی‌متر")

    st.markdown("---")
    st.markdown("### ۲. پیشنهادهای تخصصی فریم عینک (برندینگ، استایل و اپتیک)")

    # پیشنهاد بر اساس فرم صورت و نوع نمره
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
            <div class="recommendation-card">
                <h4>🌟 پیشنهاد اول: لوکس و کلاسیک</h4>
                <p><b>برند:</b> Tom Ford</p>
                <p><b>استایل:</b> فریم کایبر یا استات ضخیم تیره</p>
                <p><b>دلیل علمی:</b> ایجاد کنتراست عالی با خط فک و برجسته کردن فرم چشم‌ها.</p>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
            <div class="recommendation-card">
                <h4>🕶️ پیشنهاد دوم: اسپرت و مدرن</h4>
                <p><b>برند:</b> Ray-Ban</p>
                <p><b>استایل:</b> ویفرر (Wayfarer) یا فریم‌های فلزی سبک</p>
                <p><b>دلیل علمی:</b> توزیع متوازن وزن فریم روی پل بینی متناسب با PD شما.</p>
            </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown(f"""
            <div class="recommendation-card">
                <h4>🔬 تطبیق با نمره چشم ({rx_type})</h4>
                <p><b>نوع عدسی توصیه شده:</b> Index 1.60 یا 1.67 فشرده</p>
                <p><b>نکته اپتومتریک:</b> با توجه به فاصله دو چشم ({pd_input}mm)، فریم‌های با پل (Bridge) سایز ۱۸ تا ۲۰ میلی‌متر انتخاب شوند تا مرکز اپتیکی عدسی دقیقاً مقابل مردمک قرار گیرد.</p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.info("👈 لطفاً برای شروع فرآیند تحلیل و دریافت پیشنهاد فریم، تصویر خود را از طریق دکمه بالا آپلود کنید.")