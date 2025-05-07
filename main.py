import sys
import subprocess
import psutil                             # CPU & Bellek için
import wmi                                 # WMI için
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QPushButton, QMessageBox
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
        self.setGeometry(100, 100, 300, 200)

        # CPU ve Bellek etiketleri
        self.cpu_label = QLabel("CPU Kullanımı: …", self)
        self.cpu_label.move(20, 20)
        self.mem_label = QLabel("Boş Bellek (MB): …", self)
        self.mem_label.move(20, 60)

        # Güncelle butonu
        self.refresh_btn = QPushButton("Güncelle", self)
        self.refresh_btn.move(20, 100)
        self.refresh_btn.clicked.connect(self.refresh_stats)

        # Otomatik yenileme (opsiyonel)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(5000)  # her 5 saniyede bir

        # Başlangıç kontrolleri
        self.check_power_plan()
        self.check_pagefile()

    def refresh_stats(self):
        """CPU ve bellek değerlerini oku ve GUI'de güncelle."""
        cpu = psutil.cpu_percent(interval=1)           # blocking; ilk çağrı 0.0 olabilir :contentReference[oaicite:7]{index=7}
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
