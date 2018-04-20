import oitoRainhasv1 as v1
import oitoRainhasv2 as v2
import matplotlib.pyplot as plt
import numpy as np


def getLongestList(listOfLists):
    res = []
    for e in listOfLists:
        if(len(e)>len(res)):
            res = e
    return res

def swapLists(listOfList):
    swapedList = []
    aux=0
    maxLen = 0
    for e in listOfList:
        aux = maxLen
        maxLen = max(aux,len(e))
    print(maxLen)

    for e in range(maxLen):
        swapedList.append([])

    for e in listOfList:
        i = 0
        for t in e:
            swapedList[i].append(t)
            i+=1

    return swapedList

def avg(list):
    return sum(list)/len(list)

def avgAndStd(listOLists):
    swapedL = swapLists(listOLists)
    average = list(map(avg,swapedL))
    dev = list(map(np.std, swapedL))
    res = [average,dev]
    return res

def avalL(List):
    res = []
    for e in List:
        res.append(e[-1])
    return res

def plotGraphs(repetitions, CondParadaSel, version):
    nAvalLists =[]
    maxFitnessLists =[]
    avgFitnessLists = []
    k=0
    for e in range(repetitions):
        print(k)
        k+=1
        if(version==1):
            parameterList = v1.main(CondParadaSel,0)
        if(version==2):
            parameterList = v2.main(CondParadaSel,0)

        nAvalLists.append(parameterList["nAvalList"])
        maxFitnessLists.append( parameterList["maxFitnessList"])
        avgFitnessLists.append( parameterList["avgFitnessList"])
    nAvall = avalL(nAvalLists)
    nAvalAvg = sum(nAvall)/len(nAvall)
    nAvalStd = np.std(nAvall)

    nAvalMax = getLongestList(nAvalLists)
    [avgFitnesslAvg, avgFitnessStd] = avgAndStd(avgFitnessLists)
    x = nAvalMax
    y = avgFitnesslAvg
    e = avgFitnessStd

    plt.errorbar(x,y,e,ecolor="red")
    titulo = "Média e desvio padrão do fitness médio da versão 1 (" + str (repetitions) + " repetições)"
    plt.title(titulo)
    text = "Numero medio de avaliacoes: "+str(round(nAvalAvg,2))+"\n Desvio Padrao: "+ str(round(nAvalStd,2))
    plt.text(330,0.4,text)
    plt.ylabel("Average Fitness")
    plt.xlabel("Fitness Evaluations")
    plt.show()

    [maxFitnesslAvg, maxFitnessStd] = avgAndStd(maxFitnessLists)
    x = nAvalMax
    y = maxFitnesslAvg
    e = maxFitnessStd

    plt.errorbar(x, y, e, ecolor="red")
    titulo = "Média e desvio padrão do fitness máximo da versão 1 (" + str(repetitions) + " repetições)"
    plt.title(titulo)
    plt.ylabel("Max Fitness")
    plt.xlabel("Fitness Evaluations")
    plt.show()


    return

plotGraphs(30,1,2)

#print(getLongestList(a))