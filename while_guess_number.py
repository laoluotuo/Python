number = 23
running = True

while running:
    guess = int(input("Please enter your number:"))

    if guess == number:
        print('Congratulations!')
        running = False
    elif guess < number:
        print('Lower!')
    else:
        print("highter!")
else:
    print('While is over')
