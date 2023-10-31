import random
from deap import base, creator, tools
from prettytable import PrettyTable
from tabulate import tabulate








# Inisialisasi toolbox untuk memudahkan algoritma(Dari library Deap)
toolbox = base.Toolbox()



# Register fungsi-fungsi ke toolbox
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)




# (1)
# Representasi Kromosom & Data Awal 
subjects = [
    'Agama I', 'Pancasila', 'Bahasa Indonesia', 'Bahasa Inggris', 
    'Dasar-Dasar Sains dan Teknologi', 'Teknologi Informasi & Komunikasi', 
    'Fisika Dasar I', 'Kalkulus I', 'Kimia Dasar'] #Gen Mata Kuliah
rooms = ['R-001', 'R-002'] # Gen Kelas/Ruang
timeslots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

population_table = []

data = {
    'tempKromosom1' : [],
    'tempKromosom2' : [],
    'tempKromosom3' : [],
    'tempFitness': float,
    'tempProbFit' : float,
    'tempComFit' : float,
    'nilai_random': float,
    'cumulative_prob': []
}


# (2)
# Populasi Awal & Generate Kromosom
panjang_kromosom = len(subjects) * len(rooms)

# Fungsi untuk generate Kromosom
def generate_kromosom():
    
    population = toolbox.population(n=population_size)
    
    for i, chromosome in enumerate(population):
        population_table.append([f'Kromosom {i + 1}', *chromosome])
    return [random.choice(subjects), random.choice(rooms), random.choice(timeslots)]



# (3)
# Evaluasi Nilai Fitness
pelanggaran_kromosom = [10, 7, 8] #Nilai pelanggaran Masih hardcode, cuman contoh
# Definisikan kelas fitness dan individu

def hitung_fitness(pelanggaran):
    # logika pelanggaran
    # 
    return 1 / (1 + pelanggaran)

# Variabel menampung dalam array
fitness_kromosom = [hitung_fitness(p) for p in pelanggaran_kromosom]




# (4)
# Seleksi
# - Fungsi Untuk Menghitung Probility Fitness

def probability_fitness(): 
    total_fitness = sum(fitness_kromosom)
    probability_fitness = [fitness / total_fitness for fitness in fitness_kromosom]
    return probability_fitness
total_fitness = sum(fitness_kromosom)
probability_fitness = [fitness / total_fitness for fitness in fitness_kromosom]

# - Fungsi Untuk Menghitung Comulative Probility Fitness
def com_probability_fitness(): 
    cumulative_probabilities = [sum(probability_fitness[:i+1]) for i in range(len(probability_fitness))]
    for i, cumulative_prob in enumerate(cumulative_probabilities):
        print(f"Cumulative Probability Fitness individu {i + 1}: {cumulative_prob}")
    return cumulative_prob


#Fungsi untuk Generate 3 nilai random antara 0 dan 1 (berkoma)
def generate_rand():
    nilai_random = [random.random() for _ in range(3)]
    data['nilai_random'] = nilai_random
    # Cetak nilai random
    print("Nilai Random antara 0-1 pake data object:")
    print(data['nilai_random'])
    return nilai_random


# Kromosom baru dari membandingkan nilai random dengan Comulative Probility Fitness
def new_kromosom_seleksi():
      # Mengecek setiap nilai dalam nilai_random dengan cumulative_prob
    k = 0 
    if data['nilai_random'][2] > data['cumulative_prob'][2] and data['nilai_random'][1] > data['cumulative_prob'][1]:
        k = 3
    elif data['nilai_random'][1] > data['cumulative_prob'][1]:
        k = 2
    elif data['nilai_random'][0] > data['cumulative_prob'][0]:
        k = 1







toolbox.register("individual", tools.initRepeat, creator.Individual, generate_kromosom, n=panjang_kromosom) 
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
population_size = 3
population = toolbox.population(n=population_size)
individu = toolbox.individual
generate_kromosom()


# Contoh penggunaan
if __name__ == "__main__":
    # Data masukan
    
    # Misalnya menGenerate populasi dengan 3 kromosom, masing-masing dengan 18 individu
    # Register fungsi-fungsi ke toolbox untuk Populasi
    

# Cetak hasil populasi dalam bentuk tabel
# Ubah populasi menjadi daftar untuk tata letak tabel yang lebih rapi

    
   

# Cetak hasil populasi dalam bentuk tabel
    headers = ['Kromosom', 'Gen 1', 'Gen 2', 'Gen 3', ...]  # Ganti dengan nama gen yang sesuai
    print('Ini adalah Tabel dari dari setiap kromosom beserta nilai gennya : ')
    print(tabulate(population_table, headers=headers, tablefmt='grid'))


    # Cetak Nilai Fitness
    print('Ini adalah Fitness dari setiap kromosom : ')
    print(fitness_kromosom)

    # Menghitung Probability Fitness
    print('Ini adalah Probabily Fitness dari setiap kromosom : ')
    print(probability_fitness)

    # Menghitung Comulative Probability Values
    print('Ini adalah Comulative Probability Fitness dari setiap kromosom : ')
    print(com_probability_fitness)


    # Cetak cumulative probability fitness
    com_probability_fitness()

    # Nilai Random antara 0-1(Termasuk berkoma)
    generate_rand()
    # Menginisiasikan total fitness populasi

    # Menghitung probabilitas fitness untuk setiap individu


    # test print individu
    print("Individu pada kromosom")
    print(f"Kromosom 1 :  { population[0] }")
    print(f"Kromosom 2 :  { population[1] }")
    print(f"Kromosom 3 :  { population[2] }")
