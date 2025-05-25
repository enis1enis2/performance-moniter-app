import sys
import subprocess
import psutil                             # CPU & Bellek için
import wmi                                 # WMI için
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QPushButton, QMessageBox, QWidget, QVBoxLayout
)
from PyQt5.QtCore import QTimer

# -- WMI Bağlantısı --
wmi_conn = wmi.WMI()

def is_pagefile_system_managed():
    """Pagefile ayarının sistem yönetimli olup olmadığını kontrol eder."""
    for setting in wmi_conn.Win32_PageFileSetting():
        # MaximumSize == 0 ise system managed
        return setting.MaximumSize == 0
    return True  # Kayıt yoksa genellikle yönetimli

def set_system_managed_pagefile():
    """Pagefile ayarını sistem yönetimli moda geçirir."""
    for setting in wmi_conn.Win32_PageFileSetting():
        setting.InitialSize = 0
        setting.MaximumSize = 0
        setting.Put_()

def get_active_power_scheme():
    """
    Power plan GUID'ini döndürür.
    UTF-8 decode, hatalı karakterler ignore.
    """
    output = subprocess.check_output(
        ["powercfg", "/getactivescheme"],
        encoding='utf-8',
        errors='ignore'
    ).strip()
    return output


def set_power_scheme(guid):
    """Power plan'ı GUID ile değiştirir."""
    subprocess.run(["powercfg", "/setactive", guid], check=True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Performans Takip")
        # self.setGeometry(100, 100, 300, 200) # Geometri layout tarafından yönetilecek
        self.setMinimumSize(250, 180) # Daha iyi bir minimum boyut

        # Merkezi widget ve layout
        central_widget = QWidget() 
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout() 
        central_widget.setLayout(layout)

        layout.setContentsMargins(15, 15, 15, 15) # Pencere kenar boşlukları
        layout.setSpacing(10) # Widget'lar arası boşluk

        # CPU ve Bellek etiketleri
        self.cpu_label = QLabel("CPU Kullanımı: …") 
        layout.addWidget(self.cpu_label)

        self.mem_label = QLabel("Boş Bellek (MB): …") 
        layout.addWidget(self.mem_label)

        # Güncelle butonu
        self.refresh_btn = QPushButton("Güncelle") 
        self.refresh_btn.clicked.connect(self.refresh_stats)
        layout.addWidget(self.refresh_btn)
        
        # Otomatik yenileme (opsiyonel)
        self.timer = QTimer(self) # Timer'ın parent'ı MainWindow olabilir
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(5000)  # her 5 saniyede bir

        # Başlangıç kontrolleri
        self.check_power_plan()
        self.check_pagefile()

    def refresh_stats(self):
        """CPU ve bellek değerlerini oku ve GUI'de güncelle."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().available // (1024**2)  # MB cinsinden boş bellek
        self.cpu_label.setText(f"CPU Kullanımı: {cpu:.1f}%")
        self.mem_label.setText(f"Boş Bellek (MB): {mem}")

    def check_power_plan(self):
        """Güç planını kontrol eder ve gerekirse kullanıcıya sorar."""
        current = get_active_power_scheme()
        desired_guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"  # Yüksek Performans GUID'i örneği
        if desired_guid not in current:
            reply = QMessageBox.question(
                self, "Güç Planı",
                "Güç planı optimal değil. Yüksek Performans'a geçilsin mi?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                set_power_scheme(desired_guid)

    def check_pagefile(self):
        """Pagefile ayarını kontrol eder ve gerekirse kullanıcıya sorar."""
        if not is_pagefile_system_managed():
            reply = QMessageBox.question(
                self, "Sanal Bellek",
                "Sanal bellek yönetilmiyor. Sistem yönetimine geçilsin mi?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                set_system_managed_pagefile()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Modern ve temiz bir görünüm için QSS
    qss = """
        QMainWindow {
            background-color: #f0f0f0;
            font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
        }
        QLabel {
            color: #333333;
            font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
            font-size: 10pt;
        }
        QPushButton {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
            font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
            font-size: 10pt;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
    """
    app.setStyleSheet(qss)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
