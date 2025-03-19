import numpy as np
from scipy.optimize import curve_fit
import sys

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class OpticAligner:
    def __init__(self, coord, optic):
        self.coord = coord
        self.optic = optic


    def align_optic(self, startpos=None):
        if startpos is None:
            startpos = self.coord.getPos()

        val = self._scan_optic_cart(startpos, np.arange(-500, 501, 250), np.arange(-500, 501, 250))
        ax, ay, m, R = self._fit_spherical_tilt(val)

        ret = {}
        ret['valm'] = val

        ret['dthet'] = np.arange(0, 360, 20) / 180 * np.pi
        ret['dphi'] = np.arange(20, 81, 10) / 180 * np.pi

        val = self._scan_optic_spherical(m + np.array([0, 0, 2500+20]), ret['dthet'], ret['dphi'])
        ret['ax'], ret['ay'], ret['m'], ret['R'] = self._fit_spherical_tilt(val)

        uax = -0.180 * np.tan(np.deg2rad(ret['ax'])) / 0.5e-3
        uay = -0.155 * np.tan(np.deg2rad(ret['ay'])) / 0.5e-3
        outstr = f"Please adjust the screw\n-for alpha_x about {uax:.6f} turns\n-for alpha_y about {uay:.6f} turns."
        print(outstr)

        spnew = m + np.array([0, 0, 2500+100])

        ret['val'] = val
        return ret, spnew
 

    def _scan_optic_cart(self, startpos, dx, dy):
        lx = len(dx)
        ly = len(dy)

        mes = np.zeros((ly, lx, 5))

        for iy in range(ly):
            for ix in range(lx):
                newpos = startpos + [dx[ix], dy[iy], 0]
                self.absolutePos(x=[newpos[0],500], y=[newpos[1],500])
                mes[iy, ix, :3] = self.coord.getPos()
                mes[iy, ix, 3] = self.optic.getDistance()

            if iy > 0:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(mes[:, :, 0], mes[:, :, 1], -mes[:, :, 3])
                ax.set_xlabel('x [µm]')
                ax.set_ylabel('y [µm]')
                ax.set_zlabel('z [µm]')
                ax.grid(True)
                plt.draw()
                plt.pause(0.1)

        mes[:, :, 4] = mes[:, :, 2] - mes[:, :, 3]

        return mes

    def _scan_optic_spherical(self, startpos, dthet, dphi):
        lthet = len(dthet)
        lphi = len(dphi)

        mes = np.zeros((lphi, lthet, 5))
        addinf = np.zeros((lphi, lthet))

        for iphi in range(lphi): #TODO: Schauen ob das mit den Plots überhaupt so funktionert
            print(f"dphi={dphi[iphi]/np.pi*180:.1f}°:", end="")
            for ithet in range(lthet):
                print(f"{dthet[ithet]/np.pi*180:.1f}° ", end="")

                dpos = np.array(list(self._sph2cart(theta = dthet[ithet], phi = dphi[iphi], r =2500)))
                dpos[2] = 0
                pos = startpos + dpos
                #mes[iphi, ithet, :3] = feinmess('setposwait', startpos + dpos)
                self.coord.absolutePos(x=[pos[0],1000],y=[pos[1],1000])
                mes[iphi, ithet, :3] = self.coord.getPos()
                distance =  self.optic.getDistance()
                mes[iphi, ithet, 3] = distance
                addinf[iphi, ithet] = distance
                plt.plot(mes[iphi, :ithet+1, 0], mes[iphi, :ithet+1, 1], '.-')
                plt.grid(True)
                plt.xlabel('x-pos[µm]')
                plt.ylabel('optical measuring value [µm]')
                #plt.axis('equal')
                plt.draw()
            
            if iphi > 0 and lthet > 1:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.plot_surface(mes[:, :, 0], mes[:, :, 1], -mes[:, :, 3])
                ax.set_xlabel('x [µm]')
                ax.set_ylabel('y [µm]')
                ax.set_zlabel('z [µm]')
                ax.grid(True)
                ax.set_box_aspect((np.ptp(mes[:iphi+1, :, 0]), np.ptp(mes[:iphi+1, :, 1]), np.ptp(mes[:iphi+1, :, 3])))
                plt.draw()
                plt.pause(0.1)

        mes[:, :, 4] = mes[:, :, 2] - mes[:, :, 3]
        return mes


    
    
    def _sph2cart(theta, phi, r):
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return x, y, z

    def _fit_spherical_tilt(self,val):
        # Preprocessing
        s = val.shape
        if s[2] != 5:
            print('Dimensions of values have to be "n x m x 5"!')
            return None, None, None, None

        lval = val.reshape(-1, 5)
        lvall = len(lval)

        x = lval[:, 0]  # x
        y = lval[:, 1]  # y
        z = np.ones(x.shape)*np.mean(lval[:, 2])  # z
        o = lval[:, 3]

        ind = ~np.isnan(o)
        x = x[ind]
        y = y[ind]
        z = z[ind]
        o = o[ind]
        if lvall != len(o):
            print(f'{len(o)}/{lvall} measurement values are sorted out!')
            lvall = len(o)

        # Init System and Solve
        A = np.column_stack((np.ones(lvall), o, x, y, o*x, o*y))
        b = o**2 + x**2 + y**2 + z**2
        w = np.linalg.pinv(A) @ b

        m = np.array([w[2]/2, w[3]/2, 0])
        d = np.array([-w[4]/2, -w[5]/2, 0])
        
        value = 1 - (d[0]**2) - (d[1]**2)
       
        
        d[2] = -np.sqrt(np.array(abs(value)))
        

        value = z + ((w[1]/2) - d[0]*m[0] - d[1]*m[1]) / d[2]
        
        m[2] = value[0]

        R = np.sqrt(abs(w[0] + np.dot(m, m) - 2*z*m[2]))

        ax = np.degrees(np.arctan(-d[1]/d[2]))
        ay = np.degrees(np.arctan(d[0]/d[2]))

#        print(f'ax = {ax:.4f}°   ay = {ay:.4f}°  R = {R:.1f}µm')
 #       print(f'mx = {m[0]:.0f}µm my = {m[1]:.0f}µm mz = {m[2]:.0f}µm')

        return ax, ay, m, R
    
    
if __name__ == "__main__":
    aligner = OpticAligner()
    ret, spnew = aligner.align_optic()
    aligner.close()



