from Tkinter import *
import numpy as np
from tools import *
from dicts import *


class grid_funcs():
        def __init__(self,parent):
		self.frm = Frame(parent)
                self.frm.grid(row=0,column=0,columnspan=4,sticky=N)
		self.reg=parent.reg
		self.timedigit = parent.timedigit
		self.timemax = parent.timemax
		self.nodedigit = parent.nodedigit
		self.fname_selected = parent.fname_selected

		self.canv = tools(parent)
		self.stat_print = parent.status.set
		self.stat_clear = parent.status.clear

		self.typemasks = parent.typemasks
		self.n_ion = parent.n_ion
#		self.folder_name = parent.folder_name
		self.n_nod = parent.n_nod

#############" electro-magnetic field on the right boundary #####################""


	def em_fld_opts(self):

		self.em1_frm = Frame(self.frm)
		self.em1_frm.grid(column=0,row = 0, sticky=W,padx=10)

		self.nod_num_lab = Label(self.em1_frm,text="node index")
		self.nod_num_lab.grid(row = 0)
		self.nod_num_entr = Entry(self.em1_frm)
		self.nod_num_entr.insert(0,self.n_nod)
		self.nod_num_entr.grid(row = 1)

		self.plot_type_lab = Label(self.em1_frm,text="plot type")
                self.plot_type_lab.grid(row = 2)
		self.plot_type_lst = Listbox(self.em1_frm,exportselection=0,width=13, height=3)
		for plt_type in ['spect evol 2D','fld evol 3D', 'spect 3D']:
			self.plot_type_lst.insert(END,plt_type)
		self.plot_type_lst.select_set(1)
		self.plot_type_lst.grid(row=3)
		
		self.em2_frm = Frame(self.frm)
		self.em2_frm.grid(column=1,row = 0, sticky=W,padx=10)


		self.detect_num_lab = Label(self.em2_frm,text="detector index")
		self.detect_num_lab.grid(row = 0)
                self.detect_num_entr = Entry(self.em2_frm)
                self.detect_num_entr.insert(0,'2')
                self.detect_num_entr.grid(row = 1)

                self.tim_width_lab = Label(self.em2_frm,text="probe width")
                self.tim_width_lab.grid(row = 2)
                self.tim_width_entr = Entry(self.em2_frm)
		self.tim_width_entr.insert(0,"1000")
                self.tim_width_entr.grid(row = 3)

                self.probe_step_lab = Label(self.em2_frm, text="probe step")
                self.probe_step_lab.grid(row = 4)
                self.probe_step_entr = Entry(self.em2_frm)
		self.probe_step_entr.insert(0,"1000")
                self.probe_step_entr.grid(row = 5)

                self.freq_lab = Label(self.em2_frm,text="min:max frequencies")
                self.freq_lab.grid(row = 6)
                self.freq_entr = Entry(self.em2_frm)
		self.freq_entr.insert(0,"0:0")
                self.freq_entr.grid(row = 7)


        def em_fld_read(self):
		plt_types = ['spect evol 2D','fld evol 3D', 'spect 3D']
		plt_type = plt_types[int(self.plot_type_lst.curselection()[0])]

                nod_num = int(self.nod_num_entr.get())
                detect_num = int(self.detect_num_entr.get())
		tim_width = int(self.tim_width_entr.get())
		probe_step = int(self.probe_step_entr.get())
		freq_min = float(self.freq_entr.get().split(':')[0])
		freq_max = float(self.freq_entr.get().split(':')[1])
                return plt_type, nod_num, detect_num, tim_width, probe_step, freq_min, freq_max


