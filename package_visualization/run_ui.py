import wx
from package_visualization import desktop_app

  
app = wx.App()
frm = desktop_app.TitleFrame(None, title='Integrated Process Control Framework')
frm.Bind(wx.EVT_CLOSE, frm.OnClose)
frm.Show()
frm.setup()
app.MainLoop()
