import igraph


'''
def create_heap(array, ary):
    for i in range(len(array)-1, 1, -1):
        j = i
        while((array[j] > array[(j-1)//ary]) and j > 0):
            temp = array[j]
            array[j] = array[(j-1)//ary]
            array[(j-1)//ary] = temp
            j = (j-1)//ary

    return array
'''


def create_heap(array, ary):
    heap = []
    for node in array:
        heap = insert_node(heap, ary, node)
    return heap


def insert_node(heap, ary, node):
    heap.append(node)
    index = len(heap) - 1
    if index == 0:
        return heap
    while heap[index] > heap[(index-1)//ary]:
        temp = heap[index]
        heap[index] = heap[(index-1)//ary]
        heap[(index-1)//ary] = temp
        index = (index-1)//ary
        if index == 0:
            return heap
    return heap


def draw_heap(heap, ary, outfile):
    g = igraph.Graph.Tree(len(heap), ary)
    g.vs["label"] = heap
    g.vs["label_size"] = 16

    layout = g.layout("rt", root=[0])
    igraph.plot(g, outfile,
                layout=layout,
                bbox=(2400, 1200),
                vertex_color="green",
                vertex_size=32)