###############    fields and currents widgets   ####################


	def fld_type(self):
		self.fld_typ_lab = Label(self.frm, text="field")
		self.fld_typ_lab.grid(row=0, column=1)
                self.fld_typ_lst = Listbox(self.frm,exportselection=0,width=7, height=3)
                for fld_type in ['electric','magnetic']:
                        self.fld_typ_lst.insert(END,fld_type)
		self.fld_typ_lst.select_set(0)
                self.fld_typ_lst.grid(row=1, column=1)
	def fld_type_read(self):
		if self.fname_selected == 'field':
			fld_types =['e','b']
			return fld_types[int(self.fld_typ_lst.curselection()[0])]
		if self.fname_selected == 'current':
			return ''

	def comp_type(self):
		self.cmp_lab = Label(self.frm, text="coord",wraplength=60)
		self.cmp_lab.grid(row=0, column=0,sticky=N)
		self.cmp_lst= Listbox(self.frm,exportselection=0,width=2, height=3)
		for cmp in comps:
			self.cmp_lst.insert(END,cmp)
		self.cmp_lst.select_set(2)
		self.cmp_lst.grid(row=1, column=0,sticky=N)
	def comp_type_read(self):
		return comps[int(self.cmp_lst.curselection()[0])]

	def snap_type(self):
                self.var_snap = IntVar()
                self.snapchek = Checkbutton(self.frm, text="instant",variable=self.var_snap)
                self.snapchek.grid(row=2, column=1,sticky=N)
	def snap_type_read(self):
                if self.var_snap.get() == 1:
                        return 'i/'
                elif self.var_snap.get() == 0:
                        return 's/'

#################   time step inpute widget ####################################

	def step(self):
		self.tim_step_lab = Label(self.frm, text="time step",wraplength=40)
                self.tim_step_lab.grid(row=2, column=0,sticky=N)
		self.tim_step_entr = Entry(self.frm,width=3)
		self.tim_step_entr.insert(0, self.timemax)
		self.tim_step_entr.grid(row=3, column=0,sticky=N)
	def step_read(self):
		TIM = self.tim_step_entr.get()
		if TIM == '::':
			return TIM
		else:
			while len(TIM)< self.timedigit:
				TIM='0'+TIM
			return TIM

##############    particle sort functions     #############################


        def part_type(self):
                self.part_typ_lab = Label(self.frm, text="particle sort", wraplength=80)
                self.part_typ_lab.grid(row=0, column=0)
                self.part_typ_lst = Listbox(self.frm,exportselection=0,width=7, height=3)
		if self.n_ion == 1:
			sorts=['electron','ion']
		if self.n_ion == 2:
			sorts=['electron','ion 1','ion 2']
                for part_type in sorts:
                        self.part_typ_lst.insert(END,part_type)
		self.part_typ_lst.select_set(0)
                self.part_typ_lst.grid(row=1, column=0,sticky=N)

        def part_type_read(self):
		comps = ['0','1','2']
                return comps[int(self.part_typ_lst.curselection()[0])]

#################    phase widgets   #####################################


	def phase_comp(self):
                self.phs_frm = Frame(self.frm)
                self.phs_frm.grid(row=0, column=1,rowspan=7,stick=N, padx=10)

		self.absc_lab = Label(self.phs_frm, text="absciss",wraplength=80)
                self.absc_lab.grid(row=0, column=0,sticky=N)
                self.absc_lst= Listbox(self.phs_frm,exportselection=0,width=3, height=6)
                for cmp in ['px', 'py', 'pz','x','y','e']:
                        self.absc_lst.insert(END,cmp)
                self.absc_lst.grid(row=1, column=0,sticky=N)

		self.absc_entr = Entry(self.phs_frm,width=8)
		self.absc_entr.insert(0,"0:0")
		self.absc_entr.grid(row=2, column=0,sticky=N)

                self.ord_lab = Label(self.phs_frm, text="ordinate",wraplength=80)
                self.ord_lab.grid(row=0, column=1,sticky=N)
                self.ord_lst= Listbox(self.phs_frm,exportselection=0,width=3, height=6)
                for cmp in ['px', 'py', 'pz','x','y','e']:
                        self.ord_lst.insert(END,cmp)
                self.ord_lst.grid(row=1, column=1,sticky=N)

                self.ord_entr = Entry(self.phs_frm,width=8)
                self.ord_entr.insert(0,"0:0")
                self.ord_entr.grid(row=2, column=1,sticky=N)

                self.multi_lab = Label(self.phs_frm, text="weight multiply",wraplength=80)
                self.multi_lab.grid(row=0, column=2,sticky=N)
                self.multi_lst= Listbox(self.phs_frm,exportselection=0,width=5, height=7)
                for cmp in ['px', 'py', 'pz','x','y','e','None']:
                        self.multi_lst.insert(END,cmp)
                self.multi_lst.grid(row=1, column=2,sticky=N, rowspan=2)
		self.multi_lst.select_set(6)


        def phase_comp_read(self):
                absc_min= float(self.absc_entr.get().split(':')[0])
                absc_max= float(self.absc_entr.get().split(':')[1])
                ord_min= float(self.ord_entr.get().split(':')[0])
                ord_max= float(self.ord_entr.get().split(':')[1])
		phs_comps = ['px', 'py', 'pz','x','y','e','None']
		try:
			absc_name = phs_comps[int(self.absc_lst.curselection()[0])]
			ord_name = phs_comps[int(self.ord_lst.curselection()[0])]
		except IndexError:
			self.stat_print('choose the axes')
		multi_name= phs_comps[int(self.multi_lst.curselection()[0])]
                return absc_min, absc_max, ord_min, ord_max, absc_name, ord_name,multi_name


