import numpy as np
from pylab import imshow, rfft, fftfreq, savefig, clf, title,fft2
import mpl_toolkits.mplot3d.axes3d

from mpl_toolkits.mplot3d import Axes3D

from fnmatch import fnmatch
from os import  listdir
from namelist import Namelist
from string import replace
from dicts import *
import gzip


class tools():
	def __init__(self,parent):
		self.fig = parent.fig
		self.stat_print = parent.status.set
		self.stat_clear = parent.status.clear
		self.canvas = parent.canvas
		self.fname_selected = parent.fname_selected
		self.folder_name = parent.folder_name
		self.out_name_add = self.folder_name.split('/')[-1]
		
	def OptsExtr(self):
        	names = np.sort(listdir(self.folder_name+'/'))
        	for name in names:
	                if fnmatch(name, '*.in'):
                        	inputname = self.folder_name +'/'+ name
				break
	        self.nxd = int(Namelist(inputname).get('diag').get('par')[0].get('nx_d')[0])
        	self.nyd = int(Namelist(inputname).get('diag').get('par')[0].get('ny_d')[0])
		self.wgmmax = float(Namelist(inputname).get('geom').get('par')[0].get('wgmmax')[0].replace('d','e'))
	        N_nodes=int(Namelist(inputname).get('option').get('par')[0].get('nd_para')[0])
        	ow=float(replace( Namelist(inputname).get('wave').get('par')[0].get('ow')[0],'d','e'))
		self.ow = ow
	        c=float(replace( Namelist(inputname).get('geom').get('par')[0].get('c')[0],'d','e'))
	        nnx=int(Namelist(inputname).get('geom').get('par')[0].get('nx')[0])
	        nny=int(Namelist(inputname).get('geom').get('par')[0].get('ny')[0])
	        syslx=float(replace( Namelist(inputname).get('geom').get('par')[0].get('system_lx')[0],'d','e'))
	        sysly=float(replace( Namelist(inputname).get('geom').get('par')[0].get('system_ly')[0],'d','e'))
	        Nx = nnx/self.nxd +1
	        Ny = nny/self.nyd +1
	        Lx=ow*syslx/(2*np.pi*c)
	        Ly=ow*sysly/(2*np.pi*c)
	        return Nx, Ny, Lx, Ly, N_nodes

	def Resolxy(self):
        	names = np.sort(listdir(self.folder_name+'/'))
        	for name in names:
	                if fnmatch(name, '*.in'):
                        	inputname = self.folder_name +'/'+ name
				break
	        nnx=int(Namelist(inputname).get('geom').get('par')[0].get('nx')[0])
	        nny=int(Namelist(inputname).get('geom').get('par')[0].get('ny')[0])
	        return nnx, nny

	def more_opts_extr(self):
		names = np.sort(listdir(self.folder_name+'/'))
		for name in names:
                        if fnmatch(name, '*.in'):
                                inputname= self.folder_name+'/'+name
				break
		ndav = int(Namelist(inputname).get('diag').get('par')[0].get('ndav')[0])
		int_snap = int(Namelist(inputname).get('diag').get('par')[0].get('int_snap')[0])
		c=float(replace( Namelist(inputname).get('geom').get('par')[0].get('c')[0],'d','e'))
		return ndav, int_snap, c

	def macropart_extr(self):
                names = np.sort(listdir(self.folder_name+'/'))
                for name in names:
                        if fnmatch(name, '*.in'):
                                inputname= self.folder_name+'/'+name
				break
                np_i = float(Namelist(inputname).get('ions').get('par')[0].get('np_i')[0])
                p_mass_i = float(Namelist(inputname).get('ions').get('par')[0].get('p_mass_i')[0].replace('d','e'))
                np_e = float(Namelist(inputname).get('eons').get('par')[0].get('np_e')[0])
                p_mass_e = float(Namelist(inputname).get('eons').get('par')[0].get('p_mass_e')[0].replace('d','e'))
		no_ion =  int(Namelist(inputname).get('ions').get('par')[0].get('no_ion')[0])
                return np_i, np_e, p_mass_i, p_mass_e, no_ion

	def DensDataExtr(self,pathway,TIM,typemask,type, filemask='*_*_*_',reg=None):
		self.stat_print("reading..")
	        names = np.sort(listdir(pathway))
	        namestime=[]
	        for name in names:
                	if fnmatch(name, filemask+TIM+'*'):
	                        namestime=np.append(namestime,pathway+name)
	        namestime=np.sort(namestime)
	        f=np.array([])
	        for name in namestime:
                	if open(name).readlines():
	                        if reg == None:
                                	a = np.memmap(name, dtype=typemask)
                        	elif reg == 'zip':
	                                a = np.loadtxt(name, dtype=typemask)
                        	f=np.append(f,np.array(a[:][type], dtype='float32'))
			else:
				self.stat_clear()
				self.stat_print('file is missing or empty')
		self.stat_print('got it')
        	return f


        def PhaseDataExtr(self,pathway,TIM,Res,typemask,type_absc,type_ord, filemask,reg, filt1):
		self.stat_print("reading..")
		Fmin, Fmax, res, res_x, res_y, clrmap, multi_name = Res
		filt1_name, filt1_min, filt1_max, filt2_name, filt2_min, filt2_max = filt1
		Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
		np_i, np_e, p_mass_i, p_mass_e, no_ion = self.macropart_extr()
		typ = int(filemask.split('_')[0][1:])
		if no_ion == 1 and typ == 1:
		        n_p = np_i
                        p_mass = p_mass_i
		elif no_ion == 1 and typ == 2:
			n_p = np_e
			p_mass = p_mass_e
		elif no_ion == 2 and typ == 1:
                        n_p = np_i
                        p_mass = p_mass_i
                elif no_ion == 2 and typ == 2:
                        n_p = np_i_2
                        p_mass = p_mass_i_2
                elif no_ion == 2 and typ == 3:
                        n_p = np_e
                        p_mass = p_mass_e
                names = np.sort(listdir(pathway))
                namestime=[]
                for name in names:
                        if fnmatch(name, filemask+TIM+'*'):
                                namestime=np.append(namestime,pathway+name)
                namestime=np.sort(namestime)
                f = np.array([])
		f2 = np.array([])
        	wg = np.array([])
		filt_num = 0
                for name in namestime:
			if reg == 'zip':
				try:
					opentest = gzip.open(name).readline()
				except IOError:
					if open(name).readline():
						self.stat_print("seems some files are no gzipped. will try to open them anyway")
						opentest = True
			else:
				opentest = open(name).readline()
                        if opentest:
                                if reg == None:
                                        a = np.memmap(name, dtype=typemask)
                                elif reg == 'zip':
                                        a = np.loadtxt(name, dtype=typemask)
					if a.shape==():
						a.shape = (1,)
				wgs = np.array(a[:]['wght'],dtype='float32')/n_p/Nx/Ny
				filt_array1 = np.array(np.ones(len(wgs)),dtype=bool)
                                filt_array2 = np.array(np.ones(len(wgs)),dtype=bool)
				filt_array3 = np.array(np.ones(len(wgs)),dtype=bool)
				filt_array = np.array(np.zeros(len(wgs)),dtype=bool)
				filt_flag= False
