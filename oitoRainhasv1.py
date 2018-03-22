import operator;
import random;
import numpy;
from numpy import sum;


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


def binToIntIndiv(binI):
    indiv = [];
    for e in binI:
        indiv.append(binToInt(e));
    return indiv;


def binToIntPop(popB):
    popI = [];
    for e in popB:
        popI.append(binToIntIndiv(e));
    return popI;


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


# ------# Variaveis Globais
numFitnessAval = 0;  # condicao de parada, 10.000 avaliacoes de fitness


def fitness(indiv):
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

def evolve(pop): #funcao que roda a iteracao do algoritmo evolutivo, chama funcoes de selecao de pais, crossover e mutacao
    parents = selectParents(pop);

    return parents;

def selectParents(iniPop):
    parents =[];
    random.shuffle(iniPop);
    print("=========");

    for e in iniPop:
        if(len(parents)<5):
            parents.append(e);
    parents = sorted(parents, key=fitness);
    parents = parents[3:]; #selecionando os dois melhores
    for e in parents:
        print("fit*: ", fitness(e));
    return parents;

def main():
    populationSize = 10;
    seed = seedGen();
    populationB = populate(populationSize, seed);
    populationI = binToIntPop(populationB);
    populationI = evolve(populationI);
    print("----");
    displayPopBin(populationB);
    displayPop(populationI);
    return;


main();