###############"   filters input     #################""

        def filt_comp(self):
		self.filt_frm = Frame(self.frm)
		self.filt_frm.grid(row=0, column=2,rowspan=7,stick=N, padx=10)

		self.filt1_lab = Label(self.filt_frm, text="filters",wraplength=80)
                self.filt1_lab.grid(row=0, column=0,sticky=N, columnspan=3)
                self.filt1_lst= Listbox(self.filt_frm,exportselection=0,width=5, height=7)
                for cmp in ['px', 'py', 'pz','x','y','e','None']:
                        self.filt1_lst.insert(END,cmp)
		self.filt1_lst.select_set(6)
                self.filt1_lst.grid(row=1, column=0)

		self.filt1_entr = Entry(self.filt_frm,width=8)
                self.filt1_entr.insert(0,"0:0")
                self.filt1_entr.grid(row=2, column=0,sticky=N)

                self.filt2_lst= Listbox(self.filt_frm,exportselection=0,width=5, height=7)
                for cmp in ['px', 'py', 'pz','x','y','e','None']:
                        self.filt2_lst.insert(END,cmp)
		self.filt2_lst.select_set(6)
                self.filt2_lst.grid(row=1, column=1)

                self.filt2_entr = Entry(self.filt_frm,width=8)
                self.filt2_entr.insert(0,"0:0")
                self.filt2_entr.grid(row=2, column=1)

#                self.res_NRGfilter_lab = Label(self.filt_frm, text="energy")
#                self.res_NRGfilter_lab.grid(row=1, column=2,sticky=S)
#                self.res_NRGfilter_entr = Entry(self.filt_frm,width=9)
#                self.res_NRGfilter_entr.grid(row=2, column=2)
#                self.res_NRGfilter_entr.insert(0,"0:0")

###################################################################################

        def filt_read(self):
		phs_comps = ['px', 'py', 'pz','x','y','e','None']
		filt1_name = phs_comps[int(self.filt1_lst.curselection()[0])]
                filt1_min = float(self.filt1_entr.get().split(':')[0])
                filt1_max = float(self.filt1_entr.get().split(':')[1])
                filt2_name = phs_comps[int(self.filt2_lst.curselection()[0])]
                filt2_min = float(self.filt2_entr.get().split(':')[0])
                filt2_max = float(self.filt2_entr.get().split(':')[1])
		return filt1_name, filt1_min, filt1_max, filt2_name, filt2_min, filt2_max


        def phs_opts(self):
                self.res_frm = Frame(self.frm)
                self.res_frm.grid(row=0, column=4,rowspan=9,stick=N, padx=10)

