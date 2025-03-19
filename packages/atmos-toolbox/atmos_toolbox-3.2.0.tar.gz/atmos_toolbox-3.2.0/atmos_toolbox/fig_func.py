
import numpy as np
import matplotlib.path as mplPath

#%%

def bb_2d(b_lon, b_lat, lon_w, lat_w, b_gap=1, r0=-1e-8): #radius,
    
    """
    full name: boundary_bool_2d
    """
      
    boundary = []
    for i in np.arange(0, len(b_lon), int(b_gap)):
        AAA = (b_lon[i], b_lat[i]);
        boundary.append(AAA)
    bbPath = mplPath.Path(np.array(boundary))
    
    Lon_w, Lat_w = np.meshgrid(lon_w, lat_w)
    grid = np.zeros(Lat_w.shape)
    for xaa in lon_w:
        for yaa in lat_w:
            aaa = (xaa,yaa)
            if (bbPath.contains_point(aaa, radius=r0)==1): #radius = radius
                grid[lat_w==yaa,
                     lon_w==xaa] = 1

    return grid