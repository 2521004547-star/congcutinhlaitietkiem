
import streamlit as st

# CẤU HÌNH TRANG

st.set_page_config(
    page_title="Ứng dụng tính lãi tiết kiệm",
    page_icon="🏦",
    layout="centered"
)

# GIAO DIỆN

st.title("ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM_CAO LÊ ÁNH TUYẾT")
st.write("Nhập thông tin khoản tiền gửi để tính lãi và tổng số tiền nhận được.")

st.divider()

# NHẬP THÔNG TIN

st.subheader("Thông tin gửi tiết kiệm")

with st.form("savings_form"):
    # Số tiền gửi
    so_tien = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=100000.0,
        value=10000000.0,
        step=1000000.0,
        format="%.0f"
    )

    # Kỳ hạn gửi
    ky_han = st.number_input(
        "Kỳ hạn gửi (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

    # Lãi suất năm
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

    # Hình thức nhận lãi
    hinh_thuc = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

    # Nút tính lãi
    submit = st.form_submit_button(
        "TÍNH LÃI TIẾT KIỆM",
        use_container_width=True
    )

# XỬ LÝ VÀ TÍNH TOÁN

if submit:
    # Lãi suất theo tháng (lãi đơn, không nhập lãi vào gốc)
    lai_thang = so_tien * (lai_suat / 100) / 12

    # Tổng tiền lãi trong toàn bộ kỳ hạn
    tong_lai = lai_thang * ky_han

    # Xác định tiền lãi định kỳ và số kỳ nhận lãi
    if hinh_thuc == "Cuối kỳ":
        tien_lai_dinh_ky = tong_lai
        so_ky = 1
        ten_ky = "cuối kỳ"

    elif hinh_thuc == "Hàng tháng":
        tien_lai_dinh_ky = lai_thang
        so_ky = ky_han
        ten_ky = "tháng"

    else:  # Hàng quý
        so_ky = (ky_han + 2) // 3
        tien_lai_dinh_ky = lai_thang * 3
        ten_ky = "quý"

    # Tổng tiền gốc và lãi
    tong_tien = so_tien + tong_lai

    # HIỂN THỊ KẾT QUẢ
  
    st.divider()
    st.subheader("KẾT QUẢ TÍNH LÃI")

    st.success("Đã tính toán thành công!")

    # Định dạng tiền Việt Nam
    def dinh_dang_tien(tien):
        return f"{tien:,.0f} VNĐ"

    # Tiền lãi định kỳ
    st.metric(
        label=f"Tiền lãi mỗi {ten_ky}",
        value=dinh_dang_tien(tien_lai_dinh_ky)
    )

    # Tổng tiền lãi
    st.metric(
        label="Tổng tiền lãi",
        value=dinh_dang_tien(tong_lai)
    )

    # Tổng gốc và lãi
    st.metric(
        label="Tổng tiền gốc và lãi",
        value=dinh_dang_tien(tong_tien)
    )

    # BẢNG TÓM TẮT
    
    st.divider()
    st.subheader("BẢNG TÓM TẮT KHOẢN GỬI")

    st.write(f"**Số tiền gửi:** {dinh_dang_tien(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")
    st.write(f"**Số kỳ nhận lãi:** {so_ky} kỳ")
    st.write(f"**Tổng tiền lãi:** {dinh_dang_tien(tong_lai)}")
    st.write(f"**Tổng gốc và lãi:** {dinh_dang_tien(tong_tien)}")

    # LỊCH NHẬN LÃI
  
    st.divider()
    st.subheader("LỊCH NHẬN LÃI")

    if hinh_thuc == "Cuối kỳ":
        st.write(
            f"Khi đáo hạn sau {ky_han} tháng, "
            f"bạn nhận {dinh_dang_tien(tong_tien)} "
            f"(bao gồm cả gốc và lãi)."
        )
    else:
        import pandas as pd

        lich_nhan_lai = []
        da_nhan = 0
        for i in range(1, so_ky + 1):
            if hinh_thuc == "Hàng tháng":
                so_thang_ky = 1
            else:
                so_thang_ky = min(3, ky_han - (i - 1) * 3)

            tien_lai_ky = lai_thang * so_thang_ky
            da_nhan += tien_lai_ky

            lich_nhan_lai.append({
                "Kỳ nhận lãi": i,
                "Thời điểm": (
                    f"Tháng {i}"
                    if hinh_thuc == "Hàng tháng"
                    else f"Tháng {min(i * 3, ky_han)}"
                ),
                "Tiền lãi (VNĐ)": round(tien_lai_ky),
                "Lũy kế tiền lãi (VNĐ)": round(da_nhan)
            })

        df = pd.DataFrame(lich_nhan_lai)
        st.dataframe(
            df.style.format({
                "Tiền lãi (VNĐ)": "{:,.0f}",
                "Lũy kế tiền lãi (VNĐ)": "{:,.0f}"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.info(
            f"Khi đáo hạn, bạn nhận lại tiền gốc "
            f"{dinh_dang_tien(so_tien)}. "
            f"Tổng lãi đã nhận định kỳ là "
            f"{dinh_dang_tien(tong_lai)}."
        )

    st.caption(
        "Lưu ý: Ứng dụng tính lãi đơn theo số tháng, "
        "giả định lãi suất không đổi, không tái tục và "
        "không cộng lãi vào vốn. Đây là kết quả ước tính, "
        "chưa tính thuế, phí hoặc quy định riêng của ngân hàng."
    )
