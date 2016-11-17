#coding:utf-8
'''
----------V1.0版本------------
搭建了基本框架，和添加了最基本的功能，实现输入数据自动计算。
BUG:1,无法按ESC键退出；2，输错后重新输入有0跟在后面
----------V1.1版本------------
修复：输错后重新输入有0跟在后面
方法：先是想直接重新赋值为空，但是这样做会直接循环报错，所以先判断不为空才进行操作
----------V1.2版本------------
增加功能：可以在户数直接进行数据计算
方法：用eval方法，然后用try包住，因为在输入+-*时候会报错，在后面添加数字来避免错误
'''

import wx
from math import *

class CalulateWindow(wx.Frame):
    def __init__(self):
        super(CalulateWindow,self).__init__(None,-1,title='Calulate',size=(300,250),style=wx.CAPTION|wx.CLOSE_BOX)

        self.panel = wx.Panel(self)
        self.initUI()
        self.initNum()
        self.set_Icon()
        self.createHandler()
        
        #self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)没反应
        #self.panel.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        
        self.Centre()
        self.Show()
        
    def onKeyDown(self,evt):
        print '-------'
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            if wx.MessageBox(u'确认退出？',u'嘻嘻~',wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
                self.onClose(event)
           
    def set_Icon(self):
        icon = wx.Icon('icos/cat.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
    def initUI(self):
        wx.StaticText(self.panel,-1,label=u'户数',pos=(10,10),size=(-1,-1))
        wx.StaticText(self.panel,-1,label=u'每户人数',pos=(70,10),size=(-1,-1))
        wx.StaticText(self.panel,-1,label=u'每人每天(L)',pos=(140,10),size=(-1,-1))
        wx.StaticText(self.panel,-1,label=u'小时系数',pos=(230,10),size=(-1,-1))
        
        self.text_households = wx.TextCtrl(self.panel,-1,value='',pos=(10,30),size =(50,25))
        self.text_each_housepeople = wx.TextCtrl(self.panel,-1,value='',pos=(70,30),size =(35,25))
        self.text_each_day = wx.TextCtrl(self.panel,-1,value='',pos=(140,30),size =(50,25))
        self.text_hour_coefficient = wx.TextCtrl(self.panel,-1,value='',pos=(230,30),size =(40,25))
        self.output = wx.TextCtrl(self.panel,-1,value='',pos=(10,120),size=(200,80),style=wx.TE_MULTILINE)

    def initNum(self):
        self.max_hour_flow = 0
        self.waterbox_volume = 0
        
        self.text_households.SetValue('0')
        self.text_each_housepeople.SetValue('3.5')
        self.text_each_day.SetValue('200')
        self.text_hour_coefficient.SetValue('2.5')
        
        self.output.SetValue(u'最高日用水量: %s\n最大小时流量：%s \n水池容量：%s'%(0,self.max_hour_flow,self.waterbox_volume))

    def createHandler(self):
        
        self.Bind(wx.EVT_TEXT,self.calculate,self.text_households)
        self.Bind(wx.EVT_TEXT,self.calculate,self.text_each_housepeople)
        self.Bind(wx.EVT_TEXT,self.calculate,self.text_each_day)
        self.Bind(wx.EVT_TEXT,self.calculate,self.text_hour_coefficient)

        
    def calculate(self,evt):#计算过程
        #取值
        households = self.text_households.GetValue()
        housepeople = self.text_each_housepeople.GetValue()
        each_day = self.text_each_day.GetValue()
        hour_coefficient = self.text_hour_coefficient.GetValue()
        t=0
        #用try包住，提前判断输入条件
        try:
            t = eval(households)
        except SyntaxError:
            if households.endswith('*'):
                households = households + '1'
                t = eval(households)
            if households.endswith('+') or households.endswith('-'):
                households = households + '0'
                t = eval(households)
        except NameError:
            dlg = wx.MessageDialog(self,u'格式错误，请输入正确的等式。',u'请注意',wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.initNum()
            self.text_households.SetValue('')#去掉初始化的0
               
        if  isinstance(t,int) and t >0:#规定了int类型才进行判断
            highest_day_flow = int(t)*float(housepeople)*float(each_day)/1000
            self.max_hour_flow = '%.2f' % (highest_day_flow/24*float(hour_coefficient))
            waterbox_min = '%.2f' %(highest_day_flow*0.15)
            waterbox_max = '%.2f' %(highest_day_flow*0.20)
            self.output.SetValue(u'最高日用水量: %s\n最大小时流量: %s \n水池容量: %s~%s'%(highest_day_flow,self.max_hour_flow,waterbox_min,waterbox_max))

                
if __name__ == '__main__':
    app = wx.App()
    CalulateWindow().Show()
    app.MainLoop()