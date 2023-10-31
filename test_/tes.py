import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jadwal Kuliah")
        self.setGeometry(100, 100, 800, 600)

        # Membuat stacked widget untuk menampung tabel-tabel
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Membuat tabel-tabel untuk setiap hari dan jam
        for hari in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']:
            for jam in ['7.30-9.10', '9.30-12.00', '13.00-15.30', '16.00-17.40']:
                table = self.create_table(hari, jam)
                self.stacked_widget.addWidget(table)

    def create_table(self, hari, jam):
        # Membuat tabel dengan header dan waktu/jam
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(['', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])

        # Menambahkan waktu/jam ke dalam tabel
        table.setRowCount(4)
        table.setVerticalHeaderLabels(['7.30-9.10', '9.30-12.00', '13.00-15.30', '16.00-17.40'])

        # Mengisi sel-sel tabel dengan data
        for row in range(4):
            for col in range(1, 7):
                item = QTableWidgetItem(f"ke  ke Col -{col} {hari}  {jam}")
                table.setItem(row, col, item)

        # Mengatur layout untuk tabel
        layout = QVBoxLayout()
        layout.addWidget(table)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
