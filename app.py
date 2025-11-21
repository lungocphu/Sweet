import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CẤU HÌNH API & MODEL ---
# Key của bạn đã được điền sẵn vào đây
API_KEY = "AIzaSyDGXaBC7iRn-Iu2P62Mo4Nl5R-aAkw88FQ"

try:
    genai.configure(api_key=API_KEY)
    # Sử dụng model mạnh nhất hiện tại cho nhiệm vụ phân tích phức tạp
    # Nếu bạn có quyền truy cập model 3.0, hãy đổi chuỗi bên dưới thành 'gemini-3.0-pro-preview'
    model = genai.GenerativeModel('gemini-1.5-pro') 
except Exception as e:
    st.error(f"Lỗi cấu hình API: {e}")

# --- 2. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="SweetTech R&D Mate",
    page_icon="🍬",
    layout="wide"
)

# CSS làm đẹp giao diện (Màu Pastel & Minimalist)
st.markdown("""
<style>
    .main { background-color: #FDFBF7; } /* Màu kem nền */
    h1 { color: #2E8B57; font-family: 'Helvetica', sans-serif; }
    .stButton>button {
        background-color: #FFB7B2; /* Hồng Pastel */
        color: white;
        border-radius: 8px;
        height: 50px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #FF9E99; }
    .report-container {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #2E8B57;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HÀM XỬ LÝ PHÂN TÍCH (CORE ENGINE) ---
def analyze_product(input_text, image_data, language_opt):
    
    # Prompt hệ thống (System Instruction) - Đóng vai chuyên gia R&D
    system_prompt = f"""
    Bạn là "SweetTech R&D Mate" - Trợ lý AI cao cấp cho bộ phận R&D bánh kẹo.
    Ngôn ngữ phản hồi: {language_opt}.
    
    NHIỆM VỤ: Phân tích dữ liệu sản phẩm để hỗ trợ phát triển sản phẩm mới.
    
    CẤU TRÚC BÁO CÁO ĐẦU RA (Markdown):
    1. **🔍 Tổng Quan Sản Phẩm (Product Overview):**
       - Tên thương mại & Thương hiệu.
       - Phân loại (Hard Candy, Gummy, Jelly, Chocolate...).
       - Đặc tính nổi bật (Sugar-free, Organic, Vegan...).

    2. **⚔️ Bảng So Sánh Đối Thủ (Competitor Benchmarking):**
       - Hãy kẻ một bảng so sánh gồm 4 cột: [Sản phẩm này] vs [Đối thủ A] vs [Đối thủ B] vs [Đối thủ C].
       - Các tiêu chí so sánh: Giá bán ước tính (VND/kg), Hàm lượng đường, Texture (Cấu trúc), Điểm mạnh (USP).
       - *Lưu ý: Ưu tiên chọn đối thủ đang bán tại thị trường Việt Nam hoặc Châu Á.*

    3. **📢 Lắng Nghe Thị Trường (Review Sentiment):**
       - Đóng vai là AI Crawler, tóm tắt "Nỗi đau của khách hàng" (Pain points) từ các review trên Shopee/Lazada/Amazon đối với dòng sản phẩm này.
       - Ví dụ: "Khách than phiền kẹo bị chảy nước khi trời nóng", "Vị ngọt gắt cổ".

    4. **💡 Đề Xuất Cải Tiến R&D (Innovation):**
       - Đề xuất 03 ý tưởng cụ thể để cải thiện công thức hoặc bao bì.
       - Ví dụ: "Dùng đường Isomalt thay thế", "Thêm tinh dầu bạc hà tự nhiên".

    5. **🔗 Nguồn Tham Khảo (References):**
       - Cung cấp 2-3 từ khóa tìm kiếm hoặc Link website uy tín để kiểm chứng thông tin.

    DỮ LIỆU ĐẦU VÀO CỦA NGƯỜI DÙNG:
    """
    
    request_content = [system_prompt]
    if input_text:
        request_content.append(f"Thông tin/Ý tưởng sản phẩm: {input_text}")
    if image_data:
        request_content.append(image_data)
        request_content.append("Hãy phân tích kỹ bao bì, bảng thành phần (nếu thấy) và hình dạng sản phẩm trong ảnh.")

    with st.spinner('🤖 AI đang nghiên cứu công thức và quét dữ liệu thị trường...'):
        try:
            response = model.generate_content(request_content)
            return response.text
        except Exception as e:
            return f"❌ Lỗi kết nối: {str(e)}"

# --- 4. GIAO DIỆN NGƯỜI DÙNG (UI) ---

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081967.png", width=80)
    st.header("Cài Đặt Phân Tích")
    language = st.selectbox("Ngôn ngữ báo cáo:", ["Tiếng Việt", "English", "한국어 (Korean)"])
    st.divider()
    st.info("💡 **Mẹo R&D:** Tải ảnh bảng thành phần phía sau gói kẹo để AI phân tích phụ gia chính xác hơn.")

# Main Content
st.title("🍬 SweetTech R&D Mate")
st.caption(f"Powered by Google Gemini Pro • API Key: Active")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Nhập liệu")
    input_text = st.text_area("Mô tả sản phẩm hoặc ý tưởng:", height=150, 
                              placeholder="VD: Kẹo dẻo hỗ trợ ngủ ngon vị việt quất, dùng pectin thay gelatin...")
    
    uploaded_file = st.file_uploader("Hoặc tải ảnh sản phẩm/bao bì:", type=["jpg", "png", "jpeg"])
    
    image_val = None
    if uploaded_file:
        image_val = Image.open(uploaded_file)
        st.image(image_val, caption="Ảnh đã tải lên", use_column_width=True)

with col2:
    st.subheader("2. Kết quả phân tích")
    
    # Nút bấm kích hoạt
    analyze_btn = st.button("🚀 PHÂN TÍCH & SO SÁNH NGAY")
    
    if analyze_btn:
        if not input_text and not image_val:
            st.warning("⚠️ Vui lòng nhập mô tả hoặc tải ảnh để bắt đầu.")
        else:
            # Gọi hàm phân tích
            result = analyze_product(input_text, image_val, language)
            
            # Hiển thị kết quả
            st.markdown(f'<div class="report-container">{result}</div>', unsafe_allow_html=True)
            
            # Nút tải về
            st.download_button(
                label="📥 Xuất báo cáo (Text File)",
                data=result,
                file_name="RD_Candy_Report.md",
                mime="text/markdown"
            )

# Footer
st.markdown("---")
st.markdown("*Công cụ hỗ trợ nội bộ cho team R&D Bánh Kẹo - Phát triển trên nền tảng Google Gemini.*")
