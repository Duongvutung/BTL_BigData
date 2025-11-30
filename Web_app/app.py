from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np
import os
import warnings
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=ConvergenceWarning)

app = Flask(__name__)
app.secret_key = "abc123"

df_upload = None   # Dữ liệu upload
current_df = None  # Không dùng nữa, giữ df_upload

# --- PATH ---
STATIC_IMAGE_DIR = os.path.join("static", "images")
os.makedirs(STATIC_IMAGE_DIR, exist_ok=True)

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --- PREPROCESS ---
def preprocess_data(df, is_dummy=False):
    df.columns = df.columns.str.strip()

    mapping = {
        "Price (Rs.)": "Price",
        "Final_Price(Rs.)": "Final_Price",
        "price": "Price",
        "freight_value": "Freight"
    }
    df.rename(columns={k: v for k, v in mapping.items() if k in df.columns}, inplace=True)

    if "Price" in df.columns:
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    if "Freight" in df.columns:
        df["Freight"] = pd.to_numeric(df["Freight"], errors="coerce")

    # Tạo Total_Price
    if "Price" in df.columns and "Freight" in df.columns:
        df["Total_Price"] = df["Price"] + df["Freight"]
    elif "Price" in df.columns:
        df["Total_Price"] = df["Price"]
    else:
        raise KeyError("Không có cột Price, không thể tính Total_Price")

    required_cols = ["Price", "Total_Price"]
    if not is_dummy:
        df.dropna(subset=required_cols, inplace=True)

    return df

# --- LOAD DEFAULT DATA ---
try:
    df_default = pd.read_csv("../data/ecommerce_cleaned.csv")
    df_default = preprocess_data(df_default)
except:
    df_default = pd.DataFrame({
        "User_ID": [f"u{i}" for i in range(100)],
        "Product_ID": [f"p{i}" for i in range(100)],
        "Category": np.random.choice(["Sports", "Clothing", "Toys"], 100),
        "Price": np.random.randint(50, 500, 100).astype(float),
        "Final_Price": np.random.randint(40, 480, 100).astype(float)
    })
    df_default = preprocess_data(df_default, is_dummy=True)

# --- EDA ---
def generate_eda_plots(df, prefix="", include_category=True):
    # Biểu đồ Price
    plt.figure(figsize=(8, 5))
    if "Price" in df.columns:
        sns.histplot(df["Price"], kde=True)
        plt.title("Phân phối Giá")
    plt.savefig(os.path.join(STATIC_IMAGE_DIR, f"{prefix}price_distribution.png"))
    plt.close()

    # Biểu đồ Category chỉ khi có cột Category và include_category=True
    if include_category and "Category" in df.columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(y="Category", data=df)
        plt.title("Số lượng từng category")
        plt.savefig(os.path.join(STATIC_IMAGE_DIR, f"{prefix}category_count.png"))
        plt.close()


# --- KMEANS ---
def generate_clustering_plot(df, K=3, filename="cluster_plot.png"):
    features = ["Price", "Total_Price"]

    if not all(col in df.columns for col in features):
        plt.figure(figsize=(8, 5))
        plt.text(0.5, 0.5, "Không đủ dữ liệu Price/Total_Price", ha='center')
        plt.savefig(os.path.join(STATIC_IMAGE_DIR, filename))
        plt.close()
        return

    X = df[features].values
    kmeans = KMeans(n_clusters=K, random_state=42)
    df["Cluster"] = kmeans.fit_predict(X)

    plt.figure(figsize=(8, 6))
    palette = sns.color_palette("tab20", K)

    for i in range(K):
        cluster_data = df[df["Cluster"] == i]
        plt.scatter(
            cluster_data["Price"],
            cluster_data["Total_Price"],
            s=40,
            label=f"Cluster {i}",
            color=palette[i]
        )

    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], s=200, c="red", marker="X")
    plt.legend()
    plt.xlabel("Price")
    plt.ylabel("Total Price")
    plt.title(f"K-means Clustering (K={K})")
    plt.savefig(os.path.join(STATIC_IMAGE_DIR, filename))
    plt.close()

# --- ROUTES ---
@app.route("/")
def home():
    global df_upload

    default_table = df_default.head(10).to_html(classes="table table-striped")
    upload_table = df_upload.head(10).to_html(classes="table table-striped") if df_upload is not None else None

    return render_template(
        "home.html",
        default_table=default_table,
        upload_table=upload_table
    )

@app.route("/eda")
def eda():
    # Dữ liệu mặc định → vẫn hiển thị cả 2 biểu đồ
    generate_eda_plots(df_default, prefix="", include_category=True)
    
    # Dữ liệu upload → chỉ hiển thị biểu đồ Price
    uploaded = df_upload is not None
    if uploaded:
        generate_eda_plots(df_upload, prefix="upload_", include_category=False)

    return render_template("eda.html", uploaded=uploaded)



@app.route("/clustering", methods=["GET", "POST"])
def clustering():
    global df_upload

    # Lấy K mặc định
    K_default = int(request.form.get("k_clusters", 3)) if request.method == "POST" and "k_clusters" in request.form else 3
    generate_clustering_plot(df_default, K_default, filename="cluster_plot.png")

    # Dữ liệu upload
    uploaded = df_upload is not None
    K_upload = int(request.form.get("k_upload", 3)) if request.method == "POST" and "k_upload" in request.form else 3
    if uploaded:
        generate_clustering_plot(df_upload, K_upload, filename="upload_cluster_plot.png")

    return render_template(
        "clustering.html",
        K=K_default,
        K_upload=K_upload,
        uploaded=uploaded
    )


@app.route("/clustering_upload", methods=["POST"])
def clustering_upload():
    global df_upload

    if df_upload is None:
        flash("Chưa có dữ liệu upload để phân cụm!")
        return redirect(url_for("clustering"))

    K_upload = int(request.form.get("k_upload", 3))
    generate_clustering_plot(df_upload, K_upload, filename="upload_cluster_plot.png")
    generate_clustering_plot(df_default, 3, filename="cluster_plot.png")  # giữ luôn dữ liệu gốc

    return render_template(
        "clustering.html",
        K=3,
        K_upload=K_upload,
        uploaded=True
    )

@app.route("/cluster_table")
def cluster_table():
    df_show = df_upload if df_upload is not None else df_default

    if "Cluster" not in df_show.columns:
        flash("Bạn chưa chạy phân cụm!")
        return redirect(url_for("clustering"))

    cols = ["User_ID", "Product_ID", "Price", "Total_Price", "Cluster"]
    cols = [c for c in cols if c in df_show.columns]

    table = df_show[cols].head(20).to_html(classes="table table-striped")
    return render_template("cluster_table.html", table_html=table)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    global df_upload

    if request.method == "POST":
        f = request.files["file"]

        if f.filename == "":
            flash("Chưa chọn file!")
            return redirect(request.url)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
        f.save(filepath)

        df_new = pd.read_csv(filepath)
        df_upload = preprocess_data(df_new)

        flash("Upload thành công! Dữ liệu mới đã được thêm.")
        return redirect(url_for("home"))

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
