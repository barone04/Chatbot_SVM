
# 📚 Chatbot_SVM

Chatbot SVM là một ứng dụng chatbot tích hợp Streamlit và mô hình Gemini (Google) để trả lời câu hỏi từ dữ liệu SQL và vectorstore. Ứng dụng còn hỗ trợ các công cụ nội bộ để chạy truy vấn SQL, xem schema bảng, và phân tích dữ liệu bán hàng.

---

## 📁 Cấu trúc thư mục

```
Chatbot_SVM/
├── data/                 # File dữ liệu hoặc ảnh (nếu có)
├── img/                  # Chứa hình ảnh giao diện hoặc logo
├── src/
│   ├── agent.py          # File chạy chính (Streamlit UI + Chatbot logic)
│   ├── tools/            # Các công cụ SQL custom dùng cho Agent (BaseTool)
│   └── utils/            # Các tiện ích phụ trợ (nếu có)
├── vectorstore/          # Chứa Chroma vector DB đã được embedding
├── environment.yml       # Môi trường Conda
└── README.md             # Hướng dẫn sử dụng
```

---

## 🚀 Hướng dẫn cài đặt

### 1. Clone repository

```bash
git clone https://github.com/barone04/Chatbot_SVM.git
cd Chatbot_SVM
```

### 2. Tạo môi trường từ `environment.yml`

```bash
conda env create -f environment.yml
conda activate Chatbot_SVM
```

> 💡 Nếu bạn đã cài thêm thư viện mới, chạy `conda env update -f environment.yml` để cập nhật môi trường.

### 3. Cấu hình biến môi trường

Tạo file `.env` trong thư mục `Chatbot_SVM/` hoặc `src/` (nơi có `agent.py`) và thêm vào:

```
GOOGLE_API_KEY=your_gemini_api_key
```

> 🔑 API Key được lấy từ: https://aistudio.google.com/app/apikey

### 4. Chạy ứng dụng

```bash
cd src
streamlit run agent.py
```

---

## 🧠 Các chức năng chính

| Tính năng | Mô tả |
|----------|-------|
| 💬 Chatbot | Hỏi đáp dữ liệu dựa vào vectorstore và dữ liệu SQL |
| 🛠️ Tools nội bộ | Gồm `list_tables`, `tables_schema`, `execute_sql`, `check_sql` |
| 🖼️ UI hiện đại | Giao diện giống ChatGPT, có hiển thị câu hỏi, câu trả lời, log |
| 🔧 Tùy biến | Có thể thêm câu hỏi, vẽ bảng, hiển thị ảnh, chỉnh CSS, v.v |

---

## 🖼️ Giao diện mẫu

![Giao diện Chatbot](img/hyper.png)

---

## ❗ Lưu ý

- Hạn mức gọi model `gemini-2.0-flash` của Google chỉ cho **200 yêu cầu/ngày với gói miễn phí**.
- Nếu gặp lỗi `RateLimitError`, hãy:
  - Đợi sang ngày mới
  - Đổi sang API Key khác
  - Nâng cấp tài khoản

---

## 💡 Mẹo dùng

- Khi dùng `agent.py`, bạn có thể đặt câu hỏi như:
  ```
  Cho tôi biết số lượng sản phẩm chocopie được bán ra vào tháng 5/2025?
  Vẽ bảng thống kê phương thức thanh toán và thời gian bán ra.
  ```

---

## 🛠️ Dev & Customization

Bạn có thể thêm công cụ bằng cách kế thừa từ `BaseTool`:

```python
from crewai.tools import BaseTool

class CustomSQLTool(BaseTool):
    name: str = "execute_sql"
    description: str = "Thực hiện truy vấn SQL"

    def _run(self, query: str) -> str:
        # logic xử lý
        return QuerySQLDataBaseTool(db=db).invoke(query)
```

---

## 📬 Liên hệ

Mọi đóng góp, lỗi hoặc ý tưởng vui lòng gửi về:

**Tác giả:** [@barone04](https://github.com/barone04)  
**Email:** *<điền email nếu muốn>*
