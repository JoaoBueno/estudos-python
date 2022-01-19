import random
import statistics
from fractions import Fraction as F
from decimal import Decimal as D

horas_dormidas_semana = [7, 8, 6, 0, 7, 7, 10]

print('Horas dormidas na semana: ', horas_dormidas_semana)

# médias ==>
print('Média : ', statistics.mean(horas_dormidas_semana))

# print(statistics.mean([F(8, 10), F(11, 20), F(2, 5), F(28, 5)]))
# # # returns Fraction(147, 80)

# print(statistics.mean([D("1.5"), D("5.75"), D("10.625"), D("2.375")]))
# # # returns Decimal('5.0625')

# data_points = [ random.randint(1, 100) for x in range(1,1001) ]
# print(statistics.mean(data_points))
 
# data_points = [ random.triangular(1, 100, 80) for x in range(1,1001) ]
# print(statistics.mean(data_points))

# médias <==

# modas ==>
print('Moda : ', statistics.mode(horas_dormidas_semana))

# data_points = [ random.randint(1, 100) for x in range(1,1001) ]
# print(statistics.mode(data_points))
# # returns 94
 
# data_points = [ random.randint(1, 100) for x in range(1,1001) ]
# print(statistics.mode(data_points))
# # returns 49
 
# data_points = [ random.randint(1, 100) for x in range(1,1001) ]
# print(statistics.mode(data_points))
# # returns 32
 
# # print(statistics.mode(["cat", "dog", "dog", "cat", "monkey", "monkey", "dog"]))
# # returns 'dog'

# modas <==

# medianas ==>
print('Mediana : ', statistics.median(horas_dormidas_semana))

# data_points = [ random.randint(1, 100) for x in range(1,50) ]
# print(statistics.median(data_points))
# # returns 53
 
# data_points = [ random.randint(1, 100) for x in range(1,51) ]
# print(statistics.median(data_points))
# # returns 51.0
 
# data_points = [ random.randint(1, 100) for x in range(1,51) ]
# print(statistics.median(data_points))
# # returns 49.0
 
# data_points = [ random.randint(1, 100) for x in range(1,51) ]
# print(statistics.median_low(data_points))
# # returns 50
 
# print(statistics.median_high(data_points))
# # returns 52
 
# print(statistics.median(data_points))
# # returns 51.0

# medianas <==

# variancia <==
print('Variância : ', statistics.variance(horas_dormidas_semana))
print('Variância : ', statistics.pvariance(horas_dormidas_semana))
# variancia <==
