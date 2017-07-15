import wx
import time
import objects
import random
import wx.lib.plot

X_DIM = 500
Y_DIM = 500

class Page(wx.Frame):

    def __init__(self, parent, title):
        super(Page, self).__init__(parent, title=title,
            size=(X_DIM, Y_DIM))

        self.Show()
        #self.canvas = wx.lib.plot.PlotCanvas(self)



if __name__ == '__main__':

    app = wx.App()
    Page(None, title='Hi there')
    app.MainLoop()