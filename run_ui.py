import wx
import desktop_app

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()

    frm = desktop_app.TitleFrame(None, title='Integrated Process Control Framework')
    frm.Bind(wx.EVT_CLOSE, frm.OnClose)
    frm.Show()
    frm.setup()

    app.MainLoop()
    