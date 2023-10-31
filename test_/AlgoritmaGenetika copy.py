from deap import base, creator, tools
from prettytable import PrettyTable
from tabulate import tabulate
import numpy as np
import Pelanggaran 

# Inisialisasi toolbox untuk memudahkan algoritma(Dari library Deap)
toolbox = base.Toolbox()

# (1)
# Representasi Kromosom & Data Awal 
# Anggap data awal
subjects = [
        1, 2, 3, 4, 5, 6, 7, 8, 9,] #Gen Mata Kuliah
rooms = [1, 2,] # Gen Kelas/Ruang
timeslots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]


# Untuk menampung data nanti
data = {
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
        'last_kromosom_' : [], #Kromosom Setelah dimutasi
    }

   
# (2)
# Populasi Awal & Generate Kromosom
   

# Fungsi untuk generate Kromosom
def generate_kromosom():
    return [random.choice(subjects), random.choice(rooms), random.choice(timeslots)]
    

# (3)
# Evaluasi Nilai Fitness
#Nilai pelanggaran Masih hardcode, cuman contoh
def get_pelanggaran():  
    Pelanggaran.get_pelanggaran(data['populations'])

def hitung_fitness(pelanggaran):
    fitness_scores = []
    for pelanggaran_kromosom in pelanggaran:
        fitness = 1 / (1 + pelanggaran_kromosom)
        fitness_scores.append(fitness)
    data['tempFitness'] = fitness_scores
    print(data['tempFitness'])
    return fitness_scores


# (4)
# Seleksi
# - Fungsi Untuk Menghitung Probility Fitness

def probability_fitness(): 
    total_fitness = sum(data['tempFitness'])
    probability_fitness = [fitness / total_fitness for fitness in data['tempFitness']]
    data['tempProbFit'] = probability_fitness
    print(probability_fitness)
    return probability_fitness
    
    # - Fungsi Untuk Menghitung Comulative Probility Fitness
def com_probability_fitness(): 
    cumulative_probabilities = [sum(data['tempProbFit'][:i+1]) for i in range(len(data['tempProbFit']))]
    data['cumulative_prob'] = cumulative_probabilities

    for i, cumulative_prob in enumerate(cumulative_probabilities):
        print(f"Cumulative Probability Fitness individu {i + 1}: {cumulative_prob}")
    return cumulative_prob


# - Fungsi untuk Generate 3 nilai random antara 0 dan 1 (berkoma)
def generate_rand():
    nilai_random = [random.random() for _ in range(3)]
    data['nilai_random'] = nilai_random
    # Cetak nilai random
    
    print("Nilai Random antara 0-1 :")
    print(data['nilai_random'])
    return nilai_random


# - Kromosom baru dari membandingkan nilai random dengan Comulative Probility Fitness
def new_kromosom_seleksi():
# Mengecek setiap nilai dalam nilai_random dengan cumulative_prob
    iterasi = len(data['nilai_random'])
    print(iterasi)
    for i in range(iterasi):
        if data['nilai_random'][i] < data['cumulative_prob'][2] and data['nilai_random'][i] > data['cumulative_prob'][1]:
            data['populations'][i] = data['populations'][2]
            print('Kromosom ke ' + str(i+1) + ' Diubah menjadi Kromosom ke 3')
        
        elif data['nilai_random'][i] > data['cumulative_prob'][0] and data['nilai_random'][i] < data['cumulative_prob'][1] and data['cumulative_prob'][2]:
            data['populations'][i] = data['populations'][1]
            print('Kromosom ke ' + str(i+1) + ' Diubah menjadi Kromosom ke 2')

        else :
            data['populations'][i] = data['populations'][0]
            print('Kromosom ke ' + str(i+1) + ' Diubah menjadi Kromosom ke 1')

    # Menghasilkan nilai kromosom baru
    print('Tess Population')
    print(len(data['populations']))
    data['NewKromosom'] = data['populations']
  
    return data['NewKromosom']

# 5
# Cross Over
def cross_over():
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

    parent1 = data['NewKromosom'][index1-1] #Dikurangi 1 karena index array biasa dimulai dari 0 sedangkan kromomosom ke 0 tidak ada
    parent2 = data['NewKromosom'][index2-1]

    print('Parents ke 1')
    print(parent1)

    print('Parents ke 2')
    print(parent2)
       
    # Mencari Cut Position
     #Banyak Kromosom dikali Banyak individu
    
    nilai_random = random.randint(1, panjang_kromosom) #Generate nilai antar 0-1
    print('Cut Position adalah : ' + str(nilai_random)) 
    # Mendefinisikan operasi crossover ke tool box
    toolbox.register("mate", cross_over)    
    crossover_point = nilai_random
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    # Mengubah nya menjadi new kromosom dan mengupdate object tersebut sesuai hasil Cross Over
    data['NewKromosom'][index1-1] = child1
    data['NewKromosom'][index2-1] = child2
    # Logika memasukkan kembali kromosom baruu setelah dimutasi ke object
 
    
    print("Nilai New Kromosom sekarang setelah di Cross Over : ")
    print(f"Nilai Kromosom {data['NewKromosom']}")
    # print(f" 1 {child1}")

    return child1, child2

