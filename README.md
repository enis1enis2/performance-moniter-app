# Performance Monitor App

Python ile geliştirilmiş Windows performans takip uygulaması.

## 📂 Proje Yapısı

```
performance-monitor-app/
├── main.py           # Uygulama kodu
├── requirements.txt  # Bağımlılıklar
├── README.md         # Proje açıklaması ve kurulum adımları
└── .gitignore        # Git göz ardı listesi
```

## 🚀 Başlarken

Aşağıdaki adımları takip ederek projeyi yerel makinenize kurabilir ve çalıştırabilirsiniz.

### 1. Python 3.13.2 Kurulumu

1. [https://www.python.org/downloads/release/python-3132/](https://www.python.org/downloads/release/python-3132/) adresine gidin.
2. Windows için uygun installer (x86-64) indirin.
3. İndirilen `.exe` dosyasını çalıştırın ve **Add Python to PATH** seçeneğini işaretleyerek ilerleyin.

### 2. Depoyu Klonlama

```bash
git clone https://github.com/kullaniciadi/performance-monitor-app.git
cd performance-monitor-app
```

### 3. Sanal Ortam (venv) Oluşturma ve Aktifleştirme

**Windows + PowerShell** için:

```powershell
python -m venv venv
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # Sadece ilk kez gerekirse
.
\venv\Scripts\Activate.ps1
```

**Windows + CMD** için:

```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

### 4. Gerekli Paketlerin Yüklenmesi

```bash
pip install -r requirements.txt
```

### 5. Uygulamayı Çalıştırma

```bash
python main.py
```

### 6. .exe Dosyası Oluşturma (Opsiyonel)

PyInstaller ile tek dosyalı EXE üretmek için:

```bash
pyinstaller --onefile --windowed main.py
```

Oluşan `dist/main.exe` dosyasını `dist` klasöründen çalıştırabilirsiniz.

## 📦 requirements.txt

```
psutil
pyqt5
WMI
```

## 📄 .gitignore

```
venv/
__pycache__/
*.pyc
dist/
build/
*.spec
```

## 🤝 Katkıda Bulunma

1. Fork’layın (🔀 sağ üst köşeden)
2. Yeni bir branch oluşturun (`git checkout -b feature/özellik-adı`)
3. Değişikliklerinizi commit’leyin (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/özellik-adı`)
5. Pull request (PR) oluşturun

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.