#                self.res_lab = Label(self.res_frm, text="options")
#                self.res_lab.grid(row=0, column=0,columnspan=2)

                self.res_res_lab = Label(self.res_frm, text="resolution")
                self.res_res_lab.grid(row=1, column=0)
                self.res_res_entr = Entry(self.res_frm,width=10)
                self.res_res_entr.insert(0, 400)
                self.res_res_entr.grid(row=2, column=0)
                
                self.res_x_res_lab = Label(self.res_frm, text="resolution:x")
                self.res_x_res_lab.grid(row=8, column=0)
                self.res_x_res_entr = Entry(self.res_frm,width=10)
                self.res_x_res_entr.insert(0, 400)
                self.res_x_res_entr.grid(row=9, column=0)
                
                self.res_y_res_lab = Label(self.res_frm, text="resolution:y")
                self.res_y_res_lab.grid(row=8, column=1)
                self.res_y_res_entr = Entry(self.res_frm,width=10)
                self.res_y_res_entr.insert(0, 400)
                self.res_y_res_entr.grid(row=9, column=1)

                self.res_cmap_lab = Label(self.res_frm, text="colormap")
                self.res_cmap_lab.grid(row=3, column=0)
                self.res_cmap_entr = Entry(self.res_frm, width=12)
                self.res_cmap_entr.insert(0, "None")
                self.res_cmap_entr.grid(row=4, column=0)

                self.res_Fval_lab = Label(self.res_frm, text="Fmin:Fmax")
                self.res_Fval_lab.grid(row=5, column=0)
                self.res_Fval_entr = Entry(self.res_frm,width=9)
                self.res_Fval_entr.grid(row=6, column=0)
                self.res_Fval_entr.insert(0,"0:0")

        def phs_opts_read(self):
                res = self.res_res_entr.get()
                res_x = self.res_x_res_entr.get()
                res_y = self.res_y_res_entr.get()
                Fmin= float(self.res_Fval_entr.get().split(':')[0])
                Fmax= float(self.res_Fval_entr.get().split(':')[1])
#		EFmin = float(self.res_NRGfilter_entr.get().split(':')[0])
#		EFmax = float(self.res_NRGfilter_entr.get().split(':')[1])
                cmap = self.res_cmap_entr.get()
                if cmap == 'None':
                        cmap = None
                return Fmin, Fmax, res, res_x, res_y, cmap

#############  plotting options   ######################################

	def opts(self):
		self.res_frm = Frame(self.frm)
		self.res_frm.grid(row=0, column=2,rowspan=9,stick=N, padx=10)

		self.res_lab = Label(self.res_frm, text="options")
                self.res_lab.grid(row=0, column=0,columnspan=2)

#		self.res_res_lab = Label(self.res_frm, text="Resolution")
#                self.res_res_lab.grid(row=1, column=0)
#                self.res_res_entr = Entry(self.res_frm,width=10)
#		self.res_res_entr.insert(0,  400)
#                self.res_res_entr.grid(row=2, column=0)

                self.res_cmap_lab = Label(self.res_frm, text="colormap")
                self.res_cmap_lab.grid(row=3, column=1)
                self.res_cmap_entr = Entry(self.res_frm, width=12)
		self.res_cmap_entr.insert(0, "None")
                self.res_cmap_entr.grid(row=4, column=1)

                self.res_Xcoord_lab = Label(self.res_frm, text="Xmin:Xmax")
                self.res_Xcoord_lab.grid(row=1, column=0)
                self.res_Xcoord_entr = Entry(self.res_frm,width=9)
                self.res_Xcoord_entr.grid(row=2, column=0)
		self.res_Xcoord_entr.insert(0,"0:0")

                self.res_Ycoord_lab = Label(self.res_frm, text="Ymin:Ymax")
                self.res_Ycoord_lab.grid(row=1, column=1)
                self.res_Ycoord_entr = Entry(self.res_frm,width=9)
                self.res_Ycoord_entr.grid(row=2, column=1)
		self.res_Ycoord_entr.insert(0,"0:0")
		
		self.res_Fval_lab = Label(self.res_frm, text="Fmin:Fmax")
                self.res_Fval_lab.grid(row=3, column=0)
                self.res_Fval_entr = Entry(self.res_frm,width=9)
                self.res_Fval_entr.grid(row=4, column=0)
		self.res_Fval_entr.insert(0,"0:0")
  
  		self.res_x_res_lab = Label(self.res_frm, text="Resolution:x")
                self.res_x_res_lab.grid(row=5, column=0)
                self.res_x_res_entr = Entry(self.res_frm,width=10)
                self.res_x_res_entr.insert(0,  self.canv.Resolxy()[0])
                self.res_x_res_entr.grid(row=6, column=0)
           
                self.res_y_res_lab = Label(self.res_frm, text="Resolution:y")
                self.res_y_res_lab.grid(row=5, column=1)
                self.res_y_res_entr = Entry(self.res_frm,width=10)
		self.res_y_res_entr.insert(0,  self.canv.Resolxy()[1])
                self.res_y_res_entr.grid(row=6, column=1)

                self.var_3D = IntVar()
                self.chek3D = Checkbutton(self.res_frm, text="3D",variable=self.var_3D)
                self.chek3D.grid(row=1, column=2,sticky=N)


		
	def opts_read(self):
		res = self.res_res_entr.get()
  		res_x = self.res_x_res_entr.get()
    		res_y = self.res_y_res_entr.get()
		Nx1 = self.res_Xcoord_entr.get().split(':')[0]
                Nx2 = self.res_Xcoord_entr.get().split(':')[1]
                Ny1 = self.res_Ycoord_entr.get().split(':')[0]
                Ny2 = self.res_Ycoord_entr.get().split(':')[1]
		Fmin= float(self.res_Fval_entr.get().split(':')[0])
                Fmax= float(self.res_Fval_entr.get().split(':')[1])
		cmap = self.res_cmap_entr.get()
		if cmap == 'None':
			cmap = None
                if self.var_3D.get() == 1:
                        self.plot_mode = '3D'
                elif self.var_3D.get() == 0:
                        self.plot_mode = '2D'
		return Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmap


