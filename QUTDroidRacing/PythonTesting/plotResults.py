from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import csv

from numpy import linspace, meshgrid
from matplotlib.mlab import griddata

thetas = []
xs = []
ys = []
zs = []
with open('ResultsUnity2.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		thetas.append(float(row[0]))
		xs.append(float(row[1]))
		ys.append(float(row[2]))
		zs.append(float(row[3]))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# xs = [0,1,2,3,4] 
# ys = [0,1,2,3,4]    
# zs = [0,1,2,3,4] 
index = zs.index(max(zs))
maxTheta = thetas[index]
maxX = xs[index]
maxY = ys[index]
print "Theta, X, Y, score: ", maxTheta, maxX, maxY, zs[index]
thetas = np.asarray(thetas)
xs = np.asarray(xs)
ys = np.asarray(ys)
zs = np.asarray(zs)

LEAVE_OUT = 'a'
if LEAVE_OUT == 'theta':
	xPlot = xs[thetas == maxTheta]
	yPlot = ys[thetas == maxTheta]
	zPlot = zs[thetas == maxTheta]
	ax.scatter(xPlot, yPlot, zPlot)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
elif LEAVE_OUT == 'X':
	xPlot = thetas[xs == maxX]
	yPlot = ys[xs == maxX]
	zPlot = zs[xs == maxX]
	ax.scatter(xPlot, yPlot, zPlot)
	ax.set_xlabel('theta')
	ax.set_ylabel('Y')
elif LEAVE_OUT == 'Y':
	xPlot = thetas[ys == maxY]
	yPlot = xs[ys == maxY]
	zPlot = zs[ys == maxY]
	ax.scatter(xPlot, yPlot, zPlot)
	ax.set_xlabel('theta')
	ax.set_ylabel('X')
else:
	xPlot = xs
	yPlot = ys
	zPlot = zs
	ax.scatter(xPlot, yPlot, zPlot)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')


plt.show()  