#				filt_array2 = [True]*len(wgs)
#                                filt_array3 = [True]*len(wgs)
				if filt1_name == 'e' or filt2_name == 'e' or type_absc == 'e' or type_ord == 'e' or multi_name == 'e':
                                        px=np.array(a[:]['px'],dtype='float32')
                                        py=np.array(a[:]['py'],dtype='float32')
                                        pz=np.array(a[:]['pz'],dtype='float32')
					nrg = p_mass*0.511*(np.sqrt(px**2+py**2+pz**2+1)-1)
				if filt1_name == 'e':
					filt_flag= True
                                        filt_val = nrg
                                        filt_array1 = filt_array1*np.less(filt_val, filt1_max*np.ones(len(filt_val)))
                                        filt_array1 = filt_array1*np.greater(filt_val, filt1_min*np.ones(len(filt_val)))
					filt_array = filt_array + filt_array1
                                        filt_num += sum(filt_array1)
				elif filt1_name!='None' and filt1_name!='e':
					filt_flag= True
					filt_val = np.array(a[:][filt1_name],dtype='float32')
					filt_array1 = filt_array1*np.less(filt_val, filt1_max*np.ones(len(filt_val)))
					filt_array1 = filt_array1*np.greater(filt_val, filt1_min*np.ones(len(filt_val)))
					filt_num += sum(filt_array1)
					filt_array = filt_array + filt_array1
				if filt2_name == 'e':
                                        filt_flag= True
                                        filt_val = nrg
                                        filt_array2 = filt_array2*np.less(filt_val, filt2_max*np.ones(len(filt_val)))
                                        filt_array2 = filt_array2*np.greater(filt_val, filt2_min*np.ones(len(filt_val)))
					filt_array = filt_array + filt_array2
                                        filt_num += sum(filt_array2)
	                        elif filt2_name != 'None' and filt2_name!='e':
					filt_flag= True
                                        filt_val = np.array(a[:][filt2_name],dtype='float32')
                                        filt_array2 = filt_array2*np.less(filt_val, filt2_max*np.ones(len(filt_val)))
                                        filt_array2 = filt_array2*np.greater(filt_val, filt2_min*np.ones(len(filt_val)))
                                        filt_num += sum(filt_array2)
					filt_array = filt_array + filt_array2
