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


         
        

    def data_importing(self):
        data_nodes=pd.read_csv("./data/node_list.csv")
        data_edges=pd.read_csv("./data/edge_list.csv")
        self.data_edges=data_edges
        self.data_nodes=data_nodes
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
        print(self.list_node)
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
        G=ig.Graph(Edges, directed=False)
        labels=['x' for k in range(self.node_number)]
        layers=[-1 for k in range(self.node_number)]#initialization
        for k in range(N):
            labels[self.data_edges2['from'][k]]=self.list_node[self.data_edges2['from'][k]]
            labels[self.data_edges2['to'][k]]=self.list_node[self.data_edges2['to'][k]]
            layers[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
            layers[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]
        

        layt=G.layout('kk',dim=3)
        Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
        Yn=[layt[k][1] for k in range(N)]# y-coordinates
        Zn=[0 for k in range(self.node_number)]# z-coordinates
        Xe=[]
        Ye=[]
        Ze=[]
        for k in range(N):
            Zn[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]
            Zn[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
           
        
        for e in Edges:
            Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
            Ye+=[layt[e[0]][1],layt[e[1]][1], None]
            Ze+=[Zn[e[0]],Zn[e[1]], None]


                
        import plotly.graph_objs as go

        trace1=go.Scatter3d(x=Xe,
                    y=Ye,
                    z=Ze,
                    mode='lines',
                    name='Interaction between parameters',
                    line=dict(color='rgb(125,125,125)', width=2.5),
                    hoverinfo='none'
                    )

        trace2=go.Scatter3d(x=Xn,
                    y=Yn,
                    z=Zn,
                    mode='markers',
                    name='Parameters',
                    marker=dict(symbol='circle',
                                    size=15,
                                    color=layers,
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

            xaxis=go.XAxis(
                title='x'
            ),
            yaxis=go.YAxis(
                title='y'
            )
        )
        fig=go.Figure(data=data, layout=layout)

        print(" Please wait for the visualization...")
        plotly.offline.plot(fig, filename='Layers Visualization')
        print(" 3D visualization done...")

  



