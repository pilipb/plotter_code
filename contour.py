import scipy
import matplotlib.pyplot as plt
import numpy as np
import imageio

# make a voronoi centroid map for an image
def voronoi_centroids(img, n):
    # find the centroids of the image
    centroids = scipy.ndimage.measurements.center_of_mass(img, img, range(1, n+1))
    # make a voronoi diagram
    vor = scipy.spatial.Voronoi(centroids)
    # return the voronoi diagram and the centroids
    return vor, centroids

# make a voronoi centroid map for waves.jpg
img = im = imageio.imread('waves.jpg')
vor, centroids = voronoi_centroids(img, 10)
print(centroids[0][:][0])
# plot the voronoi diagram
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(img)
# for cen in centroids:
#     ax.plot(cen[0], cen[1], 'r.')
for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
    simplex = np.asarray(simplex)
    if np.all(simplex >= 0):
        ax.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1], 'k-')
center = vor.points.mean(axis=0)
ax.plot(vor.vertices[:,0], vor.vertices[:,1], 'go')

    # ax.plot(vor.vertices[:,0], vor.vertices[:,1], 'go')
# for region in vor.regions:
#     if not -1 in region:
#         polygon = [vor.vertices[i] for i in region]
#         ax.plot(*zip(*polygon), color='b')
plt.show()