import pandas as pd
import sqlite3
import logging

# --- Cấu hình ---
BILL_CSV_PATH = "bill.csv"
SLOT_CSV_PATH = "slot.csv"
DB_PATH = "sales.db"
BILLS_TABLE = "bill"
SLOTS_TABLE = "slot"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initial_load():
    """
    Đọc các file CSV ban đầu và tải chúng vào cơ sở dữ liệu SQLite.
    Hàm này sẽ XÓA và TẠO LẠI các bảng nếu chúng đã tồn tại.
    """
    logging.info(f"Bắt đầu quá trình tải dữ liệu ban đầu vào '{DB_PATH}'...")

    try:
        # Kết nối đến database
        conn = sqlite3.connect(DB_PATH)

        # 1. Xử lý file bill.csv
        logging.info(f"Đang đọc file '{BILL_CSV_PATH}'...")
        df_bills = pd.read_csv(BILL_CSV_PATH)

        # Ghi vào bảng 'bills', thay thế nếu bảng đã tồn tại
        df_bills.to_sql(BILLS_TABLE, conn, if_exists='replace', index=False)
        logging.info(f"Đã tải thành công {len(df_bills)} dòng vào bảng '{BILLS_TABLE}'.")

        # 2. Xử lý file slot.csv
        logging.info(f"Đang đọc file '{SLOT_CSV_PATH}'...")
        df_slots = pd.read_csv(SLOT_CSV_PATH)

        # Ghi vào bảng 'slots', thay thế nếu bảng đã tồn tại
        df_slots.to_sql(SLOTS_TABLE, conn, if_exists='replace', index=False)
        logging.info(f"Đã tải thành công {len(df_slots)} dòng vào bảng '{SLOTS_TABLE}'.")

        conn.close()
        logging.info("Quá trình tải dữ liệu ban đầu đã hoàn tất.")

    except FileNotFoundError as e:
        logging.error(f"Lỗi không tìm thấy file: {e}. Vui lòng kiểm tra lại đường dẫn file trong cấu hình.")


if __name__ == "__main__":
    print("------------------------------------------------------------------")
    print("CẢNH BÁO: Script này sẽ xóa và tạo lại các bảng trong database.")
    print("           Chỉ chạy nó MỘT LẦN để khởi tạo dữ liệu.")
    print("------------------------------------------------------------------")
    answer = input("Bạn có chắc muốn tiếp tục? (y/n): ")
    if answer.lower() == 'y':
        initial_load()
    else:
        print("Đã hủy quá trình khởi tạo.")