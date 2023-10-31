
import random
from deap import base, creator, tools
import numpy as np
# from components.AlgoritmaGenetika import AlgoritmaGenetika
import json



# Mengambil data awal       
    
def get_pelanggaran(populasi):
    # print(len(populasi))
    pelanggaran = []
# Variabel untuk menyimpan pelanggaran untuk setiap kromosom

    pelanggaran_batasan1 = 0
    pelanggaran_batasan2 = 0
    #iterasi melalui populasi
    for i, data_kromosom in enumerate(populasi):
        
        
        tempData1 = [[ sublist[1], sublist[2]] for sublist in data_kromosom ] #mengambil gen kelas/ruang dan gen waktu
        tempData2 = [[ sublist[0], sublist[1]] for sublist in data_kromosom ] #mengambil gen kuliah dan gen ruang kelas/ruang

        print('tempData 1 ', tempData1)
        print('tempData 2 ', tempData2)


        temp_cek1 = [list(t) for t in set(tuple(element) for element in tempData1)]
        pelanggaran_batasan1 = len(tempData1) - len(temp_cek1)


        # Menampung nilai array yang akan dihilangkan jika terdapat nilai duplikat
        temp_cek2 = [list(t) for t in set(tuple(element) for element in tempData2)]
        pelanggaran_batasan2 = len(tempData2) - len(temp_cek2)

        print("Pelanggaran batasan 1 :" , pelanggaran_batasan1)
        print("Pelanggaran batasan 2 :" , pelanggaran_batasan2)
        pelanggaran_per_kromosom = pelanggaran_batasan1+pelanggaran_batasan2

        print('pelanggaran Kromosom ke ', i+1, 'adalah ')
        print(pelanggaran_per_kromosom)

        pelanggaran.append(pelanggaran_per_kromosom)

    print(pelanggaran)
    return pelanggaran
        # print(f"Tes Populasi {data['tempFitness']} ")

    
# objek = Pelanggaran()
