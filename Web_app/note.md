Backend:
    Đọc dữ liệu từ CSV (hoặc dummy data nếu không có CSV) 
    Tiền xử lý dữ liệu: chuyển cột số về float, drop NaN 
    Tính toán K-means và gán nhãn cluster 

Visualizations:
    Biểu đồ EDA: phân phối giá, số lượng sản phẩm theo category 

    Biểu đồ K-means clustering: scatter plot Price vs Final_Price với màu cluster và tâm cụm 

Web App cơ bản:
    Trang home hiển thị bảng dữ liệu
    Các trang EDA và Clustering hiển thị biểu đồ
    Có navigation giữa các trang 

=> Như vậy web đã minh họa được toàn bộ workflow của đề tài: tiền xử lý → EDA → phân cụm K-means → visual. Đây là yêu cầu cơ bản của một báo cáo đồ án/data project.

Luồng web hoàn chỉnh
    1. Trang Home → xem bảng dữ liệu → link tới Upload / EDA / Clustering
    2. Trang Upload → upload CSV mới → cập nhật df → redirect Home
    3. Trang EDA → hiển thị biểu đồ Price / Category
    4. Trang Clustering → nhập K → scatter plot → link tới bảng phân cụm
    5. Trang Cluster Table → xem bảng phân cụm chi tiết

Ý nghĩa của các Cụm
    Ba cụm 0, 1, 2 đại diện cho ba phân khúc khách hàng khác nhau về hành vi chi tiêu:
    Cụm 2 (Vàng, Giá thấp): Phân khúc khách hàng nhạy cảm về giá, chủ yếu mua sắm các mặt hàng giá trị thấp.
    Cụm 0 (Tím, Giá trung bình): Phân khúc khách hàng có mức chi tiêu vừa phải, có thể chấp nhận giảm giá ít hơn một chút.
    Cụm 1 (Xanh ngọc, Giá cao): Phân khúc khách hàng chi tiêu cao, ít quan tâm đến giảm giá tuyệt đối mà tập trung vào sản phẩm giá trị lớn.

Phương pháp K-Means (Trực quan hóa 2D)
    Biểu đồ đã thành công trong việc hiển thị kết quả của thuật toán K-Means:
    Mỗi cụm là một nhóm các điểm dữ liệu tương đồng (gần nhau) trong không gian 2D.
    Các điểm X màu đỏ chính là tâm cụm (Centroids), đại diện cho giá trị trung bình của Price và Final Price trong mỗi cụm.