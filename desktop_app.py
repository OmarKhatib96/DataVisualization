import wx
import wx.grid
import wx.lib.agw.labelbook as LB
import wx.lib.msgpanel as mp
import wx.lib.newevent
from wx.lib.delayedresult import startWorker
import wx.lib.scrolledpanel as scrolled
import os
import csv
import threading

class m:
    # Main panel
    x=0
    y=0

class batttesttab(wx.Panel):
    def __init__(self, *args, **kw):
        super(batttesttab, self).__init__(*args, **kw)
        self.dirname = os.getcwd()

    def OnOpen(self):

        if self.contentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                            wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open XYZ file", wildcard="XYZ files (*.xyz)|*.xyz",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.doLoadDataOrWhatever(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def SetNotebook(self,notebook):
        self.notebook = notebook
    
    def SetTestType(self,testtype):
        self.testtype = testtype
        return testtype
  
    def CreateTab(self,lab,po,nam):
        panel = wx.Panel(self.notebook, size=(150,150))
        #TestName
        #Testid
        
        #Version 
        #Description
        #Confirm for secure connections
        self.controlunitbutton = wx.Button(panel,-1,label=lab,pos=po,name=nam)
        self.panel=panel
        if(lab=="Open"):
            self.controlunitbutton.Bind(wx.EVT_BUTTON,self.ImportFunc)


        if(lab=="Network visualization"):
            
            self.controlunitbutton.Bind(wx.EVT_BUTTON,self.DownloadNetwork)



        #self.controlunitbutton.Bind(wx.EVT_BUTTON,self.OnConnect)
        #Draw the battery progress bars on in a grid format of (rows*cols)
        #wx.StaticText(panel,-1,"Progress:", (20, 160))
        y1 = 200
        battno = 1
       
        print("inside the creattab")
        return panel

    def DownloadNetwork(self,event):
        #if (self.thread.isAlive() == False): 
                #self.thread.start()
        from network_visualization import network_visualization
        net_vis=network_visualization("Data visualization with 2 layers"," Wei-Ting Sample","Datavisualization.html")
        net_vis.network_representation()
        print("Your html file is ready!")
   
    def ImportFunc( self, event ):

        dlg=wx.FileDialog(self, 'Choose a file', self.dirname, '','CSV files (*.csv)|*.csv|All files(*.*)|*.*',wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname=dlg.GetDirectory()
            self.filename=os.path.join(self.dirname,dlg.GetFilename())
            self.file=open(self.filename, 'r')

            #check for file format with sniffer



            dialect=csv.Sniffer().sniff(self.file.readline())


            #dialect = csv.Sniffer().sniff(self.file.read(1024))
            self.file.seek(0)

            csvfile=csv.reader(self.file,dialect)
            filedata = [] #put contents of csvfile into a list
            filedata.extend(csvfile)
            self.file.seek(0)

            #grab a sample and see if there is a header
            sample=self.file.read(2048)
            self.file.seek(0)
            if csv.Sniffer().has_header(sample): #if there is a header
                colnames=next(csvfile) # label columns from first line
                datalist=[] # create a list without the header
                datalist.extend(filedata[1:len(filedata)]) #append data without header

            else:
                row1=next(csvfile) #if there is NO header
                colnames=[]
                for i in range(len(row1)):
                    colnames.append('col_%d' % i) # label columns as col_1, col_2, etc
                self.file.seek(0)
                datalist=filedata #append data to datalist

        self.file.close()
        self.createGrid(datalist, colnames)
        grid_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer.Add(self.grid, 1, wx.EXPAND)
        self.panel.SetSizer(grid_sizer)
        self.panel.Layout()
    
    #create the grid

    def createGrid(self, datalist, colnames):
        if getattr(self, 'grid', 0): 
            self.grid.Destroy()
        self.grid=wx.grid.Grid(self, 0)
        self.grid.CreateGrid(len(datalist), len(colnames)) #create grid, same size as file (rows, cols)

        #fill in headings
        for i in range(len(colnames)):
            self.grid.SetColLabelValue(i, colnames[i])

        #populate the grid
        for row in range(len(datalist)):
            for col in range(len(colnames)):
                try: 
                    self.grid.SetCellValue(row,col,datalist[row][col])
                except: 
                    pass


        self.grid.AutoSizeColumns(False) # size columns to data (from cvsomatic.py)
        self.twiddle()


    def twiddle(self): # from http://www.velocityreviews.com/forums/t330788-how-to-update-window-after-wxgrid-is-updated.html
        x,y = self.GetSize()
        self.SetSize((x, y+1))
        self.SetSize((x,y))
        print("inside twiddle")

    def Exit(self, event):
        if getattr(self, 'file',0):
            self.file.close()
            self.Close(True)


   


class TitleFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(TitleFrame, self).__init__(*args, **kw)

        '''
        self.blue = wx.Panel(self)
        self.blue.SetBackgroundColour(wx.BLUE)
        self.fbrowser = wx.GenericDirCtrl(self)
        # Setup
        self.AddPage(self.textctrl, "Text Editor")
        self.AddPage(self.blue, "Blue Panel")
        self.AddPage(self.fbrowser, "File Browser")

        '''

        frame = wx.Panel.__init__(self, None, title="Integrated Process Control Framework", size=(1000,1000))
        ico = wx.Icon('C:/Users/Omar/Desktop/ISMIN 3A/PE/DataVisualization/logo.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("Xeelas BV...")
        self.notebook=LB.LabelBook(self, -1, agwStyle=LB.INB_FIT_LABELTEXT|LB.INB_LEFT|LB.INB_BOLD_TAB_SELECTION)
      

        
    
    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
      """        
        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H", 
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        openMenu=wx.Menu

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)  


    def OnExit(self, event):
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from Xeelas")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("IoT for Humanity", 
                    "Xeelas BV",
        wx.OK|wx.ICON_INFORMATION)



    def OnClose(self, event):
        try:
            dlg = wx.MessageDialog(self,
            "Do you really want to stop testing?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                self.Destroy()
                exit()
        except:
            self.Destroy()
    


    def setup(self):
        self.tab1 = batttesttab(self.notebook)
        self.tab1.SetNotebook(self.notebook)
             

        # Add the windows to tabs and name them.

        self.notebook.AddPage(self.tab1.CreateTab("Open",(0,20),"Open"),"Import data")
        
        self.notebook.AddPage(self.tab1.CreateTab("Settings",(0,20),"settings"),"Settings")
        self.notebook.AddPage(self.tab1.CreateTab("Network visualization",(0,20),"network"),"Network")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.notebook, 3, wx.ALL|wx.EXPAND,5)


   
    
