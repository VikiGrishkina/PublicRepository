count=int(input("Введите количество билетов: "))
sum=0
for i in range(count):
    age=int(input(f"Введите возраст {i+1} посетителя: "))
    if 18<=age<25:
        sum+=990
    elif age>=25:
        sum+=1390
if count>3:
    sum*=0.9
    print(f"Сумма к оплате c учетом скидки 10%: {sum} руб.")
else:
    print(f"Сумма к оплате: {sum} руб")
