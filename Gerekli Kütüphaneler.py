import subprocess # Harici programları çalıştırmak için kullanılır (örn. pip)
import sys        # Python yorumlayıcısı ile ilgili bilgilere erişim sağlar

def install_package(package):
    """
    Belirtilen Python paketini pip kullanarak kurmaya çalışır.
    Kurulumun başarılı olup olmadığını veya bir hata oluşup oluşmadığını konsola yazdırır.
    """
    try:
        # pip'i subprocess aracılığıyla çağırarak paketi kur
        # sys.executable, mevcut Python yorumlayıcısının yolunu sağlar
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"'{package}' başarıyla kuruldu.")
    except subprocess.CalledProcessError as e:
        # pip komutu bir hata kodu ile dönerse bu hata yakalanır
        print(f"'{package}' kurulumu sırasında bir hata oluştu: {e}")
    except Exception as e:
        # Diğer tüm beklenmeyen hataları yakala
        print(f"Beklenmeyen bir hata oluştu '{package}' kurulumu sırasında: {e}")

if __name__ == "__main__":
    # Kurulması gereken Python kütüphanelerinin listesi
    required_packages = [
        "pandas",       # Veri analizi ve manipülasyonu için
        "numpy",        # Sayısal hesaplamalar için
        "matplotlib"    # Çizimler ve görselleştirmeler için
        # tkinter ve math genellikle Python'ın standart kütüphaneleriyle birlikte gelir,
        # bu nedenle ek kurulum gerektirmezler.
    ]

    print("Gerekli kütüphaneler kontrol ediliyor ve kuruluyor...")
    # Her bir paketi listeden alıp kurma fonksiyonunu çağır
    for package in required_packages:
        install_package(package)
    print("\nKurulum tamamlandı. Uygulamayı şimdi çalıştırabilirsiniz.")

