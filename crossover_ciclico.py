from random import randint


#   Receives a list of parents
def crossOver(parents):

    chance = randint(0, 9)
    children = []

    #   Return the child
    def cyclic_crossover(parent_0, parent_1):

        visitation_list = set({})
        p0 = parent_0[0]
        visitation_list.add(p0)

        cycle = False
        child = parent_1[:]

        #   Search a cycle
        while not cycle:

            p1 = parent_1[p0]
            p0 = parent_0[p1]

            if p0 not in visitation_list or p1 not in visitation_list:
                visitation_list.add(p0)
            else:
                cycle = True

        for i in visitation_list:
            child[parent_0.index(i)] = i

        return child

    #   If the crossover chance is satisfied then call the function, else return the parents
    if chance < 9:
        children.append(cyclic_crossover(parents[0], parents[1]))
        children.append(cyclic_crossover(parents[1], parents[0]))

    else:
        if chance < 9:
            children.append(parents[0])
            children.append(parents[1])

    return children


#   Testing algorithm
if __name__ == '__main__':

    print(crossOver([[0, 1, 2, 3, 4, 5, 6], [4, 3, 5, 6, 1, 2, 0]]))
    #   slide example
    print(crossOver([[0, 1, 2, 3, 4, 5, 6, 7, 8], [8, 2, 6, 7, 1, 5, 4, 0, 3]]))