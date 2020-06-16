import sys
import time

#uncomment this if running directly on the IDE (change the filename or provide proper path if the .txt file not in the same folder as .py file)
# filename = 'input2_undirected.txt'

# uncomment this part if to be run through command line - run like python dijkstra.py filename.txt  
# if len(sys.argv) < 2:
#     sys.exit("Filename not given. Please refer the README.txt for the list of file names.")
# else:
#     filename = sys.argv[1]

#Function to insert elements into a heap.
def heapInsert(a,elem):
    n= len(a)
    a.append(elem)
    i=n
    while i>1 and a[i//2]>a[i]:
        a[i],a[i//2] = a[i//2],a[i]
        i = i//2
    return a

#Function to remove the minimum element at the root of a heap.
def removeMin(a,itr):
    n = len(a)
    n = n-itr
    temp = a[1]
    a[1] = a[n]
    n = n-1
    i=1
    while i<n:
        L = 2*i
        R = (2*i)+1
        if (R) <= n:                               #if True, this node has two internal children
            if a[i] <= a[L] and a[i] <= a[R]:
                return temp                        #heap order maintained
            else:
                if a[R] < a[L]:
                    j=R
                elif a[L] <= a[R]:
                    j=L
                a[i],a[j] = a[j],a[i]              #swap whichever child node is smaller of the two
                i=j
        else:                                      #this node has zero or one internal child
            if (L) <= n:                           #if True, this node has one internal child node
                if a[i] > a[L]:
                    a[i],a[L] = a[L],a[i]
            return temp
    return temp

#Function to get the key for a given value of a dictionary.
def get_key(val):
    global dist
    for key,value in dist.items():
        if value == val:
            if key in visited:
                continue
            return key
    return None

#Function to relax the edges.
def relax(min_d, adj_d , adj_w):
    global dist
    if adj_d > min_d + adj_w:
        adj_d = min_d + adj_w
        return adj_d
    else:
        return adj_d

#Function to find parent of a given vertex.
def findParent(v, source):
    p = parent[v]
    if p!=source:
        if p not in path:
            path.append(p)
        res=findParent(p,source)
    return path

def dijkstra(filename):
    file = open(filename)
    line = file.readlines()
    content = [l.strip('\n').split() for l in line]
    n = len(content)-1
    if len(content[n]) != 1:
        print("Source not given in the file.")
        print("Enter the source vertex for the graph.")
        source = input()
        print()
        edges=[]
        if content[0][2] == 'D':
            for i in range(1,len(content)):
                edges.append(content[i])
        if content[0][2] == 'U':
            for i in range(1,len(content)):
                elem=[]
                elem.append(content[i][0])
                elem.append(content[i][1])
                elem.append(content[i][2])
                edges.append(elem)
                elem=[]
                elem.append(content[i][1])
                elem.append(content[i][0])
                elem.append(content[i][2])
                edges.append(elem)
    else:
        source = content[n][0]
        edges=[]
        if content[0][2] == 'D':
            for i in range(1,len(content)-1):
                edges.append(content[i])
        if content[0][2] == 'U':
            for i in range(1,len(content)-1):
                elem=[]
                elem.append(content[i][0])
                elem.append(content[i][1])
                elem.append(content[i][2])
                edges.append(elem)
                elem=[]
                elem.append(content[i][1])
                elem.append(content[i][0])
                elem.append(content[i][2])
                edges.append(elem)

#Dictionary to keep track of order of vertices -- vert.
    c=1
    vert = {}
    for i in range(len(edges)):
        for j in range(2):
            if edges[i][j] not in vert:
                vert[edges[i][j]] = None
    sort = sorted(vert.keys())
    for v in sort:
        vert[v] = c
        c+=1

#Initialize distance of each vertex from the source; ~infinity initially -- dist.
    global dist
    dist = {}
    for v in vert:
        if v == source:
            dist[v] = 0
        else:
            dist[v] = sys.maxsize

#Initialze parent to each vertex; None initially -- parent.
    global parent
    parent = {}
    for v in vert:
        parent[v] = None

#Create adjacency list for each vertex along with the weights.
    adj = {}
    tail_w = {}
    for v in vert:
        for elem in edges:
            if elem[0] == v:
                if elem[0] not in adj.keys():
                    key=[]
                    val=[]
                    tail_w = {}
                    key = elem[1]
                    val = elem[2]
                    tail_w[key] = val
                    adj[v] = tail_w
                else:
                    key=[]
                    val=[]
                    add = adj[v]
                    key = elem[1]
                    val = elem[2]
                    adj[v][key] = val
#     print("Adjacency list with weights: ")
#     print(adj)
#     print()

#Global variable to keep track of the visited nodes
    global visited
    visited=[]

    d=[]
    for v in vert:
        d.append(dist[v])

#Insert the initial d values into heap
    a=[]
    a.append(None)
    for i in range(len(d)):
        a=heapInsert(a,d[i])

    for itr in range(1, len(a)):
        min_d = removeMin(a,itr)
        for key,value in dist.items():
            if min_d == value:
                min_vert = get_key(min_d)
        for key in adj.keys():
            if min_vert == key:
                adj_vert = adj[key]
                for key_vert in adj_vert:
                    if key_vert not in visited:
                        adj_w = adj_vert[key_vert]
                        adj_d = dist[key_vert]
                        new_d = relax(int(min_d), int(adj_d), int(adj_w))
                        if new_d < adj_d:
                            dist[key_vert] = new_d          #update new d value in dist dictionary
                            parent[key_vert] = min_vert     #update parent of the relaxed vertex
                        idx = vert[key_vert]
                        a[idx] = new_d
                        b = []
                        b.append(None)
                        for i in range(1,len(a)):
                            b=heapInsert(b,a[i])
                        a=b
                visited.append(min_vert)
                break
            else:
                visited.append(min_vert)

    print("Cost: ", dist)
    print("Parent: ", parent)
    print()
    print("Source = ", source)
    print("Path from source")

    global path
    for v in vert:
        if v != source:
            if parent[v] == None:
                print("Path does not exist for", v)
                continue
            path=[]
            path = findParent(v,source)
            n=len(path)-1
            print(source,"->", end=" ")
            while(n>=0):
                print(path[n],"->", end=" ")
                n-=1
            print(v, " | PathCost = ", dist[v])
    print()

start_time = time.process_time()
dijkstra(filename)
end_time = time.process_time()

total_runtime = end_time - start_time
print("Runtime: ", total_runtime)