#				if EFmax!=0 or EFmin!=0:
#					filt_flag= True
#					px=np.array(a[:]['px'],dtype='float32')
#					py=np.array(a[:]['py'],dtype='float32')
#					pz=np.array(a[:]['pz'],dtype='float32')
#					nrg = p_mass*0.511*(np.sqrt(px**2+py**2+pz**2+1)-1)
#					filt_array3 = filt_array3*np.less(nrg, EFmax*np.ones(len(nrg)))
#					filt_array3 = filt_array3*np.greater(nrg, EFmin*np.ones(len(nrg)))
#					filt_num += sum(filt_array3)
#					filt_array = filt_array + filt_array3
				if type_absc == 'e':
					f = np.append(f,nrg)
				else:
					f = np.append(f, np.array(a[:][type_absc],dtype='float32'))
				if type_ord == 'e':
					f2 = np.append(f2,nrg)
				else:
					f2 = np.append(f2, np.array(a[:][type_ord],dtype='float32'))
				if filt_flag == False:
					filt_array = np.array(np.ones(len(wgs)),dtype=bool)
				wgs = wgs*filt_array
				if multi_name == 'e':
					wg = np.append(wg, wgs*nrg)
				elif multi_name == 'None':
                                	wg = np.append(wg, wgs)
				else:
					wg = np.append(wg,wgs*np.array(a[:][multi_name],dtype='float32'))
				
                        else:
				self.stat_clear()
                                self.stat_print('file is missing or empty')
		self.stat_clear()
		if filt_flag == True:
			self.stat_print(str(len(f)-filt_num)+' particles filtered out; '+str(filt_num) + ' particles read')
		else:
			self.stat_print( str(len(f))+' particles read')
                return f, f2, wg


	def ReShaper(self,f):
	        Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
	        Ny_act = len(f)/Nx
	        f=f.reshape( (Ny_act,Nx))
		if self.fname_selected=='density':
			f /= self.ow**2
		if (abs(Ny_act-Ny)>0 and self.fname_selected=='density') or (abs(Ny_act-Ny)>0 and self.fname_selected=='energy'):
			f = self.GostCellRemover(f)
	        return f

	def GostCellRemover(self, f):
		Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
	        arr=np.array([], dtype=int)
	        Nyp=Ny/N_nodes +1
	        for i in np.arange(1,N_nodes):
                	f[Nyp*i,:] = f[Nyp*i,:] + f[(Nyp*i-1),:]
                	arr=np.append(arr,(Nyp*i-1))
        	f=np.delete(f,arr,0)
        	return f

	def StepDef(self,Res):
		Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, clrmap = Res
	        Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
                res, res_x, res_y, Nx1, Nx2, Ny1, Ny2 = int(res), int(res_x), int(res_y), float(Nx1),float(Nx2),float(Ny1),float(Ny2)
                Nx1=np.rint(Nx1*Nx/Lx);Nx2=np.rint(Nx2*Nx/Lx);Ny1=np.rint(Ny1*Nx/Lx);Ny2=np.rint(Ny2*Nx/Lx)
		if Nx2==0:
			Nx2 = Nx
		if Ny2==0:
                        Ny2 = Ny
