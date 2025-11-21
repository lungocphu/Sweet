import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="SweetTech R&D Mate",
    page_icon="🍬",
    layout="wide"
)

# --- CSS TÙY CHỈNH (MÀU PASTEL) ---
st.markdown("""
<style>
    .main {
        background-color: #FDFBF7; /* Cream White */
    }
    h1 {
        color: #2E8B57; /* Sea Green */
    }
    .stButton>button {
        background-color: #FFB7B2; /* Pastel Red/Pink */
        color: white;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF9E99;
    }
    .report-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CÀI ĐẶT ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2553/2553691.png", width=100)
    st.title("Cấu Hình")
    
    # Nhập API Key để tránh lỗi kết nối
    api_key = st.text_input("Nhập Google API Key của bạn:", type="password")
    
    # Chọn ngôn ngữ hiển thị
    language = st.selectbox(
        "Ngôn ngữ hiển thị / Display Language:",
        ("Tiếng Việt", "English", "한국어 (Korean)")
    )

    st.info("💡 Mẹo: Dùng camera hoặc upload ảnh bao bì để phân tích chính xác hơn.")

# --- HÀM GỌI GEMINI API ---
def analyze_candy(api_key, input_text, image_data, lang_mode):
    if not api_key:
        return "⚠️ Vui lòng nhập API Key ở cột bên trái."
    
    genai.configure(api_key=api_key)
    
    # Cấu hình Model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Prompt hệ thống nâng cấp (Dựa trên yêu cầu trong ảnh của bạn)
    system_prompt = f"""
    Bạn là chuyên gia R&D bánh kẹo "SweetTech Mate". 
    Ngôn ngữ phản hồi bắt buộc: {lang_mode}.
    
    NHIỆM VỤ: Phân tích sản phẩm bánh kẹo dựa trên thông tin đầu vào.
    
    YÊU CẦU CẤU TRÚC BÁO CÁO (Output Format):
    1. **Hồ sơ sản phẩm (Product Profile):** Tên, Loại (Gummy, Hard candy...), Thành phần chính, Texture.
    2. **Phân tích đối thủ (Competitor Analysis):** So sánh với 3 sản phẩm tương tự trên thị trường (ưu tiên đối thủ tại Việt Nam/Hàn Quốc). Tạo bảng so sánh.
    3. **Đánh giá thị trường (Market Review):** Tóm tắt cảm nhận khách hàng (Sentiment Analysis) từ các trang TMĐT (Shopee, Lazada) về dòng sản phẩm này (VD: quá ngọt, bao bì khó mở...).
    4. **R&D Insight & Cải tiến:** Đề xuất công thức cải tiến.
    5. **Nguồn tham khảo (Source Links):** Gợi ý 2-3 link website hoặc search query để tìm thêm thông tin.

    Nếu đầu vào là "Họng Candy" (Kẹo ngậm đau họng), hãy tập trung phân tích các loại kẹo ngậm thảo dược, Lozenge.
    """

    inputs = [system_prompt]
    if input_text:
        inputs.append(f"Sản phẩm cần phân tích: {input_text}")
    if image_data:
        inputs.append(image_data)
        inputs.append("Hãy phân tích bao bì, thành phần và thương hiệu từ hình ảnh này.")

    try:
        with st.spinner('Đang phân tích dữ liệu thị trường...'):
            response = model.generate_content(inputs)
            return response.text
    except Exception as e:
        return f"❌ Lỗi kết nối API: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("🍬 SweetTech R&D Mate")
st.write("Trợ lý AI hỗ trợ phát triển sản phẩm bánh kẹo mới.")

# Tabs nhập liệu
tab1, tab2 = st.tabs(["📝 Nhập Tên/Mô Tả", "📷 Tải Ảnh/Camera"])

user_input = ""
image_input = None

with tab1:
    user_input = st.text_area("Nhập tên hoặc ý tưởng sản phẩm (VD: Kẹo ngậm đau họng vị tắc mật ong):", height=100)

with tab2:
    uploaded_file = st.file_uploader("Tải lên ảnh bao bì sản phẩm:", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image_input = Image.open(uploaded_file)
        st.image(image_input, caption="Ảnh sản phẩm tải lên", width=300)

# Nút Phân Tích
if st.button("🚀 PHÂN TÍCH NGAY", type="primary"):
    if not user_input and not image_input:
        st.warning("Vui lòng nhập thông tin hoặc tải ảnh.")
    else:
        result = analyze_candy(api_key, user_input, image_input, language)
        
        # Hiển thị kết quả
        st.markdown("---")
        st.subheader("📊 Kết Quả Phân Tích")
        st.markdown(f'<div class="report-box">{result}</div>', unsafe_allow_html=True)

        # Nút giả lập xuất báo cáo
        st.download_button("📥 Tải báo cáo (PDF)", data=result, file_name="R&D_Report.md")
