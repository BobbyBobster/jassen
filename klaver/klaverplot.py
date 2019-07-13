import numpy as np
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


# TODO: Turn this 3d plotting script into a separate module for testing and debug purposes
d.shuffle()
p.hand = d.cards[0:8]
b.resetBelief()


# setup the figure and axes
fig = plt.figure(figsize=(8, 8))
ax0 = fig.add_subplot(221, projection='3d')
ax1 = fig.add_subplot(222, projection='3d')
ax2 = fig.add_subplot(223, projection='3d')
ax3 = fig.add_subplot(224, projection='3d')
# fake data
# create grid of all cards (4x8)
_x = np.arange(4)
_y = np.arange(8)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel() 

def createTop(playerNumber):
    top = []
    for rank in range(8):
        for suit in range(4):
            top.append(b.pmf[suit, rank, playerNumber])
    return top

bottom = np.zeros_like(createTop(1))
width = depth = 1

ax0.set_zlim3d(bottom=0, top=1)
ax0.bar3d(x, y, bottom, width, depth, createTop(0))
ax0.set_title('Player 0')

ax1.set_zlim3d(bottom=0, top=1)
ax1.bar3d(x, y, bottom, width, depth, createTop(1))
ax1.set_title('Player 1')

ax2.set_zlim3d(bottom=0, top=1)
ax2.bar3d(x, y, bottom, width, depth, createTop(2))
ax2.set_title('Player 2')

ax3.set_zlim3d(bottom=0, top=1)
ax3.bar3d(x, y, bottom, width, depth, createTop(3))
ax3.set_title('Player 3')

plt.show()