#                if Nx2-Nx1 > res_x:
                if Nx2-Nx1 > res_x:
#	                dx=np.rint((Nx2-Nx1)/res)
	                dx=np.rint((Nx2-Nx1)/res_x)
                else:
	                dx=1
#                if Ny2-Ny1 >res:
                if Ny2-Ny1 >res_y:
#	                dy=np.rint((Ny2-Ny1) /res)
	                dy=np.rint((Ny2-Ny1) /res_y)
                else:
	                dy=1
	        return dx, dy

	def Plotter(self,f,Res, reg, TIM, out_name = None, flag3D='2D',frmt='png'):
	        Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
		ndav, int_step, cc = self.more_opts_extr()
		actual_time = int(TIM)*int_step/ndav
	        X=np.linspace(0,Lx,Nx)
	        Y=np.linspace(0,Ly,Ny)
	        Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, clrmap = Res
		res, res_x, res_y, Nx1, Nx2, Ny1, Ny2 = int(res), int(res_x), int(res_y), float(Nx1),float(Nx2),float(Ny1),float(Ny2)
                Nx1=int(np.rint(Nx1*Nx/Lx));Nx2=int(np.rint(Nx2*Nx/Lx))
		Ny1=int(np.rint(Ny1*Ny/Ly));Ny2=int(np.rint(Ny2*Ny/Ly))
		if Nx2==0:
                        Nx2 = Nx-1
                if Ny2==0:
                        Ny2 = Ny-1
	        dx, dy = self.StepDef(Res)
		extntX=[X[Nx1],X[Nx2]]
		extntY=[Y[Ny1],Y[Ny2]]
		def bb(N):
			if N == 0:
				return None
			else:
				return N
		Ny1,Ny2,Nx1,Nx2,Fmin, Fmax = map(bb, [Ny1,Ny2,Nx1,Nx2,Fmin, Fmax])			
		my_extent=extntX+extntY
		self.fig.clear()
		if flag3D == '2D':
			sp = self.fig.add_subplot(111, title='time step = '+str(actual_time)+r'$ \tau_0$')
	        	sp.set_xlabel(r'$x/\lambda_0$',fontsize=14)
       			sp.set_ylabel(r'$y/\lambda_0$',fontsize=14)
# plot making
			pplt = sp.imshow(f[Ny1:Ny2:dy,Nx1:Nx2:dx],vmin=Fmin,vmax=Fmax,extent=my_extent, aspect = 'auto', interpolation=intrp, origin='lower',cmap=clrmap)
			self.fig.colorbar(pplt)
		if flag3D == '3D':
			XX, YY = np.meshgrid(X[Nx1:Nx2:dx], Y[Ny1:Ny2:dy])
			sp = Axes3D(self.fig,  title='time step = '+str(actual_time)+r'$ \tau_0$')
