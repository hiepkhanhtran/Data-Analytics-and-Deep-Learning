import pandas as pd

# Bước 1: Tải dữ liệu từ file CSV
data = pd.read_csv('dulieuxettuyendaihoc.csv')

# Bước 2: In ra 10 dòng đầu tiên và 10 dòng cuối cùng để kiểm tra dữ liệu
print("10 dòng đầu tiên:")
print(data.head(10))

print("\n10 dòng cuối cùng:")
print(data.tail(10))

# Bước 3: Xác định và phân loại dữ liệu định tính và định lượng
# Dữ liệu định tính:
# - Giới tính (GT), Dân tộc (DT), Khu vực thi (KV), Khối thi (KT)
# Dữ liệu định lượng:
# - Điểm các môn T1, L1, H1, S1, V1, X1, D1, N1 (Lớp 10)
# - Điểm các môn T2, L2, H2, S2, V2, X2, D2, N2 (Lớp 11)
# - Điểm các môn T6, L6, H6, S6, V6, X6, D6, N6 (Lớp 12)
# - Điểm thi đại học: DH1, DH2, DH3

# Bước 4: Thống kê dữ liệu thiếu cho cột 'DT' (Dân tộc) và điền giá trị 0
print("\nThống kê dữ liệu thiếu cho cột Dân tộc (DT):")
print(data['DT'].isnull().sum())

# Thay thế dữ liệu thiếu trong cột 'DT' bằng 0
data['DT'].fillna(0, inplace=True)

# Bước 5: Thống kê và xử lý dữ liệu thiếu cho biến 'T1' và thay thế bằng phương pháp Mean
print("\nThống kê dữ liệu thiếu cho cột T1:")
print(data['T1'].isnull().sum())

# Tính giá trị trung bình của cột T1
mean_T1 = data['T1'].mean()

# Thay thế dữ liệu thiếu trong T1 bằng giá trị trung bình
data['T1'].fillna(mean_T1, inplace=True)

# Bước 6: Xử lý dữ liệu thiếu cho các biến điểm số còn lại (T2, T6, ...)
# Áp dụng thay thế dữ liệu thiếu bằng Mean cho các cột khác
data['T2'].fillna(data['T2'].mean(), inplace=True)
data['L2'].fillna(data['L2'].mean(), inplace=True)
data['H2'].fillna(data['H2'].mean(), inplace=True)
data['S2'].fillna(data['S2'].mean(), inplace=True)
data['V2'].fillna(data['V2'].mean(), inplace=True)
data['X2'].fillna(data['X2'].mean(), inplace=True)
data['D2'].fillna(data['D2'].mean(), inplace=True)
data['N2'].fillna(data['N2'].mean(), inplace=True)

# Tiếp tục cho các cột điểm lớp 12 (T6, L6, H6, ...)
data['T6'].fillna(data['T6'].mean(), inplace=True)
data['L6'].fillna(data['L6'].mean(), inplace=True)
data['H6'].fillna(data['H6'].mean(), inplace=True)
data['S6'].fillna(data['S6'].mean(), inplace=True)
data['V6'].fillna(data['V6'].mean(), inplace=True)
data['X6'].fillna(data['X6'].mean(), inplace=True)
data['D6'].fillna(data['D6'].mean(), inplace=True)
data['N6'].fillna(data['N6'].mean(), inplace=True)

# Bước 7: Tạo các biến TBM1, TBM2, TBM3 (Trung bình môn của các năm lớp 10, 11, 12)
data['TBM1'] = (data['T1']*2 + data['L1'] + data['H1'] + data['S1'] + data['V1']*2 + data['X1'] + data['D1'] + data['N1']) / 10
data['TBM2'] = (data['T2']*2 + data['L2'] + data['H2'] + data['S2'] + data['V2']*2 + data['X2'] + data['D2'] + data['N2']) / 10
data['TBM3'] = (data['T6']*2 + data['L6'] + data['H6'] + data['S6'] + data['V6']*2 + data['X6'] + data['D6'] + data['N6']) / 10

# Bước 8: Xếp loại học sinh theo từng năm học
# Định nghĩa hàm phân loại điểm
def xep_loai(tbm):
    if tbm < 5.0:
        return 'Y'  # yếu
    elif 5.0 <= tbm < 6.5:
        return 'TB'  # trung bình
    elif 6.5 <= tbm < 8.0:
        return 'K'  # khá
    elif 8.0 <= tbm < 9.0:
        return 'G'  # giỏi
    else:
        return 'XS'  # xuất sắc

# Áp dụng hàm phân loại cho các cột TBM1, TBM2, TBM3
data['XL1'] = data['TBM1'].apply(xep_loai)
data['XL2'] = data['TBM2'].apply(xep_loai)
data['XL3'] = data['TBM3'].apply(xep_loai)

# Bước 9: Chuyển điểm trung bình từ thang điểm 10 sang thang điểm 4 (Min-Max Normalization)
def min_max_normalization(value):
    return (value - 0) / (10 - 0) * 4

data['US_TBM1'] = data['TBM1'].apply(min_max_normalization)
data['US_TBM2'] = data['TBM2'].apply(min_max_normalization)
data['US_TBM3'] = data['TBM3'].apply(min_max_normalization)

# Bước 10: Tạo biến kết quả xét tuyển (KQXT)
def ket_qua_xet_tuyen(row):
    if row['KT'] in ['A', 'A1']:
        avg = (row['DH1']*2 + row['DH2'] + row['DH3']) / 4
    elif row['KT'] == 'B':
        avg = (row['DH1'] + row['DH2']*2 + row['DH3']) / 4
    else:
        avg = (row['DH1'] + row['DH2'] + row['DH3']) / 3
    
    return 1 if avg >= 5.0 else 0

data['KQXT'] = data.apply(ket_qua_xet_tuyen, axis=1)

# Bước 11: Lưu dữ liệu đã xử lý xuống file mới
data.to_csv('processed_dulieuxettuyendaihoc.csv', index=False)

print("\nDữ liệu đã được lưu vào file 'processed_dulieuxettuyendaihoc.csv'.")
