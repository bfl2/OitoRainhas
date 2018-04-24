import operator
import random
from random import randint
import numpy 
from numpy import sum
import pygame, sys

from pygame.locals import *

#-------# Nesta versao, a representacao adotada e a de uma lista de numeros inteiros, o codigo nao deve utilizar a representacao anterios do vetor de 24 bits. Funcoes de conversao entre binario e inteiro foram removidas.
# ------# Variaveis Globais
numAvalFitness = 0   # condicao de parada, 10.000 avaliacoes de fitness ou individuo com fitness 1 encontrado
maxFitness =0 

def seedGen():  # gera uma lista de numeros binarios com 3 casas de 0 a 7
    res = [] 
    i = 0 
    while i < 8:
        res.append(i) 
        i += 1 
    return res 

def populate(popSize, seed):
    pop = [] 
    for e in range(0, popSize):
        indiv = random.sample(seed, len(seed)) 
        pop.append(indiv) 
    return pop 


def displayPop(popI):
    global numAvalFitness 
    for e in popI:
        print ("Indiv",popI.index(e)+1,":",e, "fit: ", fitnessC(e))

    return 

def fitnessC(indiv):
    global numAvalFitness 
    global maxFitness 
    colisoes = 0 
    indivx = indiv 
    flagM1 = [0] * 15 
    flagM2 = [0] * 15 
    checkDiag = [0, -1, -2, -3, -4, -5, -6, -7] 
    checkDiag2 = [-7, -6, -5, -4, -3, -2, -1, 0] 
    m1 = [sum(i) for i in zip(indivx, checkDiag)] 
    m2 = [sum(i) for i in zip(indivx, checkDiag2)] 
    for e in m1:
        flagM1[e + 7] += 1 
        if (flagM1[e + 7] > 1):
            colisoes += 1 
    for e in m2:
        flagM2[e + 7] += 1 
        if (flagM2[e + 7] > 1):
            colisoes += 1
    for t in range(0, 8):
        count = 0
        for k in indiv:
            if (t == k):
                count += 1
                if (count > 1):
                    colisoes += 1

    fit = round(1 / (1 + colisoes / 2),3)
    maxFitness = max(maxFitness, fit)
    if(indiv == []):
        fit = 0
    return fit
def fitness(indiv):
    global numAvalFitness
    global maxFitness
    numAvalFitness+= 1
    return fitnessC(indiv)
def getFitnessAvg(pop):
    fitList =[]
    global numAvalFitness
    for e in pop:
        fitList.append(fitnessC(e))
    avg = sum(fitList)/len(fitList)
    return avg

def geraFilhos(popI,avgFit): #funcao que roda a iteracao do algoritmo evolutivo, chama funcoes de selecao de pais, crossover e mutacao
    filhos = []
    parents = selectParents(popI)
    filhos = crossOver(parents)
    filhos = mutation(filhos,avgFit)
    return filhos

def roullete(pop):
    fitnessList =[]

    for e in pop:
        fitnessList.append(fitnessC(e))
    listSum = sum(fitnessList)
    slot = []
    while(not slot):
        seed = random.uniform(0, 1) * listSum
        acumulator = 0
        i = 0
        for e in fitnessList:

            if( acumulator >= seed and  acumulator <= seed + e): #
                slot = pop[i]
                #print("max:",listSum, " intervalo", seed,"-",seed+e, " acum:",acumulator,slot, " fit: ", e, "index:", i)
                break
            acumulator += e
            i += 1

    return slot

def selectParents(iniPop):
    global numAvalFitness
    parents =[]
    while(len(parents)<2):
        candidate = roullete(iniPop)
        if(candidate not in parents):
            parents.append(candidate)

    print("   parents", parents)

    return parents
def geraIndiv(pai1,pai2,pontoCorte):#inputs e outputs em binario3
    indiv=[]
    checkMatrix = [0]*8
    for i in pai1:

        if len(indiv)<pontoCorte:#os individuos do pai1 sao o numero do ponto de corte
            checkMatrix[i] = 1
            indiv.append(i)

    pai2 = pai2[pontoCorte:] + pai2[:pontoCorte] #rearranjando lista para comecar a partir do ponto de corte

    for i in pai2:# individuos do pai2 = 8 - ponto de corte
        if len(indiv)<=8:
            if checkMatrix[i]==0:#numero disponivel, sem conflito de linha
                checkMatrix[i]=1
                indiv.append(i)

    return indiv


def crossOverC(parents):
    aux = [0] * 8
    filhos = []
    cycle = []
    cycles = []

    pai1 = parents[0][:]
    pai2 = parents[1][:]

    for i in range(0, len(aux)):

        if aux[i] == 0:
            pos = i
            index = -1

            while index != i:
                index = pai1.index(pai2[pos])
                aux[index] = 1
                pos = index
                cycle.append(index)

            cycles.append(cycle)
            cycle = []

    filhos.append(pai1)
    filhos.append(pai2)

    for i in range(0, len(cycles)):
        if (i + 1) % 2 == 0:
            for j in range(0, len(cycles[i])):
                filhos[0][cycles[i][j]], filhos[1][cycles[i][j]] = filhos[1][cycles[i][j]], filhos[0][cycles[i][j]]

    return filhos