#			sp = self.fig.add_subplot(111, title='time step = '+str(actual_time)+r'$ \tau_0$', projection='3d')
#			sp.plot_wireframe(XX,YY,f[Ny1:Ny2:dy,Nx1:Nx2:dx],cmap = 'jet',cstride=20,rstride = 20)
#			sp.plot_surface(XX,YY,f[Ny1:Ny2:dy,Nx1:Nx2:dx],cmap = clrmap,cstride=5,rstride = 5, linewidth=0)
#			sp.plot3D(np.ravel(XX), np.ravel(YY), np.ravel(f[Ny1:Ny2:dy,Nx1:Nx2:dx]))
                        sp.plot_surface(XX,YY,f[Ny1:Ny2:dy,Nx1:Nx2:dx],cmap = clrmap, linewidth=0)
		self.canvas.show()
		if reg == 'wrt':
			self.fig.savefig('./img/'+self.out_name_add+'_'+out_name+'_'+TIM+'.'+frmt)
			clf()
		return			

	def PhasePlotter(self, f, f2, wg, Res, comp, reg, TIM, out_name = None, frmt='png'):
		Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
                ndav, int_step, cc = self.more_opts_extr()
                actual_time = int(TIM)*int_step/ndav
		Fmin, Fmax, res, res_x, res_y, clrmap = Res
		absc_min, absc_max, ord_min, ord_max, absc_name, ord_name = comp
		if len(res.split('x'))>1:
			resX = int(res.split('x')[0])
			resY = int(res.split('x')[1])
		else:
			resX = int(res)
			resY = resX
		if absc_name == 'y' and absc_max==0. and absc_min==0.:
			L_absc = 0.
                	R_absc=Ly
        	elif absc_name == 'x' and absc_max==0. and absc_min==0.:
			L_absc = 0.
                	R_absc=Lx
		else:
			R_absc=absc_max
			L_absc=absc_min

                if ord_name == 'y' and ord_max==0. and ord_min == 0.:
                        L_ord = 0.
                        R_ord=Ly
			
                elif ord_name == 'x' and ord_max==0. and ord_min == 0.:
                        L_ord = 0.
                        R_ord=Lx
                else:
                        R_ord=ord_max
                        L_ord=ord_min
		a,b,c = np.histogram2d(f2, f, bins= ( resY, resX ), range=[[L_ord, R_ord],[L_absc, R_absc]],normed=False, weights = resX*resY*wg)
                if Fmin == 0.:
                         Fmin = None
                if Fmax == 0.:
                        Fmax= None
		self.fig.clear()
		sp = self.fig.add_subplot(111, title='time step = '+str(actual_time)+r'$ \tau_0$')
#	        if comp == 'x':
#        	        sp.set_xlabel(r'$x/\lambda_0$',fontsize=16)
#                	sp.set_ylabel(r'$p_x/mc$',fontsize=16)
#        	elif comp == 'y':
#	                sp.set_xlabel(r'$y/\lambda_0$',fontsize=16)
#                	sp.set_ylabel(r'$p_y/mc$',fontsize=16)
#        	elif comp == 'd':
#	                xlabel(r'$x/\lambda_0$',fontsize=16)
#                	ylabel(r'$y/\lambda_0$',fontsize=16)
        	pplt = sp.imshow(a,extent=[c[0], c[-1],b[0], b[-1]], aspect = 'auto', interpolation= intrp ,cmap = clrmap, origin='lower',vmin = Fmin, vmax = Fmax)
		self.fig.colorbar(pplt)
		self.canvas.show()
		if reg == 'wrt':
                        self.fig.savefig('./img/'+self.out_name_add+'_'+out_name+'_'+TIM+'.'+frmt)
                        clf()
                return

	def PhaseSpectPlotter(self, f, f2, wg, Res, comp, reg, TIM, out_name = None, frmt='png'):
                Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
                ndav, int_step, cc = self.more_opts_extr()
                actual_time = int(TIM)*int_step/ndav
                Fmin, Fmax, res, res_x, res_y, clrmap, freq_min, freq_max,freq2_min, freq2_max = Res
