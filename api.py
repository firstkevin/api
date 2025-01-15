import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def read_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("디자인 씽킹 비즈니스 개발 챗봇 🤖")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
        pdf_text = ""
        
        if uploaded_file:
            pdf_text = read_pdf(uploaded_file)
            st.success("PDF 파일이 성공적으로 업로드되었습니다!")
            
        # 채팅 인터페이스
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("메시지를 입력하세요"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Gemini 모델 설정
            model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
            
            context = f"""
            당신은 디자인 씽킹 방법론을 활용한 비즈니스 개발 전문가입니다.
            다음 PDF 내용을 참고하여 답변해주세요: {pdf_text}
            """
            
            response = model.generate_content([context, prompt])
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    else:
        st.warning("API 키를 입력해주세요.")

if __name__ == "__main__":
    main()
