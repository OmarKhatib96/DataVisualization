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

import plotly.express as px

class network_visualization:
    def __init__(self):
        self.edge_number=0
        self.node_number=0
        self.data_edges=0
        self.data_controllable_nodes=0
        self.data_metrology_nodes=0
        self.data_FDC_nodes=0
        self.data_edges_numbers=None
        self.data_nodes=0
        self.liste_node=[]
        self.list_layer=0
        self.list_from=[]
        self.list_to=[]
        self.data_edges2=0
        self.controllable_node_list=[]
        self.metrology_node_list=[]
        self.FDC_node_list=[]

    def writing_csv(self,data_from,data_to):

        import csv
        with open('./data/edge_list2.csv', mode='w') as edge_list_numbers:  # edge_list2.csv: 
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

        self.data_edges=data_edges
        self.data_nodes=data_nodes
        list_node=[] # y3, y1, y2, u1, u2
        list_layer=[] # 0, 1, 1, 1, 1
        list_from=[] # u1, x1, x2, x3, x5
        list_to=[] # x1, x3, x3, y1, y1
        
        controllable_node_list=[]
        metrology_node_list=[]
        FDC_node_list=[]


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
        
        self.controllable_node_list=controllable_node_list
        print("controllable_node_list: "+ str(self.controllable_node_list))

        self.metrology_node_list=metrology_node_list
        print("metrology_node_list: "+ str(self.metrology_node_list))

        self.FDC_node_list=FDC_node_list
        print("FDC_node_list: "+ str(self.FDC_node_list))

        self.list_node=list_node
        print("list_node: "+ str(self.list_node))

        self.list_layer=list_layer
        print("list_layer: "+str(self.list_layer))

        self.list_from=list_from
        print("list_from: "+str(self.list_from))

        self.list_to=list_to
        print("list_to: "+str(self.list_to))

        self.writing_csv(self.list_from,self.list_to) # create edge_list2.csv
        self.data_edges2=pd.read_csv("./data/edge_list2.csv") # data_edges2: 
                                #(to, from)=(list_node.(list_to[0]),list_node.(list_to[0]))

    def adjacency_matrix(self):
        self.data_importing()
        matrix_dimension=len(self.list_node)  # 31 nodes
        print("matrix_dimension,list_node: "+str(matrix_dimension))
        edge_dimension=len(self.list_from) # 30 edges
        print("edge_dimension,list_from: "+str(edge_dimension))

        self.edge_number=edge_dimension
        self.node_number=matrix_dimension

        adjacency_matrix=np.zeros((matrix_dimension,matrix_dimension)) # 30*30


        for i in range(edge_dimension): # 30
            current_node_from=self.list_from[i] # list_from[0]=u1
            current_node_to=self.list_to[i] # list_to[0]=x1
            index_node_from=self.list_node.index(current_node_from) # list_node.index(u1)=3
            index_node_to=self.list_node.index(current_node_to) # list_node.index(x1)=5
            adjacency_matrix.itemset((index_node_from,index_node_to),1) # (3,5,1)
        return adjacency_matrix


    def network_representation(self):
        self.adjacency_matrix()
        N=len(self.data_edges2) # edge_list2.csv
        print("N="+str(N)) # N=30
        Edges=[(self.data_edges2['from'][k], self.data_edges2['to'][k]) for k in range(N)]
        print("Edges:"+str(Edges))
        G=ig.Graph(Edges, directed=False)

        labels=['x' for k in range(self.node_number)] # node_number=matrix_dimension=30
        layers=[-1 for k in range(self.node_number)] # initialization

        colors=[0 for k in range(self.node_number)] # init color

        for i in range(N):
            if self.list_node[i] in self.controllable_node_list:
                colors[i]=0
            if self.list_node[i] in self.FDC_node_list:
                colors[i]=1
            if self.list_node[i] in self.metrology_node_list:
                colors[i]=2  

        print('colors: '+str(colors))

        for k in range(N): # N=30
            labels[self.data_edges2['from'][k]]=self.list_node[self.data_edges2['from'][k]]
            # data_edges2['from'][0]= 5, labels[5]=list_node[5]=x1
            labels[self.data_edges2['to'][k]]=self.list_node[self.data_edges2['to'][k]]
            # data_edges2['to'][0]= 3, labels[3]=list_node[3]=u1

            layers[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]
            # data_edges2['from'][0]= 5, layers[5]=list_layer[5]=1
            layers[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
            # data_edges2['to'][0]= 3, layers[3]=list_layer[3]=1
        
        print('labels: '+str(labels))
        print('layers: '+str(layers))

        layt=G.layout('kk',dim=3)
        print('layt:'+str(layt))  # Layout with 31 vertices(nodes) and 3 dimensions

        Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
        Yn=[layt[k][1] for k in range(N)]# y-coordinates
        Zn=[0 for k in range(self.node_number)]# z-coordinates=0  # node_number = 30 

        Xe=[] # x-coordinates of edge ends
        Ye=[]
        Ze=[]

        for k in range(N):
            Zn[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]
            Zn[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
            # z-coordinates = 0 or 1  
        
        for e in Edges:
            Xe+=[layt[e[0]][0],layt[e[1]][0], None] # x-coordinates of edge, start=layt[e[0]][0], end=layt[e[1]][0] for the first edge
            Ye+=[layt[e[0]][1],layt[e[1]][1], None]
            Ze+=[Zn[e[0]],Zn[e[1]], None]

        import plotly.graph_objs as go

        trace1=go.Scatter3d(x=Xe,
                    y=Ye,
                    z=Ze,
                    mode='lines',
                    line=dict(color='rgb(125,125,125)', width=2.5),
                    hoverinfo='none'
                    )

        trace2=go.Scatter3d(x=Xn,
                    y=Yn,
                    z=Zn,
                    mode='markers',
                    name='parameters',
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

        layout = go.Layout(
                title="Data Visualization of the sample data of edge list",
                width=1000,
                height=1000,
                showlegend=False,
                scene=dict(
                    xaxis=dict(axis),
                    yaxis=dict(axis),
                    zaxis=dict(axis),
                ),
            hovermode='closest',
            annotations=[
                dict(
                showarrow=True,
                    text="Data source:Wei-Ting data sample",
                    xref='paper',
                    yref='paper',
                    x=0,
                    y=0.1,
                    xanchor='left',
                    yanchor='bottom',
                    font=dict(
                    size=14
                    )
                    )
                ],    )
        data=[trace1, trace2]
        data.append(go.Mesh3d(
        # 8 vertices of a cube
        x=[-4, 4, 4, -4, -4, 4, 4, -4],
        y=[-4, -4, 4, 4, -4, -4, 4, 4],
        z=[1, 1, 1, 1, 1, 1, 1, 1],
        colorbar_title='z',
        colorscale=[[0, 'gold'],
                    [0, 'mediumturquoise'],
                    [0, 'magenta']],
        # Intensity of each vertex, which will be interpolated and color-coded
        intensity = np.linspace(0, 1, 3, endpoint=True),
        # i, j and k give the vertices of triangles
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        name='Layer t',
        showlegend=True,
        opacity=0.2,


        showscale=False
    ))
        data.append(go.Mesh3d(
            # 8 vertices of a cube
            x=[-4, 4, 4, -4, -4, 4, 4, -4],
            y=[-4, -4, 4, 4, -4, -4, 4, 4],
            z=[0, 0, 0, 0, 0, 0, 0, 0],
            colorbar_title='z',
            colorscale=[[0, 'gold'],
                        [0.5, 'mediumturquoise'],
                        [1, 'magenta']],
            # Intensity of each vertex, which will be interpolated and color-coded
            intensity = np.linspace(0, 1, 1, endpoint=True),
            # i, j and k give the vertices of triangles
            i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],

            name='layer t-1',
            showscale=False,
            showlegend=True,
            opacity=0.2
        ))

        fig=go.Figure(data=data, layout=layout)

        print(" Please wait for the visualization...")
        plotly.offline.plot(fig, filename='Data-Visualization.html')
        print(" 3D visualization done...")

  



