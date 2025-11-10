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