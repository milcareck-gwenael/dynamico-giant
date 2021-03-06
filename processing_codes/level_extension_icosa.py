##################################
import numpy as np
import netCDF4 as nc
from scipy import *
##################################

### NetCDF file on 64 levels created by makestart: just to take theta_rhodz
ncfile="start_icosa_1.nc"
file = nc.Dataset(ncfile,'r')
theta               = file.variables['theta_rhodz'][:,:]

### NetCDF file on 32 levels that contains q,theta_rhodz, u, ulon, ulat
ncfile="start_icosa_270_aspiga.nc"

### Get variables
file = nc.Dataset(ncfile,'r')

lat_mesh            = file.variables['lat_mesh'][:]
lon_mesh            = file.variables['lon_mesh'][:]
bounds_lon_mesh     = file.variables['bounds_lon_mesh'][:,:]
bounds_lat_mesh     = file.variables['bounds_lon_mesh'][:,:]
lev                 = file.variables['lev'][:]
nq                  = file.variables['nq'][:]
lat_u               = file.variables['lat_u'][:]
lon_u               = file.variables['lon_u'][:]
bounds_lon_u        = file.variables['bounds_lon_u'][:,:]
bounds_lat_u        = file.variables['bounds_lat_u'][:,:]
iteration           = file.variables['iteration'][:]
ps                  = file.variables['ps'][:,:]
phis                = file.variables['phis'][:,:]
q                   = file.variables['q'][:,:,:,:] 
#theta32             = file.variables['theta_rhodz'][:,:,:]
u                   = file.variables['u'][:,:,:]
ulat                = file.variables['ulat'][:,:,:]
ulon                = file.variables['ulon'][:,:,:]

file.close()

#########################################################################################################
###                              Creation of NetCDF file on 64 levels 
#########################################################################################################

axis_nbounds = 2
cell_mesh = 252812
nvertex_mesh = 6
nq = 1
cell_u = 758430
nvertex_u= 2

newlvl = 61
#newlvl = 32

#output = nc.Dataset('start_icosa_270.nc','w',format='NETCDF4')
output = nc.Dataset('start_icosa_270-smooth.nc','w',format='NETCDF4')

output.createDimension('cell_mesh',cell_mesh)
output.createDimension('lev',newlvl)
output.createDimension('nq',nq)
output.createDimension('cell_u',cell_u)
output.createDimension('axis_nbounds',axis_nbounds)
output.createDimension('nvertex_mesh',nvertex_mesh)
output.createDimension('nvertex_u',nvertex_u)
output.createDimension('time_counter',0)

lat_meshlvl64            = output.createVariable('lat_mesh','f4','cell_mesh')
lon_meshlvl64            = output.createVariable('lon_mesh','f4','cell_mesh')
bounds_lon_meshlvl64     = output.createVariable('bounds_lon_mesh','f4',('cell_mesh','nvertex_mesh'))
bounds_lat_meshlvl64     = output.createVariable('bounds_lat_mesh','f4',('cell_mesh','nvertex_mesh'))
lev                      = output.createVariable('lev','f4','lev')
nqlvl64                  = output.createVariable('nq','f4','nq')
lat_ulvl64               = output.createVariable('lat_u','f4','cell_u')
lon_ulvl64               = output.createVariable('lon_u','f4','cell_u')
bounds_lon_ulvl64        = output.createVariable('bounds_lon_u','f4',('cell_u','nvertex_u'))
bounds_lat_ulvl64        = output.createVariable('bounds_lat_u','f4',('cell_u','nvertex_u'))
iterationlvl64           = output.createVariable('iteration','f4')#,0)
pslvl64                  = output.createVariable('ps','f4',('cell_mesh'))
phislvl64                = output.createVariable('phis','f4',('cell_mesh'))
qlvl64                   = output.createVariable('q','f4',('nq','lev','cell_mesh'))
thetalvl64               = output.createVariable('theta_rhodz','f4',('lev','cell_mesh'))
ulvl64                   = output.createVariable('u','f4',('lev','cell_u'))
ulatlvl64                = output.createVariable('ulat','f4',('lev','cell_mesh'))
ulonlvl64                = output.createVariable('ulon','f4',('lev','cell_mesh'))

################################ GET GLOBAL ATTRIBUTES FOR NEW FILE ######################################

output.name        = 'restart_icosa'
output.description = 'Created by xios'
output.title       = 'Created by xios'
output.Conventions = 'CF-1.6'
output.timeStamp   = '2018-Jun-01 20:49:38 GMT'
output.uuid        = 'cfddba90-e494-44e1-b07d-1bd53a2a748a' 

