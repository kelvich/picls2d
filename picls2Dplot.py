#
#! /usr/bin/env python

from Tkinter import *
from tkFileDialog import askdirectory
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import mpl_toolkits.mplot3d.axes3d
from mpl_toolkits.mplot3d import Axes3D

from IPython.frontend.terminal.embed import InteractiveShellEmbed

from pylab import imshow, rfft, fftfreq, xlabel, ylabel, colorbar, axis, figure
from os import listdir
from fnmatch import fnmatch
from os import system
from namelist import Namelist

from dicts import *
from tools import *
from func_classes import *


class StatusBar():
    def __init__(self, master):
        self.label = Label(master, bd=1, relief=SUNKEN, anchor=W)
        self.label.grid(sticky=SW+SE)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class FirstFrame():
	def __init__(self,parent):
		self.frm = Frame(parent)
		self.frm.grid()
		self.scr_height = parent.winfo_screenheight()
		self.frm.fname_selected='<HOME>'

		self.home_choise(parent)
		self.frm.status = StatusBar(parent)
		self.frm.status.set('Hi, Doc, whatz up?')


		self.frm.fig = figure()
		dpi_val = 100
		self.frm.fig.set_dpi(dpi_val)
		self.frm.fig.set_figheight(0.5*self.scr_height/dpi_val )

		self.frm.canvas = FigureCanvasTkAgg(master=self.frm, figure=self.frm.fig)
		canvwidg=self.frm.canvas.get_tk_widget().grid(row=1,column=0,columnspan=4)

		self.frm.toolbar_frame = Frame(self.frm)
		self.frm.toolbar_frame.grid(column = 0, row = 2,columnspan=4, sticky=W) 
		toolbar = NavigationToolbar2TkAgg( self.frm.canvas,self.frm.toolbar_frame )
		toolbar.update()

		self.frm.var_zip = IntVar()
		self.frm.zipchek = Checkbutton(self.frm, text="ZIP",variable=self.frm.var_zip)
		self.frm.zipchek.grid(row=3, column=2)

		menubar = Menu(parent)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open folder",command=lambda: self.folder_refresh(parent))
		filemenu.add_command(label="Show input",command=self.input_show)
		filemenu.add_command(label="Let be the Python",command=self.py_invoke)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=parent.quit)
		menubar.add_cascade(label="Menu", menu=filemenu)

		func_menu = Menu(menubar, tearoff=0)
		func_menu.add_command(label= '<HOME>',command = lambda: self.func_chosen(parent,'<HOME>'))
		func_menu.add_command(label= 'field',command = lambda: self.func_chosen(parent,'field'))
		func_menu.add_command(label= 'current',command = lambda: self.func_chosen(parent,'current'))
                func_menu.add_command(label= 'density',command = lambda: self.func_chosen(parent,'density'))
                func_menu.add_command(label= 'energy',command = lambda: self.func_chosen(parent,'energy'))
                func_menu.add_command(label= 'phase',command = lambda: self.func_chosen(parent,'phase'))
                func_menu.add_command(label= 'em_field',command = lambda: self.func_chosen(parent,'em_field'))
		menubar.add_cascade(label="Functions", menu=func_menu)
		parent.config(menu=menubar)

	def py_invoke(self):
		ipshell = InteractiveShellEmbed()
		ipshell()
		return
	def input_show(self):
		names = np.sort(listdir(self.frm.folder_name+'/'))
                for name in names:
                	if fnmatch(name, '*.in'):
                               	inputname = self.frm.folder_name +'/'+ name
				break		
		tx=open(inputname).readlines()
		new_txbox_wg= Tk()
		txbox_frm = Frame(new_txbox_wg)
		txbox = Text(txbox_frm)
		txbox_scrl = Scrollbar(txbox_frm)
		for l in tx:
			txbox.insert(END,l)

		txbox.focus_set()
		txbox_scrl.config(command=txbox.yview)
		txbox.config(yscrollcommand=txbox_scrl.set)
		txbox.grid(column=0,row=0)
		txbox_scrl.grid(column=1,row=0, sticky=S+N)
		txbox_frm.grid()
		new_txbox_wg.title(inputname)
		new_txbox_wg.mainloop()
		new_txbox_wg.quit()
		return

	def func_chosen(self,parent,funcname):
		self.frm.fname_selected=funcname
		self.choise(parent)		

#	def button_doubleclick(self,event,parent):
#		self.frm.fname_selected=funclist[int(self.listi.curselection()[0])]
#		self.choise(parent)

	def folder_refresh(self,parent):
		self.folder_input(parent)
#		self.choise(parent)

	def home_choise(self,parent):
		self.a1=Frame(self.frm)
		self.a1.grid(row=0, column=0)
		self.a1.cnv = Canvas(self.a1, width=100, height = 180)
		self.a1.photo= PhotoImage(file="bugsbunny.gif")
		self.a1.cnv.create_image((50,90),image=self.a1.photo)
		self.a1.cnv.grid(row=0, column=0)
