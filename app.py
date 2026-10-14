import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản lý điểm sinh viên", page_icon="📚", layout="wide")

# #1. Tạo dữ liệu 10 sinh viên
du_lieu = {
    "Ho_ten": ["An", "Bình", "Chi", "Dũng", "Hà", "Lan", "Minh", "Nam", "Phúc", "Trang"],
    "Chuyen_can": [9.0, 8.5, 7.0, 9.5, 8.0, 6.5, 9.0, 7.5, 8.0, 9.5],
    "Giua_ky":    [8.0, 9.0, 6.5, 9.0, 7.5, 7.0, 8.5, 8.0, 8.5, 9.0],
    "Cuoi_ky":    [8.5, 8.8, 7.5, 9.2, 8.0, 6.8, 8.7, 7.8, 8.2, 9.5]
}
df = pd.DataFrame(du_lieu)

# #2. Tính điểm tổng kết
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"] +
    0.3 * df["Giua_ky"] +
    0.5 * df["Cuoi_ky"]
).round(2)

# #3. Xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# #4. Tiêu đề và bảng điểm
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Bảng điểm gồm 10 sinh viên, tính theo công thức 20% chuyên cần, 30% giữa kỳ và 50% cuối kỳ.")

bang_hien_thi = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})
st.subheader("Bảng điểm")
st.dataframe(bang_hien_thi, use_container_width=True, hide_index=True)

# #5. Thống kê
diem_tb = df["Tong_ket"].mean()
sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = int((df["Tong_ket"] >= 5).sum())

st.subheader("Thống kê kết quả")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{sv_cao_nhat['Tong_ket']:.2f}", str(sv_cao_nhat["Ho_ten"]))
c3.metric("Điểm thấp nhất", f"{sv_thap_nhat['Tong_ket']:.2f}", str(sv_thap_nhat["Ho_ten"]))
c4.metric("Số sinh viên đạt", f"{so_sv_dat}/{len(df)}")

# #6. Chọn sinh viên và xem điểm chi tiết
st.subheader("Tra cứu điểm theo sinh viên")
ten_chon = st.selectbox("Chọn sinh viên", df["Ho_ten"].tolist())
sv = df.loc[df["Ho_ten"] == ten_chon].iloc[0]
a, b, c, d, e = st.columns(5)
a.metric("Chuyên cần", f"{sv['Chuyen_can']:.2f}")
b.metric("Giữa kỳ", f"{sv['Giua_ky']:.2f}")
c.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.2f}")
d.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
e.metric("Xếp loại", sv["Xep_loai"])

# #7. Biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Ho_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.xticks(rotation=30)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# #8. Thông tin người tạo - hãy thay bằng thông tin thật trước khi nộp
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:12px;'>"
    "Người tạo: [Họ và tên của bạn] | MSSV: [MSSV của bạn]"
    "</div>",
    unsafe_allow_html=True
)