####################  spectrum calculus   ####################3

	def spect_opts(self):
               	self.spect_frm = Frame(self.frm)
               	self.spect_frm.grid(row=0, column=3,rowspan=7, stick=N,padx=10)
		self.spect_lab = Label(self.spect_frm, text="spectral opts")
                self.spect_lab.grid(row=0, column=0,columnspan=2)

                self.spect_x_var = IntVar()
                self.spect_x_check = Checkbutton(self.spect_frm, text="x",variable=self.spect_x_var)
                self.spect_x_check.grid(row=1, column=0)

                self.spect_y_var = IntVar()
                self.spect_y_check = Checkbutton(self.spect_frm, text="y",variable=self.spect_y_var)
                self.spect_y_check.grid(row=1, column=1)


                self.spect_freq_lab = Label(self.spect_frm, text="Kx_min Kx_max")
                self.spect_freq_lab.grid(row=2, column=0)
                self.spect_freq_entr = Entry(self.spect_frm,width=9)
                self.spect_freq_entr.grid(row=3, column=0)
                self.spect_freq_entr.insert(0,"0:5")

                self.spect_freq2_lab = Label(self.spect_frm, text="Ky_min Ky_max")
                self.spect_freq2_lab.grid(row=4, column=0)
                self.spect_freq2_entr = Entry(self.spect_frm,width=9)
                self.spect_freq2_entr.grid(row=5, column=0)
                self.spect_freq2_entr.insert(0,"0:5")

	def spect_opts_read(self):
                if self.spect_x_var.get() == 1 and self.spect_y_var.get() == 1:
                        spect_type= 's'
                elif self.spect_x_var.get() == 1 and self.spect_y_var.get() == 0:
                        spect_type= 'sx'
		elif self.spect_x_var.get() == 0 and self.spect_y_var.get() == 1:
			spect_type= 'sy'
		else:
			spect_type=None
		freq_min= float(self.spect_freq_entr.get().split(':')[0])
		freq_max= float(self.spect_freq_entr.get().split(':')[1])
		freq2_min= float(self.spect_freq2_entr.get().split(':')[0])
		freq2_max= float(self.spect_freq2_entr.get().split(':')[1])
		return spect_type, freq_min, freq_max, freq2_min, freq2_max

######   triggers  ########################


	def em_read_trig(self,parent):
		self.stat_clear()
                self.folder_name = parent.folder_name
                Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmp = self.opts_read()
                typ = self.fld_type_read()
                TIM = self.step_read()
		if TIM=='::':
			print 'cant read all at a time'
                comp = self.comp_type_read()
                add=self.snap_type_read()
                fname = fnames[self.fname_selected]+typ+comp
                Res = [Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x,res_y, cmp]
                reg=self.reg
                pathway = self.folder_name + pathways[fname]+add
                filemask = '*_*_*_'
		self.dat = self.canv.DensDataExtr(pathway, TIM, self.typemasks[fname],fname[-1],filemask,reg)
		self.dat = self.canv.ReShaper(self.dat)

	def em_show_trig(self,parent):
		self.folder_name = parent.folder_name