#                freq_min,freq_max = float(freq_min), float(freq_max)
                absc_min, absc_max, ord_min, ord_max, absc_name, ord_name = comp
		try:
                	if len(res.split('x'))>1:
	                        resX = int(res.split('x')[0])
                        	resY = int(res.split('x')[1])
                	else:
	                        resX = int(res)
                        	resY = resX
		except ValueError:
			self.stat_print("something's wrong with resolution")			
                if absc_name == 'y' and absc_max==0. and absc_min==0.:
                        L_absc = 0.
                        R_absc=Ly
                elif absc_name == 'x' and absc_max==0. and absc_min==0.:
                        L_absc = 0.
                        R_absc=Lx
                else:
                        R_absc=absc_max
                        L_absc=absc_min

                if ord_name == 'y' and ord_max==0. and ord_min == 0.:
                        L_ord = 0.
                        R_ord=Ly

                elif ord_name == 'x' and ord_max==0. and ord_min == 0.:
                        L_ord = 0.
                        R_ord=Lx
                else:
                        R_ord=ord_max
                        L_ord=ord_min
                a,b,c = np.histogram2d(f2, f, bins= ( resY, resX ), range=[[L_ord, R_ord],[L_absc, R_absc]],normed=False, weights = resX*resY*wg)
                if Fmin == 0.:
                         Fmin = None
                if Fmax == 0.:
                        Fmax= None
                aa = abs(fft2(a))[:len(b)/2,:len(c)/2]
                freqX = fftfreq(len(c),c[1]-c[0])[:len(c)/2]
                freqY = fftfreq(len(b),b[1]-b[0])[:len(b)/2]
                self.fig.clear()
		sp = self.fig.add_subplot(111, title='time step = '+str(actual_time)+r'$ \tau_0$')
		pplt = sp.imshow(aa,vmin=Fmin,vmax=Fmax,extent=[freqX[0],freqX[-1],freqY[0],freqY[-1]], aspect = 'auto', interpolation=intrp,cmap = clrmap, origin='lower')
                sp.axis((freq_min,freq_max,freq2_min, freq2_max))
                self.fig.colorbar(pplt)
		self.canvas.show()


##################################################################
	def SpectPlotter(self,f,Res, reg, TIM = None, out_name = None , flag3D='2D',frmt='png'):
                Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
                ndav, int_step, cc = self.more_opts_extr()
                actual_time = int(TIM)*int_step/ndav
                Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, clrmap, freq_min, freq_max,freq2_min, freq2_max = Res
                res, res_x, res_y, Nx1, Nx2, Ny1, Ny2, freq_min,freq_max = int(res), int(res_x), int(res_y), float(Nx1),float(Nx2),float(Ny1),float(Ny2), float(freq_min), float(freq_max)
		Nx1=int(np.rint(Nx1*Nx/Lx));Nx2=int(np.rint(Nx2*Nx/Lx)) 
                Ny1=int(np.rint(Ny1*Ny/Ly));Ny2=int(np.rint(Ny2*Ny/Ly))
	        dX=Lx/Nx
	        dY=Ly/Ny
		if Fmin == 0.:
                	Fmin = None
                if Fmax == 0.:
                        Fmax= None
                if Nx2==0:
                        Nx2 = Nx-1
                if Ny2==0:
                        Ny2 = Ny-1
		dx, dy = self.StepDef(Res[:-4])
		dx=int(np.ceil(dx/2.))
		dy=int(np.ceil(dy/2.))
               	aa = abs(fft2(f[Ny1:Ny2,Nx1:Nx2]))[:(Ny2-Ny1)/2:dy,:(Nx2-Nx1)/2:dx]
               	freqX = fftfreq(Nx2-Nx1, dX)[:(Nx2-Nx1)/2:dx]
               	freqY = fftfreq(Ny2-Ny1, dY)[:(Ny2-Ny1)/2:dy]
		self.fig.clear()
		if flag3D == '3D':
                        XX, YY = np.meshgrid(freqX, freqY)
			Xmin_ind = int(len(freqX)*freq_min/freqX[-1])
			Xmax_ind = int(len(freqX)*freq_max/freqX[-1])
                        Ymin_ind = int(len(freqY)*freq_min/freqY[-1])
                        Ymax_ind = int(len(freqY)*freq_max/freqY[-1])
                        sp = Axes3D(self.fig,  title='time step = '+str(actual_time)+r'$ \tau_0$')
