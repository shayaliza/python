age = int(input("Enter your age: "))
day = str(input("Enter the day: "))

if(age >= 18):
    price = 12
elif(age >= 12):
    price = 8
else:
    price = -1

if(day == "wednesday"):
    final_price = price - 2
else:
    final_price = price


print(f"Your ticket price is {final_price}")