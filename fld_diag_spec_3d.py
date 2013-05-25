#! /usr/bin/env python

from pylab import figure, loadtxt, arange, ones,fftfreq, rfft
from mpl_toolkits.mplot3d import Axes3D

fig = figure()
ax = Axes3D(fig)

inp = raw_input("input xfel_xx number xx and node index:").split(' ')

xx = inp[0]

node=inp[1]

d = loadtxt('../xfel_'+xx+'/etc/fld_00'+node+'_000')

ll = len(d[0])-1

for i in ll-arange(ll):
	y=i*ones(len(d)/2)
	ax.plot(fftfreq(len(d), 0.04)[:len(d)/2], y ,abs(rfft(d[:,i]))[:-1])
        ax.set_xlim3d(0.9,1.1)
        fig.show()

fig.show()

raw_input("Press Enter to continue...")
