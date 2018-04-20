import operator 
import random 
import numpy 
from numpy import sum 
import pygame, sys
from pygame.locals import *

# ------# Variaveis Globais
numAvalFitness = 0   # condicao de parada, 10.000 avaliacoes de fitness ou individuo com fitness 1 encontrado
maxFitness =0 

def bin3Gen(num):
    bin3 = [] 
    while num > 1:
        bin3.append(num % 2) 
        num = num // 2 
    bin3.append(num) 
    while len(bin3) < 3:
        bin3.append(0) 

    bin3.reverse() 
    return bin3 


def seedGen():  # gera uma lista de numeros binarios com 3 casas de 0 a 7
    res = [] 
    c = [] 
    i = 0 
    while i < 8:
        c = bin3Gen(i) 
        res.append(c) 
        i += 1 
    return res 


def binToInt(bin):
    res = 0 
    res = bin[0] * 4 + bin[1] * 2 + bin[2] * 1 
    return res 


def binToIntIndiv(indivB):
    indivI = [] 
    for e in indivB:
        indivI.append(binToInt(e)) 
    return indivI 


def binToIntPop(popB):
    popI = [] 
    for e in popB:
        popI.append(binToIntIndiv(e)) 
    return popI 

def intToBinIndiv(indivI):
    indivB =[] 
    for e in indivI:
        indivB.append(bin3Gen(e)) 

    return indivB 

def intToBinPop(popI):
    popB = [] 
    for e in popI:
        popB.append(intToBinIndiv(e)) 
    return popB 


def populate(popSize, seed):
    pop = [] 
    for e in range(0, popSize):
        indiv = random.sample(seed, len(seed)) 
        pop.append(indiv) 
    return pop 


def displayPopBin(pop):
    for indiv in pop:
        for e in indiv:
            print(e) 

        print('---@---') 
    return 


def displayPop(popI):
    global numAvalFitness 
    for e in popI:
        print ("Indiv",popI.index(e)+1,":",e) 
        print("fit: ", fitness(e)) 
        numAvalFitness-=1  #desprezado o calculo de fitness, pois este esta sendo recalculado

    return 

def fitness(indiv):
    global numAvalFitness 
    global maxFitness 
    numAvalFitness+= 1 
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

    fit = 1 / (1 + colisoes / 2) 
    maxFitness = max(maxFitness, fit) 

    return fit 
def getFitnessAvg(pop):
    fitList =[] 
    global numAvalFitness 
    for e in pop:
        fitList.append(fitness(e)) 
        numAvalFitness-=1  ##desconsiderar o calculo de fitness refeito
    avg = sum(fitList)/len(fitList) 
    return avg 

def geraFilhos(popI): #funcao que roda a iteracao do algoritmo evolutivo, chama funcoes de selecao de pais, crossover e mutacao
    filhos = [] 
    parents = selectParents(popI) 
    parentsB = intToBinPop(parents) 
    filhosB = intToBinPop(filhos) 
    filhosB = crossOver(parentsB) 
    filhosB = mutation(filhosB) 
    filhos = binToIntPop(filhosB) 


    return filhos 

def selectParents(iniPop):
    global numAvalFitness 
    parents =[] 
    random.shuffle(iniPop) 
    for e in iniPop:
        if(len(parents)<5):
            parents.append(e) 
    parents = sorted(parents, key=fitness, reverse=True) 
    numAvalFitness-=5 
    parents = parents[:2]  #selecionando os dois melhores invididuos do conjunto de 5 aleatorios.

    return parents 
def geraIndiv(pai1,pai2,pontoCorte):#inputs e outputs em binario3
    indiv=[] 
    checkMatrix = [0]*8 
    for e in pai1:
        i = e[0]*4 + e[1]*2 + e[2]*1 
        if len(indiv)<pontoCorte:#os individuos do pai1 sao o numero do ponto de corte
            checkMatrix[i] = 1 
            indiv.append(e) 

    pai2 = pai2[pontoCorte:] + pai2[:pontoCorte] #rearranjando lista para comecar a partir do ponto de corte

    for k in pai2:# individuos do pai2 = 8 - ponto de corte
        if len(indiv)<=8:
            i = k[0]*4 + k[1]*2 +k[2]*1 
            if checkMatrix[i]==0:#numero disponivel, sem conflito de linha
                checkMatrix[i]=1 
                indiv.append(k) 

    return indiv 

def crossOver(parents): #### DONE ####
    crossChance = 0.9 
    filhos =[] 
    seed = random.randint(0,100) 
    if(seed<crossChance*100):
        pontoCorte = random.randint(1,6) 
        f1 = geraIndiv(parents[0],parents[1], pontoCorte) 
        f2 = geraIndiv(parents[1], parents[0], pontoCorte) 
        filhos.append(f1) 
        filhos.append(f2) 

    else: ### Quando nao ha crossover, os filhos sao os proprios pais
        filhos = parents 

    return filhos 

def mutation(filhos):
    mutationChance =0.4 
    filhosM = filhos 
    for e in filhosM:
        seed = random.randint(0, 100) 
        if (seed < mutationChance * 100):
            ix = random.sample(range(0,7),2) 
            e[ix[0]],e[ix[1]] = e[ix[1]],e[ix[0]]  #troca de numeros entre as colunas

    return filhosM 

def selecaoPop(popI, filhos):
    ## funcao acomoda filhos na populacao e retirar os piores individuos ate que restem 100 individuos na populacao
    global numAvalFitness 
    popRanked = sorted(popI+filhos, key=fitness) #populacao com 102 individuos ordenados pelo fitness
    numAvalFitness-=100 # reducao para compensar os fitness recalculados dos 100 individuos da populacao
    popRanked.reverse() 
    popSel = popRanked[:-2] # populacao com a retirada dos 2 piores individuos
    return popSel 

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

def main(sel): ##sel=1 -> maxFitness //sel=0 -> avgFitness ##popB -> populacao no formato binario, popI -> populacao no formato inteiro
    global numAvalFitness
    global maxFitness
    numAvalFitness = 0
    maxFitness = 0
    limiteAval = 10000 
    condicaoParada = False 
    populationSize = 100 
    numGeracoes = 1
    ##Inicializacao da populacao
    seed = seedGen() 
    populationB = populate(populationSize, seed) 
    populationI = binToIntPop(populationB) 
    populationI = sorted(populationI, key=fitness,reverse=True)
    nAvalList = []
    maxFitnessList =[]
    avgFitnessList = []

    displayPop(populationI) 


    #Etapa evolutiva
    while (condicaoParada != True):

        filhos = geraFilhos(populationI) 
        populationI = selecaoPop(populationI,filhos) 
        avgFitness = getFitnessAvg(populationI) 
        print("   geracao: ", numGeracoes, "max Fitness: ",maxFitness," avg Fitness: ", avgFitness, "Num aval: ", numAvalFitness) 
        numGeracoes += 1
        nAvalList.append(numAvalFitness)
        maxFitnessList.append(maxFitness)
        avgFitnessList.append(avgFitness)
        if ((numAvalFitness > limiteAval) or (maxFitness  == 1 and sel) or (avgFitness == 1 and not sel) ):
            condicaoParada = True 
            displayPop(populationI) 


        
    print("|||-Individuo com maior fitness encontrado:",fitness(populationI[0]), "-", populationI[0]) 
    #displayChessBoard(populationI[0])
    parametersDict ={"nAvalList":nAvalList, "maxFitnessList":maxFitnessList, "avgFitnessList":avgFitnessList}

    return parametersDict

### funcoes para dar display no tabuleiro
#main(1)