m1 = {'id':1,'nome':'com um brilhozinho nos olhos'}
m2 = {'id':2,'nome':'raven'}
print(m1,m2)
print(f'\n{m1}\n{m2}')

print(f'ID:{m1["id"]}')
print(f'Nome:{m1["nome"]}')

print(m1.keys())
print(m1.values())

m1['estilo']='Pop portuguesa'
m2['estilo']='Jazz contemporaneo'

musicas = [m1,m2]

# musicas.append(m1)
# musicas.append(m2)

print(musicas)

for musica in musicas:
    print(musica)
    print(f'ID:{musica["id"]}')
    print(f'Nome:{musica["nome"]}')
    print(f'Estilo:{musica["estilo"]}')

musicas.append({'id':3,'nome':'Welcome to the pleasure dome'})    
musicas[2]['estilo']='Brit Pop'

for musica in musicas:
    print(f'ID:{musica["id"]}')
    print(f'Nome:{musica["nome"]}')
#    print(f'Estilo:{musica["estilo"]}')


print('\nfiltrar listas')
for musica in musicas:
    if musica['estilo'] == 'Brit Pop':
        for chave,valor in musica.items():    
            print(f'{chave}:{valor}')

# apenas musicas brit pop