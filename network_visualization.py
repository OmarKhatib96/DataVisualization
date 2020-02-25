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
            if self.list_node[3]==data_from[0]:
                print('oui')
            print((self.list_node[3]))
            print((data_from[0]))   
            for i in range (len(data_from)):
                edge_writer.writerow([self.list_node.index(data_from[i]),self.list_node.index(data_to[i])])


         
        

    def data_importing(self):
        data_nodes=pd.read_csv("./data/node_list.csv")
        data_edges=pd.read_csv("./data/edge_list.csv")
        self.data_edges=data_edges
        self.data_nodes=data_nodes
        #print(data.head())
        list_node=[]
        list_layer=[]
        list_from=[]
        list_to=[]
        for node in data_nodes['node_name']:
            list_node.append(node)
        for layer in data_nodes[' layer']:
            list_layer.append(layer)
        for from_node in data_edges['from']:
            list_from.append(from_node)

        for to_node in data_edges['to']:
            list_to.append(to_node)
        
        
        self.list_node=list_node
        self.list_layer=list_layer
        self.list_from=list_from
        self.list_to=list_to
        self.writing_csv(self.list_from,self.list_to)
        self.data_edges2=pd.read_csv("./data/edge_list2.csv")

    def adjacency_matrix(self):
        self.data_importing()
        matrix_dimension=len(self.list_node)
        edge_dimension=len(self.list_from)
        self.edge_number=edge_dimension
        self.node_number=matrix_dimension
        

        adjacency_matrix=np.zeros((matrix_dimension,matrix_dimension))

    
        print(adjacency_matrix)
        #Adj=np.array(adjacency_matrix)

        #print(Adj)

        for i in range(edge_dimension):
            current_node_from=self.list_from[i]
            current_node_to=self.list_to[i]
            print(current_node_to)
            index_node_from=self.list_node.index(current_node_from)
            #print(index_node_from)
            index_node_to=self.list_node.index(current_node_to)
            adjacency_matrix.itemset((index_node_from,index_node_to),1)

        return adjacency_matrix


    #print(adjacency_matrix())

    def network_representation(self):
        self.adjacency_matrix()
        N=len(self.data_edges2)
        Edges=[(self.data_edges2['from'][k], self.data_edges2['to'][k]) for k in range(N)]
        G=ig.Graph(Edges, directed=False)
        layt=G.layout('kk',dim=3)
        print(layt[5])
        Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
        Yn=[layt[k][1] for k in range(N)]# y-coordinates
        Zn=[layt[k][2] for k in range(N)]# z-coordinates
        Xe=[]
        Ye=[]
        Ze=[]
        for e in Edges:
            Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
            Ye+=[layt[e[0]][1],layt[e[1]][1], None]
            Ze+=[layt[e[0]][2],layt[e[1]][2], None]

                
        import plotly.graph_objs as go

        trace1=go.Scatter3d(x=Xe,
                    y=Ye,
                    z=Ze,
                    mode='lines',
                    line=dict(color='rgb(125,125,125)', width=1),
                    hoverinfo='none'
                    )

        trace2=go.Scatter3d(x=Xn,
                    y=Yn,
                    z=Zn,
                    mode='markers',
                    name='actors',
                    marker=dict(symbol='circle',
                                    size=6,
                                    colorscale='Viridis',
                                    line=dict(color='rgb(50,50,50)', width=0.5)
                                    ),
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
            margin=dict(
                t=100
            ),
            hovermode='closest',
            annotations=[
                dict(
                showarrow=False,
                    text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
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
        fig=go.Figure(data=data, layout=layout)

        plotly.offline.plot(fig, filename='Data-Visualization.html')

  



