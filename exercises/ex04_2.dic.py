ordet = {'id':1,'nome' : 'Ordet' }
everP = {'id':2,'nome': 'Ever Present'}

musicas = []
musicas.append(ordet)
musicas.append(everP)

# listar todas as musicas
print(musicas)

# listar musicas completas à vez
for musica in musicas:
    print(musica)

# listar os atributos de cada lista
for musica in musicas:
    for chave, valor in musica.items():
        print(f"{chave}: {valor}")

# passando aos artistas
KM = {'id':'KM001', 'nome':'Kham Meslien', 'origem':'FR'}

# podemos implementar a relação:
realizam = []

realizam.append({'musica':ordet,'artista':KM})
print(realizam)

# ou, se quisermos apenas parte dos dados:
for realiza in realizam:
    print(f'{realiza['artista']['nome']} interpreta "{realiza['musica']['nome']}"')

# Também podemos adicionar o artista à musica e vice-versa
ordet['artista']=KM
print(ordet)    
print(f'{ordet["artista"]['nome']} interpreta {ordet["nome"]}')



