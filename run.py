import wx
from package_visualization import desktop_app

if __name__ == '__main__':
  
    app = wx.App()
    frm = desktop_app.TitleFrame(None, title='Integrated Process Control Framework')
    frm.Bind(wx.EVT_CLOSE, frm.OnClose)
    frm.Show()
    frm.setup()
    app.MainLoop()
    