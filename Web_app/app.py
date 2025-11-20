from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np
import os
import warnings
from sklearn.exceptions import ConvergenceWarning
import pandas.api.types as pdt 

# Tắt cảnh báo KMeans 
warnings.filterwarnings("ignore", category=ConvergenceWarning)

app = Flask(__name__)

# --- Cấu hình Đường dẫn và Thư mục ---
STATIC_IMAGE_DIR = os.path.join('static', 'images')
os.makedirs(STATIC_IMAGE_DIR, exist_ok=True) 

# --- HÀM TIỀN XỬ LÝ DỮ LIỆU ---
def preprocess_data(data_frame, is_dummy=False):
    """
    Tiền xử lý dữ liệu: 
    1. Đổi tên cột để chuẩn hóa (sử dụng tên cột CHÍNH XÁC từ file CSV).
    2. Chuyển đổi các cột giá tiền về kiểu float.
    3. Loại bỏ các giá trị thiếu (NaN).
    """
    
    # Ánh xạ tên cột (Đã sửa để khớp CHÍNH XÁC với file CSV của bạn)
    COL_MAPPING = {
        'Price(Rs.)': 'Price',        
        'Final_Price(Rs.)': 'Final_Price' 
    }
    
    # 1. Đổi tên cột (chỉ đổi tên các cột tồn tại)
    # Nếu là dữ liệu giả định, tên cột đã đúng nên không cần đổi tên.
    if not is_dummy:
        columns_to_rename = {k: v for k, v in COL_MAPPING.items() if k in data_frame.columns}
        data_frame.rename(columns=columns_to_rename, inplace=True)
    
    # Tên cột mới được sử dụng cho phân tích
    numeric_cols_standard = ['Price', 'Final_Price']
    
    # 2. Xử lý các cột số và chuyển đổi kiểu dữ liệu
    for col in numeric_cols_standard:
        if col in data_frame.columns:
            # Chuyển sang kiểu số. errors='coerce' sẽ biến các giá trị không phải số thành NaN
            # Dữ liệu thật có thể là object nên cần bước này
            data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce')
        else:
            print(f"WARNING: Cột chuẩn hóa '{col}' không tồn tại trong DataFrame. Vui lòng kiểm tra lại COL_MAPPING hoặc dữ liệu đầu vào.")

    # 3. Xử lý các giá trị NaN (chỉ áp dụng cho các cột được sử dụng cho K-means)
    # Chỉ loại bỏ NaN nếu các cột chuẩn hóa thực sự tồn tại
    cols_exist = [col for col in numeric_cols_standard if col in data_frame.columns]
    data_frame.dropna(subset=cols_exist, inplace=True)
    
    print("DataFrame Info after preprocessing:")
    data_frame.info()
    
    return data_frame

# --- Load Dữ liệu ---
try:
    # 1. Thử tải dữ liệu thật
    df = pd.read_csv("../data/ecommerce_cleaned.csv") 
    df = preprocess_data(df, is_dummy=False) # Áp dụng tiền xử lý
except FileNotFoundError:
    # 2. Nếu không tìm thấy, tạo dữ liệu giả định
    print("WARNING: File ../data/ecommerce_cleaned.csv not found. Using dummy data for demonstration.")
    # SỬ DỤNG TÊN CỘT CHUẨN HÓA SẴN CHO DỮ LIỆU GIẢ ĐỊNH
    data = {
        'User_ID': [f'u{i}' for i in range(100)],
        'Product_ID': [f'p{i}' for i in range(100)],
        'Category': np.random.choice(['Sports', 'Clothing', 'Toys', 'Electronics', 'Beauty'], 100),
        'Price': np.random.randint(50, 500, 100) * 1.0, # Tạo sẵn dưới dạng số (float)
        'Discount': np.random.randint(10, 30, 100) * 1.0,
        'Final_Price': np.random.randint(40, 400, 100) * 1.0
    }
    df = pd.DataFrame(data)
    df = preprocess_data(df, is_dummy=True) # is_dummy=True để bỏ qua bước rename trong preprocess


