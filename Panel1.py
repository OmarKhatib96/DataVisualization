import wx
import wx.grid as gridlib
import pandas as pd
#myStyles = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION | wx.MINIMIZE_BOX
GRID_LINE_COLOUR = '#ccc'
#Ce code permet d'avoir une fenetre qui récupère les données depuis un dossier
#Il s'agit de la fenêtre 1 du projet
class MyFrame(wx.Frame):
        def __init__(self,parent,title):
            myStyles = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION | wx.MINIMIZE_BOX
            super(MyFrame,self).__init__(parent, title = title , size = (500,600))
            self.panel = MyPanel(self)
            
class MyPanel(wx.Panel):
    def __init__(self, parent) : 
        super(MyPanel, self).__init__(parent)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)  
        hbox2 = wx.BoxSizer(wx.HORIZONTAL) 
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)     
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)     
         
        self.Btn = wx.Button(self, label = "Open", size = (120,45) )
        hbox1.Add(self.Btn, 0)
        self.Btn.Bind(wx.EVT_BUTTON, onClickMe)


        self.label = wx.StaticText(self, label = "File name...", size = (100,50))
        hbox1.Add(self.label, 0)
        
        self.label2 = wx.StaticText(self, label = "Number of Wafers : ", size = (120,55))
        hbox2.Add(self.label2, 0) 
        self.labelNmbWafers = wx.StaticText(self, label = " ", size = (120,55))
        hbox2.Add(self.labelNmbWafers, 0) 
             
        self.label3 = wx.StaticText(self, label = "Number of Variables : ",  size = (120,55))
        hbox3.Add(self.label3, 0)
        self.labelNmbVar = wx.StaticText(self, label = " ",  size = (120,55))
        hbox3.Add(self.labelNmbVar, 0)  
         
        self.labelData = wx.StaticText(self, label = " ",  size = (300,300))
        hbox4.Add(self.labelData, 0)  

        self.vbox.Add(hbox1,0, wx.ALL)
        self.vbox.Add(hbox2,0, wx.ALL) 
        self.vbox.Add(hbox3,0, wx.ALL)
        self.vbox.Add(hbox4,1, wx.ALL)

        self.SetSizer(self.vbox) 

               
class MyApp(wx.App):
    def OnInit(self):

        self.frame = MyFrame(parent = None, title = "Import data prototype1")
        self.frame.Center()
        self.frame.Show()
        self.frame.Fit()
        return True
        
def onClickMe( event):
    print(event)
    # Create open file dialog
    openFileDialog = wx.FileDialog(app.frame, "Open", "", "", 
        "Excel files (*.csv)|*.csv", 
        wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    
    openFileDialog.ShowModal()
    print(openFileDialog.GetPath())
    app.frame.panel.label.SetLabelText(openFileDialog.GetPath())
    ShowData(openFileDialog.GetPath())
    openFileDialog.Destroy()
    event.Skip() 

def ShowData(FilePath):
    data = pd.read_csv(FilePath)
    print(data.head())
    Ligne = str( len(data))
    Colonne = str(len(data.columns))
    app.frame.panel.labelNmbWafers.SetLabelText(Ligne)    
    app.frame.panel.labelNmbVar.SetLabelText(Colonne)
    '''
    grid = gridlib.Grid(app.frame.panel)
    grid.AutoSizeColumns(True)
    grid.SetGridLineColour(GRID_LINE_COLOUR)
    grid.SetRowLabelSize(10)
    grid.SetColLabelSize(30)
    grid.CreateGrid(len(data),len(data.columns))
    grid.SetTable(gridlib.GridTableBase(data))
    grid.AutoSize()
    '''
    
    app.frame.panel.labelData.SetLabelText(str(data.head()))

    app.frame.panel.SetSizer( app.frame.panel.vbox)          
    app.frame.panel.Refresh()

app = MyApp()
    
app.MainLoop()