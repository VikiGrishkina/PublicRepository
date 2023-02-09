per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
money=int(input('Введите сумму, которую планируете положить на вклад '))
deposit=[]
for value in list(per_cent.values()):
    deposit.append(int(value*money/100))
print('deposit = ',deposit)
print('Максимальная сумма, которую вы можете заработать — ',max(deposit))