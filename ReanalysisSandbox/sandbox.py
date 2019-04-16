from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.examples.arrows import sample_data

file = './Data/pgb.anl.201903.cantos364362.nc'

ds = Dataset(file, mode='r')
lats = ds.variables['lat_2'][:]
lons = ds.variables['lon_2'][:]

time = ds.variables['initial_time0_hours'][:]
wind_v = ds.variables['V_GRD_2_ISBL'][:][10][3]
wind_u = ds.variables['U_GRD_2_ISBL'][:][10][3]

print (ds)
fig, ax = plt.subplots(subplot_kw=dict(projection=ccrs.PlateCarree()))

def quadrado(centro, dist):
    south = centro[0] - dist
    north = centro[0] + dist
    east = centro[1] - dist
    west = centro[1] + dist
    return south, north, east, west

ponto = [-22, -47]
s,n,e,w = quadrado(ponto, 10)
ax.set_extent([e, w, s, n])
#ax.set_extent([-90, 75, 10, 60])
ax.stock_img()

ax.coastlines()
x, y, u, v, vector_crs = sample_data(shape=(80, 100))

print(lats[::2].shape, lons[::2, ].shape, wind_v.shape , wind_v[::2].shape)
print(max(wind_v[1]-180), min(lons-180))
print(x.shape, y.shape, u.shape, v.shape)



magnitude2 = (wind_u ** 2 + wind_v ** 2) ** 0.5
wind_v[1] = wind_v[1] - 180
wind_u[1] = wind_u[1] - 180
lons = lons - 180
ax.streamplot(lons, lats, wind_u, wind_v, linewidth=1, density=3, color=magnitude2)

sk = 2
ax.barbs(lons[::sk], lats[::sk], wind_u[::sk,::sk], wind_v[::sk,::sk], linewidth=1)

plt.show()