# --- Hàm hỗ trợ: Tạo và Lưu biểu đồ EDA ---
def generate_eda_plots(data_frame):
    """Tạo và lưu các biểu đồ EDA vào thư mục static/images."""
    
    # 1. Biểu đồ Phân phối giá (Price Distribution)
    plt.figure(figsize=(8, 5))
    # Kiểm tra đảm bảo cột Price tồn tại và là kiểu số
    if 'Price' in data_frame.columns and pdt.is_numeric_dtype(data_frame['Price']):
        sns.histplot(data_frame['Price'], kde=True) 
        plt.xlabel('Giá (Price)')
        plt.title('Phân phối Giá (Price Distribution)')
        plt.ylabel('Tần suất')
    else:
        plt.text(0.5, 0.5, "LỖI: Thiếu cột Price hoặc dữ liệu không phải dạng số.", ha='center', va='center', fontsize=12)
        plt.title('LỖI Biểu đồ Phân phối Giá')
        
    plt.savefig(os.path.join(STATIC_IMAGE_DIR, 'price_distribution.png'))
    plt.close()

    # 2. Biểu đồ Đếm Category (Category Count)
    plt.figure(figsize=(8, 5))
    if 'Category' in data_frame.columns:
        sns.countplot(y='Category', data=data_frame, order = data_frame['Category'].value_counts().index)
        plt.title('Số lượng Sản phẩm theo Category')
        plt.xlabel('Số lượng')
        plt.ylabel('Category')
    else:
        plt.text(0.5, 0.5, "LỖI: Thiếu cột Category.", ha='center', va='center', fontsize=12)
        plt.title('LỖI Biểu đồ Đếm Category')
        
    plt.savefig(os.path.join(STATIC_IMAGE_DIR, 'category_count.png'))
    plt.close()

# --- Hàm hỗ trợ: Tạo và Lưu biểu đồ Clustering ---
def generate_clustering_plot(data_frame):
    """Thực hiện K-means và lưu biểu đồ phân cụm vào thư mục static/images."""
    
    # SỬ DỤNG TÊN CỘT ĐÃ CHUẨN HÓA: 'Price' và 'Final_Price'
    features = ['Price', 'Final_Price']
    
    # Kiểm tra đảm bảo các cột cần thiết đã được làm sạch và tồn tại
    if not all(col in data_frame.columns and pdt.is_numeric_dtype(data_frame[col]) for col in features):
        print("ERROR: Các cột giá tiền không phải dạng số hoặc bị thiếu sau tiền xử lý.")
        # Nếu không đủ dữ liệu, tạo biểu đồ lỗi
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, "LỖI: Không đủ dữ liệu số để Phân cụm.", ha='center', va='center', fontsize=14, color='red')
        plt.title('LỖI K-means Clustering')
        plt.savefig(os.path.join(STATIC_IMAGE_DIR, 'cluster_plot.png'))
        plt.close()
        return

    # 1. Chuẩn bị dữ liệu
    X = data_frame[features].values
    
    # 2. Thực hiện K-means 
    K = 3
    # Đảm bảo n_init='auto' để tránh cảnh báo.
    kmeans = KMeans(n_clusters=K, random_state=42, n_init='auto') 
    data_frame['Cluster'] = kmeans.fit_predict(X)
    
    # 3. Tạo biểu đồ phân cụm
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(
        x='Price', 
        y='Final_Price', 
        hue='Cluster', 
        data=data_frame, 
        palette='viridis', 
        legend='full',
        s=100
    )
    
    # Vẽ các tâm cụm
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=300, alpha=0.9, marker='X', label='Tâm cụm')
    
    plt.title(f'K-means Clustering Results (K={K})')
    plt.xlabel('Giá (Price)')
    plt.ylabel('Giá cuối (Final Price)')
    
    # 4. Lưu biểu đồ vào thư mục static/images
    plt.savefig(os.path.join(STATIC_IMAGE_DIR, 'cluster_plot.png'))
    plt.close()


# --- Tuyến đường Home ---
@app.route("/")
def home():
    # Sử dụng df.head() đã được tiền xử lý
    return render_template("home.html", title="Home", rows=df.head().to_html(classes="table table-striped"))

# --- Tuyến đường EDA ---
@app.route("/eda")
def eda():
    generate_eda_plots(df) 
    return render_template("eda.html", title="Exploratory Data Analysis")

# --- Tuyến đường Clustering ---
@app.route("/clustering")
def clustering():
    generate_clustering_plot(df)
    return render_template("clustering.html", title="K-means Clustering")

if __name__ == "__main__":
    app.run(debug=True)