################################# GET ATTRIBUTES FOR NEW VARIABLES #######################################

qlvl64.online_operation     = 'once'
qlvl64.coordinates          = 'lat_mesh lon_mesh'

pslvl64.online_operation    = 'once'
pslvl64.coordinates         = 'lat_mesh lon_mesh'

phislvl64.online_operation  = 'once'
phislvl64.coordinates       = 'lat_mesh lon_mesh'

thetalvl64.online_operation = 'once'
thetalvl64.coordinates      = 'lat_mesh lon_mesh'

ulonlvl64.online_operation  = 'once'
ulonlvl64.coordinates       = 'lat_mesh lon_mesh'

ulatlvl64.online_operation  = 'once'
ulatlvl64.coordinates       = 'lat_mesh lon_mesh'

ulvl64.online_operation     = 'once'
ulvl64.coordinates          = 'lat_u lon_u'
	
lat_meshlvl64.standard_name = 'latitude'
lat_meshlvl64.long_name     = 'Latitude'
lat_meshlvl64.units         = 'degrees_north'
lat_meshlvl64.bounds        = 'bounds_lat_mesh'

lon_meshlvl64.standard_name = 'longitude'
lon_meshlvl64.long_name     = 'Longitude'
lon_meshlvl64.units         = 'degrees_east'
lon_meshlvl64.bounds        = 'bounds_lon_mesh'

lat_ulvl64.standard_name    = 'latitude'
lat_ulvl64.long_name        = 'Latitude'
lat_ulvl64.units            = 'degrees_north'
lat_ulvl64.bounds           = 'bounds_lat_u'

lon_ulvl64.standard_name    = 'longitude'
lon_ulvl64.long_name        = 'Longitude'
lon_ulvl64.units            = 'degrees_east'
lon_ulvl64.bounds           = 'bounds_lon_u'

#nqlvl64.name = 'nq'

lev.standard_name           = 'atmosphere_hybrid_sigma_pressure_coordinate'
lev.long_name               = 'hybrid level at midpoints'
lev.positive                = 'down'

#iteration.online_operation  = 'once'
#iteration.coordinates       = ' '

################################# GET VALUES FOR NEW VARIABLES ########################################

lat_meshlvl64[:]            = lat_mesh
lon_meshlvl64[:]            = lon_mesh
bounds_lon_meshlvl64[:]     = bounds_lon_mesh
bounds_lat_meshlvl64[:]     = bounds_lat_mesh
nqlvl64[:]                  = nq
lat_ulvl64[:]               = lat_u
lon_ulvl64[:]               = lon_u
bounds_lon_ulvl64[:]        = bounds_lon_u
bounds_lat_ulvl64[:]        = bounds_lat_u
iterationlvl64[:]           = 8.608032e+07 #time iteration value of this specific start file
pslvl64[:]                  = ps[0,:]
phislvl64[:]                = phis[0,:]
lev[:]                      = range(1,62,1)
thetalvl64[:]               = theta

# Initialisation:
ulvl64[:,:]    = 0.
ulonlvl64[:,:] = 0.
ulatlvl64[:,:] = 0.

# Calculations:
for i in range(30):
	ulvl64[i,:]     = u[0,i,:]
	ulonlvl64[i,:]  = ulon[0,i,:]
	ulatlvl64[i,:]  = ulat[0,i,:]
	#thetalvl64[i,:] = theta32[0,i,:]
	qlvl64[:,i,:]   = q[0,:,i,:]

# Linear decreasing to zero between 30th and 45th vertical levels
for i in range(15):
	ulvl64[i+30,:]     = (15-i)*u[0,29,:]/15.
	ulonlvl64[i+30,:]  = (15-i)*ulon[0,29,:]/15.
	ulatlvl64[i+30,:]  = (15-i)*ulat[0,29,:]/15.
# Exponential decreasing to zero between 30th and 45th vertical levels 
#for i in range(15):
#	ulvl64[i+30,:]     = 
#	ulonlvl64[i+30,:]  = 
#	ulatlvl64[i+30,:]  = 

for i in range(31):
	#thetalvl64[i+30,:] = theta[i+30,:]
	qlvl64[:,i+30,:]   = q[0,:,29,:]

print "i, u_64, q_64"
for i in range(61):
        print i,ulvl64[i,3456],qlvl64[0,i,3456]

# tests
print("q_lvl32",shape(q))
print("q_lvl64",shape(qlvl64))
print("level",shape(lev))


output.close()
