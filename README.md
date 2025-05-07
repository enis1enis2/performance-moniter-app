# 🖥️ Performance Monitor App

Python ile geliştirilmiş Windows performans takip uygulaması. CPU ve RAM kullanımını izler, sistem ayarlarını (güç planı, sanal bellek) kontrol eder ve optimize eder.

---

## 📁 Proje Yapısı

```
performance-monitor-app/
├── main.py           # Uygulama kodu
├── requirements.txt  # Bağımlılıklar
├── README.md         # Kurulum ve kullanım talimatları
├── .gitignore        # Git göz ardı listesi
└── dist/             # (Oluşursa) EXE dosyası
```

---

## 🐍 Python 3.13.2 Kurulumu

1. [Python 3.13.2 indir](https://www.python.org/downloads/release/python-3132/)
2. Windows 64-bit Installer'ı indirin: `Windows installer (64-bit)`
3. Kurulum sırasında **"Add Python to PATH"** kutusunu işaretleyin
4. "Install Now" seçeneğiyle kurulumu tamamlayın

Kurulumun başarılı olduğunu kontrol etmek için terminal veya PowerShell'de:

```bash
python --version
```

> Çıktı: `Python 3.13.2`

---

## 🧬 Depoyu Klonlama ve Sanal Ortam Kurulumu

### 1. Git ile projeyi klonlayın:

```bash
git clone https://github.com/kullaniciadi/performance-monitor-app.git
cd performance-monitor-app
```

### 2. Sanal ortam (venv) oluşturun:

```bash
python -m venv venv
```

### 3. Sanal ortamı etkinleştirin:

* **PowerShell**:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # (ilk kez gerekebilir)
.\venv\Scripts\Activate.ps1
```

* **CMD**:

```cmd
.\venv\Scripts\activate.bat
```

Başarılı olursa terminal başında `(venv)` yazar.

---

## 📦 Gerekli Paketlerin Yüklenmesi

```bash
pip install -r requirements.txt
```

Eğer `requirements.txt` yoksa:

```bash
pip install psutil pyqt5 wmi
```

---

## 🧪 Uygulamayı Çalıştırma

```bash
python main.py
```

---

## 🛠️ .exe Oluşturma (PyInstaller)

1. PyInstaller'ı yükleyin:

```bash
pip install pyinstaller
```

2. EXE oluşturun:

```bash
pyinstaller --onefile --windowed main.py
```

3. EXE dosyanız `dist/` klasörü içinde oluşur:

```
dist/main.exe
```

> **Not:** Ayar değişiklikleri için EXE dosyasını "Yönetici olarak çalıştırmanız" gerekebilir.

---

## 📄 requirements.txt

```
psutil
pyqt5
WMI
```

---

## 🙈 .gitignore

```
venv/
__pycache__/
*.pyc
dist/
build/
*.spec
```

---

## 🤝 Katkıda Bulunma

1. Fork’layın
2. Yeni bir branch oluşturun:

```bash
git checkout -b yeni-ozellik
```

3. Değişikliklerinizi commit’leyin:

```bash
git commit -m "Özellik eklendi"
```

4. Branch’i gönderin:

```bash
git push origin yeni-ozellik
```

5. Pull request (PR) oluşturun

---

## 📝 Lisans

MIT Lisansı. Detaylar için `LICENSE` dosyasına bakabilirsiniz.
