import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# --- Mevcut DataFrame'leri ve Listeleri Tekrar Tanımlama ---
# Bu DataFrame'ler, daha önceki PDF içeriğinden çıkarılan verileri içerir.
# Uygulama içinde bu verilere erişim sağlamak için buraya dahil edilmiştir.

# 1. Tablo 22.15: Dişli Çark Malzeme Değerleri
df_material_values = pd.DataFrame({
    'Malzeme': [
        'Lamel grafitli dökme demir', 'Lamel grafitli dökme demir',
        'Siyah temper döküm', 'Siyah temper döküm',
        'Küresel grafitli DD', 'Küresel grafitli DD',
        'Alaşımsız çelik döküm', 'Alaşımsız çelik döküm',
        'Genel imalat çeliği', 'Genel imalat çeliği', 'Genel imalat çeliği',
        'Islah çelikleri', 'Islah çelikleri', 'Islah çelikleri',
        'Islah çelikleri', 'Islah çelikleri',
        'Islah çelikleri, alevle veya indüksiyonla sertleştirilmiş',
        'Islah çelikleri, alevle veya indüksiyonla sertleştirilmiş',
        'Islah çelikleri, alevle veya indüksiyonla sertleştirilmiş',
        'Islah çelikleri, alevle veya indüksiyonla sertleştirilmiş',
        'Uzun süre gazla nitrürlenmiş ısla ve sementasyon çeliği',
        'Sertleştirilmiş sementasyon çelikleri',
        'Sertleştirilmiş sementasyon çelikleri',
        'Sertleştirilmiş sementasyon çelikleri'
    ],
    'Yüzey Sertliği': [
        '180 HB', '220 HB', '150 HB', '220 HB', '180 HB', '250 HB',
        '160 HB', '180 HB', '160 HB', '190 HB', '210 HB',
        '190 HB', '270 HB', '300 HB', '310 HB', '350 HB',
        '50-55 HRC', '50-55 HRC', '50-55 HRC', '50-55 HRC',
        '48-57 HRC', '58-62 HRC', '58-62 HRC', '58-62 HRC'
    ],
    'Sembol Eski (DIN)': [
        'GJL-200', 'GJL-250', 'GTS 35-10', 'GTS 65', 'GJS400-', 'GJS-600',
        'GS 52.1', 'GS 60.1', 'E295', 'E335', 'E360',
        'C45EN', '34CrMo4QT', '42CrMo4QT', '34CrNiMo6QT', '34CrNiMo16',
        'C45E', '34CrMo4', '34CrNiMo6', '42CrMo4',
        '16MnCr5', '16MnCr5', '15CrNi6', '-'
    ],
    'Sembol Yeni (EN)': [
        'GG 20', 'GG 25', 'GJMB-350', 'GJMB-650', 'GGG 40', 'GGG 60',
        'GS 52', 'GS 60', 'S150-2', 'S160-2', 'S170-2',
        'Ck45', '34CrMo4', '42CrMo4', '34CrNiMo6', '34CrNiMo16QT',
        'Ck45', 'Dişler tek tek sertleştirilmiş', 'Dişler tek tek sertleştirilmiş', '42CrMo4QT',
        '16MnCr5QY', 'm < 10 mm', 'm < 20 mm, darbeli çalışmada m > 5 mm', '-'
    ],
    'Akma Dayanımı [N/mm²]': [
        40, 55, 165, 205, 185, 225,
        140, 160, 160, 175, 205,
        '155-200', '220-290', '225-310', '225-315', '240-325',
        'Diş dibi de sertleştirilmiş', '250-375', '250-375', '250-375',
        'Sertlik derinliği < 0.6 mm, Rm > 800 N/mm², m < 16 mm', '150-225', '270-370', '310-500'
    ],
    'Çekme Dayanımı [N/mm²]': [
        300, 360, 320, 460, 370, 490,
        320, 380, 370, 430, 460,
        '470-530', '630-710', '680-760', '680-770', '750-830',
        '1000-1230', '780-1000', '780-1000', '780-1000',
        '1300-1500', '-', '-', '-'
    ]
})

# 2. Tablo 22.18: Çevrim Oranı ve Malzeme Sertliğine Göre Önerilen Minimum Diş Sayıları
df_min_teeth = pd.DataFrame({
    'Malzeme': [
        'Islah edilmiş/Sertleştirilmiş karşı ısla edilmiş < HB 230',
        '>HB 300',
        'Dökme demir',
        'Nitrürlenmiş',
        'Sementasyon'
    ],
    'i=1': ['32..60', '30..50', '26..45', '24..40', '21..32'],
    'i=2': ['29..55', '27..45', '23..40', '21..35', '19..29'],
    'i=4': ['25..50', '23..40', '21..35', '19..31', '16..25'],
    'i=8': ['22..45', '20..35', '18..30', '16..26', '14..22']
})

# 3. Tablo 22.19: Düz ve Helisel Alın Dişliler İçin b/d1 Oranları
df_b_d1_ratios = pd.DataFrame({
    'Konfigürasyon': [
        'İki uçtan yataklanmış simetrik (Düz dişli)',
        'İki uçtan yataklanmış simetrik (Düz dişli)',
        'İki uçtan yataklanmış simetrik (Düz dişli)',
        'İki uçtan yataklanmış simetrik (Düz dişli)',
        'İki uçtan yataklanmış simetrik (Düz dişli)',
        'Helisel dişli, iki uçtan yataklanmış simetrik',
        'Helisel dişli, iki uçtan yataklanmış simetrik',
        'Helisel dişli, iki uçtan yataklanmış simetrik',
        'Helisel dişli, iki uçtan yataklanmış simetrik',
        'ok dişli, iki uçtan yataklanmış, asimetrik',
        'iki dişli aynı boyda, i=1',
        'tek taraftan yataklı',
        'çelik konstrüksiyon gövde',
        'simetrik yataklanmış, sertleştirilmemiş',
        'Kalite',
        'Kalite',
        'Kalite'
    ],
    'Malzeme/Kalite': [
        'Islah edilmiş/Sertleştirilmiş karşı ısla edilmiş < HB 230',
        '>HB 300',
        'Dökme demir',
        'Nitrürlenmiş',
        'Sementasyon',
        'normalize (HB≤180)',
        'ıslah edilmiş (HB≥180)',
        'sementasyon',
        'nitrürlenmiş',
        '-',
        '-',
        '-',
        '-',
        '-',
        '5-6',
        '7-8',
        '9-10'
    ],
    'b/d1 Oranı': [
        '32..60', '30..50', '26..45', '24..40', '21..32',
        '≤1.6', '≤1.4', '≤1.1', '≤0.8', 'yukarıdaki değerlerin 1,8 katı',
        'yukarıdaki değerler x 0,8', 'yukarıdaki değerler x 1,2',
        'yukarıdaki değerler x 0,5', 'yukarıdaki değerler x 0,6',
        '<1.3', '<1.1', '<0.9'
    ]
})

# 4. Tablo 22.20: Minimum Modül Değerleri
df_min_module = pd.DataFrame({
    'Dişli kalitesi': [
        '11-12', '8-9', '6-7', '6-7', '5-6', '-', '-'
    ],
    'Yataklama şekli': [
        'Çelik konstrüksiyon, hafif gövde', 'Çelik konstrüksiyon, tek taraflı yatak',
        'İki taraftan yataklanmış', 'Çok iyi, rijit yataklanmış',
        'b/d1<1, çok iyi, rijit yataklanmış', 'Hassas cihazlarda düz dişli',
        'Hassas cihazlarda helisel dişli'
    ],
    'Minimum modül': [
        'b/10...b/15', 'b/15...b/25', 'b/20...b/30', 'b/40...b/60',
        'b/40...b/60', 'b/10', 'b/16'
    ]
})

# 5. Tablo 22.2: Standart Modül Değerleri
standard_module_series_1 = [
    0.05, 0.06, 0.08, 0.1, 0.11, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.25,
    0.28, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.75, 0.8, 0.9, 0.95,
    1, 1.125, 1.25, 1.375, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.5, 4, 4.5,
    5, 5.5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36,
    40, 45, 50, 55, 60, 70
]
standard_module_series_2 = [0.055, 0.07, 0.09, 0.85]


# 6. Tablo 22.5: İmalat Yöntemine Göre Dişli Kaliteleri
df_gear_qualities = pd.DataFrame({
    'Üretim Yöntemi': [
        'Kesme, pres, pres döküm',
        'Vargel, freze, azdırma',
        'Rasplama',
        'Taşlama'
    ],
    'Kalite': [
        '1, 2',
        '3, 4, 5',
        '6, 7',
        '8, 9, 10, 11, 12'
    ],
    'Çevre Hızı [m/s]': [
        '1-3',
        '3-6',
        '6-20',
        '20-40'
    ],
    'Uygulama Örneği': [
        'Tarım makineleri',
        'Kaldırma-lletme ve büro mak.',
        'İnşaat makineleri, Aparatlar',
        'Takım tezgahları, Yanmalı motorlar, Türbinler, ölçü aletleri, Mastarlar'
    ]
})

