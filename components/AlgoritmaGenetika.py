import random
from deap import base, creator, tools
from prettytable import PrettyTable
from tabulate import tabulate
import numpy as np
from components import Pelanggaran 
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
import json
import sys
from py_ui import Hasil_2, Generate 
import math
# from operator import itemgetter
# from collections import Counter
# import copy
# import itertools

# Inisialisasi toolbox untuk memudahkan algoritma(Dari library Deap)
toolbox = base.Toolbox()

# (1)
# Representasi Kromosom & Data Awal 



class AlgoritmaGenetika(QtCore.QThread):
    # Current phase of the algorithm
    statusSignal = QtCore.pyqtSignal(str)
    # Genetic algorithm variable details
    detailsSignal = QtCore.pyqtSignal(list)
    # Running process type
    operationSignal = QtCore.pyqtSignal(int)
    # List of chromosomes for preview
    dataSignal = QtCore.pyqtSignal(list)

    def __init__(self, data):
        super().__init__() 
        self.averageFitness = float
        self.pastAverageFitness = float
        self.highestFitness = float
        self.lowestFitness = float
        self.running = True
       
        self.data = {
            'rooms': [],
            'instructors': [],
            'subjects': [],
            'results': []
            
        }
        self.data = data
        self.results = []
        self.mutationRate = .25
       
        self.mata_kuliah = list(self.data['subjects'].keys())
        self.kelas = list(self.data['rooms'].keys())
        self.timeslots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        # Untuk menampung data nanti temporary nanti
        self.dataTemp = {
                'tempKromosom1' : None,
                'tempKromosom2' : None,
                'tempKromosom3' : None,
                'tempFitness': float,
                'tempProbFit' : float,
                'tempComFit' : float,
                'nilai_random': float,
                'cumulative_prob': [],
                'populations': [],  
                'NewKromosom': [],
                'parents' : None,
                'cut_position' : None, 
                'cut_position' : None,
                'index_mutasi' : [], #Index/Nomor untuk Mutasi
                'last_kromosom' : [], #Kromosom Setelah dimutasi
                'NewFitness' : float
            }
        self.stopWhenMaxFitnessAt = 99
         
        self.panjang_kromosom = len(self.data['subjects']) * len(self.data['rooms'])
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        
        toolbox.register("individual", tools.initRepeat, creator.Individual, self.generate_kromosom, n=self.panjang_kromosom) 
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
       # Mengubah string JSON menjadi struktur data Python (list)
        
        
        
        
        
    def run(self):
        self.kromosom = self.dataTemp['NewKromosom']
        self.generation = 0
        # self.detailsSignal.emit(
        #             [generation, len(self.kromosom), int(self.mutationRate * 100), round(self.averageFitness, 2),
        #              round(self.pastAverageFitness, 2), self.highestFitness, self.lowestFitness])
        
        # Generate kromosom
        
        self.generate_kromosom()
        
        population_size = 3
        # nantinya fungsi ini menampung populasi
        population = toolbox.population(n=population_size)
        population_table = []

            # Cetak hasil populasi dalam bentuk objek /tabel
        for i, chromosome in enumerate(population):
            self.dataTemp['populations'].append([*chromosome])
                # population_table.append([f'Kromosom {i + 1}', *chromosome])                
                # Taruh dalam objek
                
            
            # print("Individu pada kromosom")
            # print(f"Kromosom 1 :  { data['tempKromosom1'] }")
            # print(f"Kromosom 2 :  { data['tempKromosom2'] }")
            # print(f"Kromosom 3 :  { data['tempKromosom3'] }")      
            # print('--------------')       
            # test print individu
        
        self.new_fitness = self.dataTemp['NewFitness']
        self.fitness = int
        # self.averageFitness =  sum(self.new_fitness) / len(self.new_fitness)
        
        # Avg = np.mean(self.new_fitness)
        # self.averageFitness = Avg
        # self.highestFitness = max(self.new_fitness)
        # self.lowestFitness = min(self.new_fitness)
        
        # if (self.averageFitness - self.pastAverageFitness < 0):
        #     self.pastAverageFitness = self.averageFitness
        # else:
        #     pass
        
        while (self.fitness != 1):
        # for i in range(1):
            # Avg = np.mean(self.new_fitness)
            # self.averageFitness = Avg
            
            #Menghitung Pelanggaran 
            populasi = self.dataTemp['populations']
            Pelanggaran.get_pelanggaran(populasi)
            self.pelanggaran = Pelanggaran.get_pelanggaran(populasi)
        
        
            # Cetak Nilai Fitness
            print('Ini adalah Fitness dari setiap kromosom : ')
            self.hitung_fitness(self.pelanggaran)
            
            # Menampung hasiil fitness ke var
            self.new_fitness = self.hitung_fitness(self.pelanggaran)
            
            for fitness in self.new_fitness:
                self.fitness = fitness
            # Evaluasi Solusi /Top Kromosom
            self.evaluasi_solusi(self.new_fitness)
            if(self.generation >= 99):     
                for i in range(1, 3):           
                    self.getAltSolution()
                    
                    last_kromosom = self.dataTemp['last_kromosom'] 
                    last_kromosom.append(self.results)
                print("---------------------------------------------------------------------------------------------------------------")
                print("Generasi ke-", self.generation)                
                print("---------------------------------------------------------------------------------------------------------------")
                print("Populasi Terakhir")
                # population_size = 3
                # # nantinya fungsi ini menampung populasi
                # population = toolbox.population(n=population_size)
                # for i, chromosome in enumerate(population):
                #     self.dataTemp['last_kromosom'].append([*chromosome])               
                print(last_kromosom)
                print("---------------------------------------------------------------------------------------------------------------")
                Pelanggaran.get_pelanggaran(last_kromosom)
                print("Fitness Terbaru adalah", self.new_fitness)
                print("Top Kromosom/Solusi adalah", self.results)                
                self.openResult()
                break
            # Mengupdate average fitness
            
            # self.highestFitness = self.data if self.new_fitness > self.highestFitness else self.highestFitness
            # self.lowestFitness = self.new_fitness if self.new_fitness < self.lowestFitness else self.lowestFitness
            
            # Menghitung Probability Fitness
            print('Ini adalah Probabily Fitness dari setiap kromosom : ')
            self.probability_fitness()

            # Menghitung Comulative Probability Values
            print('Ini adalah Comulative Probability Fitness dari setiap kromosom : ')
            self.com_probability_fitness()

            # Nilai Random antara 0-1(Termasuk berkoma)
            self.generate_rand()
            
            # Seeleksi New Kromosom
            self.new_kromosom_seleksi()
            kromosom_baru = self.dataTemp['NewKromosom']
            print("Menampilkan Kromosom Baru")
            for i in range(len(kromosom_baru)):
                print(f"Kromosom baru ke {i + 1}: {kromosom_baru[i]}")

            # CrossOver
            # Femanggil fungsi penghitungan Crossover (One-point CrossOver)
            self.cross_over() 
            # toolbox.register("mate", cross_over)


            # Mutasi
            print("Ini adalah Hasil Mutasi : ") 
            self.mutation()
            
            self.generation += 1
            
            print("---------------------------------------------------------------------------------------------------------------")
            print("Generasi ke-", self.generation)
            
            print("---------------------------------------------------------------------------------------------------------------")
            print("Fitness Terbaru adalah", self.new_fitness)
        
        else:
            print("---------------------------------------------------------------------------------------------------------------")
            print("Top Kromosom/Solusi adalah", self.results)
            
            self.openResult()
            
            
           

    def openResult(self):
        app = QApplication(sys.argv)
        window = Hasil_2.Hasil(self.results, self.kelas)
        window.show()
        sys.exit(app.exec_())
    
    # Untuk studi kasus ini solusi nya perkelas
    def getJumlahSolusi(self):
        return self.data['rooms']
    
    def getResult(self):
        return self.results
    
    
    # (2)
    # Populasi Awal & Generate Kromosom
    # Fungsi untuk generate Kromosom
    def generate_kromosom(self):
        
        return [random.choice(self.mata_kuliah), random.choice(self.kelas), random.choice(self.timeslots)]
        

    # (3)
    # Evaluasi Nilai Fitness
    #Nilai pelanggaran Masih hardcode, cuman contoh
    def hitung_fitness(self, pelanggaran):
        totalChromosomeFitness = 0
        
        pelanggaran = self.pelanggaran
        fitness_scores = []
        for pelanggaran_kromosom in pelanggaran:
            fitness = 1 / (1 + pelanggaran_kromosom)
            fitness_scores.append(fitness)
        self.dataTemp['tempFitness'] = fitness_scores
        print(self.dataTemp['tempFitness'])
        
        
       
        # chromosomeFitness = sorted(enumerate(map(lambda chromosome: chromosome.fitness, self.chromosomes)),
        #                            key=itemgetter(1))
        
        return fitness_scores


    # (4)
    # Seleksi
    # - Fungsi Untuk Menghitung Probility Fitness
    def probability_fitness(self): 
        total_fitness = sum(self.dataTemp['tempFitness'])
        probability_fitness = [fitness / total_fitness for fitness in self.dataTemp['tempFitness']]
        self.dataTemp['tempProbFit'] = probability_fitness
        print(probability_fitness)
        return probability_fitness
        
    # - Fungsi Untuk Menghitung Comulative Probility Fitness
    def com_probability_fitness(self): 
        cumulative_probabilities = [sum(self.dataTemp['tempProbFit'][:i+1]) for i in range(len(self.dataTemp['tempProbFit']))]
        self.dataTemp['cumulative_prob'] = cumulative_probabilities

        for i, cumulative_prob in enumerate(cumulative_probabilities):
            print(f"Cumulative Probability Fitness individu {i + 1}: {cumulative_prob}")
        return cumulative_prob


    # - Fungsi untuk Generate 3 nilai random antara 0 dan 1 (berkoma)
    def generate_rand(self):
        nilai_random = [random.random() for _ in range(3)]
        self.dataTemp['nilai_random'] = nilai_random
        # Cetak nilai random
        
        print("Nilai Random antara 0-1 :")
        print(self.dataTemp['nilai_random'])
        return nilai_random


    # - Kromosom baru dari membandingkan nilai random dengan Comulative Probility Fitness
    def new_kromosom_seleksi(self):
    # Mengecek setiap nilai dalam nilai_random dengan cumulative_prob
        iterasi = len(self.dataTemp['nilai_random'])
        print(iterasi)
        for i in range(iterasi):
            if self.dataTemp['nilai_random'][i] < self.dataTemp['cumulative_prob'][2] and self.dataTemp['nilai_random'][i] > self.dataTemp['cumulative_prob'][1]:
                self.dataTemp['populations'][i] = self.dataTemp['populations'][2]
                print('Kromosom ke ' + str(i+1) + ' Diubah menjadi Kromosom ke 3')
            
            elif self.dataTemp['nilai_random'][i] > self.dataTemp['cumulative_prob'][0] and self.dataTemp['nilai_random'][i] < self.dataTemp['cumulative_prob'][1] and self.dataTemp['cumulative_prob'][2]:
                self.dataTemp['populations'][i] = self.dataTemp['populations'][1]
                print('Kromosom ke ' + str(i+1) + ' Diubah menjadi Kromosom ke 2')

            else :
                self.dataTemp['populations'][i] = self.dataTemp['populations'][0]
                print('Kromosom ke ' + str(i+1) + ' Diubah menjadi Kromosom ke 1')

        # Menghasilkan nilai kromosom baru
        print('Tess Population')
        print(len(self.dataTemp['populations']))
        self.dataTemp['NewKromosom'] = self.dataTemp['populations']
        new_kromosom = self.dataTemp['NewKromosom']
        return new_kromosom

    # 5
    # Cross Over
    def cross_over(self):
        # Anggap 50%
        crossover_rate = 0.5  
        parents = []
        
        adaParents = False
        while adaParents == False:
            random_values = [random.random() for _ in range(3)]
            count_values_below_crossover_rate = sum(value < crossover_rate for value in random_values)
                
            if count_values_below_crossover_rate <= 2:
                parents.append(random_values)
                for i, parent in enumerate(parents):
                    print(f"Percobaan Mencari Parents ke {i + 1}: {parent}")
                if(count_values_below_crossover_rate ==2):
                    print("2 Parents sudah ditemukan !")
                    adaParents = True
                    
                # Mencocokkan dengan kromosom
                kromosom_parent = [index+1 for index, value in enumerate(random_values) if value < crossover_rate]
                formatted = " & ".join(map(str, kromosom_parent))
                print("Kromosom yang akan dijadikan induk/parents adalah " + formatted)

            # Jika tidak ditemukan 2 induk
            else:
                print("Loading..No parents found")
                parents.append(None)
        
        # Menetapkan Kromosom mana yang dijadikan induk
        index1 = kromosom_parent[0]
        index2 = kromosom_parent[1]

        parent1 = self.dataTemp['NewKromosom'][index1-1] #Dikurangi 1 karena index array biasa dimulai dari 0 sedangkan kromomosom ke 0 tidak ada
        parent2 = self.dataTemp['NewKromosom'][index2-1]

        print('Parents ke 1')
        print(parent1)

        print('Parents ke 2')
        print(parent2)
        
        # Mencari Cut Position
        #Banyak Kromosom dikali Banyak individu
        
        nilai_random = random.randint(1, self.panjang_kromosom) #Generate nilai antar 0-1
        print('Cut Position adalah : ' + str(nilai_random)) 
        # Mendefinisikan operasi crossover ke tool box
        toolbox.register("mate", self.cross_over)    
        crossover_point = nilai_random
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        # Mengubah nya menjadi new kromosom dan mengupdate object tersebut sesuai hasil Cross Over
        self.dataTemp['NewKromosom'][index1-1] = child1
        self.dataTemp['NewKromosom'][index2-1] = child2
        # Logika memasukkan kembali kromosom baruu setelah dimutasi ke object
    
        
        print("Nilai New Kromosom sekarang setelah di Cross Over : ")
        print(f"Nilai Kromosom {self.dataTemp['NewKromosom']}")
        # print(f" 1 {child1}")

        return child1, child2

    # 5
    # Mutation
    def mutation(self):
        #Mutation rate misanya ditetapkan 25%

        mutate_rate = 0.5
        jumlah_kromosom = len(self.dataTemp['NewKromosom']) 
        panjang_individu = len(self.dataTemp['NewKromosom'][0]) 
        ngen = jumlah_kromosom * panjang_individu
        #Untuk mencari jumlah mutasi dikalikan jumlah individu x dengan mutation rate nya, kemudian dibulatkan menggunakan round()
        jumlah_mutasi = round(mutate_rate * ngen) 
        # Generate nilai random sebanyak jumlah mutasi untuk index mutasi ditampung dalam array sebenyak jumlah_mutasi
        # Indeks yang akan dimutasi    
        index_mutasi = [random.randint(1, ngen) for _ in range(jumlah_mutasi)]
        
        
        toolbox.register("mutate", self.mutation)  # Operator mutasi tukar gen
        toolbox.register("select", tools.selTournament, tournsize=3)  # Operator seleksi turnamen
        
        
        semua_kromosom = []
        for i in range(jumlah_kromosom):
            for j in range(panjang_individu):    
                semua_kromosom.append(self.dataTemp['NewKromosom'][i][j])


            
        print("Semua Panjang Kromosom : ")
        print(len(semua_kromosom))

        for i, idx in enumerate(semua_kromosom):
            print(f"Nilai Gen dari individu ke {i} = {semua_kromosom[i]}"  )
            # update_gen = generate_kromosom()
            semua_kromosom[i] = self.generate_kromosom()
            print(f"Nilai Terbaru setelah dimutasi {semua_kromosom[i]}"  )


        # Masukkan lagi ke dalam objek kromosom
        new_kromosom_mutasi = []
        for i in range(jumlah_kromosom): 
            array_2d =[]   
            # Tambahkan gen ke array list 2 dimensi
            for j in range(panjang_individu):
                array_2d.append(semua_kromosom[j])
            # Tambahkan array list 2 dimensi ke array list 3 dimensi
            new_kromosom_mutasi.append(array_2d) 

        self.dataTemp['last_kromosom_'] = new_kromosom_mutasi 
        
        # Agar bisa diulangi
        self.dataTemp['populations'] =  new_kromosom_mutasi 
        print(new_kromosom_mutasi)
        # print('panjang array ' + str(len(new_kromosom_mutasi)))
        return new_kromosom_mutasi
        
    


    def evaluasi_solusi(self, new_fitness):
        for i,fitness in enumerate(new_fitness):
            topChromosome = self.dataTemp['populations'][i]
        if fitness == 1:
            self.results = topChromosome
               
        return self.results

    def getAltSolution(self):
        def generate_rand_mk_r() :
            return [random.randint(1, 9),random.randint(1,2)]
        

        unique_combined_array = [generate_rand_mk_r() for i in range(18)]
        unique_combined_array = [list(t) for t in set(tuple(element) for element in unique_combined_array)]
        while (len(unique_combined_array)<18):
            unique_combined_array.append(generate_rand_mk_r())
            unique_combined_array = [list(t) for t in set(tuple(element) for element in unique_combined_array)]
            # print(unique_combined_array)

        tmslots = list(range(1, 24))
        random.shuffle(tmslots)
        tmslots = tmslots[:18]
        # print(tmslots)

        for i, mk_ruang in enumerate(unique_combined_array):
            mk_ruang.append(tmslots[i])

        random.shuffle(unique_combined_array)
        self.results = unique_combined_array
        
      
        

    