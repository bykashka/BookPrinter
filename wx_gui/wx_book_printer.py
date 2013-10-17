#! /usr/bin/env python
# -*- coding:utf8 -*-
import wx
import os
import time

class Book_printer(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id,
        'Печать книги', size=(230, 200), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.panel = wx.Panel(self)

        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        open_file = menu1.Append(wx.NewId(), '&Открыть\tCtrl-O')
        menu1.AppendSeparator()
        exit = menu1.Append(wx.NewId(), '&Выход\tCtrl-Q')
        menuBar.Append(menu1, '&Файл')
        menu2 = wx.Menu()
        help = menu2.Append(wx.NewId(), 'He&lp\tF1')
        menu2.AppendSeparator()
        about = menu2.Append(wx.NewId(), '&About')
        menuBar.Append(menu2, '&Help')

        self.SetMenuBar(menuBar)

        string = '> или < рамка в см.'
        self.border = wx.CheckBox(self.panel, -1, string, (10, 30), (150, 20))
        self.border_vlue = wx.TextCtrl(self.panel, -1, '0.0', (160, 30), (50, 20))
        self.border_vlue.Enable(False)
        wx.StaticText(self.panel, -1, 'Страниц в книге:', (10, 55), (150, 20))
        self.book_pages = wx.TextCtrl(self.panel, -1, '0', (160, 55), (50, 20))
        wx.StaticText(self.panel, -1, 'Страниц в тетраде:', (10, 80), (150, 20))
        self.part_pages = wx.TextCtrl(self.panel, -1, '32', (160, 80), (50, 20))

        self.btn_print = wx.Button(self.panel, -1, 'Печать', (10, 105), (200, 25))

        self.Bind(wx.EVT_MENU, self.OnOpen, open_file)
        self.Bind(wx.EVT_MENU, self.OnExit, exit)
        self.Bind(wx.EVT_MENU, self.OnHelp, help)
        self.Bind(wx.EVT_MENU, self.OnAbout, about)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, self.border)
        self.Bind(wx.EVT_BUTTON, self.OnPrint, self.btn_print)
        #self.Bind(wx.EVT_IDLE, self.SowGauge)

        self.select = wx.StaticText(self.panel, -1, 'Выбор:', (10, 10), (150, 20))

    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Открыть *.ps файл...",
        os.getcwd(), style=wx.OPEN,
        wildcard='*.ps')
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.select.SetLabel(u'Выбрано: ' + os.path.split(self.filename)[-1])
        dlg.Destroy()

    def OnExit(self, event):
        self.Close()

    def OnHelp(self, event):
        pass

    def OnAbout(self, event):
        pass

    def OnCheck(self, event):
        value = self.border.GetValue()
        if value:
            self.border_vlue.Enable(True)
        else:
            self.border_vlue.Enable(False)

    def OnPrint(self, event):
        path_to_book_old = self.filename
        book_path, book_name = os.path.split(path_to_book_old)
        self.path_to_book = os.path.join(book_path, 'resize_' + book_name)

        #self.st_progress.SetLabel('Proces is begin, please wait some time...')
        #If resize border is set
        if self.border:
            os.spawnv(os.P_WAIT, '/usr/bin/psnup', 
            ['/usr/bin/psnup', 
            '-b' + str(self.border_vlue.GetValue()) + 'cm', 
            path_to_book_old, 
            self.path_to_book,])

        # Set working directory
        os.chdir(os.path.split(self.path_to_book)[0])

        # Create new working directory
        dir_name = os.path.splitext(os.path.basename(self.path_to_book))[0]
        self.work_dir = os.path.join(os.getcwd(), dir_name)
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)

        # Set new working directory
        os.chdir(self.work_dir)

        # Get count of book pages
        pages = int(self.book_pages.GetValue())

        # Get count of byklet pages
        byklet_pages = int(self.part_pages.GetValue())

        # Add some empty pages
        while divmod(pages, 8)[1] != 0:
            pages += 1

        #print pages

        # Get byklets pages
        page = 0
        byklets = []
        while page <= pages:
            page += 1
            from_page = page
            page += byklet_pages - 1
            to_page = page
            byklets.append((from_page, to_page))
        #print byklets

        # Get byklets
        all_output_files = []
        for i in byklets:
            output_file = os.path.join(self.work_dir, str(i[0]) + '_' + str(i[1])+ ".ps")
            all_output_files.append(output_file)
            os.spawnv(os.P_WAIT, '/usr/bin/psselect',
                    ['/usr/bin/psselect',
                    '-p',
                    str(i[0]) + '-' + str(i[1]),
                    self.path_to_book,
                    output_file,])

        all_byklet_files = []
        for in_file in all_output_files:
            f_name = os.path.basename(in_file)
            output_file = os.path.join(
                os.path.split(in_file)[0], 'byklet_' + f_name)
            all_byklet_files.append(output_file)
            os.spawnv(os.P_WAIT, '/usr/bin/psbook',
                    ['/usr/bin/psbook',
                    in_file,
                    output_file,])

        # 1 list format A4 -> 2 lists format A5
        for in_byklet_file in all_byklet_files:
            f_name = os.path.basename(in_byklet_file)
            output_file_rez = os.path.join(
                os.path.split(in_byklet_file)[0], 'rez_' + f_name)
    
            os.spawnv(os.P_WAIT, '/usr/bin/psnup',
                    ['/usr/bin/psnup',
                    '-l4',
                    '-2',
                    in_byklet_file,
                    output_file_rez,])

        # Delete others files
        for p in all_output_files:
            os.remove(p)
            #print ".",
            
            #print "\nDeleting byklet files"
        for p in all_byklet_files:
            os.remove(p)
            #print ".",
            
if __name__ == '__main__':
    app = wx.App()
    #app.Yield(onlyIfNeeded=True)
    frame = Book_printer(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
    # TODO - find book about wxPython and make GUI for current program more comfortable.
    # TODO - make CLI for current programm.
    # TODO - rewrite current program using OOP.
