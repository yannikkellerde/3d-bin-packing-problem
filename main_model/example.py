#!/usr/bin/env python
# coding: utf-8

from packer import *
import numpy as np


packer = Packer()

packer.add_bin(Bin('Auto', 130,73,62, 100))

packer.add_item(Item('Kiste', 62, 35, 38, 1))
packer.add_item(Item('Kiste', 62, 35, 38, 1))
packer.add_item(Item('Kiste', 62, 35, 38, 1))
packer.add_item(Item('Kiste', 62, 35, 38, 1))
packer.add_item(Item('PC-Kiste', 51,36,48, 1, valid_rotations=RotationType.FACE_UP))
packer.add_item(Item('Wäschekorb', 49,29,27, 1, valid_rotations=RotationType.FACE_UP))
packer.add_item(Item('Werkzeugbox', 39,19,18, 1))
packer.add_item(Item('Ikea Tüte', 40,24,18, 1))

packer.pack(bigger_first=True)





import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def set_axes_equal(ax,xmax,ymax,zmax):
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    """

    #x_limits = ax.get_xlim3d()
    #y_limits = ax.get_ylim3d()
    #z_limits = ax.get_zlim3d()
    x_limits = (0,xmax)
    y_limits = (0,ymax)
    z_limits = (0,zmax)

    print(x_limits,y_limits,z_limits)

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])
    print(x_middle,plot_radius)

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])





colormap = {
    "Kiste":[125, 79, 6],
    "PC-Kiste":[0,0,0],
    "Wäschekorb":[100,100,100],
    "Werkzeugbox":[222, 222, 0],
    "Ikea Tüte":[0,0,255],
    "Longboard":[219, 170, 9]
}





divo = 5

for b in packer.bins:
    volsum = 0
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1.0, 1.0, 1.0])
    axes = np.array([int(b.length), int(b.width),int(b.height)],dtype=int)//divo
    ax.set_xticks(np.arange(0,axes[0]+1,10//divo))
    ax.set_yticks(np.arange(0,axes[1]+1,10//divo))
    ax.set_zticks(np.arange(0,axes[2]+1,10//divo))
    data = np.zeros(axes, dtype=np.bool)
    colors = np.zeros(axes.tolist() + [4], dtype=np.float32)

    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    for item in b.items:
        volsum += item.get_volume()
        dim = np.array(item.get_dimension(),dtype=int)//divo
        p = np.array(item.position,dtype=int)//divo
        colors[int(p[0]):int(dim[0]+p[0]),int(p[1]):int(dim[1]+p[1]),int(p[2]):int(dim[2]+p[2]),:] = np.array(colormap[item.name]+[160])/255
        data[int(p[0]):int(dim[0]+p[0]),int(p[1]):int(dim[1]+p[1]),int(p[2]):int(dim[2]+p[2])] = True
        print(item.get_dimension())
        print("====> ", item.string())

    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("====> ", item.string())
    ax.voxels(data, facecolors=colors)
    set_axes_equal(ax,*axes)
    print("Container volume:",b.get_volume())
    print("Items volume:",volsum)
    plt.show()
    print("***************************************************")
    print("***************************************************")

