import streamlit as st
from agent import SQLDeveloperCrew


def main():
    # Set page config
    st.set_page_config(page_title="Chatbot SVM", layout="wide")

    # Title
    st.image("../img/hyper.png", width=120, caption="CHATBOT SVM")


    with st.expander("ℹ️ Hướng dẫn", expanded=True):
        st.markdown("""
        📌 **Lưu ý:** Chỉ hỏi các câu liên quan đến sản phẩm có trong máy bán hàng. Nếu được thì nêu rõ tên sản phẩm, tên trường.
    
        💡 **Gợi ý:** hỏi về số lượng bán, phương thức thanh toán, thời gian bán, top sản phẩm, v.v.
        """)

    # Session state cho tin nhắn
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị tin nhắn cũ
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Thanh nhập ở dưới cùng
    user_input = st.chat_input("💬 Nhập câu hỏi về bán hàng...")

    if user_input:
        # Hiển thị câu hỏi
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            inputs = {"query": user_input.strip()}
            crew_instance = SQLDeveloperCrew()
            response = crew_instance.crew().kickoff(inputs=inputs)

            # Hiển thị phản hồi
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # 🧾 Ghi log nếu muốn
            with open("crew.log.txt", "a", encoding="utf-8") as log:
                log.write(f"[USER] {user_input}\n[ASSISTANT] {response}\n\n")

        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")


if __name__ == "__main__":
    main()