#			sp.set_zlim3d(Fmin,Fmax)
#			sp.set_xlim3d(freq_min,freq_max)
			sp.set_ylim3d(freq_min,freq_max)
                        sp.plot_surface(XX[Ymin_ind:Ymax_ind,Xmin_ind:Xmax_ind],YY[Ymin_ind:Ymax_ind,Xmin_ind:Xmax_ind],aa[Ymin_ind:Ymax_ind,Xmin_ind:Xmax_ind],cmap = clrmap, linewidth=0)
                if flag3D == '2D':
			sp = self.fig.add_subplot(111, title='time step = '+str(actual_time)+r'$ \tau_0$')
               		pplt = sp.imshow(aa,vmin=Fmin,vmax=Fmax,extent=[freqX[0],freqX[-1],freqY[0],freqY[-1]], aspect = 'auto', interpolation=intrp,cmap = clrmap, origin='lower')
               		sp.set_xlabel(r'$k_x/k_0$',fontsize=14)
               		sp.set_ylabel(r'$k_y/k_0$',fontsize=14)
               		sp.axis((freq_min,freq_max,freq2_min, freq2_max))
               		self.fig.colorbar(pplt)
		self.canvas.show()
                if reg == 'wrt':
                        self.fig.savefig('./img/'+self.out_name_add+'_'+out_name+'_s_'+TIM+'.'+frmt)
                        clf()
                return


	def SpectSpacePlotter(self,f,Res, reg, TIM = None, out_name = None, flag3D='2D', frmt='png'):
		Nx, Ny, Lx, Ly, N_nodes = self.OptsExtr()
                ndav, int_step, cc = self.more_opts_extr()
                actual_time = int(TIM)*int_step/ndav
                Nx1, Nx2, Ny1, Ny2, Fmin, Fmax, res, res_x, res_y, clrmap, freq_min, freq_max,freq2_min, freq2_max, ax = Res
                res, res_x, res_y, Nx1, Nx2, Ny1, Ny2,freq_max = int(res), int(res_x), int(res_y), float(Nx1),float(Nx2),float(Ny1),float(Ny2), float(freq_max)
                Nx1=int(np.rint(Nx1*Nx/Lx));Nx2=int(np.rint(Nx2*Nx/Lx))
                Ny1=int(np.rint(Ny1*Ny/Ly));Ny2=int(np.rint(Ny2*Ny/Ly))
                dX=Lx/Nx
                dY=Ly/Ny
		X=np.linspace(0,Lx,Nx)
                Y=np.linspace(0,Ly,Ny)
		dx, dy = self.StepDef(Res[:-5])
                if Fmin == 0.:
                        Fmin = None
                if Fmax == 0.:
                        Fmax= None
                if Nx2==0:
                        Nx2 = Nx-1
                if Ny2==0:
                        Ny2 = Ny-1
        	if ax=='x':
	                Nn1=Nx
                	Nn2=Ny
                	Xx=X
                	Yy=Y
                	Ll=Ly
			ddx=int(np.ceil(dx/2.))
                	ddy=dy
			freq_min, freq_max = freq_min, freq_max
        	elif ax=='y':
			f=f.transpose()
	                Nn1=np.shape(f)[1]
                	Nn2=Nx
                	Xx=Y
                	Yy=X
                	Ll=Lx
                	ddx=int(np.ceil(dy/2.))
                	ddy=dx
			freq_min, freq_max = freq2_min, freq2_max
        	datFFT =  np.zeros((Nn2, Nn1/2+1))
        	XFFT = abs(fftfreq( Nn1, Xx[1])[:Nn1/2+1])
        	for j in np.arange(Nn2):
	                datFFT[j] = abs(rfft(f[j]))
		myextent=[XFFT[0],XFFT[-1],Yy[0],Yy[-1]]
                self.fig.clear()
                if flag3D == '3D':
                        XX, YY = np.meshgrid(XFFT, Yy)
                        sp = Axes3D(self.fig,  title='time step = '+str(actual_time)+r'$ \tau_0$')
                        sp.plot_surface(XX,YY,datFFT, cmap = clrmap, linewidth=0)
			sp.set_zlim3d(Fmin,Fmax)
                if flag3D == '2D':
                	sp = self.fig.add_subplot(111, title='time step = '+str(actual_time)+r'$ \tau_0$')
	        	if ax=='x':
                		sp.set_ylabel(r'$y/\lambda_0$',fontsize=14)
                		sp.set_xlabel(r'$k_x/k_0$',fontsize=14)
        		elif ax=='y':
	               		sp.set_ylabel(r'$x/\lambda_0$',fontsize=14)
                		sp.set_xlabel(r'$k_y/k_0$', fontsize=14)
	        	pplt = sp.imshow(datFFT[::ddy,::ddx],extent=myextent, aspect = 'auto', interpolation=intrp,origin='lower',vmin=Fmin, vmax=Fmax, cmap = clrmap)
	        	sp.axis((freq_min,freq_max,0,Ll))
                	self.fig.colorbar(pplt)
                self.canvas.show()
                if reg == 'wrt':
                        self.fig.savefig('./img/'+self.out_name_add+'_'+out_name+'_s'+ax+'_'+TIM+'.'+frmt)
                        clf()
                return

        def SpecEvolPlot(self, d,windwidth,step,wmin,wmax, rowind):
                dd=np.array([])
		ndav, int_step, cc = self.more_opts_extr()
                Tim=np.arange(windwidth, len(d)-windwidth,step)
                for n in Tim:
                        dd=np.append(dd, np.abs(rfft(d[n-windwidth:n+windwidth,rowind]))[:-1])
                Freq=fftfreq(2*windwidth, (d[1,0]-d[0,0])/(ndav/cc))[:windwidth]
		if wmax!=0:
                	nFrqMax= int(wmax/(Freq[1]-Freq[0]))
		else:
			nFrqMax=len (Freq)
                nFrqMin= int(wmin/(Freq[1]-Freq[0]))
                dd=dd.reshape(len(Tim),len(Freq))[:,nFrqMin:nFrqMax].transpose()
                self.fig.clear()
                sp = self.fig.add_subplot(111)
                pplt = sp.imshow(dd, origin='lower',aspect='auto',extent=[d[Tim[0],0]/(ndav/cc), d[Tim[-1],0]/(ndav/cc),Freq[nFrqMin],Freq[nFrqMax]])
		sp.set_xlabel(r'$t/\tau_0$',fontsize=14)
		sp.set_ylabel(r'$\omega/\omega_0$',fontsize=14)
		self.fig.colorbar(pplt)
                self.canvas.show()
                return


        def TemporalSpectPlot(self, d,wmin,wmax):
                self.fig.clear()
		sp = Axes3D(self.fig)
		ndav, int_step, cc = self.more_opts_extr()
		ll = len(d[0])-1
		for i in ll-np.arange(ll):
	        	y=i*np.ones(len(d)/2)
	        	sp.plot(fftfreq(len(d), (d[1,0]-d[0,0])/(ndav/cc))[:len(d)/2], y ,abs(rfft(d[:,i]))[:-1])
	        	sp.set_xlim3d(wmin,wmax)
		sp.set_xlabel(r'$\omega/\omega_0$',fontsize=14)
		sp.set_ylabel('node index',fontsize=14)
		sp.set_zlabel(r'$\langle E_z \rangle_\omega$',fontsize=14)
		self.canvas.show()

        def TemporalFldPlot(self, d):
                self.fig.clear()
		sp = Axes3D(self.fig)
                ndav, int_step, cc = self.more_opts_extr()
		if len(d)>3000:
			res = len(d)/3000
		else:
			res=1
		time = d[::res,0]/(ndav/cc)
        	ll = len(d[0])-1
        	for i in ll-np.arange(ll):
	                sp.plot(time, i*np.ones(len(time)), d[::res,i])
		sp.set_xlabel(r'$t/\tau_0$',fontsize=14)
                sp.set_ylabel('node index',fontsize=14)
                sp.set_zlabel(r'$E_z$',fontsize=14)
                self.canvas.show()
