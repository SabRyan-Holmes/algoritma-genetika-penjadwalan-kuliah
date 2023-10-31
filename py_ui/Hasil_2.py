import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,  QLabel
from components import AlgoritmaGenetika, ScenarioComposer
from collections import defaultdict
import math

class Hasil(QMainWindow):
    def __init__(self, results, solusi):
        super().__init__()
        self.setWindowTitle("Jadwal Kuliah")
        self.setGeometry(100, 100, 800, 600)
        # self.setWTitle("Jadwal Kuliah")

        # Membuat stacked widget untuk menampung tabel-tabel
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.data = {
            # 'results': [],
            'rooms': [],
            'instructors': [],
            'subjects': [],
            # 'sections': [],
            # 'sharings': [],
        }
        data = self.data
        composer = ScenarioComposer.ScenarioComposer()
        composer = composer.getScenarioData()
        self.data.update(composer)
        self.results = results
        
        # Membuat tabel-tabel untuk setiap hari dan jam
        # Untuk Penjadwalan
        self.seminggu = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
        self.timeslots = ['7.30-9.10', '9.30-12.00', '13.00-15.30', '16.00-17.40']
      
   
        self.all_mk = []
        self.all_mkcode = []
        for j in range(len(self.data['subjects'])):
            self.all_mk.append(data['subjects'][j+1][0])
            self.all_mkcode.append(data['subjects'][j+1][2])
            
        self.all_rooms = []
        for j in range(len(self.data['rooms'])):
            self.all_rooms.append(data['rooms'][j+1][0])

        
       
        print("Ini Semua keys ")
        print(data['rooms'].keys())
     
        nama_kelas = set()
        for key_kelas in self.all_rooms:
            (nama_kelas.add(key_kelas))
            self.list_kelas = list(nama_kelas)
            
       
        
        # print("Data Kelas dengan nama" )
        # print(self.list_kelas)
  
        # print("Data MK dengan nama" )
        # print(self.list_mk)
  
                        
     
        
            
        
        self.judul_label = QLabel("Jadwal Optimal Kuliah")
        layout = QVBoxLayout()
        layout.addWidget(self.judul_label)
        table = self.create_table(self.list_kelas, self.all_mk)
        self.stacked_widget.addWidget(table)
                           
                                
                                
        # print("Jadwal Kelas/Ruang ", data['rooms'][i+1][0])
    def create_table(self, kelas, mata_kuliah):
        
        
        # Membuat tabel dengan header dan waktu/jam
        table = QTableWidget()
        table.setColumnCount(6)
        hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
        table.setHorizontalHeaderLabels(hari)

        # Menambahkan waktu/jam ke dalam tabel
        table.setRowCount(9)
        jam = ['7.30-9.10', '9.30-12.00', '13.00-15.30', '16.00-17.40', '--------- ' ,'7.30-9.10', '9.30-12.00', '13.00-15.30', '16.00-17.40']
        table.setVerticalHeaderLabels(jam)

        # Mengatur layout untuk tabel
        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(self.judul_label)
        widget = QWidget()
        widget.setLayout(layout)
        
        
        # print('Semua mata kuliah :')
        # print(mata_kuliah)
        
        # nama_mk = set()
        # for key_mk in self.all_mk:
        #     (nama_mk.add(key_mk))
        #     self.list_mk = list(nama_mk)
        
        
        
                
        # MNengisi Tabel beerdasarkan timeslots
        print('Ini Gen MK ,Ruang dan Timeslot dari Solusi')
        for i,gen in enumerate(self.results):
            gen_mk = gen[0] #Mengambil gen timeslot
            gen_ruang = gen[1]
            timeslot = gen[2] #Mengambil gen timeslot
            
            print(gen_mk, gen_ruang, timeslot)
            
            baris_jam = (gen_ruang - 1)* 5 + (timeslot % 4) #Sebagai row/baris
            
            jadwal = self.all_mk[gen_mk-1]
                
            kolom_hari = math.ceil(timeslot / 4) #Sebagai column/kolom            
            
            item = QTableWidgetItem(f"{jadwal} ") 
            table.setItem(baris_jam, kolom_hari, item)
                
            # for baris_jam in range(len(jam)):
            #     # baris_jam += 1
            #     for kolom_hari in range(len(hari)):
            #         # kolom_hari = kolom_hari * 4                  
            #         if(timeslot <= 4):
            #             item = QTableWidgetItem(f"{gen_mk} | ") 
            #             table.setItem(baris_jam, kolom_hari, item)
            #         elif(timeslot > 4 and timeslot <=24 and kolom_hari >= 1):         
            #             kolom_hari = kolom_hari * 4
            #             if(timeslot >=5+kolom_hari and timeslot <=8+kolom_hari):
            #                 item = QTableWidgetItem(f"{gen_mk} | ") 
            #                 table.setItem(baris_jam, kolom_hari, item)
                    # jam = jam * 4
                    # for(re)
            # if(timeslot <= 4):                                      
         

        return widget

