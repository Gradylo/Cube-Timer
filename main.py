#!/usr/bin/python
# -*- coding: utf-8 -*-

# move.py

import wx
import time
import objects

X_DIM = 1500
Y_DIM = 1000



class PageState(object):
    TIME = 1
    PAUSED = 2

class myTimer(wx.Timer):
    def Notify(et, st):
        self.elapsed_time = time.clock() - self.start_time
        self.time_text.SetLabel(str(self.elapsed_time))


class Page(wx.Frame):

    def __init__(self, parent, title):
        super(Page, self).__init__(parent, title=title,
            size=(X_DIM, Y_DIM))

        timer_font = wx.Font(48, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        lareger_font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        normal_font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        self.Move((800, 250))
        self.Show()
        #self.Maximize()

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('BLACK')

        text = "hi how are you"

        self.page_state = PageState.PAUSED

        self.times = objects.Set()


        #for now
        self.start_time = time.time()
        self.elapsed_time = 0.0

        self.time_text = wx.StaticText(self.panel,-1,pos = (X_DIM / 2, 200), style = wx.ALIGN_CENTER_HORIZONTAL)
        self.time_text.SetFont(timer_font)
        self.time_text.SetLabel(str(self.elapsed_time))

        self.summary_text = wx.StaticText(self.panel, -1, pos=(X_DIM / 2, 500), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.summary_text.SetFont(lareger_font)
        self.summary_text.SetLabel(self.get_summary_text())

        self.timer = wx.Timer(self)
        print(self.timer.Start(1))
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)



    def get_summary_text(self):
        return "Session Average: " + "{0:.2f}".format(self.times.get_average()) + "\nSession Mean: " + "{0:.2f}".format(self.times.get_mean())


    def update(self, event):
        if self.page_state == PageState.TIME:
            self.elapsed_time = time.time() - self.start_time
            self.time_text.SetLabel("{0:.2f}".format(self.elapsed_time))


    def start(self):
        self.start_time = time.time()
        self.page_state = PageState.TIME

    def stop(self):
        self.page_state = PageState.PAUSED
        self.times.add_time(self.elapsed_time)
        self.summary_text.SetLabel(self.get_summary_text())


    def onKeyPress(self, event):
        print("here")
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            if self.page_state == PageState.PAUSED:
                self.start()
            else:
                self.stop()
            print("pressed space")
        event.Skip()



if __name__ == '__main__':

    app = wx.App()
    Page(None, title='Hi there')
    app.MainLoop()