#		self.stat_clear()
                Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmp = self.opts_read()
                typ = self.fld_type_read()
                TIM = self.step_read()
                comp = self.comp_type_read()
                add=self.snap_type_read()
		spect_type, freq_min, freq_max,freq2_min, freq2_max = self.spect_opts_read()
                fname = fnames[self.fname_selected]+typ+comp
                Res = [Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmp]
                reg=self.reg
                pathway = self.folder_name + pathways[fname]+add
                filemask = '*_*_*_'
		if spect_type == 's':
                	Res = Res + [freq_min, freq_max,freq2_min, freq2_max]
                	self.maker = self.canv.SpectPlotter
		elif spect_type == 'sx' or spect_type == 'sy':
			Res =Res +[freq_min, freq_max, freq2_min, freq2_max, spect_type[-1]]
			self.maker = self.canv.SpectSpacePlotter
		else:
			self.maker = self.canv.Plotter
                if TIM=='::':
                        for i in np.arange(0,self.timemax+1):
                                time=str(i)
                                while len(time)<self.timedigit:
                                        time=str(0)+time
                                f = self.canv.DensDataExtr(pathway, time, self.typemasks[fname],fname[-1],filemask,reg)
                                f = self.canv.ReShaper(f)
                                self.maker(f,Res, 'wrt', time, fname,flag3D=self.plot_mode)
		else:
			try:
				self.maker(self.dat,Res, 'disp', TIM, flag3D=self.plot_mode)
			except AttributeError:
				self.stat_print("havent read the file or somethings wrong.")
				return

	def den_read_trig(self,parent):
		self.folder_name = parent.folder_name
#		self.stat_clear()
		Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmp = self.opts_read()
                typ = self.part_type_read()
                TIM = self.step_read()
		if TIM=='::':
			print 'cant read all at a time'
                fname = fnames[self.fname_selected]+typ
                Res = [Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmp]
                reg=self.reg
                pathway = self.folder_name + pathways[fname]
                filemask = '*_*_*_'
		self.dat = self.canv.DensDataExtr(pathway, TIM, self.typemasks[fname],fname[-1],filemask,reg)
		self.dat = self.canv.ReShaper(self.dat)
#		self.dat = self.canv.GostCellRemover(self.dat)

	def den_show_trig(self,parent):
		self.folder_name = parent.folder_name
#		self.stat_clear()
                Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmp = self.opts_read()
		typ = self.part_type_read()
                TIM = self.step_read()
		spect_type,freq_min, freq_max, freq2_min, freq2_max = self.spect_opts_read()
                fname = fnames[self.fname_selected]+typ
                Res = [Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, cmp]
                reg=self.reg
                pathway = self.folder_name +  pathways[fname]
                filemask = '*_*_*_'
                if spect_type == 's':
                        Res = Res + [freq_min, freq_max,freq2_min, freq2_max]
                        self.maker = self.canv.SpectPlotter
                elif spect_type == 'sx' or spect_type == 'sy':
                        Res = Res +[freq_min, freq_max, freq2_min, freq2_max, spect_type[-1]]
                        self.maker = self.canv.SpectSpacePlotter
                else:
                        self.maker = self.canv.Plotter
		if TIM=='::':
			self.dat=0
                        for i in np.arange(0,self.timemax+1):
                                time=str(i)
                                while len(time)<self.timedigit:
                                        time=str(0)+time
                                f = self.canv.DensDataExtr(pathway, time, self.typemasks[fname],fname[-1],filemask,reg)
                                f = self.canv.ReShaper(f)
  #                              f = self.canv.GostCellRemover(f)
                                self.maker(f,Res,'wrt', time,fname,flag3D=self.plot_mode)
		else:
			try:
				self.maker(self.dat ,Res, 'disp', TIM,fname,flag3D=self.plot_mode)
                        except AttributeError:
                                self.stat_print("haven\'t read the file or something\'s wrong.")
				return

	
        def phase_read_trig(self,parent):