#		self.folder_choose = Button(self.a1,text="choose the folder, Doc", command= lambda: self.folder_input(parent))
#                self.folder_choose.grid(row=0, column=0)


	def time_opts_read(self):
		names_target = ('/dnss', '/empi', '/emsi', '/rjci','/emss', '/emes', '/emps', '/rjcs',  '/phs')
		try:
			names_listed = np.sort(listdir(self.frm.folder_name))
		except TypeError:
			self.frm.status.set( 'it seems you should show me the folder, Doc')
			return False
		for name_pat in names_target:
			for name in names_listed:
				if fnmatch('/'+name, name_pat) and len(listdir(self.frm.folder_name +'/'+ name+'/'))!=0:
					folder = '/'+name
					break
			if fnmatch(folder, name_pat) and len(listdir(self.frm.folder_name+folder+'/'))!=0:
				break
		folder = self.frm.folder_name + folder+'/'

		lastname = np.sort(listdir(folder))[-1].split('.')
		self.lastname = lastname[0]
		self.frm.timemax = int(self.lastname.split('_')[-1])
		self.frm.timedigit = len(self.lastname.split('_')[-1])
		self.frm.nodedigit = len(self.lastname.split('_')[-2])
		return True


	def folder_input(self,parent):
		self.frm.folder_name = askdirectory()
		parent.title(self.frm.folder_name)

        def zip_choise_read(self):
		if self.frm.var_zip.get() == 1:
                        self.frm.reg = 'zip'
                        self.frm.typemasks=typemasks_zip
                elif self.frm.var_zip.get() == 0:
                        self.frm.typemasks=typemasks_map
                        self.frm.reg = None


        def some_opts_extr(self):
		try:
                	names = np.sort(listdir(self.frm.folder_name))
		except TypeError:
                        self.frm.status.set( 'it seems you should show me the folder, Doc')
                        return False
                for name in names:
                        if fnmatch(name, '*.in'):
                                inputname=self.frm.folder_name + '/'+name
                No_ion = int(Namelist(inputname).get('ions').get('par')[0].get('no_ion')[0])
		self.frm.n_nod=int(Namelist(inputname).get('option').get('par')[0].get('nd_para')[0])-1
                return No_ion


	def typemask_set(self):
		self.zip_choise_read()
		self.frm.n_ion = self.some_opts_extr()
		if self.frm.reg == 'zip':
			self.frm.typemasks=typemasks_zip
			if self.frm.n_ion==2:
				for fn in ['d0','d1','e0','e1']:
					self.frm.typemasks[fn][1:]=[('2', 'float32')] + self.frm.typemasks[fn][1:]
				self.frm.typemasks['d2']=self.frm.typemasks['d1']
				self.frm.typemasks['e2']=self.frm.typemasks['e1']
		elif self.frm.reg == None:
			self.frm.typemasks=typemasks_map
			if self.frm.n_ion==2:
                                for fn in ['d0','d1','e0','e1']:
                                        self.frm.typemasks[fn][2:]=[('f01', 'S2'), ('2', 'S11')] + self.frm.typemasks[fn][2:]
				self.frm.typemasks['d2']=self.frm.typemasks['d1']
                                self.frm.typemasks['e2']=self.frm.typemasks['e1']


	def choise(self,parent):
		self.a1.destroy()
		if self.frm.fname_selected == '<HOME>':
			self.home_choise(parent)
			return
#		self.zip_choise_read()
		try:
			if self.time_opts_read():
				True
			else:
				return
		except UnboundLocalError:
			self.frm.status.set('it seems you should show me the folder, Doc')
			return
		self.typemask_set()
		if self.frm.fname_selected == 'em_field':
                        self.a1 = grid_funcs(self.frm)
			self.a1.em_fld_opts()
			self.frm.show_trig = lambda: self.a1.em_fld_trig(self.frm)
			self.frm.read_trig = lambda: self.a1.em_fld_trig(self.frm)
		elif self.frm.fname_selected == 'field' or self.frm.fname_selected == 'current':
			self.a1 = grid_funcs(self.frm)
			if self.frm.fname_selected == 'field':
				self.a1.fld_type()
			self.a1.comp_type()
			self.a1.snap_type()
			self.a1.step()
			self.a1.opts()
			self.a1.spect_opts()
			self.frm.show_trig = lambda: self.a1.em_show_trig(self.frm)
			self.frm.read_trig = lambda: self.a1.em_read_trig(self.frm)
		elif self.frm.fname_selected == 'density' or self.frm.fname_selected == 'energy':
			self.a1 = grid_funcs(self.frm)
			self.a1.part_type()
			self.a1.step()
			self.a1.opts()
			self.a1.spect_opts()
			self.frm.show_trig = lambda: self.a1.den_show_trig(self.frm)
			self.frm.read_trig = lambda: self.a1.den_read_trig(self.frm)
		elif self.frm.fname_selected == 'phase':
			self.a1 = grid_funcs(self.frm)
			self.a1.part_type()
			self.a1.step()
			self.a1.phase_comp()
			self.a1.filt_comp()
			self.a1.spect_opts()
			self.a1.phs_opts()
			self.frm.read_trig = lambda: self.a1.phase_read_trig(self.frm)
			self.frm.show_trig = lambda: self.a1.phase_show_trig(self.frm)
		self.frm.read_button = Button(self.frm, text="Read", command= self.frm.read_trig)
		self.frm.read_button.grid(row=3, column=0)
                self.frm.button = Button(self.frm, text="Go!", command= self.frm.show_trig)
                self.frm.button.grid(row=3, column=1)

root = Tk()
root.title('picls2Dplot')
root.resizable(width=FALSE, height=TRUE)
app = FirstFrame(root)
root.mainloop()