# 5
# Mutation
def mutation():
    #Mutation rate misanya ditetapkan 25%
    # individu_awal = toolbox.individual()

    mutate_rate = 0.25
    jumlah_kromosom = len(data['NewKromosom']) 
    panjang_individu = len(data['NewKromosom'][0]) 
    ngen = jumlah_kromosom * panjang_individu
    #Untuk mencari jumlah mutasi dikalikan jumlah individu x dengan mutation rate nya, kemudian dibulatkan menggunakan round()
    jumlah_mutasi = round(mutate_rate * ngen) 
    # Generate nilai random sebanyak jumlah mutasi untuk index mutasi ditampung dalam array sebenyak jumlah_mutasi
    # Indeks yang akan dimutasi    
    index_mutasi = [random.randint(1, ngen) for _ in range(jumlah_mutasi)]
    
    
    toolbox.register("mutate", mutation)  # Operator mutasi tukar gen
    toolbox.register("select", tools.selTournament, tournsize=3)  # Operator seleksi turnamen
    
    # def create_individual():
    #     return [random.randint(1, 9), random.randint(1, 2), random.randint(1, 24) for _ in range(ngen)]

    
    
        # semua_kromosom.append(data['NewKromosom'][i])
    semua_kromosom = []
    for i in range(jumlah_kromosom):
        for j in range(panjang_individu):    
            semua_kromosom.append(data['NewKromosom'][i][j])


        
    print("Semua Panjang Kromosom : ")
    print(len(semua_kromosom))

    for idx in index_mutasi: 
        print(f"Nilai Kromosom dari index {idx} = {semua_kromosom[idx-1]}"  )
        # update_gen = generate_kromosom()
        semua_kromosom[idx] = generate_kromosom()
        print(f"Nilai Terbaru setelah dimutasi {semua_kromosom[idx-1]}"  )


    # Masukkan lagi ke dalam objek kromosom
    new_kromosom_mutasi = []
    for i in range(jumlah_kromosom): 
        array_2d =[]   
        # Tambahkan gen ke array list 2 dimensi
        for j in range(panjang_individu):
            array_2d.append(semua_kromosom[j])
        # Tambahkan array list 2 dimensi ke array list 3 dimensi
        new_kromosom_mutasi.append(array_2d) 

    data['last_kromosom_'] = new_kromosom_mutasi 
    print(new_kromosom_mutasi)
    # print('panjang array ' + str(len(new_kromosom_mutasi)))
    return new_kromosom_mutasi
    
   


    


    # Contoh penggunaan
if __name__ == "__main__":
    # Data masukan
        
    # Misalnya menGenerate populasi dengan 3 kromosom, masing-masing dengan 18 individu
     
    panjang_kromosom = len(subjects) * len(rooms)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)


    toolbox.register("individual", tools.initRepeat, creator.Individual, generate_kromosom, n=panjang_kromosom) 
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
   
    generate_kromosom()
    
    
    # nantinya fungsi ini menampung populasi
    get_pelanggaran()

    # Cetak hasil populasi dalam bentuk tabel
    population_size = 3
    population = toolbox.population(n=population_size)
    population_table = []

    # Cetak hasil populasi dalam bentuk tabel
    for i, chromosome in enumerate(population):
        population_table.append([f'Kromosom {i + 1}', *chromosome])
        data['populations'].append([*chromosome])
        
    #Menghitung Pelanggaran 
    get_pelanggaran()
    
    
    # headers = ['Kromosom', 'Gen 1', 'Gen 2', 'Gen 3', ...]  # Ganti dengan nama gen yang sesuai
    # print('Ini adalah Tabel dari dari setiap kromosom beserta nilai gennya : ')
    # print(tabulate(population_table, headers=headers, tablefmt='grid'))

    # data['tempKromosom1'] = population[0] 
    # data['tempKromosom2'] = population[1]
    # data['tempKromosom3'] = population[2]  
    # data['population_table'] = population_table

  
    
    print("Individu pada kromosom")
    print(f"Kromosom 1 :  { data['tempKromosom1'] }")
    print(f"Kromosom 2 :  { data['tempKromosom2'] }")
    print(f"Kromosom 3 :  { data['tempKromosom3'] }")      
    print('--------------')       
   # test print individu
    print(data['populations'][1])      
    print(f"Panjang individu : {len(data['populations'][1])}")      
    print('--------------')  


    # Cetak Nilai Fitness
    print('Ini adalah Fitness dari setiap kromosom : ')
    pelanggaran = [10, 7, 8] 
    hitung_fitness(pelanggaran)

        # Menghitung Probability Fitness
    print('Ini adalah Probabily Fitness dari setiap kromosom : ')
    probability_fitness()

    # Menghitung Comulative Probability Values
    print('Ini adalah Comulative Probability Fitness dari setiap kromosom : ')
    com_probability_fitness()


    # Nilai Random antara 0-1(Termasuk berkoma)
    generate_rand()
    
    # Seeleksi New Kromosom
    new_kromosom_seleksi()
    kromosom_baru = data['NewKromosom']
    print("Menampilkan Kromosom Baru")
    for i in range(len(kromosom_baru)):
        print(f"Kromosom baru ke {i + 1}: {kromosom_baru[i]}")

    # CrossOver
    # Femanggil fungsi penghitungan Crossover (One-point CrossOver)
    cross_over() 
    # toolbox.register("mate", cross_over)


    # Mutasi
    print("Ini adalah Hasil Mutasi : ") 
    mutation()

    # 


    
