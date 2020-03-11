import plotly as plotly
import plotly.graph_objs as graph_objs
import pandas as pd
import plotly
import matplotlib.pyplot as plt 
from plotly.graph_objs import Scatter, Layout
from plotly import tools
import plotly.figure_factory as ff
import csv
import time
import numpy as np
import igraph as ig
#For animations


class network_visualization:


    def __init__(self):
        self.edge_number=0
        self.node_number=0
        self.data_edges=0
        self.data_edges_numbers=None
        self.data_nodes=0
        self.liste_node=[]
        self.list_layer=0
        self.list_from=[]
        self.list_to=[]
        self.data_edges2=0

    def writing_csv(self,data_from,data_to):

        import csv
        with open('./data/edge_list2.csv', mode='w') as edge_list_numbers:
            edge_writer = csv.writer(edge_list_numbers, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fieldnames = ['to', 'from']
            edge_writer.writerow(fieldnames)
            for i in range (len(data_from)):
                edge_writer.writerow([self.list_node.index(data_from[i]),self.list_node.index(data_to[i])])
            # data_from[0]=list_from[0]=u1, list_node.index(data_from[0])=3
            # data_to[0]=list_to[0]=x1, list_node.(data_to[0])=5
            # edge_list2.row[0]=(3,5)
        

    def data_importing(self):

        data_nodes=pd.read_csv("./data/node_list.csv")
        data_edges=pd.read_csv("./data/edge_list.csv")
        data_controllable_nodes=pd.read_csv("./data/controllable_node.csv")
        data_metrology_nodes=pd.read_csv("./data/metrology_node.csv")
        data_FDC_nodes=pd.read_csv("./data/FDC_node.csv")

        controllable_node_list=[]
        metrology_node_list=[]
        FDC_node_list=[]


        self.data_edges=data_edges
        self.data_nodes=data_nodes

        list_node=[] # y3, y1, y2, u1, u2
        list_layer=[] # 0, 1, 1, 1, 1
        list_from=[] # u1, x1, x2, x3, x5
        list_to=[] # x1, x3, x3, y1, y1

        for node in data_nodes['node_name']:
            list_node.append(node)
        for layer in data_nodes[' layer']:
            list_layer.append(layer)
        for from_node in data_edges['from']:
            list_from.append(from_node)

        for to_node in data_edges['to']:
            list_to.append(to_node)
        
        for controllable_node in data_controllable_nodes['controllable_node']:
            controllable_node_list.append(controllable_node)
        for metrology_node in data_metrology_nodes['metrology_node']:
            metrology_node_list.append(metrology_node)
        for FDC_node in data_FDC_nodes['FDC_node']:
            FDC_node_list.append(FDC_node)

        self.list_node=list_node
        print("node_list: "+str(self.list_node))

        self.list_layer=list_layer
        print("list_layer: "+str(self.list_layer))

        self.list_from=list_from
        print("list_from: "+str(self.list_from))

        self.list_to=list_to
        print("list_to: "+str(self.list_to))


        self.writing_csv(self.list_from,self.list_to)  # create edge_list2.csv
        self.data_edges2=pd.read_csv("./data/edge_list2.csv")   #(to, from)=(list_node.(list_to[0]),list_node.(list_to[0]))

        self.controllable_node_list=controllable_node_list
        print("controllable_node_list: "+ str(self.controllable_node_list))

        self.metrology_node_list=metrology_node_list
        print("metrology_node_list: "+ str(self.metrology_node_list))

        self.FDC_node_list=FDC_node_list
        print("FDC_node_list: "+ str(self.FDC_node_list))



    def adjacency_matrix(self):
        self.data_importing()

        matrix_dimension=len(self.list_node)
        print("matrix_dimension,list_node: "+str(matrix_dimension))

        edge_dimension=len(self.list_from)
        print("edge_dimension,list_from: "+str(edge_dimension))

        self.edge_number=edge_dimension
        self.node_number=matrix_dimension
        adjacency_matrix=np.zeros((matrix_dimension,matrix_dimension))


        for i in range(edge_dimension):
            current_node_from=self.list_from[i]
            current_node_to=self.list_to[i]
            index_node_from=self.list_node.index(current_node_from)
            index_node_to=self.list_node.index(current_node_to)
            adjacency_matrix.itemset((index_node_from,index_node_to),1)

        return adjacency_matrix


    def network_representation(self):

        self.adjacency_matrix()
        N=len(self.data_edges2)
        Edges=[(self.data_edges2['from'][k], self.data_edges2['to'][k]) for k in range(N)]
        print("Edges: "+str(Edges))

        G=ig.Graph(Edges, directed=True)
        labels=['x' for k in range(self.node_number)]

        layers=[-1 for k in range(self.node_number)] # initialization
        colors=[0 for k in range(self.node_number)] # init color

        for i in range(self.node_number):
            if self.list_node[i] in self.controllable_node_list:
                colors[i]=0
            if self.list_node[i] in self.FDC_node_list:
                colors[i]=1
            if self.list_node[i] in self.metrology_node_list:
                colors[i]=2  

        print('list_node: '+str(self.list_node))


        for k in range(N):
            labels[self.data_edges2['from'][k]]=self.list_node[self.data_edges2['from'][k]]
            # data_edges2['from'][0]= 5, labels[5]=list_node[5]=x1
            labels[self.data_edges2['to'][k]]=self.list_node[self.data_edges2['to'][k]]
            # data_edges2['to'][0]= 3, labels[3]=list_node[3]=u1
            layers[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
            # data_edges2['from'][0]= 5, layers[5]=list_layer[5]=1
            layers[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]
            # data_edges2['to'][0]= 3, layers[3]=list_layer[3]=1

        layt=G.layout('kk',dim=3)

        print('labels: '+str(labels))
        print("node_number: "+str(self.node_number))         # node_number = 32     

        Xn=[layt[k][0] for k in range(self.node_number)]    # x-coordinates of nodes                       
        print("x-coordinates of nodes: "+str(Xn))           
        Yn=[layt[k][1] for k in range(self.node_number)]    # y-coordinates 
        print("y-coordinates of nodes: "+str(Yn))
        Zn=[0 for k in range(self.node_number)]             # z-coordinates


        # modify t0 nodes' posotion x,y
        list_node_t=[]
        list_node_t0=[]
        for k in self.list_node:
            if 't0' in k:
                list_node_t0.append(k) 
            else:
                list_node_t.append(k) 
        print("list_node_t: "+str(list_node_t))
        for i in list_node_t:  
            Xn[self.list_node.index(i+'_t0')]=Xn[self.list_node.index(i)]
            Yn[self.list_node.index(i+'_t0')]=Yn[self.list_node.index(i)]
        print("Xn_modified: " + str(Xn))
        print("Yn_modified: " + str(Yn))
        # modify t0 nodes' posotion x,y   

        Xe=[] # x-coordinates of edges ends
        Ye=[] 
        Ze=[]

        print("data_edges2: "+str(self.data_edges2))

        for k in range(N):
            Zn[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]
            Zn[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
            # z-coordinates = 0 or 1 
        print("z-coordinates of nodes: "+str(Zn))
 
        for e in Edges:
            Xe+=[layt[e[0]][0],layt[e[1]][0], None] # x-coordinates of edge start, ends, None
            Ye+=[layt[e[0]][1],layt[e[1]][1], None]
            Ze+=[Zn[e[0]],Zn[e[1]], None]

        print("Xe:" +str(Xe))
        print("Ye:" +str(Ye))
        print("Ze:" +str(Ze))



        data_edges_t0=pd.DataFrame(columns=['to', 'from'])
        data_edges_t=pd.DataFrame(columns=['to', 'from'])
        data_edges_from_t0_to_t = pd.DataFrame(columns=['to', 'from'])
        index_edges_t0 = []
        index_edges_t = []
        index_edges_from_t0_to_t = []

        for k in range(len(self.data_edges)):
            if 't0' in self.data_edges.iloc[k]['to'] and 't0' in self.data_edges.iloc[k]['from']:
                index_edges_t0.append(k)
                data_edges_t0=data_edges_t0.append({'to': self.data_edges.iloc[k]['to'], 'from': self.data_edges.iloc[k]['from']},ignore_index=True)
            if 't0' not in self.data_edges.iloc[k]['to'] and 't0' not in self.data_edges.iloc[k]['from']:
                index_edges_t.append(k)
                data_edges_t=data_edges_t.append({'to': self.data_edges.iloc[k]['to'], 'from': self.data_edges.iloc[k]['from']},ignore_index=True)
            if 't0' in self.data_edges.iloc[k]['from'] and 't0' not in self.data_edges.iloc[k]['to']:
                index_edges_from_t0_to_t.append(k)
                data_edges_from_t0_to_t=data_edges_from_t0_to_t.append({'to': self.data_edges.iloc[k]['to'], 'from': self.data_edges.iloc[k]['from']},ignore_index=True)
        
        print(data_edges_from_t0_to_t)
        print(index_edges_from_t0_to_t)



        # modify t0 intra edges
        for k in index_edges_t:
            old_index = k  #0
            old_index_from = k*3 #0
            old_index_to = k*3+1 #1
            new_index = self.data_edges[(self.data_edges['from'] == self.data_edges.iloc[k]['from']+'_t0')
                           & (self.data_edges['to'] == self.data_edges.iloc[k]['to']+'_t0')].index.tolist()[0]  #14
            new_index_from = new_index*3 #42
            new_index_to = new_index*3+1 #43
            #print(old_index,old_index_from,old_index_to,new_index,new_index_from,new_index_to)
            #print(Xe[old_index_from], Xe[old_index_to])
            Xe[new_index_from]=Xe[old_index_from]
            Xe[new_index_to]=Xe[old_index_to]
            #print(Xe[new_index_from], Xe[new_index_to])
            Ye[new_index_from]=Ye[old_index_from]
            Ye[new_index_to]=Ye[old_index_to]
        # modify t0 intra edges



        for k in index_edges_from_t0_to_t:
            lenA = len(self.data_edges[(self.data_edges['from'] == self.data_edges.iloc[k]['from'])   #y1_t0,y1
                         & (self.data_edges['to'] != self.data_edges.iloc[k]['to']+'_t0')].index)
            lenB = len(self.data_edges[(self.data_edges['to'] == self.data_edges.iloc[k]['from'])
                         & (self.data_edges['from'] != self.data_edges.iloc[k]['to']+'_t0')].index)
            old_index = k
            old_index2 = k*3+1
            if lenA>1:
                new_index = self.data_edges[(self.data_edges['from'] == self.data_edges.iloc[k]['from'])   
                         & (self.data_edges['to'] != self.data_edges.iloc[k]['to']+'_t0')].index.tolist()[0]   
                new_index2 = new_index*3
                
            else:
                new_index=self.data_edges[(self.data_edges['to'] == self.data_edges.iloc[k]['from'])  # x3_to y1_t0
                         & (self.data_edges['from'] != self.data_edges.iloc[k]['to']+'_t0')].index.tolist()[0]
                new_index2 = new_index*3+1

            print("old_index: "+str(old_index)+" old_index2:"+str(old_index2)+" new_index: "+str(new_index)+" new_index_2: "+str(new_index2))
            
            print(Xe[old_index2],Xe[new_index2])
            Xe[old_index2] = Xe[new_index2]
            Ye[old_index2] = Ye[new_index2]
            print(Xe[old_index2],Xe[new_index2])


                
        import plotly.graph_objs as go

        # plot edges
        trace1=go.Scatter3d(x=Xe,
                    y=Ye,
                    z=Ze,
                    mode='lines',
                    name='Interaction between parameters',
                    line=dict(color='rgb(125,125,125)', width=2.5),
                    hoverinfo='none'
                    )

        # plot nodes
        trace2=go.Scatter3d(x=Xn,   
                    y=Yn,
                    z=Zn,
                    mode='markers',
                    name='Parameters',
                    marker=dict(symbol='circle',
                                    size=15,
                                    color=colors,
                                    colorscale='Viridis',
                                    line=dict(color='rgb(50,50,50)', width=4)
                                    ),
                    text=labels,
                    hoverinfo='text'
                    )

        axis=dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )
       

      
        data=[trace1, trace2]
        data.append(go.Mesh3d(
        # 8 vertices of a cube  # plot layer t
        x=[-10, 10, 10, -10, -10, 10, 10, -10],
        y=[-10, -10, 10, 10, -10, -10, 10, 10],
        z=[1, 1, 1, 1, 1, 1, 1, 1],
        colorbar_title='z',
        colorscale=[[0, 'blue'],
                    [0.5, 'blue'],
                    [1, 'blue']],
        # Intensity of each vertex, which will be interpolated and color-coded
        intensity = np.linspace(0, 1, 3, endpoint=True),
        # i, j and k give the vertices of triangles
        name='Layer t',
        showlegend=True,
        opacity=0.2,


        showscale=False
    ))
        data.append(go.Mesh3d(
           
            # 8 vertices of a cube  # plot layer t-1
            x=[-10, 10, 10, -10, -10, 10, 10, -10],
            y=[-10, -10, 10, 10, -10, -10, 10, 10],
            z=[0, 0, 0, 0, 0, 0, 0, 0],
            colorbar_title='z',
            colorscale=[[0, 'red'],
                        [0.5, 'red'],
                        [1, 'red']],
            # Intensity of each vertex, which will be interpolated and color-coded
            intensity = np.linspace(0, 1, 1, endpoint=True),
           

            name='Layer t-1',
            showscale=False,
            showlegend=True,
            opacity=0.2
        ))
        
        layout = go.Layout(
            annotations=[
            dict(
            showarrow=True,
                text="Data source: Wei-Ting data sample",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                
                font=dict(
                size=17
                )
                )
            ],
            scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis)),
            title="Data Visualization of the sample data of edge list",

        )
        fig=go.Figure(data=data, layout=layout)

        print(" Please wait for the visualization...")
        plotly.offline.plot(fig, filename='Layers Visualization.html')
        print(" 3D visualization done...")

  



