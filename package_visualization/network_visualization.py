
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
from datetime import date



class network_visualization:
    def __init__(self,title,reference,filename,dirData):
        self.filename=filename
        self.title=title
        self.reference=reference
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
        self.dirData=dirData

    def writing_csv(self,data_from,data_to):
        '''This function writes in a new csv file the nodes numerically'''
        import csv
        with open(self.dirData+'/edge_list2.csv', mode='w') as edge_list_numbers:
            edge_writer = csv.writer(edge_list_numbers, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fieldnames = ['to', 'from']
            edge_writer.writerow(fieldnames)
            for i in range (len(data_from)):
                edge_writer.writerow([self.list_node.index(data_from[i]),self.list_node.index(data_to[i])])


         
        

    def data_importing(self):
        '''Import different csv files from the the data folder'''
        data_nodes=pd.read_csv(self.dirData+"/node_list.csv")
        data_edges=pd.read_csv(self.dirData+"/edge_list.csv")
        data_controllable_nodes=pd.read_csv(self.dirData+"/controllable_node.csv")
        data_metrology_nodes=pd.read_csv(self.dirData+"/metrology_node.csv")
        data_FDC_nodes=pd.read_csv(self.dirData+"/FDC_node.csv")
        controllable_node_list=[]
        metrology_node_list=[]
        FDC_node_list=[]
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
        for controllable_node in data_controllable_nodes['controllable_node']:
            controllable_node_list.append(controllable_node)
        for metrology_node in data_metrology_nodes['metrology_node']:
            metrology_node_list.append(metrology_node)
        for FDC_node in data_FDC_nodes['FDC_node']:
            FDC_node_list.append(FDC_node)
        self.list_node=list_node
        self.list_layer=list_layer
        self.list_from=list_from
        self.list_to=list_to
        self.writing_csv(self.list_from,self.list_to)
        self.data_edges2=pd.read_csv(self.dirData+"/edge_list2.csv")
        self.controllable_node_list=controllable_node_list
        self.metrology_node_list=metrology_node_list
        self.FDC_node_list=FDC_node_list


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

        '''Builds the connected network'''
        self.adjacency_matrix()

        N=len(self.data_edges2)
        Edges=[(self.data_edges2['from'][k], self.data_edges2['to'][k]) for k in range(N)]

        G=ig.Graph(Edges, directed=True)
        layt=G.layout('large')

        labels=['x' for k in range(self.node_number)]
        layers=[-1 for k in range(self.node_number)]#initialization
        colors=[0 for k in range(self.node_number)] # init color

        for i in range(self.node_number):
            if self.list_node[i] in self.controllable_node_list:
                colors[i]="blue"
            if self.list_node[i] in self.FDC_node_list:
                colors[i]="brown"
            if self.list_node[i] in self.metrology_node_list:
                colors[i]="gold"
        
        
        for k in range(N):
            labels[self.data_edges2['from'][k]]=self.list_node[self.data_edges2['from'][k]]
            labels[self.data_edges2['to'][k]]=self.list_node[self.data_edges2['to'][k]]
            layers[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
            layers[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]                   
            
        Xn=[layt[k][0] for k in range(self.node_number)]# x-coordinates of nodes
        Yn=[layt[k][1] for k in range(self.node_number)]# y-coordinates of the nodes
        Zn=[0 for k in range(self.node_number)]# z-coordinates of the node

        '''To scatter the nodes as much as possible on the layer'''
        max_yn=max(Yn)
        max_xn=max(Xn)
        max_coord=max(max_yn,max_xn)+1   
        
        Xe=[]
        Ye=[]
        Ze=[]
        for k in range(N):
            Zn[self.data_edges2['from'][k]]=self.list_layer[self.data_edges2['from'][k]]
            Zn[self.data_edges2['to'][k]]=self.list_layer[self.data_edges2['to'][k]]
           
        for sommet in range(self.node_number):
            for sommet2 in range(self.node_number):
                if labels[sommet][0:2]==labels[sommet2][0:2] and labels[sommet]!=labels[sommet2]:
                    Xn[sommet2]=Xn[sommet]
                    Yn[sommet2]=Yn[sommet]
    
        for sommet in range(self.node_number):
            layt[sommet][0]=Xn[sommet]
            layt[sommet][1]=Yn[sommet]
        
        for e in Edges:
            Xe+=[layt[e[0]][0],layt[e[1]][0]]# x-coordinates of edge ends
            Ye+=[layt[e[0]][1],layt[e[1]][1]]
            Ze+=[Zn[e[0]],Zn[e[1]]]


        data=[]
        import plotly.graph_objs as go

       
        #plot the nodes individually
        for i in range(self.node_number):
            
            trace=go.Scatter3d(x=np.array(Xn[i]),y=np.array(Yn[i]),z=np.array(Zn[i]),mode='markers',marker=dict(symbol='circle',
                                    size=15,
                                    color=colors[i],
                                    line=dict(color='rgb(50,50,50)', width=4)
                                ),  name=labels[i],
                                    text=labels[i],
                                    hoverinfo='text'
                                
                                )


            data.append(trace)


        #plot the nodes individually
        trace2=[]
       

        for i in range(0,len(Xe)-1,2):
                    
                    X=[Xe[i],Xe[i+1]]
                    Y=[Ye[i],Ye[i+1]]
                    Z=[Ze[i],Ze[i+1]]
                    
                    trace2=go.Scatter3d(x=X,y=Y,z=Z,mode='lines', name=labels[self.data_edges2['from'][int(i/2)]]+', '+labels[self.data_edges2['to'][int(i/2)]]

                                            ,line=dict(color='rgb(125,125,125)', width=2.5),

                                            hoverinfo='none',
                                            opacity=0.17,
                                            
                                        
                                        )
                    X=[]
                    Y=[]
                    Z=[]

                    data.append(trace2)
      

        axis=dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )
       
        
      
        data.append(go.Mesh3d(
        # 8 vertices of a cube
        x=[-max_coord, max_coord, max_coord, -max_coord, -max_coord, max_coord, max_coord, -max_coord],
        y=[-max_coord, -max_coord, max_coord, max_coord, -max_coord, -max_coord, max_coord, max_coord],
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
        hoverinfo="none",
        opacity=0.2,

        showscale=False
    ))
        data.append(go.Mesh3d(
           
            # 8 vertices of a cube
            x=[-max_coord, max_coord, max_coord, -max_coord, -max_coord, max_coord, max_coord, -max_coord],
            y=[-max_coord, -max_coord, max_coord, max_coord, -max_coord, -max_coord, max_coord, max_coord],
            z=[0, 0, 0, 0, 0, 0, 0, 0],
            colorbar_title='z',
            colorscale=[[0, 'red'],
                        [0.5, 'red'],
                        [1, 'red']],
            # Intensity of each vertex, which will be interpolated and color-coded
            intensity = np.linspace(0, 1, 1, endpoint=True),
           
            text='',
            hoverinfo="none",
            name='Layer t-1',
            showscale=False,
            showlegend=True,
            opacity=0.2
        ))
        today = date.today()

        today_date = today.strftime("%d/%m/%Y")

        
        layout = go.Layout(
            annotations=[
            dict(
            showarrow=False,
                text="<b>"+self.reference+" ("+today_date+")"+"</b>",
                xref='paper',
                yref='paper',
                x=0.01,
                y=0,
                xanchor='left',
                yanchor='bottom',
                
                font=dict(
                size=13
                )
                )
            ],
            scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis)),

            

        )
        fig=go.Figure(data=data, layout=layout)

        fig.add_layout_image(
            dict(
                source="https://upload.wikimedia.org/wikipedia/commons/9/95/Logo_emse.png",
                xref="paper", yref="paper",
                x=0.08, y=1,
                sizex=0.3, sizey=0.2,
                xanchor="right", yanchor="bottom"
            )
        )

        fig.add_layout_image(
                dict(
                    source="https://pbs.twimg.com/profile_images/620547650505560064/P4xNTRTd_400x400.png",
                    xref="paper", yref="paper",
                    x=1.08, y=1,
                    sizex=0.15, sizey=0.15,
                    xanchor="right", yanchor="bottom"
                )
            )
        fig.add_layout_image(
        dict(
            source="https://www.electronicsmedia.info/wp-content/uploads/2020/02/Semiconductors.png",
            xref="x",
            yref="y",
            
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.5,
            layer="below")
)


        fig.update_xaxes(
            visible=False,
        )
        fig.update_yaxes(
            visible=False,
        )
        fig.update_layout(title_text="<b>"+self.title+"</b>", title_x=0.5)


       

        print(" Please wait for the visualization...")
        plotly.offline.plot(fig, filename=self.filename)
        print(" 3D visualization done...")

  
