"""Viagens de avião — fase 1. Python 3.10+, apenas biblioteca padrão.
Dados em memória. Contactos/cartões: validação local simulada, sem banco.
"""
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_FLOOR
import re


def texto(pergunta):
    while True:
        valor = input(pergunta).strip()
        if valor:
            return valor
        print('O campo é obrigatório.')


def numero(pergunta, minimo=0, maximo=None, inteiro=False):
    while True:
        try:
            valor = Decimal(input(pergunta).strip().replace(',', '.'))
            if not valor.is_finite() or valor < minimo or (maximo is not None and valor > maximo):
                raise ValueError
            if inteiro and valor != valor.to_integral_value():
                raise ValueError
            return int(valor) if inteiro else valor
        except (InvalidOperation, ValueError):
            print('Número inválido ou fora dos limites.')


def data_hora(pergunta):
    while True:
        try:
            return datetime.strptime(input(pergunta).strip(), '%Y-%m-%d %H:%M')
        except ValueError:
            print('Use AAAA-MM-DD HH:MM, com uma data e hora válidas.')


def contacto(pergunta='Contacto (email): '):
    while True:
        valor = texto(pergunta)
        if re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', valor):
            return valor
        print('Email inválido.')


def menu(titulo, opcoes):
    print('\n' + titulo)
    for chave, descricao in opcoes.items():
        print(f'{chave} — {descricao}')
    while True:
        escolha = input('Opção: ').strip()
        if escolha in opcoes:
            return escolha
        print('Opção inválida.')