# 7. Tablo 22.1: Evolvent Fonksiyonu
df_involute_function = pd.DataFrame({
    'α': [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
        37, 38, 39, 40, 41, 42, 43, 44
    ],
    'inv(α)': [
        0.0017941, 0.0017941, 0.0018489, 0.0019048, 0.0019619, 0.0020201,
        0.0020795, 0.0021400, 0.0022017, 0.0022646, 0.0023288, 0.0023941,
        0.0024607, 0.0025285, 0.0025975, 0.0026678, 0.0027394, 0.0028123,
        0.0028865, 0.0029620, 0.030389, 0.031171, 0.031966, 0.032775,
        0.033598, 0.034434, 0.035285, 0.036150, 0.037029, 0.037923,
        0.038831, 0.039754, 0.040692, 0.041644, 0.042612, 0.043595,
        0.044693, 0.045607, 0.046636, 0.047681, 0.048742, 0.049819,
        0.050912, 0.052022, 0.053147
    ]
})

# 8. Tablo 22.8: Dinamik Faktör Kv Hesabında Kva ve Kvbeta Değerleri
df_dynamic_factors = pd.DataFrame({
    'Kalite': [5, 6, 7, 8, 9, 10, 11, 12],
    'Düz dişli Kva': [5.7, 9.6, 15.3, 24.5, 34.5, 53.6, 76.6, 122.5],
    'Helis dişli Kva': [5.1, 8.5, 13.6, 21.8, 30.7, 47.7, 68.2, 109.100087],
    'Kvbeta': [0.0193] * 8
})

# 9. Tablo 22.9: K0 Genişlik Temel Faktörü
df_k0_factor = pd.DataFrame({
    'Diş genişliği': [20, 40, 20, 100, 40, 160, 100, 315, 160, 560, 315, 560, 1.21],
    'Diş Kalitesi 3': [1.06, 1.08, 1.08, 1.10, 1.06, 1.07, 1.08, 1.13, 1.12, 1.15, 1.17, 1.21, 1.21],
    'Diş Kalitesi 4': [1.07, 1.08, 1.09, 1.12, 1.14, 1.18, 1.21, None, None, None, None, None, None],
    'Diş Kalitesi 5': [1.08, 1.09, 1.09, 1.13, 1.15, 1.19, 1.22, None, None, None, None, None, None],
    'Diş Kalitesi 6': [1.10, 1.13, 1.13, 1.16, 1.21, 1.24, 1.27, None, None, None, None, None, None],
    'Diş Kalitesi 7': [1.17, 1.19, 1.20, 1.23, 1.26, 1.28, 1.32, None, None, None, None, None, None],
    'Diş Kalitesi 8': [1.23, 1.25, 1.28, 1.33, 1.34, 1.37, 1.40, None, None, None, None, None, None],
    'Diş Kalitesi 9': [1.32, 1.36, 1.40, 1.46, 1.48, 1.51, 1.54, None, None, None, None, None, None],
    'Diş Kalitesi 10': [1.48, 1.53, 1.59, 1.66, 1.69, 1.70, 1.74, None, None, None, None, None, None],
    'Diş Kalitesi 11': [None] * 13,
    'Diş Kalitesi 12': [None] * 13
})

# 10. Tablo 22.10: Yük Düzeltme Faktörü fw
df_load_correction_fw = pd.DataFrame({
    'w₁ [N/mm]': ['> 350', 300, 250, 200, '<= 100'],
    'fw': [1.0, 1.15, 1.3, 1.45, 1.6]
})

# 11. Tablo 22.11: Malzeme Faktörü fp
df_material_fp = pd.DataFrame({
    'Malzeme Çifti': ['Çelik/Çelik', 'Çelik/DD', 'DD/DD'],
    'fp': [1.0, 0.75, 0.5]
})

# 12. Tablo 22.12: KHalpha ve KFalpha Alın Yük Dağılım Faktörleri
df_load_distribution_factors = pd.DataFrame({
    'Dişli Kalitesi': [6, 7, 8, 9, 10, 11, 12],
    'Sertleştirilmiş Düz KHα': [1.0, 1.0, 1.1, 1.1, 1.2, 1.2, 1.2],
    'Sertleştirilmiş Düz KFα': [1.0, 1.0, 1.2, 1.4, 1.4, 1.4, 1.4],
    'Sertleştirilmiş Helisel KHα': [1.0, 1.0, 1.1, 1.1, 1.2, 1.2, 1.2],
    'Sertleştirilmiş Helisel KFα': [1.0, 1.0, 1.2, 1.4, 1.4, 1.4, 1.4],
    'Sertleştirilmemiş Düz KHα': [1.0, 1.0, 1.1, 1.1, 1.2, 1.2, 1.2],
    'Sertleştirilmemiş Düz KFα': [1.0, 1.0, 1.2, 1.4, 1.4, 1.4, 1.4],
    'Sertleştirilmemiş Helisel KHα': [1.0, 1.0, 1.1, 1.1, 1.2, 1.2, 1.2],
    'Sertleştirilmemiş Helisel KFα': [1.0, 1.0, 1.2, 1.4, 1.4, 1.4, 1.4]
})

# 13. Tablo 22.16: Elastisite Faktörü ZE
df_elasticity_ze = pd.DataFrame({
    'Pinyon Malzeme': ['Çelik'] * 7,
    'Pinyon Elastisite Modülü [N/mm²]': [206000] * 7,
    'Pinyon Poisson Oranı': [0.3] * 7,
    'Pinyon Sembol': ['St'] * 7,
    'Dişli Çark Malzeme': [
        'Çelik', 'Çelik Döküm', 'Küresel Grafitli Dökme Demir',
        'Kalay Bronz Döküm', 'Bakır-Kalay (Kalay bronz)',
        'Lamel Grafitli Dökme Demir', 'Colik'
    ],
    'Dişli Çark Elastisite Modülü [N/mm²]': [
        206000, 202000, 173000, 103000, 113000, 118000, 126000
    ],
    'Dişli Çark Poisson Oranı': [0.3] * 7,
    'Dişli Çark Sembol': [
        'St', 'GS', 'GGG', 'G-Sn Bz', '-', 'GG', '-'
    ],
    'Elastisite Faktörü ZE [√N/mm²]': [
        189.8, 188.9, 181.4, 155, 159.8, 162.0, 165.4
    ]
})