#		self.stat_clear()
                self.folder_name = parent.folder_name
                Fmin, Fmax, res, res_x, res_y, cmp = self.phs_opts_read()
                TIM = self.step_read()
                typ = self.part_type_read()
		filt1 = self.filt_read()
                absc_min, absc_max, ord_min, ord_max, absc_name, ord_name, multi_name = self.phase_comp_read()
                fname = fnames[self.fname_selected]
		Res = [Fmin, Fmax, res, res_x, res_y, cmp, multi_name]
                reg=self.reg
                pathway = self.folder_name + pathways[fname]
		if self.n_ion == 1:
			filemasks={'0':'*02_*_', '1': '*01_*_'}
		if self.n_ion == 2:
			filemasks={'0':'*03_*_', '1':'*01_*_','2':'*02_*_'}
#                if typ == '0':
#                        filemask = '*02_*_'
#                elif typ == '1':
#                         filemask = '*01_*_'
		filemask = filemasks[typ]
		self.dat, self.dat2, self.wg = self.canv.PhaseDataExtr(pathway, TIM,Res, self.typemasks[fname], absc_name, ord_name,filemask,reg,filt1)

        def phase_show_trig(self,parent):
		self.folder_name = parent.folder_name
#		self.stat_clear()
		spect_type, freq_min, freq_max, freq2_min, freq2_max = self.spect_opts_read()
                Fmin, Fmax, res, res_x, res_y, cmp = self.phs_opts_read()
                TIM = self.step_read()
                typ = self.part_type_read()
		filt1 = self.filt_read()
#		comp = self.phase_comp_read()
                absc_min, absc_max, ord_min, ord_max, absc_name, ord_name,multi_name = self.phase_comp_read()
		comp = absc_min, absc_max, ord_min, ord_max, absc_name, ord_name
                fname = fnames[self.fname_selected]
                Res_read = [Fmin, Fmax, res, res_x, res_y, cmp,multi_name]
		Res = [Fmin, Fmax, res, res_x, res_y, cmp]
                reg=self.reg
                pathway = self.folder_name + pathways[fname]
                if spect_type == 's':
                        Res = Res + [freq_min, freq_max,freq2_min, freq2_max]
                        self.maker = self.canv.PhaseSpectPlotter
                else:
                        self.maker = self.canv.PhasePlotter
                if self.n_ion == 1:
                        filemasks={'0':'*02_*_', '1': '*01_*_'}
                if self.n_ion == 2:
                        filemasks={'0':'*03_*_', '1': '*01_*_','2':'*02_*_'}
#                if typ == '0':
#                        filemask = '*02_*_'
#                elif typ == '1':
#                         filemask = '*01_*_'
		filemask = filemasks[typ]
                if TIM=='::':
                        for i in np.arange(0,self.timemax+1):
                                time=str(i)
                                while len(time)<self.timedigit:
                                        time=str(0)+time
                                f, f2, wg = self.canv.PhaseDataExtr(pathway, time,Res_read, self.typemasks[fname],absc_name, ord_name,filemask,reg,filt1)
                                self.maker(f, f2, wg, Res,comp,'wrt', time, fname)
		else:
                	self.maker(self.dat, self.dat2, self.wg, Res, comp,'disp', TIM, fname)

	def em_fld_trig(self,parent):
		self.folder_name = parent.folder_name
#		self.stat_clear()
		plt_type, nod_num, detect_num, tim_width, probe_step, freq_min, freq_max = self.em_fld_read()
		nod_num = str(nod_num)
		while len(nod_num)< self.nodedigit:
			nod_num = '0'+nod_num
		self.dat = np.genfromtxt(self.folder_name + '/etc/fld_'+nod_num+'_'+'0'*3)
		if plt_type == 'spect evol 2D':
			self.canv.SpecEvolPlot(self.dat,rowind=detect_num+1,windwidth=tim_width, step=probe_step, wmin=freq_min, wmax=freq_max)
		if plt_type == 'spect 3D':
			self.canv.TemporalSpectPlot(self.dat,freq_min,freq_max)			
		if plt_type == 'fld evol 3D':
			self.canv.TemporalFldPlot(self.dat)

	def destroy(self):
		self.frm.destroy()





