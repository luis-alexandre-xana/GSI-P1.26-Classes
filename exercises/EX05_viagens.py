# cada uma das versões resolve o mesmo problema mas de maneiras diferentes
# V1: dicionário para menus
# V2: menus em print individualizads e validação com um linha IF e 'OR'
# V3: menus em print individualizads e validação com ELIF
# V4: lista para menus
# o problema em mãos é criar uma interface de utilizador por sucessão de menus em linha de comandos
## Opção 1
print(f'\nOPÇÃO 1\n- menus em dicionário\n')
menu={"1":"Administração","2":"Companhia","3":"Passageiro","0":"Sair"}
menuadm={"1":"Adicionar Companhia","2":"Listar Companhias","3":"Apagar Companhia","0":"Voltar"}
opcao = None
while opcao != "0":
    print("\nMENU PRINCIPAL\n")
    for indice,desc in menu.items():
        print(f'{indice} - {desc}')

    opcao = input("escolha uma opção >")

    if opcao not in menu:
        print(f'opção {opcao} não é valida')
    else:
        print(f'opção {opcao} é valida')

    if opcao == "1":
        print(f'\nMENU {menu[opcao].upper}')   
        opcao = None
        while opcao != "0":
            for indice,desc in menuadm.items():
                print(f'{indice} - {desc}')

            opcao = input("escolha uma opção >")

            if opcao not in menuadm:
                print(f'opção {opcao} não é valida')
            else:
                print(f'opção {opcao} é valida')
        opcao = None

## Opção 2
print(f'\nOPÇÃO 2\n- menus em print individual; validação com 1 linha IF\n')
opcao = None

while opcao !=0:
    print("1 - Administração")
    print("2 - Companhia")
    print("3 - Passageiro")
    print("0 - Sair")

    opcao = input("escolha uma opção >")

    if opcao.isnumeric():
        opcao = int(opcao)   
    else:
        print(f'opção {opcao} não é valida')

    if opcao==0 or opcao==1 or opcao==2 or opcao==3:
        print(f'opção {opcao} é valida')
    else:
        print(f'opção {opcao} não é valida')

## Opção 3
print(f'\nOPÇÃO 3\n- menus em print individual; validação em sequência de ELIF\n')
opcao = None

while opcao !=0:
    print("1 - Administração")
    print("2 - Companhia")
    print("3 - Passageiro")
    print("0 - Sair")

    opcao = input("escolha uma opção >")

    if opcao.isnumeric():
        opcao = int(opcao)   
    else:
        print(f'opção {opcao} não é valida')

    if opcao==0: 
        print(f'opção {opcao} é valida')
    elif opcao==1:
        print(f'opção {opcao} é valida')
    elif opcao==2:
        print(f'opção {opcao} é valida')
    elif opcao==3:
        print(f'opção {opcao} é valida')
    else:
        print(f'opção {opcao} não é valida')

## Opção 4
print(f'\nOPÇÃO 4\n- menus em lista\n')
menu = ["1 - Administração","2 - Companhia","3 - Passageiro","0 - Sair"]
menuadm=["1 - Adicionar Companhia","2 - Listar Companhias","3 - Apagar Companhia","0 - Voltar"]
opcao = None

while opcao !=0:
    for m in menu:
        print(m)
    opcao = input("escolha uma opção >")

    if opcao.isnumeric():
        opcao = int(opcao)   
    else:
        print(f'opção {opcao} não é valida')

    if opcao==0: 
        print(f'opção {opcao} é valida')
    elif opcao==1:
        
        opcao = None

        while opcao !=0:
            for m in menuadm:
                print(m)
            opcao = input("escolha uma opção >")

            if opcao.isnumeric():
                opcao = int(opcao)   
            else:
                print(f'opção {opcao} não é valida')
        opcao = None

    elif opcao==2:
        print(f'opção {opcao} é valida')
    elif opcao==3:
        print(f'opção {opcao} é valida')
    else:
        print(f'opção {opcao} não é valida')
