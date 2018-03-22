import operator;
import random;
import numpy;
from numpy import sum;

# ------# Variaveis Globais
numAvalFitness = 0;  # condicao de parada, 10.000 avaliacoes de fitness

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
    for e in popI:
        print (e);
        print("fit: ", fitness(e));

    return;

def fitness(indiv):
    global numAvalFitness;
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
    return fit;

def geraFilhos(popI): #funcao que roda a iteracao do algoritmo evolutivo, chama funcoes de selecao de pais, crossover e mutacao
    filhos = [];
    parents = selectParents(popI);
    filhosB = intToBinPop(filhos); ## fazer crossover e mutacao com a representacao binaria
    ##filhosB = crossOver(parents); ## A implementar
    ##filhosB = mutation(filhos);   ## A implementar



    return filhos;

def selectParents(iniPop):
    parents =[];
    random.shuffle(iniPop);
    for e in iniPop:
        if(len(parents)<5):
            parents.append(e);
    parents = sorted(parents, key=fitness);
    parents = parents[3:]; #selecionando os dois melhores invididuos do conjunto de 5 aleatorios.

    return parents;

def crossOver(parents): #### A ser implementado ####
    crossChance = 0.9;
    filhos =[];

    return filhos;

def mutation(filhos): #### A ser implementado ####
    mutationChance =0.1;

    return filhos;

def selecaoPop(popI, filhos):#### A ser implementado ####
    ## funcao deve acomodar filhos na populacao e retirar os piores individuos ate que restem 100 individuos na populacao
    popSel =[];##retornar esta

    return popI;

def main(): ##popB -> populacao no formato binario, popI -> populacao no formato inteiro
    ##Inicializacao da populacao
    global numAvalFitness;
    condicaoParada = False;
    populationSize = 10;
    numGeracoes = 0;
    seed = seedGen();
    populationB = populate(populationSize, seed);
    populationI = binToIntPop(populationB);

    displayPop(populationI);


    #Etapa evolutiva
    while (condicaoParada != True and False):
        filhos = geraFilhos(populationI);
        populationI = selecaoPop(populationI,filhos);
        numGeracoes+=1;

        if(numAvalFitness>100):
            condicaoParada = True;
        displayPop(populationI);
        print("geracao: ", numGeracoes);

    return;



### funcoes de conversao de inteiro para binario e binario para inteiro implementadas mais em cima
main();

