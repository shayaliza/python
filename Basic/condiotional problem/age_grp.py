user_age = int(input("Enter your age: "))

if user_age < 18:
    print("kids")
elif user_age >= 18 and user_age <= 60:
    print("Adults")
else:
    print("seniors")