class Aplicacao:
    def __init__(self):
        self.companhias = {}
        self.aeroportos = {}
        self.passageiros = {}
        self.voos = {}
        self.reservas = {}

    def escolher(self, dados, rotulo):
        if not dados:
            raise ValueError(f'Não existem {rotulo}.')
        for chave, item in dados.items():
            print(chave, '—', item.get('nome', item.get('codigo', chave)))
        while True:
            chave = texto(f'Identificador de {rotulo} (0 para voltar): ').upper()
            if chave == '0':
                raise ValueError('Operação interrompida.')
            if chave in dados:
                return chave
            print('Identificador inexistente.')

    def companhia(self, alterar=False):
        codigo = self.escolher(self.companhias, 'companhias') if alterar else texto('Sigla: ').upper()
        if not alterar and (codigo == '0' or codigo in self.companhias):
            raise ValueError('Sigla reservada ou já existente.')
        dados = dict(nome=texto('Nome: '), pais=texto('País: '), tipo=texto('Tipo de companhia: '))
        dados['ativa'] = self.companhias[codigo]['ativa'] if alterar else True
        self.companhias[codigo] = dados
        print('Companhia guardada.')

    def aeroporto(self):
        codigo = texto('Código IATA (3 letras): ').upper()
        if not re.fullmatch('[A-Z]{3}', codigo) or codigo in self.aeroportos:
            raise ValueError('Código inválido ou já existente.')
        self.aeroportos[codigo] = dict(nome=texto('Nome: '), cidade=texto('Cidade: '), pais=texto('País: '))
        print('Aeroporto inserido.')

    def registar(self):
        nome = texto('Nome do utilizador: ')
        email = contacto()
        if any(p['contacto'].casefold() == email.casefold() for p in self.passageiros.values()):
            raise ValueError('Já existe um registo com este contacto.')
        print('Validação de contacto e cartão apenas simulada. Use dados fictícios.')
        # Não são recolhidos números completos de cartão nem códigos de segurança.
        while True:
            cartao = texto('Últimos 4 algarismos do cartão fictício: ')
            if re.fullmatch('[0-9]{4}', cartao):
                break
            print('Introduza quatro algarismos.')
        chave = str(len(self.passageiros) + 1)
        self.passageiros[chave] = dict(nome=nome, contacto=email, cartao_final=cartao)
        print('Passageiro registado. Identificador:', chave)

    def reservas_ativas(self, voo):
        return [r for r in self.reservas.values() if r['voo'] == voo and r['ativa']]

    def limite(self, voo, classe):
        return int((Decimal(voo['lugares'][classe]) * (1 + voo['overbooking'] / 100)).to_integral_value(rounding=ROUND_FLOOR))

    def livres(self, codigo, classe, excluir=None):
        ocupados = sum(r['ativa'] and r['voo'] == codigo and r['classe'] == classe and rid != excluir
                       for rid, r in self.reservas.items())
        return self.limite(self.voos[codigo], classe) - ocupados

    def voo(self, companhia, alterar=False):
        if not self.companhias[companhia]['ativa']:
            raise ValueError('A companhia está inativa.')
        if alterar:
            codigo = self.escolher({k: v for k, v in self.voos.items() if v['companhia'] == companhia and v['ativo']}, 'voos ativos da companhia')
            if self.reservas_ativas(codigo):
                raise ValueError('Não é possível alterar um voo com reservas ativas.')
        else:
            codigo = texto('Código único do voo: ').upper()
            if codigo == '0' or codigo in self.voos:
                raise ValueError('Código reservado ou já existente.')
        origem = self.escolher(self.aeroportos, 'aeroportos de origem')
        destino = self.escolher(self.aeroportos, 'aeroportos de destino')
        if origem == destino:
            raise ValueError('Origem e destino têm de ser diferentes.')
        partida = data_hora('Partida (AAAA-MM-DD HH:MM): ')
        chegada = data_hora('Chegada, no fuso da origem (AAAA-MM-DD HH:MM): ')
        if chegada <= partida or partida <= datetime.now():
            raise ValueError('A partida deve ser futura e a chegada posterior à partida.')
        diferenca = numero('Diferença horária destino − origem, em horas (-12 a 14): ', -12, 14)
        escalas = []
        for _ in range(numero('Número de escalas: ', 0, len(self.aeroportos) - 2, True)):
            aeroporto = self.escolher(self.aeroportos, 'aeroportos de escala')
            if aeroporto in [origem, destino] or any(e['aeroporto'] == aeroporto for e in escalas):
                raise ValueError('Escala repetida ou igual à origem/destino.')
            escalas.append(dict(aeroporto=aeroporto, minutos=numero('Duração da escala em minutos: ', 1, inteiro=True)))
        if sum(e['minutos'] for e in escalas) >= (chegada - partida).total_seconds() / 60:
            raise ValueError('A duração das escalas deve ser inferior à duração do voo.')
        lugares, precos = {}, {}
        for classe in ('turistica', 'executiva'):
            lugares[classe] = numero(f'Lugares {classe}: ', 0, inteiro=True)
            precos[classe] = numero(f'Preço {classe} (€): ', Decimal('0.01'))
        if sum(lugares.values()) == 0:
            raise ValueError('O voo tem de ter lugares.')
        overbooking = numero('Overbooking (%): ', 0, 100)
        tipo = menu('Tripulação', {'1': 'Da própria companhia', '2': 'Independente'})
        tripulacao = dict(companhia=companhia if tipo == '1' else None,
                          codigo=texto('Código da tripulação: '), capitao=texto('Nome do capitão: '))
        self.voos[codigo] = dict(codigo=codigo, companhia=companhia, origem=origem, destino=destino,
                                partida=partida, chegada=chegada, diferenca=diferenca, escalas=escalas,
                                lugares=lugares, precos=precos, overbooking=overbooking,
                                tripulacao=tripulacao, ativo=True)
        print('Voo guardado.')

    def disponivel(self, voo):
        return voo['ativo'] and self.companhias[voo['companhia']]['ativa'] and voo['partida'] > datetime.now()

    def mostrar_voo(self, codigo):
        v = self.voos[codigo]
        local = v['chegada'] + timedelta(hours=float(v['diferenca']))
        print(f"{codigo} | {v['companhia']} | {v['origem']} → {v['destino']} | "
              f"{v['partida']:%Y-%m-%d %H:%M} → {v['chegada']:%Y-%m-%d %H:%M} (fuso da origem) | "
              f"chegada local {local:%Y-%m-%d %H:%M} | duração {v['chegada'] - v['partida']} | "
              f"{'ativo' if v['ativo'] else 'anulado'}")
        for classe in v['lugares']:
            print(f"  {classe}: {v['precos'][classe]:.2f} €; {self.livres(codigo, classe)} reservas disponíveis")
        print('  Escalas:', v['escalas'] or 'sem escalas', '| Tripulação:', v['tripulacao'])

    def consultar(self, comparar=False):
        origem = self.escolher(self.aeroportos, 'aeroportos de origem')
        destino = self.escolher(self.aeroportos, 'aeroportos de destino')
        candidatos = [k for k, v in self.voos.items() if self.disponivel(v) and v['origem'] == origem and v['destino'] == destino
                      and any(self.livres(k, c) > 0 for c in v['lugares'])]
        while True:
            entrada = input('Data pretendida AAAA-MM-DD (Enter: todas): ').strip()
            try:
                objetivo = datetime.strptime(entrada, '%Y-%m-%d').date() if entrada else None
                break
            except ValueError:
                print('Data inválida.')
        if comparar:
            criterio = menu('Critério de comparação', {'1': 'Proximidade à data pretendida', '2': 'Duração', '3': 'Preço'})
            classe = self.classe()
            candidatos = [k for k in candidatos if self.livres(k, classe) > 0]
            if criterio == '1' and objetivo is None:
                raise ValueError('A comparação por data exige uma data pretendida.')
            def chave(k):
                v = self.voos[k]
                return {'1': abs((v['partida'].date() - objetivo).days) if objetivo else 0,
                        '2': (v['chegada'] - v['partida']).total_seconds(), '3': v['precos'][classe]}[criterio]
            candidatos.sort(key=lambda k: (chave(k), self.voos[k]['partida'], k))
            if candidatos:
                print('Sugestão segundo o critério escolhido:', candidatos[0])
        else:
            candidatos = [k for k in candidatos if objetivo is None or self.voos[k]['partida'].date() == objetivo]
            candidatos.sort(key=lambda k: self.voos[k]['partida'])
        for codigo in candidatos:
            self.mostrar_voo(codigo)
        if not candidatos:
            print('Não existem voos disponíveis para os critérios indicados.')

    def classe(self):
        return {'1': 'turistica', '2': 'executiva'}[menu('Classe', {'1': 'Turística', '2': 'Executiva (VIP)'})]

    def reserva(self, passageiro, alterar=False):
        if alterar:
            rid = self.escolher({k: r for k, r in self.reservas.items() if r['titular'] == passageiro and r['ativa']}, 'reservas ativas')
            if self.voos[self.reservas[rid]['voo']]['partida'] <= datetime.now():
                raise ValueError('Não é possível alterar reservas de voos já partidos.')
        else:
            rid = str(len(self.reservas) + 1)
        disponiveis = {k: v for k, v in self.voos.items() if self.disponivel(v)}
        for k in disponiveis:
            self.mostrar_voo(k)
        codigo = self.escolher(disponiveis, 'voos disponíveis')
        classe = self.classe()
        if self.livres(codigo, classe, rid if alterar else None) <= 0:
            raise ValueError('Não há disponibilidade nesta classe.')
        nome = texto('Nome completo da pessoa que viaja: ')
        documento = texto('Documento de identificação civil: ')
        email = contacto('Contacto da pessoa que viaja (email): ')
        while True:
            nif = texto('NIF (9 algarismos): ')
            if re.fullmatch('[0-9]{9}', nif):
                break
            print('O NIF deve ter nove algarismos (validação apenas de formato).')
        if any(k != rid and r['ativa'] and r['voo'] == codigo and r['documento'].casefold() == documento.casefold()
               for k, r in self.reservas.items()):
            raise ValueError('Esta pessoa já tem uma reserva ativa neste voo.')
        ementa = texto('Ementa pretendida: ') if classe == 'executiva' else None
        self.reservas[rid] = dict(titular=passageiro, voo=codigo, classe=classe, nome=nome,
                                  documento=documento, contacto=email, nif=nif, ementa=ementa,
                                  preco=self.voos[codigo]['precos'][classe], ativa=True)
        print('Reserva guardada. Identificador:', rid)

    def listar_reservas(self, companhia=None, passageiro=None):
        encontrou = False
        for rid, r in self.reservas.items():
            if companhia is not None and self.voos[r['voo']]['companhia'] != companhia:
                continue
            if passageiro is not None and r['titular'] != passageiro:
                continue
            encontrou = True
            print(f"Reserva {rid} | voo {r['voo']} | {r['nome']} | {r['classe']} | "
                  f"{r['preco']:.2f} € | {'ativa' if r['ativa'] else 'anulada'} | ementa: {r['ementa'] or '—'}")
        if not encontrou:
            print('Sem reservas.')

    def anular_voo(self, companhia):
        codigo = self.escolher({k: v for k, v in self.voos.items() if v['companhia'] == companhia and v['ativo']}, 'voos ativos da companhia')
        if self.reservas_ativas(codigo):
            raise ValueError('Não é possível anular um voo com reservas ativas.')
        self.voos[codigo]['ativo'] = False
        print('Voo anulado.')

    def anular_reserva(self, passageiro):
        rid = self.escolher({k: r for k, r in self.reservas.items() if r['titular'] == passageiro and r['ativa']}, 'reservas ativas')
        if self.voos[self.reservas[rid]['voo']]['partida'] <= datetime.now():
            raise ValueError('Não é possível anular reservas de voos já partidos.')
        self.reservas[rid]['ativa'] = False
        print('Reserva anulada; lugar libertado.')

    def gerir(self):
        while True:
            op = menu('Gestão da aplicação', {'1': 'Inserir companhia', '2': 'Alterar companhia', '3': 'Ativar/desativar companhia', '4': 'Inserir aeroporto', '5': 'Listar companhias e aeroportos', '0': 'Voltar'})
            if op == '0':
                return
            try:
                if op == '1': self.companhia()
                elif op == '2': self.companhia(True)
                elif op == '3':
                    k = self.escolher(self.companhias, 'companhias')
                    self.companhias[k]['ativa'] = not self.companhias[k]['ativa']
                    print('Estado ativo:', self.companhias[k]['ativa'])
                elif op == '4': self.aeroporto()
                else:
                    print('Companhias:', self.companhias)
                    print('Aeroportos:', self.aeroportos)
            except ValueError as erro:
                print('Aviso:', erro)

    def area_companhia(self):
        companhia = self.escolher(self.companhias, 'companhias')
        while True:
            op = menu(f'Companhia {companhia}', {'1': 'Inserir voo', '2': 'Alterar voo', '3': 'Anular voo', '4': 'Consultar reservas', '5': 'Listar voos', '0': 'Voltar'})
            if op == '0': return
            try:
                if op == '1': self.voo(companhia)
                elif op == '2': self.voo(companhia, True)
                elif op == '3': self.anular_voo(companhia)
                elif op == '4': self.listar_reservas(companhia=companhia)
                else:
                    for k, v in self.voos.items():
                        if v['companhia'] == companhia: self.mostrar_voo(k)
            except ValueError as erro:
                print('Aviso:', erro)

    def area_passageiro(self):
        op = menu('Entrada de passageiros', {'1': 'Registar passageiro', '2': 'Selecionar passageiro registado', '0': 'Voltar'})
        if op == '0': return
        if op == '1':
            self.registar()
            return
        passageiro = self.escolher(self.passageiros, 'passageiros')
        while True:
            op = menu(f"Passageiro: {self.passageiros[passageiro]['nome']}", {'1': 'Consultar voos', '2': 'Comparar voos', '3': 'Efetuar reserva', '4': 'Alterar reserva', '5': 'Anular reserva', '6': 'Consultar as minhas reservas', '0': 'Voltar'})
            if op == '0': return
            try:
                if op == '1': self.consultar()
                elif op == '2': self.consultar(True)
                elif op == '3': self.reserva(passageiro)
                elif op == '4': self.reserva(passageiro, True)
                elif op == '5': self.anular_reserva(passageiro)
                else: self.listar_reservas(passageiro=passageiro)
            except ValueError as erro:
                print('Aviso:', erro)

    def executar(self):
        print('VIAGENS DE AVIÃO — dados mantidos apenas nesta execução.')
        print('Seleção de perfil sem autenticação. Utilize dados fictícios.')
        try:
            while True:
                op = menu('Identifique o seu perfil', {'1': 'Gestão da aplicação', '2': 'Companhia de aviação', '3': 'Passageiro', '0': 'Sair'})
                if op == '0': break
                try:
                    if op == '1': self.gerir()
                    elif op == '2': self.area_companhia()
                    else: self.area_passageiro()
                except ValueError as erro:
                    print('Aviso:', erro)
        except (EOFError, KeyboardInterrupt):
            print('\nEntrada terminada.')
        print('Aplicação terminada. Os dados em memória foram descartados.')


if __name__ == '__main__':
    Aplicacao().executar()
