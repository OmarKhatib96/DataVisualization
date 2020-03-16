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
from wx.lib.intctrl import IntCtrl
from threading import Thread
import wx.richtext as rt


class batttesttab(wx.Panel):
    def __init__(self, *args, **kw):
        super(batttesttab, self).__init__(*args, **kw)
        self.dirname = os.getcwd()
       


    def OnOpen(self):

        if self.contentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                            wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        with wx.FileDialog(self, "Open XYZ file", wildcard="XYZ files (*.xyz)|*.xyz",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.doLoadDataOrWhatever(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def SetNotebook(self,notebook):
        self.notebook = notebook
    
    
  
    def CreateTab(self,lab,po,nam):
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,underline=False)

        panel = wx.Panel(self.notebook, size=(150,150))

        if(lab=="Home"):
            self.panelHome=panel
            try:
        
                image_file = 'C:/Users/Omar/Desktop/ISMIN 3A/PE/DataVisualization/images.jfif'
                bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                self.panelHome.bitmap1 = wx.StaticBitmap(self.panelHome, -1, bmp1, (40, 70),size=(200,200))
                str1 = "%s  %dx%d" % (image_file, bmp1.GetWidth(), bmp1.GetHeight()) 

                #pParagraph

                self.rtc1 = rt.RichTextCtrl(self.panelHome,pos=(10,300),size=(350,90),style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE)
                self.rtc2 = rt.RichTextCtrl(self.panelHome,pos=(10,400),size=(350,90),style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE)

                self.Show()
                """
                attr_super = wx.richtext.RichTextAttr()
                attr_super.SetTextEffects(wx.TEXT_ATTR_EFFECT_SUPERSCRIPT)
                attr_super.SetFlags(wx.TEXT_ATTR_EFFECTS)
                attr_super.SetTextEffectFlags(wx.TEXT_ATTR_EFFECT_SUPERSCRIPT)
                self.rtc1.WriteText("Is this super?")
                self.rtc1.SetStyle (7, 13, attr_super)
                """

            except IOError:
                raise SystemExit
    
        if(lab=="Open"):
            self.panelOpen=panel

            text=wx.StaticText(self.panelOpen,-1,"Choose a csv file",(20,20))
            text.SetFont(font)

            self.controlunitbutton = wx.Button(self.panelOpen,-1,label=lab,pos=po,name=nam)

            self.controlunitbutton.Bind(wx.EVT_BUTTON,self.ImportFunc)


        if(lab=="Run"):
            self.panelRun=panel
            
            
            text=wx.StaticText(self.panelRun,-1,"Launch the data visualization",(20,20))
            text.SetFont(font)

            self.controlunitbutton = wx.Button(self.panelRun,-1,label=lab,pos=po,name=nam)

            
            self.controlunitbutton.Bind(wx.EVT_BUTTON,self.DownloadNetwork)
            
        if(lab=="Settings"):
            self.panelSettings=panel
            
            setting_title=wx.StaticText(self.panelSettings,-1,"Model settings",(12,15),(260,-1),wx.ALIGN_CENTER)
            setting_title.SetBackgroundColour('blue')
            setting_title.SetForegroundColour('white')
            self.cb1 = wx.CheckBox(self.panelSettings, label = 'Bayesian network',pos = (20,40)) 
            self.cb2 = wx.CheckBox(self.panelSettings, label = 'Dynamic Bayesian network',pos = (20,80)) 
            self.cb3 = wx.CheckBox(self.panelSettings, label = 'Blacklist',pos = (20,120))
            self.cb4 = wx.CheckBox(self.panelSettings, label = 'Hill climbing-random start',pos = (20,160))
            wx.StaticText(self.panelSettings,-1,"Number of restarts",(25,200))
            wx.StaticText(self.panelSettings,-1,"Number of perturbing edges",(25,220))
            IntCtrl(self.panelSettings,-1,0,(190,195),style=3,min=0,max=20,size=(20,22))
            IntCtrl(self.panelSettings,-1,0,(190,225),style=1,min=0,max=20,size=(20,22))


            self.controlunitbutton = wx.Button(self.panelSettings,-1,label='import',pos=(100,115),name=nam)

            self.controlunitbutton.Bind(wx.EVT_BUTTON,self.ImportFunc)

            wx.StaticText(self.panelSettings,-1,"Training set (%)",(20,275))

            slider=wx.Slider(self.panelSettings,-1,0,0,100,pos=(20,305),size=(190,60),style=wx.SL_AUTOTICKS|wx.SL_LABELS)
            slider.SetTickFreq(2)
            wx.StaticText(self.panelSettings,-1,"Application",(20,400))

            self.cb5 = wx.CheckBox(self.panelSettings, label = 'Run to Run control',pos = (25,430)) 
            self.cb6 = wx.CheckBox(self.panelSettings, label = 'Virtual metrology',pos = (25,460)) 
            self.cb7 = wx.CheckBox(self.panelSettings, label = 'Process monitoring',pos = (25,490))
            
            self.controlunitbutton = wx.Button(self.panelSettings,-1,label='Save',pos=(20,530),name=nam)



        return panel

    def DownloadNetwork(self,event):
        



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
            dialect=csv.Sniffer().sniff(self.file.readline())
            self.file.seek(0)
            csvfile=csv.reader(self.file,dialect)
            filedata = [] 
            filedata.extend(csvfile)
            self.file.seek(0)
        
            sample=self.file.read(2048)
            self.file.seek(0)
            if csv.Sniffer().has_header(sample): 
                colnames=next(csvfile) 
                datalist=[] 
                datalist.extend(filedata[1:len(filedata)]) 

            else:
                row1=next(csvfile) 
                colnames=[]
                for i in range(len(row1)):
                    colnames.append('col_%d' % i) 
                self.file.seek(0)
                datalist=filedata 

            self.file.close()
            self.createGrid(datalist, colnames)     
            grid_sizer = wx.BoxSizer(wx.VERTICAL)
            grid_sizer.Add(self.grid,flag=wx.ALIGN_CENTER_HORIZONTAL)
            grid_sizer.AddStretchSpacer()

            self.panelOpen.SetSizer(grid_sizer)


            #self.panelOpen.Refresh()
        
    #create the grid

    def createGrid(self, datalist, colnames):
        if getattr(self, 'grid', 0): 
            self.grid.Destroy()
        self.grid=wx.grid.Grid(self.panelOpen)#crucial tu put self.panelOpen in parameter
        print(len(datalist),len(colnames))
        self.grid.CreateGrid(len(datalist), len(colnames)) #create grid, same size as file (rows, cols)

        for i in range(len(colnames)):
            self.grid.SetColLabelValue(i, colnames[i])

        for row in range(len(datalist)):
            for col in range(len(colnames)):
                try: 
                    self.grid.SetCellValue(row,col,datalist[row][col])

                except: 
                    print("in the exception of populating")
                    pass

                 
        self.twiddle()
        
        
    def SetGridAlignment(self,halign,valign,nrows,ncols):
      
        for ii in range(nrows):
            for jj in range(ncols):
                self.grid.SetCellAlignment(ii,jj,halign,valign)

    
    def twiddle(self): # from http://www.velocityreviews.com/forums/t330788-how-to-update-window-after-wxgrid-is-updated.html
        x,y = self.GetSize()
        print("size=",x,y)
        self.SetSize((x, y+1))
        self.SetSize((x,y))
        print("inside twiddle")
        #self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        #self.SetGridAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE,x,y)


    def Exit(self, event):
        if getattr(self, 'file',0):
            self.file.close()
            self.Close(True)


   


class TitleFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(TitleFrame, self).__init__(*args, **kw)
        frame = wx.Panel.__init__(self, None, title="Integrated Process Control Framework", size=(650,650))
        ico = wx.Icon('C:/Users/Omar/Desktop/ISMIN 3A/PE/DataVisualization/logo.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("Ecole des Mines de Saint-Etienne 2020")
        self.notebook=LB.LabelBook(self, -1, agwStyle=LB.INB_FIT_LABELTEXT|LB.INB_LEFT|LB.INB_BOLD_TAB_SELECTION|LB.INB_GRADIENT_BACKGROUND|LB.INB_BORDER|LB.INB_USE_PIN_BUTTON|LB.INB_DRAW_SHADOW


    )
      
       

        self.SetBackgroundColour("grey"+"yellow")


        
    
    def makeMenuBar(self):
             
        fileMenu = wx.Menu()

        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H", 
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)


    
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)  


    def OnExit(self, event):
        self.Close(True)


    def OnHello(self, event):
        wx.MessageBox("Hello again from FENG Yuan, KHATIB Omar, TESOR Florian ")


    def OnAbout(self, event):
        wx.MessageBox("Data visualization for metrology", 
                    "Ecole des Mines de Saint-Etienne",
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
        self.notebook.AddPage(self.tab1.CreateTab("Home",(20,45),"Home"),"Home")
        self.notebook.AddPage(self.tab1.CreateTab("Open",(20,45),"Open"),"Import data")
        self.notebook.AddPage(self.tab1.CreateTab("Settings",(20,45),"settings"),"Settings")
        self.notebook.AddPage(self.tab1.CreateTab("Run",(20,45),"network"),"Network")
       

   
    