def crossOver(parents):
    crossChance = 1
    filhos =[]
    seed = random.randint(0,99)
    if(seed<crossChance*100):
        pontoCorte = random.randint(1,6)
        f1 = geraIndiv(parents[0],parents[1], pontoCorte)
        f2 = geraIndiv(parents[1], parents[0], pontoCorte)
        filhos.append(f1)
        filhos.append(f2)

    else: ### Quando nao ha crossover, os filhos sao os proprios pais
        filhos = parents

    return filhos


def mutationI(individuo, avgFit):
    cut1 = cut2 = random.randint(1, 6)

    while cut1 == cut2:
        cut2 = random.randint(1, 6)

    if cut1 > cut2:
        cut1, cut2 = cut2, cut1

    individuoNovo = individuo[0:cut1 + 1] + [individuo[cut2]] + individuo[cut1 + 1: cut2] + individuo[cut2 + 1: 8]

    return individuoNovo

def mutation(filhos,avgFit):
    mutationChance = 0.5
    filhosM = filhos
    for e in filhosM:
        seed = random.randint(0, 100)
        if (seed < mutationChance * 100):
            ix = random.sample(range(0,7),2)
            e[ix[0]],e[ix[1]] = e[ix[1]],e[ix[0]]  #troca de numeros entre as colunas
    if(maxFitness<1):
        for e in filhosM:
            seed = random.randint(0, 100)
            if (seed < mutationChance * 100):
                ix = random.sample(range(0, 7), 2)
                e[ix[0]], e[ix[1]] = e[ix[1]], e[ix[0]]  # troca de numeros entre as colunas

    return filhosM

def selecaoPopSub(popI,avgFit):
    ## funcao acomoda filhos na populacao e retirar os piores individuos ate que restem 100 individuos na populacao
    global numAvalFitness
    filhos = geraFilhos(popI,avgFit)
    popRanked = sorted(popI+filhos, key=fitnessC) #populacao com 102 individuos ordenados pelo fitness
    numAvalFitness+=2 # 2 novos fitness calculados
    popRanked.reverse()
    popSel = popRanked[:-2] # populacao com a retirada dos 2 piores individuos
    return popSel

def selecaoPopGer(pop, avgFit):
    percFilhos = 1.00
    nextGen =[]
    while(len(nextGen) < len(pop)*percFilhos):
        filhos = geraFilhos(pop,avgFit)
        nextGen.append(filhos[0])
        nextGen.append(filhos[1])

    print("-----NextGen",nextGen)
    return nextGen

def displayChessBoard(chessBoard):
    WHITE = [255, 255, 255]
    GRAY = (100, 100, 100)
    BLACK = (0, 0, 0)
    RED = (255,0,0)
    pygame.init()
    tileSize = 50
    offsetx = 200
    offsety = 50
    DISPLAY = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption('Problema das Oito Rainhas')
    DISPLAY.fill(GRAY)
    for x in range(0, 8):
        for y in range(0, 8):
            if (x + y) % 2 == 0:
                cor = WHITE
            else:
                cor = BLACK
            pygame.draw.rect(DISPLAY, cor, (offsetx + x * tileSize, offsety + y * tileSize, tileSize, tileSize))
            pygame.display.update()
    for y in chessBoard:
        x = chessBoard.index(y)
        pygame.draw.circle(DISPLAY,RED,(offsetx + 25 + x*tileSize,offsety + 25 +y*tileSize),25,0)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    return

def main(sel, displayCBFlag): # popI -> populacao no formato inteiro #sel -> condicao de parada: 0: Max fitness=1, 1: avg fitness=1,
    global numAvalFitness
    global maxFitness
    avgFitness = 0
    tipoSelecao = "Sub"
    numAvalFitness = 0
    maxFitness = 0
    limiteAval = 10000
    condicaoParada = False
    populationSize = 30
    numGeracoes = 1
    nAvalList = []
    maxFitnessList = []
    avgFitnessList = []
    ##Inicializacao da populacao
    seed = seedGen() 
    populationI =  populate(populationSize, seed) 
    populationI = sorted(populationI, key=fitness,reverse=True) 
    displayPop(populationI) 
    #Etapa evolutiva
    while (condicaoParada != True):

        if(tipoSelecao == "Sub" ):
            populationI = selecaoPopSub(populationI,avgFitness)
        if(tipoSelecao == "Ger"):
            populationI = selecaoPopGer(populationI,avgFitness)
            populationI = sorted(populationI, key=fitness, reverse=True)

        avgFitness = getFitnessAvg(populationI) 
        print("   geracao: ", numGeracoes, "max Fitness: ",maxFitness," avg Fitness: ", avgFitness, "Num aval: ", numAvalFitness) 
        numGeracoes += 1
        nAvalList.append(numAvalFitness)
        maxFitnessList.append(maxFitness)
        avgFitnessList.append(avgFitness)
        if ((numAvalFitness > limiteAval) or (maxFitness == 1 and sel) or (avgFitness == 1 and not sel)):
            condicaoParada = True 
            displayPop(populationI) 
    print("||Avaliacoes ",numAvalFitness,"||-Individuo com maior fitness encontrado:",fitness(populationI[0]), "-", populationI[0], " Fitness medio da populacao:", avgFitness) 
    if(displayCBFlag):
        displayChessBoard(populationI[0])
    parametersDict = {"nAvalList": nAvalList, "maxFitnessList": maxFitnessList, "avgFitnessList": avgFitnessList}
    return parametersDict