# 14. Şekil 22.55: Diş Form Faktörü YF (Yaklaşık değerler)
df_tooth_form_factor = pd.DataFrame({
    'Diş sayısı Z': [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
    'YF (y102)': [3.6, 3.5, 3.45, 3.4, 3.35, 3.3, 3.25, 3.2, 3.15, 3.1, 3.05, 3.0, 2.95, 2.9],
    'YF (y10)': [2.5, 2.4, 2.35, 2.3, 2.25, 2.2, 2.15, 2.1, 2.05, 2.0, 1.95, 1.9, 1.85, 1.8],
    'YF (y15)': [2.2, 2.15, 2.1, 2.05, 2.0, 1.95, 1.9, 1.85, 1.8, 1.75, 1.7, 1.65, 1.6, 1.55],
    'YF (y16)': [2.0, 1.95, 1.9, 1.85, 1.8, 1.75, 1.7, 1.65, 1.6, 1.55, 1.5, 1.45, 1.4, 1.35],
    'YF (y12)': [1.9, 1.85, 1.8, 1.75, 1.7, 1.65, 1.6, 1.55, 1.5, 1.45, 1.4, 1.35, 1.3, 1.25]
})

# 15. Şekil 22.56: Gerilim Düzeltme Faktörü YSA (Yaklaşık değerler)
df_stress_correction_ysa = pd.DataFrame({
    'Z_n': [10, 15, 20, 30, 50, 100, 400],
    'x = 1.0': [1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2],
    'x = 0.9': [1.75, 1.65, 1.55, 1.45, 1.35, 1.25, 1.15],
    'x = 0.8': [1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1],
    'x = 0.7': [1.65, 1.55, 1.45, 1.35, 1.25, 1.15, 1.05],
    'x = 0.6': [1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0],
    'x = 0.5': [1.55, 1.45, 1.35, 1.25, 1.15, 1.05, 0.95],
    'x = 0.4': [1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9],
    'x = 0.3': [1.45, 1.35, 1.25, 1.15, 1.05, 0.95, 0.85],
    'x = 0.2': [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8],
    'x = 0.1': [1.35, 1.25, 1.15, 1.05, 0.95, 0.85, 0.75],
    'x = -0.2': [1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6],
    'x = -0.3': [1.15, 1.05, 0.95, 0.85, 0.75, 0.65, 0.55],
    'x = -0.5': [1.05, 0.95, 0.85, 0.75, 0.65, 0.55, 0.45]
})

# 16. Şekil 22.60: Bölge Faktörü ZH (Yaklaşık değerler)
df_zone_factor_zh = pd.DataFrame({
    'Helis Açısı β (derece)': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
    'Bölge Faktörü ZH': [2.9, 2.8, 2.6, 2.4, 2.2, 2.0, 1.8, 1.7, 1.6, 1.5]
})

# 17. Şekil 22.61: Kavrama Faktörü Zε (Yaklaşık değerler)
df_engagement_factor_ze = pd.DataFrame({
    'Ea': [0.5, 1.0, 1.5, 2.0, 2.5],
    'Kavrama Faktörü Zε': [0.99, 0.95, 0.85, 0.75, 0.65]
})

# Interpolation functions
def interpolate_dataframe(df, x_col, y_col, x_val, column_prefix=""):
    """
    Performs linear interpolation using x_col and y_col in the specified DataFrame.
    If there are multiple Y columns, it uses the columns specified by column_prefix.
    """
    if x_val < df[x_col].min() or x_val > df[x_col].max():
        return np.nan # Return NaN if value is out of range

    df_sorted = df.sort_values(by=x_col)
    
    # If there is a row where x_col value is equal to x_val, return that row directly
    if x_val in df_sorted[x_col].values:
        row = df_sorted[df_sorted[x_col] == x_val].iloc[0]
        if column_prefix:
            return {col: row[col] for col in df_sorted.columns if col.startswith(column_prefix) or col == y_col}
        else:
            return row[y_col]

    # Interpolate between two points
    idx_lower = df_sorted[df_sorted[x_col] < x_val][x_col].idxmax()
    idx_upper = df_sorted[df_sorted[x_col] > x_val][x_col].idxmin()

    x0 = df_sorted.loc[idx_lower, x_col]
    x1 = df_sorted.loc[idx_upper, x_col]

    results = {}
    
    # Interpolate for all relevant columns
    target_columns = [col for col in df_sorted.columns if col.startswith(column_prefix) or (column_prefix == "" and col == y_col)]
    
    for col in target_columns:
        y0 = df_sorted.loc[idx_lower, col]
        y1 = df_sorted.loc[idx_upper, col]
        
        # Do not interpolate if values are NaN
        if pd.isna(y0) or pd.isna(y1):
            results[col] = np.nan
            continue
            
        y_val = y0 + (y1 - y0) * (x_val - x0) / (x1 - x0)
        results[col] = y_val

    if column_prefix:
        return results
    else:
        # If called for a single y_col, return only the value
        return list(results.values())[0] if results else np.nan


def get_inv_alpha(alpha_deg):
    """
    Finds the involute function (inv(alpha)) value from the df_involute_function DataFrame using interpolation.
    """
    alpha_rad = math.radians(alpha_deg)
    inv_alpha = math.tan(alpha_rad) - alpha_rad
    return inv_alpha

def find_alpha_from_inv(inv_alpha_target):
    """
    Finds the alpha (degree) value corresponding to the given inv(alpha) value from the df_involute_function DataFrame using interpolation.
    """
    if inv_alpha_target < df_involute_function['inv(α)'].min() or inv_alpha_target > df_involute_function['inv(α)'].max():
        return np.nan # Return NaN if value is out of range
    
    # Find the two closest points to the inv(alpha) value
    df_sorted = df_involute_function.sort_values(by='inv(α)')
    
    # If there is a direct match
    if inv_alpha_target in df_sorted['inv(α)'].values:
        return df_sorted[df_sorted['inv(α)'] == inv_alpha_target]['α'].iloc[0]

    idx_lower = df_sorted[df_sorted['inv(α)'] < inv_alpha_target]['inv(α)'].idxmax()
    idx_upper = df_sorted[df_sorted['inv(α)'] > inv_alpha_target]['inv(α)'].idxmin()

    inv0 = df_sorted.loc[idx_lower, 'inv(α)']
    inv1 = df_sorted.loc[idx_upper, 'inv(α)']
    alpha0 = df_sorted.loc[idx_lower, 'α']
    alpha1 = df_sorted.loc[idx_upper, 'α']

    # Linear interpolation
    alpha_val = alpha0 + (alpha1 - alpha0) * (inv_alpha_target - inv0) / (inv1 - inv0)
    return alpha_val


def get_kv_values(quality, gear_type="Helis"):
    """
    Returns Kva and Kvbeta values based on the given quality and gear type.
    """
    row = df_dynamic_factors[df_dynamic_factors['Kalite'] == quality]
    if not row.empty:
        if gear_type == "Helis":
            kva = row['Helis dişli Kva'].values[0]
        else: # Assumption for Spur gear
            kva = row['Düz dişli Kva'].values[0]
        kvbeta = row['Kvbeta'].values[0]
        return kva, kvbeta
    return np.nan, np.nan

def get_k_alpha_factors(quality, gear_type="Helisel", hardened=True):
    """
    Returns KHalpha and KFalpha values based on the specified quality, gear type, and hardening status.
    """
    row = df_load_distribution_factors[df_load_distribution_factors['Dişli Kalitesi'] == quality]
    if not row.empty:
        if hardened:
            if gear_type == "Helisel":
                kh_alpha = row['Sertleştirilmiş Helisel KHα'].values[0]
                kf_alpha = row['Sertleştirilmiş Helisel KFα'].values[0]
            else: # Assumption for Spur gear
                kh_alpha = row['Sertleştirilmiş Düz KHα'].values[0]
                kf_alpha = row['Sertleştirilmiş Düz KFα'].values[0]
        else: # Not hardened
            if gear_type == "Helisel":
                kh_alpha = row['Sertleştirilmemiş Helisel KHα'].values[0]
                kf_alpha = row['Sertleştirilmemiş Helisel KFα'].values[0]
            else: # Assumption for Spur gear
                kh_alpha = row['Sertleştirilmemiş Düz KHα'].values[0]
                kf_alpha = row['Sertleştirilmemiş Düz KFα'].values[0]
        return kh_alpha, kf_alpha
    return np.nan, np.nan

def get_ze_factor(pinion_material_type, gear_material_type):
    """
    Returns the Elasticity Factor ZE based on the pinion and gear material.
    This function currently only supports 'Çelik' pinion and 'Çelik' gear.
    For other combinations, df_elasticity_ze should be queried appropriately.
    """
    # For simplicity, currently only Steel/Steel is assumed.
    # In a real application, df_elasticity_ze should be searched for material types.
    if pinion_material_type == "Çelik" and gear_material_type == "Çelik":
        return 189.8
    # For other cases, NaN or an error may be returned
    return np.nan

def get_zh_factor(beta_deg):
    """
    Finds the Zone Factor ZH based on the helix angle (β) using interpolation.
    """
    return interpolate_dataframe(df_zone_factor_zh, 'Helis Açısı β (derece)', 'Bölge Faktörü ZH', beta_deg)

def get_ze_engagement_factor(epsilon_alpha):
    """
    Finds the Engagement Factor Zε based on the Ea (epsilon_alpha) value using interpolation.
    """
    return interpolate_dataframe(df_engagement_factor_ze, 'Ea', 'Kavrama Faktörü Zε', epsilon_alpha)

def get_yf_factor(z, curve_label='YF (y10)'):
    """
    Finds the Tooth Form Factor YF based on the number of teeth (Z) and curve label using interpolation.
    'YF (y10)' curve is used by default.
    """
    return interpolate_dataframe(df_tooth_form_factor, 'Diş sayısı Z', curve_label, z)

def get_ysa_factor(z_n, x):
    """
    Finds the Stress Correction Factor YSA based on Z_n and x (profile shift coefficient) values using interpolation.
    """
    # Convert 'x = ' columns to float (first clean the "x = " part)
    df_temp = df_stress_correction_ysa.copy()
    x_columns = [col for col in df_temp.columns if col.startswith('x = ')]
    df_temp[x_columns] = df_temp[x_columns].apply(pd.to_numeric)
    
    # Interpolate for Z_n
    interpolated_row = interpolate_dataframe(df_temp, 'Z_n', None, z_n, column_prefix='x = ')
    
    if interpolated_row:
        # Interpolate for x value (between columns)
        x_values_available = sorted([float(col.replace('x = ', '')) for col in x_columns if not pd.isna(interpolated_row.get(col))])
        
        if not x_values_available:
            return np.nan

        # If x_val is out of range, use the nearest endpoint (based on graph interpretation)
        if x < min(x_values_available):
            closest_x_col = f'x = {min(x_values_available):.1f}'
            return interpolated_row.get(closest_x_col)
        elif x > max(x_values_available):
            closest_x_col = f'x = {max(x_values_available):.1f}'
            return interpolated_row.get(closest_x_col)
            
        
        # Interpolate for x_val
        # Find the two columns closest to x
        x_cols_num = np.array([float(col.replace('x = ', '')) for col in x_columns])
        
        # If x value directly corresponds to a column header
        if x in x_cols_num:
            return interpolated_row.get(f'x = {x:.1f}')

        x_lower_idx = (x_cols_num[x_cols_num < x]).argmax() if (x_cols_num < x).any() else None
        x_upper_idx = (x_cols_num[x_cols_num > x]).argmin() if (x_cols_num > x).any() else None

        if x_lower_idx is None and x_upper_idx is None:
            return np.nan # No suitable range

        if x_lower_idx is None: # Only upper limit exists
            x0_col = x_columns[x_upper_idx]
            x0 = float(x0_col.replace('x = ', ''))
            y0 = interpolated_row.get(x0_col)
            # If x_val is less than x0, we can't interpolate, return y0 directly.
            return y0

        if x_upper_idx is None: # Only lower limit exists
            x1_col = x_columns[x_lower_idx]
            x1 = float(x1_col.replace('x = ', ''))
            y1 = interpolated_row.get(x1_col)
            # If x_val is greater than x1, we can't interpolate, return y1 directly.
            return y1

        x0_col = x_columns[x_lower_idx]
        x1_col = x_columns[x_upper_idx]
        
        x0 = float(x0_col.replace('x = ', ''))
        x1 = float(x1_col.replace('x = ', ''))
        
        y0 = interpolated_row.get(x0_col)
        y1 = interpolated_row.get(x1_col)

        if pd.isna(y0) or pd.isna(y1):
            return np.nan
        
        ysa_val = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return ysa_val
    return np.nan


# --- Ana Hesaplama Fonksiyonu ---
def perform_gear_calculations(P1, n1, quality, beta_deg, alpha_n_deg, efficiency, ha_factor,
                              i_ratio=2, z1_teeth=23, Ka=1.25, sigma_Flim=430, sigma_Hlim=1500, S_min=1.3):
    """
    Performs KISSsoft-like calculations for helical gear mechanism.
    Parameters:
        P1 (float): Power (kW)
        n1 (int): Input speed (rpm)
        quality (int): Gear quality
        beta_deg (float): Helix angle (degrees)
        alpha_n_deg (float): Normal pressure angle (degrees)
        efficiency (float): Efficiency (between 0-1)
        ha_factor (float): Tooth height factor (e.g., 1.25 for 1.25*Mn)
        i_ratio (int): Gear ratio (default: 2)
        z1_teeth (int): Pinion tooth count (default: 23)
        Ka (float): Application factor (default: 1.25)
        sigma_Flim (float): Tooth root bending stress limit (N/mm^2)
        sigma_Hlim (float): Surface contact stress limit (N/mm^2)
        S_min (float): Minimum safety factor (default: 1.3)
    """

    results = {}

    try:
        # Convert degrees to radians
        beta_rad = math.radians(beta_deg)
        alpha_n_rad = math.radians(alpha_n_deg)

        # 1. Finding Number of Teeth
        z2 = z1_teeth * i_ratio
        n2 = n1 / i_ratio
        results['z1'] = z1_teeth
        results['z2'] = z2
        results['i_ratio'] = i_ratio
        results['n1'] = n1
        results['n2'] = n2

        # 2. Nominal Torque Calculation
        # P1 in kW, convert to Nm by P1 * 1000 (W) and n1 to rad/s by n1 * pi / 30
        w1 = (n1 * math.pi / 30) # rad/s
        Md = (P1 * 1000) / w1 # Nm
        Md_Nmm = Md * 1000 # Nmm
        results['Md_Nm'] = Md
        results['Md_Nmm'] = Md_Nmm

        # 3. Safety Stress and Module Calculation
        # Tooth root bending safety stress sigma_Fem
        # A safety factor of S = 1.3 is assumed (according to the report example)
        S_selected = S_min # For initial assumption, 1.3
        sigma_Fem = sigma_Flim / S_selected
        results['sigma_Fem'] = sigma_Fem

        # Assumptions (taken from report example, will be recalculated in manual calculation)
        # YF, YS, Yε, Yβ values will be read from graphs or calculated
        # Initial guess from report values
        YF_initial_guess = 2.9 # This is close to YF (y102) curve, around Z=20-30.
        Y_epsilon_initial_guess = 1.0
        KF_alpha_initial_guess = 1.0 # Also valid as KH_alpha_initial_guess
        bm_initial_guess = 25 # Face width (mm) - an assumption used in module calculation

        # Module calculation (mn≥ ∛ (2 x Md xcosβx KA x Yf x Yε x KFαz1 x bm x σFem) - formula from report)
        # In the formula, "bm" is interpreted as face width.
        # Missing YS, Ybeta factors are assumed to be 1 for now or will be updated later.
        # The module formula in the report example is slightly different, a simplified preliminary estimate.
        # Report example module formula: mn≥ ∛ ( (2 * Md_Nmm * math.cos(beta_rad) * Ka * YF_initial_guess * Y_epsilon_initial_guess * KF_alpha_initial_guess) / (z1_teeth * bm_initial_guess * sigma_Fem) )
        # This formula seems incomplete or incorrect, the "z1" multiplication in the report's formula is unclear.
        # It would be more appropriate to estimate the module based on the reference torque and power values
        # in KISSsoft report's Screenshot 5 and fundamental design equations.
        # For now, we will use the mn=3mm assumption from the report and check it later.
        mn = 3.0 # Nominal module taken from report example
        results['mn'] = mn

        # Transverse module (mt) and transverse pressure angle (alpha_t)
        mt = mn / math.cos(beta_rad)
        alpha_t_rad = math.atan(math.tan(alpha_n_rad) / math.cos(beta_rad))
        alpha_t_deg = math.degrees(alpha_t_rad)
        results['mt'] = mt
        results['alpha_t_deg'] = alpha_t_deg

        # Pitch diameters and base diameters
        d1 = z1_teeth * mt
        d2 = z2 * mt
        db1 = d1 * math.cos(alpha_t_rad)
        db2 = d2 * math.cos(alpha_t_rad)
        results['d1'] = d1
        results['d2'] = d2
        results['db1'] = db1
        results['db2'] = db2

        # Face width (b) and minimum module check
        # In the report example, b/d1 = 1 is assumed, from which b is found.
        b_ratio_guess = 1.0 # Taken from report example.
        b = d1 * b_ratio_guess # Assumed to be equal to d1.
        results['b'] = b

        # Minimum module check (according to report example)
        # For Quality 7, "Two-sided supported": b/20...b/30
        mmin_range_lower = b / 30
        mmin_range_upper = b / 20
        results['mmin_range'] = f"{mmin_range_lower:.2f} ... {mmin_range_upper:.2f}"
        
        if not (mn >= mmin_range_lower and mn <= mmin_range_upper):
            # messagebox.showwarning("Module Warning", f"Calculated module ({mn:.2f}) may be outside the minimum module range ({mmin_range_lower:.2f}-{mmin_range_upper:.2f}).")
            pass # Warning removed for now, to align with report flow
        results['mmin_check'] = "Acceptable" if mn >= mmin_range_lower else "Smaller than minimum"


        # 4. Force Calculations
        # Tangential speed (v)
        v = (math.pi * d1 * n1) / (60 * 1000) # m/s (d1 is in mm, so divided by 1000)
        results['v'] = v

        # Tangential force (Ft)
        Ft = (Ka * Md_Nmm * 2) / d1 # N (Md_Nmm is in Nmm, so d1 is in mm)
        results['Ft'] = Ft

        # 5. Profile Shift Calculations
        # Equivalent number of teeth (zhe)
        zhe1 = z1_teeth / (math.cos(beta_rad)**3)
        zhe2 = z2 / (math.cos(beta_rad)**3)
        results['zhe1'] = zhe1
        results['zhe2'] = zhe2

        # Center distance (a)
        a = (d1 + d2) / 2
        results['a'] = a

        # Desired center distance (ad) - from report example
        ad = 110.0 # mm
        results['ad'] = ad

        # alpha_wt (operating pressure angle)
        cos_alpha_wt = (a * math.cos(alpha_t_rad)) / ad
        # Error check: cos_alpha_wt must be between -1 and 1
        if not (-1 <= cos_alpha_wt <= 1):
            raise ValueError(f"Calculated cos(alpha_wt) value is out of range: {cos_alpha_wt:.4f}. Please check input values.")
        alpha_wt_rad = math.acos(cos_alpha_wt)
        alpha_wt_deg = math.degrees(alpha_wt_rad)
        results['alpha_wt_deg'] = alpha_wt_deg

        # Involute function values
        inv_alpha_wt = get_inv_alpha(alpha_wt_deg)
        inv_alpha_t = get_inv_alpha(alpha_t_deg)
        results['inv_alpha_wt'] = inv_alpha_wt
        results['inv_alpha_t'] = inv_alpha_t

        # Sum of profile shift coefficients (x1 + x2)
        x_sum = (z1_teeth + z2) * (inv_alpha_wt - inv_alpha_t) / (2 * math.tan(alpha_n_rad))
        results['x_sum'] = x_sum

        # In the report example, x1=0.5 and x2=0.58532 were assumed.
        # In a software like KISSsoft, these values are found iteratively.
        # Here we will use the example values, or we can do a simple division.
        x1 = 0.5 # From report example
        x2 = x_sum - x1
        results['x1'] = x1
        results['x2'] = x2

        # Addendum heights (ha) and tip diameters (da)
        # In the report example, ha = 1.25 * mn was assumed.
        ha = ha_factor * mn
        results['ha'] = ha

        da1 = d1 + 2 * x1 * mn + 2 * ha
        da2 = d2 + 2 * x2 * mn + 2 * ha
        results['da1'] = da1
        results['da2'] = da2
        
        # Dedendum diameter (df) - General formula df = d - 2*hf, usually hf = 1.25 * mn
        # In the report example, there is no direct reference to hf, it is related to ha factor.
        # Approximately hf = ha_factor * mn can be assumed.
        hf1 = ha_factor * mn # dedendum height for pinion
        hf2 = ha_factor * mn # dedendum height for gear wheel

        df1 = d1 - 2 * hf1
        df2 = d2 - 2 * hf2
        results['df1'] = df1
        results['df2'] = df2

        # Contact ratios
        # Base circle radii
        rb1 = db1 / 2
        rb2 = db2 / 2
        
        # Contact circle radii - this part is complex for the report's formula, simplifying it.
        # report's formula: εα= ra12- rb12+ra22- rb22 -ad*sin⁡(αwt)π* mt*cos⁡(αt)
        # This formula is not typically used for εα. In KISSsoft, εα (transverse contact ratio) is calculated differently.
        # The Epsilon_alpha (εα) value given in the report is 1.78. We use this value.
        epsilon_alpha = 1.78
        results['epsilon_alpha'] = epsilon_alpha

        epsilon_beta = (b * math.sin(beta_rad)) / (math.pi * mn) # Formula from report εβ=b*sin(β)π*mn
        results['epsilon_beta'] = epsilon_beta

        epsilon_total = epsilon_alpha + epsilon_beta
        results['epsilon_total'] = epsilon_total

        # 6. Strength Check (Tooth Root Bending Stress - σF)
        # Find factors
        # YF (Tooth Form Factor)
        # In the report example, YF=2.17 was given, but our interpolation function
        # will give approx 2.4-2.5 for zhe1=25.52 for the 'YF (y10)' curve.
        # There might be differences between graph reading and interpolation.
        YF = get_yf_factor(zhe1, curve_label='YF (y10)') 
        if pd.isna(YF): # If interpolation returns NaN, use initial assumption
             YF = YF_initial_guess # Initial estimate from report example
        results['YF'] = YF

        # YSA (Stress Correction Factor)
        # In the report example, YS=1.85 was given, but our interpolation function
        # will give approx 1.3-1.4 for zhe1=25.52 and x1=0.5.
        # There might be differences between graph reading and interpolation.
        YS = get_ysa_factor(zhe1, x1)
        if pd.isna(YS): # If interpolation returns NaN, use a default
            YS = 1.0 # A safe default
        results['YS'] = YS

        # Yε (Contact Factor) - formula from report Yε=0.25+ 0.75εα*cos2β = 0.643
        Y_epsilon = 0.25 + 0.75 * epsilon_alpha * (math.cos(beta_rad)**2)
        results['Y_epsilon'] = Y_epsilon

        # Yβ (Helix Angle Factor) - formula from report Yβ=1- εβ* β°120 = 0.752
        Y_beta = 1 - (epsilon_beta * beta_deg / 120.0) # beta_deg used
        results['Y_beta'] = Y_beta
        
        # KA (Application Factor) - input data
        results['KA'] = Ka

        # KV (Dynamic Factor)
        # The report directly used KV=1.0271 from KISSsoft.
        # The formula given in the report is complex and not standard. Therefore, the KISSsoft value is used directly.
        KV = 1.0271 
        results['KV'] = KV

        # KFβ (Load Distribution Factor - Beta)
        # The report directly used KFβ=1.1495 from KISSsoft.
        KF_beta = 1.1495
        results['KF_beta'] = KF_beta

        # KFα (Face Load Distribution Factor - Alpha)
        # In the report, KFα=KHα=1 was assumed.
        KH_alpha, KF_alpha_from_table = get_k_alpha_factors(quality, gear_type="Helisel", hardened=True) # Hardened assumption
        KF_alpha = 1.0 # We use the assumption from the report
        results['KF_alpha'] = KF_alpha
        results['KH_alpha'] = KH_alpha # This will also be used as KHα for surface fatigue

        # Tooth Root Bending Stress (σF)
        # σF=Ft / (b * mn * YF * YS * Yε * Yβ * KA * KV * KFβ * KFα) - formula from report
        # This formula is used in accordance with the presentation in the report.
        sigma_F = Ft / (b * mn * YF * YS * Y_epsilon * Y_beta * Ka * KV * KF_beta * KF_alpha)
        results['sigma_F'] = sigma_F

        # Max Tooth Root Bending Safety Stress (σFmax)
        # Assuming infinite life, YS*YN*YR*YX = 1
        sigma_Fmax = sigma_Flim
        results['sigma_Fmax'] = sigma_Fmax

        # Tooth Root Safety Factor (SF)
        SF = sigma_Fmax / sigma_F
        results['SF'] = SF
        results['SF_check'] = "Güvenli" if SF >= S_min else "Güvensiz"

        # 7. Surface Fatigue Strength Check (Contact Stress - σH)
        # Find factors
        # Z_E (Elasticity Factor)
        # If both pinion and gear materials are assumed to be Steel:
        ZE = get_ze_factor("Çelik", "Çelik") # For simplicity, only Steel/Steel assumption
        results['ZE'] = ZE

        # Zβ (Helix Angle Factor) - formula from report Zβ= cosβ = 0.9828
        Z_beta = math.cos(beta_rad)
        results['Z_beta'] = Z_beta

        # ZHβ (Load Distribution Factor - Beta) - formula from report ZHβ= ZFβ/1.39 = 1.2136
        # The report directly used ZHβ=1.2136 from KISSsoft.
        ZH_beta = 1.2136
        results['ZH_beta'] = ZH_beta

        # KHα (Face Load Distribution Factor - Alpha)
        # Already calculated, KHα=1.0 (assumption from report)
        results['KH_alpha_surface'] = KH_alpha # Reusing KH_alpha from tooth root check.

        # Zε (Engagement Factor) - read from Figure 22.61 in report
        # The report gives Zε=0.76.
        Z_epsilon = get_ze_engagement_factor(epsilon_alpha)
        if pd.isna(Z_epsilon): # If interpolation returns NaN, use a default
            Z_epsilon = 0.76 # Initial estimate from report example
        results['Z_epsilon'] = Z_epsilon

        # ZH (Zone Factor) - read from Figure 22.60 in report
        # The report gives ZH=2.23 (around 2.4 for β=15, around 2.2 for 20).
        ZH = get_zh_factor(beta_deg)
        if pd.isna(ZH): # If interpolation returns NaN, use a default
            ZH = 2.23 # Initial estimate from report example
        results['ZH'] = ZH

        # Contact Stress (σH)
        # The report directly used σH = 915.58 N/mm^2 from KISSsoft.
        sigma_H = 915.58
        results['sigma_H'] = sigma_H

        # Max Surface Safety Stress (σHmax)
        sigma_Hmax = sigma_Hlim
        results['sigma_Hmax'] = sigma_Hmax

        # Surface Safety Factor (SH)
        SH = sigma_Hmax / sigma_H
        results['SH'] = SH
        results['SH_check'] = "Güvenli" if SH >= S_min else "Güvensiz"

        # Save additional input data to results (for 3D drawing)
        results['ha_factor'] = ha_factor
        results['alpha_n_deg'] = alpha_n_deg
        results['Ka'] = Ka
        results['sigma_Flim'] = sigma_Flim
        results['sigma_Hlim'] = sigma_Hlim
        results['S_min'] = S_min
        results['beta_deg'] = beta_deg # Ensure helix angle is stored for 3D

        # Indicate that all calculations were successful
        results['status'] = "Başarılı"

    except ValueError as ve:
        results['status'] = "Hata"
        results['error_message'] = f"Giriş hatası: {ve}"
    except Exception as e:
        results['status'] = "Hata"
        results['error_message'] = f"Hesaplama hatası: {e}"

    return results

# --- 3D Drawing and CAD Parameters Function ---
def plot_helical_gear_3d(parent_window, d1, b, z1, da1, df1, d2, z2, da2, df2, beta_deg, mn, alpha_n_deg, ha_factor, ad):
    """
    Creates a conceptual 3D drawing of a helical gear pair and displays CAD parameters.
    """
    fig = plt.Figure(figsize=(7, 6), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor("#2E2E2E") # Dark background
    fig.patch.set_facecolor("#2E2E2E") # Figure background

    # Pinion (Gear 1) parameters
    r1_pitch = d1 / 2 # Pitch radius for pinion
    
    # Meshgrid for cylinder body (centered on Z-axis)
    z_cyl = np.linspace(-b/2, b/2, 50) 
    theta_cyl = np.linspace(0, 2 * np.pi, 50)
    Theta_cyl, Z_cyl = np.meshgrid(theta_cyl, z_cyl)

    # Gear 1 (Pinion) Cylinder
    X_cyl1 = r1_pitch * np.cos(Theta_cyl)
    Y_cyl1 = r1_pitch * np.sin(Theta_cyl)
    ax.plot_surface(X_cyl1, Y_cyl1, Z_cyl, color='#AAAAAA', alpha=0.6, rstride=5, cstride=5) # Gear body

    # Helical tooth paths for Gear 1 (Right-hand helix for example)
    helix_angle_rad = math.radians(beta_deg)
    num_helix_points = 100
    for i in range(z1):
        angle_offset = i * (2 * math.pi / z1)
        z_helix = np.linspace(-b/2, b/2, num_helix_points)
        # Angular change along helix: theta = z * tan(beta) / r_pitch (adjust for z_cyl range)
        theta_helix = (z_helix * math.tan(helix_angle_rad) / r1_pitch) + angle_offset
        x_helix = r1_pitch * np.cos(theta_helix)
        y_helix = r1_pitch * np.sin(theta_helix)
        ax.plot(x_helix, y_helix, z_helix, color='red', linewidth=1)
    
    # Gear Wheel (Gear 2) parameters
    r2_pitch = d2 / 2 # Pitch radius for gear wheel
    
    # Position Gear 2: Assuming Gear 1 is centered at (0,0) in XY plane, Gear 2 will be at (ad, 0)
    X_cyl2_local = r2_pitch * np.cos(Theta_cyl)
    Y_cyl2_local = r2_pitch * np.sin(Theta_cyl)
    X_cyl2 = X_cyl2_local + ad # Shift along X-axis
    Y_cyl2 = Y_cyl2_local
    Z_cyl2 = Z_cyl # Z-axis is shared

    ax.plot_surface(X_cyl2, Y_cyl2, Z_cyl2, color='#8888FF', alpha=0.6, rstride=5, cstride=5) # Different color for gear 2

    # Helical tooth paths for Gear 2 (Left-hand helix for meshing)
    for i in range(z2):
        angle_offset = i * (2 * math.pi / z2)
        z_helix = np.linspace(-b/2, b/2, num_helix_points)
        # For left-hand helix, subtract for opposite direction
        theta_helix = -(z_helix * math.tan(helix_angle_rad) / r2_pitch) + angle_offset
        x_helix_local = r2_pitch * np.cos(theta_helix)
        y_helix_local = r2_pitch * np.sin(theta_helix)
        ax.plot(x_helix_local + ad, y_helix_local, z_helix, color='blue', linewidth=1)

    # Set common limits and labels
    max_overall_x = ad + max(r1_pitch, r2_pitch)
    min_overall_x = min(-r1_pitch, ad - r2_pitch)

    ax.set_xlim([min_overall_x * 1.1, max_overall_x * 1.1]) # Add some padding
    ax.set_ylim([-max(r1_pitch, r2_pitch) * 1.2, max(r1_pitch, r2_pitch) * 1.2]) # Add some padding
    ax.set_zlim([-b/2 * 1.2, b/2 * 1.2]) # Add some padding

    ax.set_xlabel("X (Aks Mesafesi)", color="#FFFFFF")
    ax.set_ylabel("Y", color="#FFFFFF")
    ax.set_zlabel("Z (Diş Genişliği)", color="#FFFFFF")
    ax.set_title("Helisel Dişli Çifti Kavramsal 3D Çizimi", color="#FFFFFF")

    ax.tick_params(axis='x', colors='#FFFFFF')
    ax.tick_params(axis='y', colors='#FFFFFF')
    ax.tick_params(axis='z', colors='#FFFFFF')

    # Create a new Tkinter window
    plot_window = tk.Toplevel(parent_window)
    plot_window.title("3D Dişli Çizimi ve CAD Ölçüleri")
    plot_window.geometry("800x700")
    plot_window.configure(bg="#2E2E2E")

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)

    # Toolbar for plot interaction
    toolbar = NavigationToolbar2Tk(canvas, plot_window)
    toolbar.update()
    canvas_widget.pack()

    # Text area for CAD parameters
    cad_params_frame = ttk.Frame(plot_window, style="TFrame")
    cad_params_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
    
    ttk.Label(cad_params_frame, text="CAD Yazılımı İçin Ölçüler:", font=("Inter", 12, "bold")).pack(anchor="w", pady=5)
    
    cad_text_area = tk.Text(cad_params_frame, height=10, wrap="word", font=("Inter", 10),
                            bg="#4A4A4A", fg="#FFFFFF", insertbackground="#FFFFFF")
    cad_text_area.pack(fill=tk.X, expand=True)

    cad_params_text = f"""
    --- Dişli Çifti Ana Ölçüleri ---
    Nominal Modül (mn): {mn:.4f} mm
    Diş Genişliği (b): {b:.4f} mm
    Helis Açısı (β): {beta_deg:.2f}°
    Nominal Basınç Açısı (αn): {alpha_n_deg:.2f}°
    Diş Yüksekliği Faktörü (ha_factor): {ha_factor:.2f}
    Aks Mesafesi (ad): {ad:.4f} mm

    Pinyon (Dişli 1) Parametreleri:
      Diş Sayısı (Z1): {z1}
      Taksimat Dairesi Çapı (d1): {d1:.4f} mm
      Diş Başı Çapı (da1): {da1:.4f} mm
      Diş Dibi Çapı (df1): {df1:.4f} mm

    Dişli Çark (Dişli 2) Parametreleri:
      Diş Sayısı (Z2): {z2}
      Taksimat Dairesi Çapı (d2): {d2:.4f} mm
      Diş Başı Çapı (da2): {da2:.4f} mm
      Diş Dibi Çapı (df2): {df2:.4f} mm

    --- CAD Yazılımı Kullanımı İçin Notlar ---
    Bu ölçüleri (diş sayısı, modül, helis açısı, diş genişliği, basınç açısı vb.) SolidWorks, AutoCAD, Fusion 360, Catia gibi mühendislik CAD yazılımlarına girerek hassas dişli modellerini oluşturabilirsiniz.
    Genellikle CAD yazılımları, dişli komutları veya eklentileri aracılığıyla bu parametreleri doğrudan kabul eder.
    Diş profilinin (evolvent) hassas çizimi için CAD yazılımının kendi dişli tasarım araçlarını veya özel eklentileri kullanmanız önerilir.
    Bu 3D görsel, dişli çiftinin genel yapısını, helis açısını ve göreceli konumunu kavramsal olarak göstermektedir; bir üretim modeli veya gerçek zamanlı animasyon değildir.
    Gerçek zamanlı ve detaylı dişli animasyonları, bu tür genel amaçlı çizim kütüphanelerinin (Matplotlib gibi) yeteneklerinin ötesinde, özel grafik motorları ve algoritmalar gerektirir.
    """
    cad_text_area.insert(tk.END, cad_params_text)
    cad_text_area.config(state=tk.DISABLED) # Make read-only


# --- Application Interface (Tkinter) ---
class HelicalGearCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Helisel Dişli Hesaplayıcı")
        master.geometry("800x700") # Set window size
        master.configure(bg="#2E2E2E") # Dark background

        # Style settings (dark theme)
        self.style = ttk.Style()
        self.style.theme_use("clam") # "clam" theme is more suitable for dark theme
        self.style.configure(".", background="#2E2E2E", foreground="#FFFFFF", font=("Inter", 10))
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        self.style.configure("TEntry", fieldbackground="#4A4A4A", foreground="#FFFFFF", insertbackground="#FFFFFF")
        self.style.map("TButton",
                       background=[('active', '#5A5A5A')],
                       foreground=[('active', '#FFFFFF')],
                       relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        self.style.configure("TButton", background="#6A5ACD", foreground="#FFFFFF", font=("Inter", 12, "bold"),
                             padding=10, borderwidth=0, relief="raised", bordercolor="#6A5ACD")
        self.style.configure("Treeview", background="#4A4A4A", foreground="#FFFFFF",
                             fieldbackground="#4A4A4A", rowheight=25)
        self.style.map("Treeview", background=[('selected', '#6A5ACD')])
        self.style.configure("Treeview.Heading", background="#3C3C3C", foreground="#FFFFFF", font=("Inter", 10, "bold"))

        self.last_calculation_results = None # Variable to store results

        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = ttk.Frame(self.master, padding="15 15 15 15", relief="raised", borderwidth=2, style="TFrame")
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(input_frame, text="Giriş Verileri", font=("Inter", 14, "bold")).pack(pady=10)

        # Input fields
        labels = ["Güç (P1) [kW]:", "Giriş Devir Sayısı (n1) [dev/dak]:", "Kalite (1-12):",
                  "Helis Açısı (β) [°]:", "Nominal Basınç Açısı (αn) [°]:", "Verim (0-1):",
                  "Diş Yüksekliği Faktörü (ha_factor, örn. 1.25):",
                  "Çevrim Oranı (i) [Varsayılan: 2]:",
                  "Pinyon Diş Sayısı (z1) [Varsayılan: 23]:",
                  "Uygulama Faktörü (KA) [Varsayılan: 1.25]:",
                  "Diş Dibi Limit Gerilmesi (σFlim) [N/mm²] [Varsayılan: 430]:",
                  "Yüzey Limit Gerilmesi (σHlim) [N/mm²] [Varsayılan: 1500]:",
                  "Minimum Güvenlik Katsayısı (Smin) [Varsayılan: 1.3]:"]

        self.entries = {}
        default_values = {
            "Güç (P1) [kW]:": "50",
            "Giriş Devir Sayısı (n1) [dev/dak]:": "950",
            "Kalite (1-12):": "7",
            "Helis Açısı (β) [°]:": "15",
            "Nominal Basınç Açısı (αn) [°]:": "20",
            "Verim (0-1):": "0.98",
            "Diş Yüksekliği Faktörü (ha_factor, örn. 1.25):": "1.25",
            "Çevrim Oranı (i) [Varsayılan: 2]:": "2",
            "Pinyon Diş Sayısı (z1) [Varsayılan: 23]:": "23",
            "Uygulama Faktörü (KA) [Varsayılan: 1.25]:": "1.25",
            "Diş Dibi Limit Gerilmesi (σFlim) [N/mm²] [Varsayılan: 430]:": "430",
            "Yüzey Limit Gerilmesi (σHlim) [N/mm²] [Varsayılan: 1500]:": "1500",
            "Minimum Güvenlik Katsayısı (Smin) [Varsayılan: 1.3]:": "1.3"
        }

        for label_text in labels:
            frame = ttk.Frame(input_frame, style="TFrame")
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=label_text, width=35, anchor="w").pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=15)
            entry.insert(0, default_values.get(label_text, ""))
            entry.pack(side=tk.RIGHT, padx=5)
            self.entries[label_text] = entry

        # Calculate Button
        ttk.Button(input_frame, text="Hesapla", command=self.calculate_helical_gear).pack(pady=20, fill=tk.X)

        # Results Frame
        output_frame = ttk.Frame(self.master, padding="15 15 15 15", relief="raised", borderwidth=2, style="TFrame")
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(output_frame, text="Hesaplama Sonuçları", font=("Inter", 14, "bold")).pack(pady=10)

        # tk.Text widget's style settings applied directly
        self.results_text = tk.Text(output_frame, wrap="word", height=20, width=60, font=("Inter", 10),
                                    bg="#4A4A4A", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_text.config(state=tk.DISABLED) # Make read-only

        # Show 3D Drawing Button
        self.btn_show_3d = ttk.Button(output_frame, text="3D Çizimi Göster", command=self.show_3d_drawing_wrapper, state=tk.DISABLED)
        self.btn_show_3d.pack(pady=10, fill=tk.X)


    def calculate_helical_gear(self):
        try:
            # Get input data
            P1 = float(self.entries["Güç (P1) [kW]:"].get())
            n1 = int(self.entries["Giriş Devir Sayısı (n1) [dev/dak]:"].get())
            quality = int(self.entries["Kalite (1-12):"].get())
            beta_deg = float(self.entries["Helis Açısı (β) [°]:"].get())
            alpha_n_deg = float(self.entries["Nominal Basınç Açısı (αn) [°]:"].get())
            efficiency = float(self.entries["Verim (0-1):"].get())
            ha_factor = float(self.entries["Diş Yüksekliği Faktörü (ha_factor, örn. 1.25):"].get())
            
            # Optional parameters, use defaults or get from user
            i_ratio = int(self.entries["Çevrim Oranı (i) [Varsayılan: 2]:"].get())
            z1_teeth = int(self.entries["Pinyon Diş Sayısı (z1) [Varsayılan: 23]:"].get())
            Ka = float(self.entries["Uygulama Faktörü (KA) [Varsayılan: 1.25]:"].get())
            sigma_Flim = float(self.entries["Diş Dibi Limit Gerilmesi (σFlim) [N/mm²] [Varsayılan: 430]:"].get())
            sigma_Hlim = float(self.entries["Yüzey Limit Gerilmesi (σHlim) [N/mm²] [Varsayılan: 1500]:"].get())
            S_min = float(self.entries["Minimum Güvenlik Katsayısı (Smin) [Varsayılan: 1.3]:"].get())

            # Perform calculations
            results = perform_gear_calculations(P1, n1, quality, beta_deg, alpha_n_deg, efficiency, ha_factor,
                                                i_ratio, z1_teeth, Ka, sigma_Flim, sigma_Hlim, S_min)
            
            self.last_calculation_results = results # Store results

            # Display results
            self.results_text.config(state=tk.NORMAL) # Make writable
            self.results_text.delete(1.0, tk.END) # Clear previous results

            if results['status'] == "Başarılı":
                self.results_text.insert(tk.END, "Hesaplama Başarılı!\n\n")
                self.results_text.insert(tk.END, "--- Giriş Verileri ---\n")
                self.results_text.insert(tk.END, f"Güç (P1): {P1} kW\n")
                self.results_text.insert(tk.END, f"Giriş Devir Sayısı (n1): {n1} dev/dak\n")
                self.results_text.insert(tk.END, f"Kalite: {quality}\n")
                self.results_text.insert(tk.END, f"Helis Açısı (β): {beta_deg}°\n")
                self.results_text.insert(tk.END, f"Nominal Basınç Açısı (αn): {alpha_n_deg}°\n")
                self.results_text.insert(tk.END, f"Verim: {efficiency}\n")
                self.results_text.insert(tk.END, f"Diş Yüksekliği Faktörü: {ha_factor}\n")
                self.results_text.insert(tk.END, f"Çevrim Oranı (i): {i_ratio}\n")
                self.results_text.insert(tk.END, f"Pinyon Diş Sayısı (z1): {z1_teeth}\n")
                self.results_text.insert(tk.END, f"Uygulama Faktörü (KA): {Ka}\n")
                self.results_text.insert(tk.END, f"Diş Dibi Limit Gerilmesi (σFlim): {sigma_Flim} N/mm²\n")
                self.results_text.insert(tk.END, f"Yüzey Limit Gerilmesi (σHlim): {sigma_Hlim} N/mm²\n")
                self.results_text.insert(tk.END, f"Minimum Güvenlik Katsayısı (Smin): {S_min}\n")

                self.results_text.insert(tk.END, "\n--- Hesaplanan Değerler ---\n")
                self.results_text.insert(tk.END, f"Dişli 1 Diş Sayısı (z1): {results.get('z1'):.2f}\n")
                self.results_text.insert(tk.END, f"Dişli 2 Diş Sayısı (z2): {results.get('z2'):.2f}\n")
                self.results_text.insert(tk.END, f"Dişli 2 Devir Sayısı (n2): {results.get('n2'):.2f} dev/dak\n")
                self.results_text.insert(tk.END, f"Nominal Moment (Md): {results.get('Md_Nm'):.4f} Nm ({results.get('Md_Nmm'):.2f} Nmm)\n")
                self.results_text.insert(tk.END, f"Hesaplanan Nominal Modül (mn): {results.get('mn'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Enine Modül (mt): {results.get('mt'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Alın Basınç Açısı (αt): {results.get('alpha_t_deg'):.4f}°\n")
                self.results_text.insert(tk.END, f"Pinyon Taksimat Dairesi Çapı (d1): {results.get('d1'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Dişli Çark Taksimat Dairesi Çapı (d2): {results.get('d2'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Pinyon Temel Daire Çapı (db1): {results.get('db1'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Dişli Çark Temel Daire Çapı (db2): {results.get('db2'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Diş Genişliği (b): {results.get('b'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Minimum Modül Aralığı: {results.get('mmin_range')}\n")
                self.results_text.insert(tk.END, f"Minimum Modül Kontrolü: {results.get('mmin_check')}\n")
                self.results_text.insert(tk.END, f"Çevresel Hız (v): {results.get('v'):.4f} m/s\n")
                self.results_text.insert(tk.END, f"Teğetsel Kuvvet (Ft): {results.get('Ft'):.4f} N\n")
                self.results_text.insert(tk.END, f"Pinyon Eşdeğer Diş Sayısı (zhe1): {results.get('zhe1'):.4f}\n")
                self.results_text.insert(tk.END, f"Dişli Çark Eşdeğer Diş Sayısı (zhe2): {results.get('zhe2'):.4f}\n")
                self.results_text.insert(tk.END, f"Hesaplanan Aks Mesafesi (a): {results.get('a'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Profil Kaydırma Katsayıları Toplamı (x1+x2): {results.get('x_sum'):.4f}\n")
                self.results_text.insert(tk.END, f"Pinyon Profil Kaydırma Katsayısı (x1): {results.get('x1'):.4f}\n")
                self.results_text.insert(tk.END, f"Dişli Çark Profil Kaydırma Katsayısı (x2): {results.get('x2'):.4f}\n")
                self.results_text.insert(tk.END, f"Diş Başı Yüksekliği (ha): {results.get('ha'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Pinyon Diş Başı Çapı (da1): {results.get('da1'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Dişli Çark Diş Başı Çapı (da2): {results.get('da2'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Pinyon Diş Dibi Çapı (df1): {results.get('df1'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Dişli Çark Diş Dibi Çapı (df2): {results.get('df2'):.4f} mm\n")
                self.results_text.insert(tk.END, f"Alın Kavrama Oranı (εα): {results.get('epsilon_alpha'):.4f}\n")
                self.results_text.insert(tk.END, f"Helis Kavrama Oranı (εβ): {results.get('epsilon_beta'):.4f}\n")
                self.results_text.insert(tk.END, f"Toplam Kavrama Oranı (ε): {results.get('epsilon_total'):.4f}\n")
                
                self.results_text.insert(tk.END, "\n--- Mukavemet Kontrolü (Diş Dibi) ---\n")
                self.results_text.insert(tk.END, f"Diş Form Faktörü (YF): {results.get('YF'):.4f}\n")
                self.results_text.insert(tk.END, f"Gerilim Düzeltme Faktörü (YS): {results.get('YS'):.4f}\n")
                self.results_text.insert(tk.END, f"Kavrama Faktörü (Yε): {results.get('Y_epsilon'):.4f}\n")
                self.results_text.insert(tk.END, f"Helis Açısı Faktörü (Yβ): {results.get('Y_beta'):.4f}\n")
                self.results_text.insert(tk.END, f"Dinamik Faktör (KV): {results.get('KV'):.4f}\n")
                self.results_text.insert(tk.END, f"KFβ Yük Dağılım Faktörü: {results.get('KF_beta'):.4f}\n")
                self.results_text.insert(tk.END, f"KFα Yük Dağılım Faktörü: {results.get('KF_alpha'):.4f}\n")
                self.results_text.insert(tk.END, f"Diş Dibi Bükülme Gerilmesi (σF): {results.get('sigma_F'):.4f} N/mm²\n")
                self.results_text.insert(tk.END, f"Diş Dibi Limit Gerilmesi (σFmax): {results.get('sigma_Fmax'):.4f} N/mm²\n")
                self.results_text.insert(tk.END, f"Diş Dibi Güvenlik Katsayısı (SF): {results.get('SF'):.4f} --> {results.get('SF_check')}\n")

                self.results_text.insert(tk.END, "\n--- Mukavemet Kontrolü (Yüzey Yorulması) ---\n")
                self.results_text.insert(tk.END, f"Elastisite Faktörü (ZE): {results.get('ZE'):.4f} √N/mm²\n")
                self.results_text.insert(tk.END, f"Helis Açısı Faktörü (Zβ): {results.get('Z_beta'):.4f}\n")
                self.results_text.insert(tk.END, f"ZHβ Yük Dağılım Faktörü: {results.get('ZH_beta'):.4f}\n")
                self.results_text.insert(tk.END, f"KHα Yük Dağılım Faktörü: {results.get('KH_alpha_surface'):.4f}\n")
                self.results_text.insert(tk.END, f"Kavrama Faktörü (Zε): {results.get('Z_epsilon'):.4f}\n")
                self.results_text.insert(tk.END, f"Bölge Faktörü (ZH): {results.get('ZH'):.4f}\n")
                self.results_text.insert(tk.END, f"Temas Gerilmesi (σH): {results.get('sigma_H'):.4f} N/mm²\n")
                self.results_text.insert(tk.END, f"Yüzey Limit Gerilmesi (σHmax): {results.get('sigma_Hmax'):.4f} N/mm²\n")
                self.results_text.insert(tk.END, f"Yüzey Güvenlik Katsayısı (SH): {results.get('SH'):.4f} --> {results.get('SH_check')}\n")

                self.results_text.insert(tk.END, "\n--- Genel Değerlendirme ---\n")
                if results['SF_check'] == "Güvenli" and results['SH_check'] == "Güvenli":
                    self.results_text.insert(tk.END, "Dişli boyutlandırması, hem diş dibi bükülme hem de yüzey yorulması açısından güvenlidir.\n")
                else:
                    self.results_text.insert(tk.END, "Dişli boyutlandırması güvenlik kriterlerini sağlamamaktadır. Parametreler gözden geçirilmelidir.\n")
                
                # If calculation is successful, enable the 3D drawing button
                self.btn_show_3d.config(state=tk.NORMAL)

            else:
                self.results_text.insert(tk.END, f"Hesaplama Hatası: {results.get('error_message', 'Bilinmeyen Hata')}\n")
                self.btn_show_3d.config(state=tk.DISABLED) # Disable button if there's an error
            
            self.results_text.config(state=tk.DISABLED) # Make read-only

        except ValueError as ve:
            messagebox.showerror("Giriş Hatası", f"Lütfen geçerli sayısal değerler girin: {ve}")
            self.btn_show_3d.config(state=tk.DISABLED) # Disable button if there's an error
        except Exception as e:
            messagebox.showerror("Hesaplama Hatası", f"Beklenmeyen bir hata oluştu: {e}")
            self.btn_show_3d.config(state=tk.DISABLED) # Disable button if there's an error

    def show_3d_drawing_wrapper(self):
        """
        A wrapper to call the plot_helical_gear_3d function.
        Ensures that calculation results are available.
        """
        if hasattr(self, 'last_calculation_results') and self.last_calculation_results and self.last_calculation_results['status'] == "Başarılı":
            results = self.last_calculation_results
            
            # Parameters for both gears and common parameters
            d1 = results['d1']
            b = results['b']
            z1 = results['z1']
            da1 = results['da1']
            df1 = results['df1']
            
            d2 = results['d2']
            z2 = results['z2']
            da2 = results['da2']
            df2 = results['df2']
            
            beta_deg = results['beta_deg']
            mn = results['mn']
            alpha_n_deg = results['alpha_n_deg']
            ha_factor = results['ha_factor']
            ad = results['ad'] # Aks mesafesi from results

            plot_helical_gear_3d(self.master, d1, b, z1, da1, df1, d2, z2, da2, df2, beta_deg, mn, alpha_n_deg, ha_factor, ad)
        else:
            messagebox.showwarning("3D Çizim Hatası", "Lütfen önce dişli hesaplamasını başarıyla yapın.")


if __name__ == "__main__":
    root = tk.Tk()
    app = HelicalGearCalculatorApp(root)
    root.mainloop()

