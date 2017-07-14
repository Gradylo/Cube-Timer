#!/usr/bin/python
# -*- coding: utf-8 -*-

# move.py

import wx
import time
import objects
import random

X_DIM = 1500
Y_DIM = 1000
SCRAMBLE_LEN = 25

'''
PageState is essentially an enum which helps keep track of
the state of the application.
'''
class PageState(object):
    TIME = 1
    PAUSED = 2

scramble_direction = {
    0 : 'R',
    1 : 'U',
    2 : 'L',
    3 : 'D',
    4 : 'F',
    5 : 'B'
}



'''
Our subclass of wx.Frame.
'''
class Page(wx.Frame):

    def __init__(self, parent, title):
        super(Page, self).__init__(parent, title=title,
            size=(X_DIM, Y_DIM))


        #initialize several different fonts
        timer_font = wx.Font(48, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        lareger_font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        normal_font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        self.Move((800, 250))
        self.Show()
        #self.Maximize()

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('BLACK')

        #pagestate keeps track of timer mode
        self.page_state = PageState.PAUSED

        #times is the set which will keep track of all cube times
        self.times = objects.Set()
        self.times_list = ""


        #for now
        self.start_time = time.time()
        self.elapsed_time = 0.0

        #time_text is a StaticText for the timer text
        self.time_text = wx.StaticText(self.panel,-1,pos = ((X_DIM - 350) / 2, 200), style = wx.ALIGN_CENTER_HORIZONTAL)
        self.time_text.SetFont(timer_font)
        self.time_text.SetLabel(str(self.elapsed_time))

        #summary_text is a StaticText for a brief summary or overview of the users's stats
        self.summary_text = wx.StaticText(self.panel, -1, pos=((X_DIM - 350) / 2 - 100, 300), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.summary_text.SetFont(lareger_font)
        self.summary_text.SetLabel(self.get_summary_text())

        #stats_text is a StaticText for the users's in-depth statistics
        self.stats_text = wx.StaticText(self.panel, -1, pos = (X_DIM - 300, 100))
        self.stats_text.SetFont(normal_font)
        self.stats_text.SetLabel(self.get_stats_text())

        self.ln = wx.StaticLine(self.panel, -1, pos=(X_DIM - 350, 0), size=(0, Y_DIM), style=wx.LI_VERTICAL)
        #self.ln.SetSize((30,30))

        #timer helps us update continually, by sending EVT_TIMER events
        #to be handled by update()
        self.timer = wx.Timer(self)
        self.timer.Start(1)

        #Bind actions to their handlers
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        print(self.scramble())



    def get_summary_text(self):
        return "Session Average: " + "{0:.2f}".format(self.times.get_average()) \
            + "\nSession Mean: " + "{0:.2f}".format(self.times.get_mean())

    def get_stats_text(self):
        return "Solves: " + str(self.times.get_count()) +  "\nCurrent ao5: " + "{0:.2f}".format(self.times.curr_avg5()) \
            + "\nCurrent ao12: " + "{0:.2f}".format(self.times.curr_avg12()) + "\nCurrent ao100: " \
            + "{0:.2f}".format(self.times.curr_avg100()) \
            + "\n\nBest ao5: " + "{0:.2f}".format(self.times.best_avg5()) + "\nBest ao12: " \
            + "{0:.2f}".format(self.times.best_avg12()) + "\nBest ao100: " \
            + "{0:.2f}".format(self.times.best_avg100()) + "\n\nTimes: " + self.times_list


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

        #add time to times list for display
        if self.times.get_count() > 1:
            self.times_list += ", "
        self.times_list += "{0:.2f}".format(self.elapsed_time)

        self.summary_text.SetLabel(self.get_summary_text())
        self.stats_text.SetLabel(self.get_stats_text())
        self.stats_text.Wrap(300)

    def scramble(self):
        scramble_code = []
        prev_direct = None
        curr_direct = None
        turn_type = None

        for i in range(SCRAMBLE_LEN):

            #set curr_direct to a random direction
            if i == 0:
                curr_direct = random.randint(0, 5)
            else:
                while curr_direct == prev_direct:
                    curr_direct = random.randint(0, 5)

            turn_type = random.randint(0, 2)
            prev_direct = curr_direct

            #add appropriate letter code to scramble_code
            if turn_type == 0:
                scramble_code.append(scramble_direction[curr_direct] + " ")
            elif turn_type == 1:
                scramble_code.append(scramble_direction[curr_direct] + "2 ")
            else:
                scramble_code.append(scramble_direction[curr_direct] + "' ")

        return ''.join(scramble_code)




    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            if self.page_state == PageState.PAUSED:
                self.start()
            else:
                self.stop()
        event.Skip()



if __name__ == '__main__':

    app = wx.App()
    Page(None, title='Hi there')
    app.MainLoop()