import random, math
lmin,lmax = 1,100
numbertoguess = random.randint(lmin,lmax)  

# guess = input(f"adivinha o numero entre {lmin} e {lmax}: -->")

# print(f'valor inserido: {guess}, do tipo ({type(guess).__name__})')
# print(f'{guess.isnumeric()} ;{guess.isdecimal()}')
guess = ""
attempt = 0
tentativas = []

while (guess != numbertoguess and guess != 'end'):
    guess = input(f"adivinha o numero entre {lmin} e {lmax}: -->")
    guess = guess.strip()

    try:
        guess = int(guess)          # Só esta linha é que tem potencial de erro       
        tentativas.append(guess) # adiciona a última tentativa ao fim da lista de tentativas
        
        if (guess > numbertoguess):
            print("mais baixo")
        elif (guess < numbertoguess):
            print("mais alto")
        else:
            print("acertou") 
    except Exception as ex:
        if guess != 'end':
            print(f'O valor "{guess}" não é um número válido: {type(ex).__name__}: {ex}')
    finally:
        attempt += 1 # equivalente a attempt = attempt + 1
        print(f'valor inserido "{guess}" à {attempt}ª tentativa')  
   

# fim do while

if (guess == 'end'):
    print(f'desitiu ao fim de {attempt} tentativas')
else:
    print(f'acertou no numero {numbertoguess} em {attempt} tentativas')
    print(tentativas)
for tentativa in tentativas:
    print(tentativa)