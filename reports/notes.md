===== CÂU 1: Dataset có bao nhiêu dòng và cột? =====
Số dòng: 3660
Số cột: 8

===== CÂU 2: Có bao nhiêu giá trị bị thiếu hoặc không hợp lệ? =====
Không có giá trị thiếu!

===== CÂU 3: Các cột quan trọng trong bộ dữ liệu =====
['User_ID', 'Product_ID', 'Category', 'Price (Rs.)', 'Discount (%)', 'Final_Price(Rs.)', 'Payment_Method', 'Purchase_Date']

===== CÂU 4: Dữ liệu trải dài trong khoảng thời gian nào? =====
Khoảng thời gian: từ 2024-01-01 00:00:00 đến 2024-12-11 00:00:00

===== CÂU 5: Có cột nào cần tách, gộp hoặc xử lý đặc biệt không? =====
→ Kiểm tra kiểu dữ liệu:
User_ID                     object
Product_ID                  object
Category                    object
Price (Rs.)                float64
Discount (%)                 int64
Final_Price(Rs.)           float64
Payment_Method              object
Purchase_Date       datetime64[ns]
dtype: object

Gợi ý: Kiểm tra các cột có dạng phần trăm (%) hoặc ký hiệu tiền tệ để xử lý

# 1️⃣ 01_Data_Preprocessing.ipynb
Mục tiêu: Làm sạch, chuẩn hóa và lưu dữ liệu sạch
Nội dung chính:
Đọc dữ liệu thô (Customer_Purchase_History.csv)
Kiểm tra dữ liệu bị thiếu
Xử lý lỗi, chuyển kiểu dữ liệu, thêm cột Month, Year
Tính toán các đặc trưng đơn giản (ví dụ: tổng chi tiêu theo tháng)
Lưu lại thành data_cleaned.csv

# 2️⃣ 02_Data_Analysis.ipynb
Mục tiêu: Phân tích hành vi mua sắm trước khi gom cụm.
Nội dung dự kiến:
Phân tích phân phối của:
    Danh mục sản phẩm (Category)
    Phương thức thanh toán
    Giá trung bình, chiết khấu trung bình
Trực quan hóa:
    Biểu đồ cột/tỷ lệ % giữa các danh mục
    Phân tích xu hướng chi tiêu theo thời gian (Month, Year)
    Biểu đồ hộp (boxplot) giá trị Final_Price để thấy outlier

=> Rút ra nhận xét và insight
Nhận xét sau khi chạy xong file 02_Data_Analysis.ipynb
Nhận xét sơ bộ:
1. Một số danh mục đóng góp phần lớn vào tổng doanh thu.
2. Có sự khác biệt rõ rệt giữa các phương thức thanh toán — có thể gợi ý cho chiến lược ưu đãi riêng.
3. Xu hướng chi tiêu theo tháng giúp xác định thời điểm cao điểm trong năm.

# 3️⃣ 03_Customer_Clustering.ipynb
Mục tiêu: Áp dụng K-Means để phân nhóm khách hàng theo hành vi mua sắm
Nội dung dự kiến:
    Chọn các đặc trưng phù hợp (ví dụ: tổng chi tiêu, số đơn hàng, số danh mục đã mua, mức giảm giá trung bình, v.v.)
    Chuẩn hóa dữ liệu (StandardScaler)
    Chọn số cụm tối ưu (Elbow method, Silhouette score)
    Thực hiện K-Means
    Gắn nhãn cụm và trực quan hóa kết quả
    Nhận xét đặc trưng của từng nhóm khách hàng