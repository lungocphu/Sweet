import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="Chat với AI của tôi")

# Lấy API Key từ hệ thống (bảo mật)
# Bạn sẽ cài đặt key này ở Bước 3, không dán trực tiếp vào đây để lộ key
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Cấu hình Model (Copy từ AI Studio dán vào đây)
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)

