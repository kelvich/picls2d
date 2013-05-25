#! /usr/bin/env python

from pylab import figure, loadtxt, arange, ones
from mpl_toolkits.mplot3d import Axes3D


fig = figure()

flag=True

while flag:
	fig.clf()
	ax = Axes3D(fig)
	inp = raw_input("input xfel_xx number xx and node index:").split(' ')
	xx = inp[0]
	node=inp[1]
	d = loadtxt('../xfel_'+xx+'/etc/fld_00'+node+'_000')
	time = d[::5,0]/2.5
	ll = len(d[0])-1
	for i in ll-arange(ll):
	        ax.plot(time, i*ones(len(time)), d[::5,i])
		fig.show()
	fig.show()
	if raw_input("Press Enter to continue ") == 'exit':
		flag=False
