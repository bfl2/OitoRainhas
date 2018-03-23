import operator;
import random;
import numpy;
from numpy import sum;

# ------# Variaveis Globais
numAvalFitness = 0;  # condicao de parada, 10.000 avaliacoes de fitness
maxFitness =0;

def bin3Gen(num):
    bin3 = [];
    while num > 1:
        bin3.append(num % 2);
        num = num // 2;
    bin3.append(num);
    while len(bin3) < 3:
        bin3.append(0);

    bin3.reverse();
    return bin3;


def seedGen():  # gera uma lista de numeros binarios com 3 casas de 0 a 7
    res = [];
    c = [];
    i = 0;
    while i < 8:
        c = bin3Gen(i);
        res.append(c);
        i += 1;
    return res;


def binToInt(bin):
    res = 0;
    res = bin[0] * 4 + bin[1] * 2 + bin[2] * 1;
    return res;


def binToIntIndiv(indivB):
    indivI = [];
    for e in indivB:
        indivI.append(binToInt(e));
    return indivI;


def binToIntPop(popB):
    popI = [];
    for e in popB:
        popI.append(binToIntIndiv(e));
    return popI;

def intToBinIndiv(indivI):
    indivB =[];
    for e in indivI:
        indivB.append(bin3Gen(e));

    return indivB;

def intToBinPop(popI):
    popB = [];
    for e in popI:
        popB.append(intToBinIndiv(e));
    return popB;


def populate(popSize, seed):
    pop = [];
    for e in range(0, popSize):
        indiv = random.sample(seed, len(seed));
        pop.append(indiv);
    return pop;


def displayPopBin(pop):
    for indiv in pop:
        for e in indiv:
            print(e);

        print('---@---');
    return;


def displayPop(popI):
    global numAvalFitness;
    for e in popI:
        print ("Indiv",popI.index(e)+1,":",e);
        print("fit: ", fitness(e));
        numAvalFitness-=1; #desprezado o calculo de fitness, pois este esta sendo recalculado

    return;

def fitness(indiv):
    global numAvalFitness;
    global maxFitness;
    numAvalFitness+= 1;
    colisoes = 0;
    indivx = indiv;
    flagM1 = [0] * 15;
    flagM2 = [0] * 15;
    checkDiag = [0, -1, -2, -3, -4, -5, -6, -7];
    checkDiag2 = [-7, -6, -5, -4, -3, -2, -1, 0];
    m1 = [sum(i) for i in zip(indivx, checkDiag)];
    m2 = [sum(i) for i in zip(indivx, checkDiag2)];
    for e in m1:
        flagM1[e + 7] += 1;
        if (flagM1[e + 7] > 1):
            colisoes += 1;
    for e in m2:
        flagM2[e + 7] += 1;
        if (flagM2[e + 7] > 1):
            colisoes += 1;

    fit = 1 / (1 + colisoes / 2);
    maxFitness = max(maxFitness, fit);

    return fit;

def geraFilhos(popI): #funcao que roda a iteracao do algoritmo evolutivo, chama funcoes de selecao de pais, crossover e mutacao
    filhos = [];
    parents = selectParents(popI);
    parentsB = intToBinPop(parents);
    filhosB = intToBinPop(filhos); ## fazer crossover e mutacao com a representacao binaria
    filhosB = crossOver(parentsB); ## A implementar
    filhosB = mutation(filhosB);   ## A implementar
    filhos = binToIntPop(filhosB);


    return filhos;

def selectParents(iniPop):
    parents =[];
    random.shuffle(iniPop);
    for e in iniPop:
        if(len(parents)<5):
            parents.append(e);
    parents = sorted(parents, key=fitness, reverse=True);
    parents = parents[:2]; #selecionando os dois melhores invididuos do conjunto de 5 aleatorios.

    return parents;
def geraIndiv(pai1,pai2,pontoCorte):#inputs e outputs em binario3
    indiv=[];
    checkMatrix = [0]*8;
    for e in pai1:
        i = e[0]*4 + e[1]*2 + e[2]*1;
        if len(indiv)<pontoCorte:#os individuos do pai1 sao o numero do ponto de corte
            checkMatrix[i] = 1;
            indiv.append(e);

    pai2 = pai2[pontoCorte:] + pai2[:pontoCorte];#rearranjando lista para comecar a partir do ponto de corte

    for k in pai2:# individuos do pai2 = 8 - ponto de corte
        if len(indiv)<=8:
            i = k[0]*4 + k[1]*2 +k[2]*1;
            if checkMatrix[i]==0:#numero disponivel, sem conflito de linha
                checkMatrix[i]=1;
                indiv.append(k);

    return indiv;

def crossOver(parents): #### DONE ####
    crossChance = 0.9;
    filhos =[];
    seed = random.randint(0,100);
    if(seed<crossChance*100):
        pontoCorte = random.randint(1,6);
        f1 = geraIndiv(parents[0],parents[1], pontoCorte);
        f2 = geraIndiv(parents[1], parents[0], pontoCorte);
        filhos.append(f1);
        filhos.append(f2);

    else: ### Quando nao ha crossover, os filhos sao os proprios pais
        filhos = parents;

    return filhos;

def mutation(filhos): #### A ser implementado ####
    mutationChance =0.1;
    filhosM = filhos;
    for e in filhosM:
        seed = random.randint(0, 100);
        if (seed < mutationChance * 100):
            ix = random.sample(range(0,7),2);
            e[ix[0]],e[ix[1]] = e[ix[1]],e[ix[0]]; #troca de numeros entre as colunas

    return filhosM;

def selecaoPop(popI, filhos):#### A ser implementado ####
    ## funcao deve acomodar filhos na populacao e retirar os piores individuos ate que restem 100 individuos na populacao
    global numAvalFitness;
    popRanked = sorted(popI+filhos, key=fitness);#populacao com 102 individuos ordenados pelo fitness
    numAvalFitness-=100;# reducao para compensar os fitness recalculados dos 100 individuos da populacao
    popRanked.reverse();
    popSel = popRanked[:-2];# populacao com a retirada dos 2 piores individuos
    return popSel;

def main(): ##popB -> populacao no formato binario, popI -> populacao no formato inteiro
    ##Inicializacao da populacao
    global numAvalFitness;
    condicaoParada = False;
    populationSize = 100;
    numGeracoes = 1;
    seed = seedGen();
    populationB = populate(populationSize, seed);
    populationI = binToIntPop(populationB);
    populationI = sorted(populationI, key=fitness,reverse=True);


    displayPop(populationI);


    #Etapa evolutiva
    while (condicaoParada != True):
        filhos = geraFilhos(populationI);
        populationI = selecaoPop(populationI,filhos);
        print("   geracao: ", numGeracoes, "max Fitness: ", maxFitness, "Num aval: ", numAvalFitness);
        numGeracoes += 1;
        if (numAvalFitness > 10000 or maxFitness == 1):
            condicaoParada = True;
            displayPop(populationI);
    print("|||-Individuo com maior fitness encontrado:",fitness(populationI[0]), "-", populationI[0]);
    return;



### funcoes de conversao de inteiro para binario e binario para inteiro implementadas mais em cima
main();