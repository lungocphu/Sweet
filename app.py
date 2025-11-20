import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="Chat với AI của tôi")

# Lấy API Key từ hệ thống (bảo mật)
# Bạn sẽ cài đặt key này ở Bước 3, không dán trực tiếp vào đây để lộ key
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Cấu hình Model (Copy từ AI Studio dán vào đây)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash", # Hoặc model bạn chọn
  generation_config=generation_config,
  # Dán system instruction của bạn vào đây nếu có
)

# Giao diện Chat
st.title("🤖 Trợ lý AI của tôi")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
    except Exception as e:
        st.error(f"Lỗi: {e}")
