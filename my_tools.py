from pylab import *
#from scipy import *

class tools():
        def my_print(self):
                print "hi"

        def growth_rateEWOK(self,d,start=2000,end = 25000, row = 1, dt=0.04):
                xdata = dt*np.arange(end-start)
                ydata = log(abs(d[start:end,row]))
                coeffs = polyfit(xdata,ydata,1)
                return coeffs[0]

	def growth_rate(self,d,start=2000,end = 25000, row = 1):
		xdata = d[start:end,0]/2.5
		ydata = log(abs(d[start:end,row]))
		coeffs = polyfit(xdata,ydata,1)
		return coeffs[0]

        def growth_rate_fit(self,d,start=2000,end = 25000, row = 1):
                xdata = d[start:end,0]/2.5
                ydata = log(abs(d[start:end,row]))
                coeffs = polyfit(xdata,ydata,1)
		yfit = polyval(coeffs, xdata)
                return xdata, yfit

	def all_detectors_read(self,index, nnodes = 8, address = '../XFEL_SCRATCH/xfel_', extension = '/etc/fld_'):
		d=[]
		index = str(index)
		nodes = np.arange(nnodes)
		while len(index)<2:
                	index = '0'+index
		for node in nodes:
			node = str(node)
			while len(node)<3:
                        	node = '0'+node
			d.append(loadtxt(address+index+extension+node+'_000'))
		return d

	def all_detectors_shaper(self,d):
		shape0 = np.shape(d)
		nnodes = shape0[0]
		detector_data = np.arange(nnodes)
		time_data = d[0][:,0]/2.5
		data = zeros((shape0[1],0))
		for i in detector_data:
			data = np.hstack((data,d[i][:,1:]))
		return data.transpose(), time_data, detector_data

	def arrays_read(self,index_array=[1,2,3,4,5,6,7,8],address = '../XFEL_SCRATCH/xfel_', extension = '/etc/fld_004_000'):
		"""
		reading modif-PICLS2D em field data from address folders with the names containig indexes index_array
		"""
		d=[]
		for i in index_array:
			indx_name = str(i)
			while len(indx_name)<2:
				indx_name = '0'+indx_name
			d.append(loadtxt(address+indx_name+extension))
		return d

	def growth_rate_array(self,d,start=2000,end = 25000, row = 1):
		gr=[]
		for d0 in d:
			gr.append(self.growth_rate(d0,start,end, row))
		return gr


tool = tools()


