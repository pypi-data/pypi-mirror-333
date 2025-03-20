try:
    # framework is running
    from .startup_choice import *
except ImportError as _excp:
    # class is imported by itself
    if (
        'attempted relative import with no known parent package' in str(_excp)
        or 'No module named \'omfit_classes\'' in str(_excp)
        or "No module named '__main__.startup_choice'" in str(_excp)
    ):
        from startup_choice import *
    else:
        raise

from omfit_classes.omfit_ascii import OMFITascii

import xarray
import numpy as np

from scipy.interpolate import griddata

__all__ = ['OMFITmars', 'OMFITnColumns', 'OMFITmarsProfile']


class OMFITmars(SortedDict, OMFITobject):
    """
    Class used to interface with MARS results directory

    :param filename: directory where the MARS result files are stored

    :param extra_files: Any extra files that should be loaded

    :param Nchi: Poloidal grid resolution for real-space
    """

    def __init__(self, filename=None, extra_files=[], Nchi=None, **kw):

        if Nchi is None:
            Nchi = 200
            printw(f'OMFITmars using default Nchi value of {Nchi}')

        if isinstance(filename, (list, tuple)):
            kw['tunnel'] = filename[2]
            kw['server'] = filename[1]
            filename = filename[0]

        if ',' not in filename:
            outputs = [
                'BPLASMA.OUT',
                'BPLASMA',
                'JACOBIAN.OUT',
                'JACOBIAN',
                'RMZM_F.OUT',
                'RMZM_F',
                'XPLASMA.OUT',
                'XPLASMA',
                'JPLASMA.OUT',
                'JPLASMA',
                'PROFEQ.OUT',
                'PROFEQ',
                'RESULT.OUT',
                'RESULT',
                'FREQUENCIES.OUT',
                'TIMEEVOL.OUT',
                'DWK_ENERGY_DENSITY.OUT',
                'PROFNTV.OUT',
                'TORQUENTV.OUT',
                'PROFNUSTAR.OUT',
            ]
            outputs += extra_files
            filename = ','.join([filename + os.sep + x for x in outputs])

        kw['file_type'] = 'dir'
        OMFITobject.__init__(self, filename, **kw)
        self.OMFITproperties.pop('file_type', 'dir')
        self.OMFITproperties['Nchi'] = Nchi
        self.sim = 'sim0'
        SortedDict.__init__(self)
        self.dynaLoad = True

    """
    Reading methods, used to read MARS output files.
    """

    def read_RMZM(self, filename):
        with open(filename) as fin:
            x = [ii.strip() for ii in fin.readlines()]

        RMZM_F = np.zeros((len(x), 4))

        for ii, line in enumerate(x):
            RMZM_F[ii] = line.split()

        # Number of poloidal harmonics for equilibrium (RMZM)
        Nm0 = int(RMZM_F[0, 0])
        Ns1 = int(RMZM_F[0, 1])
        Ns2 = int(RMZM_F[0, 2])

        R0EXP = RMZM_F[0, 3]
        B0EXP = RMZM_F[1, 3]

        Ns = Ns1 + Ns2

        NRATSURF = int(RMZM_F[1, 1])
        Iratsurf = np.array(RMZM_F[2 : NRATSURF + 2, 1], int)
        # s coordinate over full domain
        s = np.array(RMZM_F[1 : Ns + 1, 0], float)
        # s coordinate in plasma
        sp = np.array(RMZM_F[1 : Ns1 + 1, 0], float)
        # s coordinate in vacuum
        svac = np.array(RMZM_F[Ns1 + 1 : Ns + 1, 0], float)
        RM = np.array(RMZM_F[Ns + 1 :, 0] + RMZM_F[Ns + 1 :, 1] * 1j, complex)
        ZM = np.array(RMZM_F[Ns + 1 :, 2] + RMZM_F[Ns + 1 :, 3] * 1j, complex)

        RM = np.reshape(RM, (Nm0, Ns)).T
        ZM = np.reshape(ZM, (Nm0, Ns)).T

        RM[:, 1:] = 2 * RM[:, 1:]
        ZM[:, 1:] = 2 * ZM[:, 1:]
        Nchi = self.OMFITproperties['Nchi']

        self[self.sim]['RM'] = xarray.DataArray(RM, dims=['s', 'm'], coords={'m': range(Nm0), 's': s})
        self[self.sim]['ZM'] = xarray.DataArray(ZM, dims=['s', 'm'], coords={'m': range(Nm0), 's': s})
        self[self.sim]['sp'] = xarray.DataArray(sp, dims=['sp'], coords={'sp': sp}, attrs={'Description': 's-coord in plasma domain'})
        self[self.sim]['svac'] = xarray.DataArray(
            svac, dims=['svac'], coords={'svac': svac}, attrs={'Description': 's-coord in vacuum domain'}
        )
        self[self.sim]['Iratsurf'] = xarray.DataArray(Iratsurf)
        self[self.sim]['R0EXP'] = xarray.DataArray(R0EXP)
        self[self.sim]['B0EXP'] = xarray.DataArray(B0EXP)
        self[self.sim]['Ns1'] = xarray.DataArray(Ns1, attrs={'Description': 'Number of radial points in plasma'})
        self[self.sim]['Ns2'] = xarray.DataArray(Ns2, attrs={'Description': 'Number of radial points in vacuum'})
        self[self.sim]['Nm0'] = xarray.DataArray(Nm0, attrs={'Description': 'Number of poloidal harmonics for equilibrium'})
        self[self.sim]['Nchi'] = xarray.DataArray(Nchi, attrs={'Description': 'Number of points along poloidal angle (from CHEASE)'})

        return RM, ZM

    def read_JPLASMA(self, filename, JNORM=1.0):
        """
        Read JPLASMA.OUT file corresponding to perturbed currents

        :param filename: name of file

        :param JNORM: normalization
        """
        JPLASMA = np.loadtxt(filename)
        # Nm1 = Number of poloidal harmonics for stability (perturbed quantities, M1...M2)
        Nm1, Ns, n, _, _, _ = map(int, JPLASMA[0, :])
        JPLASMA = JPLASMA[1:, :]

        Mm = JPLASMA[:Nm1, 1].astype(int)
        JM1 = JPLASMA[Nm1:, 0] + 1j * JPLASMA[Nm1:, 1]
        JM2 = JPLASMA[Nm1:, 2] + 1j * JPLASMA[Nm1:, 3]
        JM3 = JPLASMA[Nm1:, 4] + 1j * JPLASMA[Nm1:, 5]

        JM1 = np.reshape(JM1, (Nm1, Ns)).T
        JM2 = np.reshape(JM2, (Nm1, Ns)).T
        JM3 = np.reshape(JM3, (Nm1, Ns)).T
        JM1 = JM1 * JNORM
        JM2 = JM2 * JNORM
        JM3 = JM3 * JNORM

        # Note that JM1 is defined at half-points, recompute at integer-points
        x = np.asarray((self[self.sim]['s'][0:Ns] + self[self.sim]['s'][1 : Ns + 1]) * 0.5)
        JM1new = copy.deepcopy(JM1)
        JM1new[1:-1, :] = griddata(x.flatten(), JM1[0:-1, :], np.asarray(self[self.sim]['s'][1 : Ns - 1]).flatten(), method='cubic')
        JM1new[0, :] = 0
        JM1new[-1, :] = JM1new[-2, :]
        JM1 = copy.deepcopy(JM1new)

        # Patch first three points
        JM1[0:3] = 0.0
        JM2[0:3] = 0.0
        JM3[0:3] = 0.0

        # Remove surface currents
        if True:
            II = np.where((self[self.sim]['s'] > 0.9985) & (self[self.sim]['s'] <= 1.0))
            JM1[II[0][:]] = 0
            JM2[II[0][:]] = 0
            JM3[II[0][:]] = 0

        #  get phase of JM2 for m=2 harmonic at rational surface Iratsurf(1)
        #  and modify phase to remove real part
        if len(self[self.sim]['Iratsurf']):
            from cmath import log

            m0 = 2
            I0 = int(self[self.sim]['Iratsurf'][0])
            m1 = int(m0 - Mm[0] + 1)
            p0 = -np.angle(JM2[I0 - 1, m1 - 1]) + np.pi / 2.0
            f0 = np.exp(1j * p0)
            JM1 = JM1 * f0
            JM2 = JM2 * f0
            JM3 = JM3 * f0
        self['JPLASMA'] = xarray.Dataset()
        self['JPLASMA']['JM1'] = xarray.DataArray(JM1, dims=['s', 'Mm'], coords={'s': self[self.sim]['s'][:Ns], 'Mm': Mm})
        self['JPLASMA']['JM2'] = xarray.DataArray(JM2, dims=['s', 'Mm'], coords={'s': self[self.sim]['s'][:Ns], 'Mm': Mm})
        self['JPLASMA']['JM3'] = xarray.DataArray(JM3, dims=['s', 'Mm'], coords={'s': self[self.sim]['s'][:Ns], 'Mm': Mm})

    def read_BPLASMA(self, filename, BNORM=1.0):
        """
        Read BPLASMA.OUT file corresponding to perturbed magnetic field

        :param filename: name of file

        :param BNORM: normalization
        """
        spline_B23 = 1
        BPLASMA = np.loadtxt(filename)
        Nm1, Ns, n, _, _, _ = map(int, BPLASMA[0, :])
        BPLASMA = BPLASMA[1:, :]

        Mm = BPLASMA[:Nm1, 1].astype(int)

        BM1 = BPLASMA[Nm1:, 0] + 1j * BPLASMA[Nm1:, 1]
        BM2 = BPLASMA[Nm1:, 2] + 1j * BPLASMA[Nm1:, 3]
        BM3 = BPLASMA[Nm1:, 4] + 1j * BPLASMA[Nm1:, 5]

        BM1 = np.reshape(BM1, (Nm1, Ns)).T
        BM2 = np.reshape(BM2, (Nm1, Ns)).T
        BM3 = np.reshape(BM3, (Nm1, Ns)).T

        BM1 = BM1[0:Ns, :] * BNORM
        BM2 = BM2[0:Ns, :] * BNORM
        BM3 = BM3[0:Ns, :] * BNORM
        if spline_B23 == 2:
            BM2[1:, :] = BM2[0:-1, :]
            BM3[1:, :] = BM3[0:-1, :]
        elif spline_B23 == 1:
            x = np.asarray((self[self.sim]['s'][0 : Ns - 1] + self[self.sim]['s'][1:Ns]) * 0.5)
            # B2
            BM2new = copy.deepcopy(BM2)
            BM2new[1:-1, :] = griddata(x.flatten(), BM2[0:-1, :], np.asarray(self[self.sim]['s'][1 : Ns - 1]).flatten(), method='cubic')
            BM2new[0, :] = 0
            BM2new[-1, :] = BM2new[-2, :]
            BM2 = copy.deepcopy(BM2new)
            # B3
            BM3new = copy.deepcopy(BM3)
            BM3new[1:-1, :] = griddata(x.flatten(), BM3[0:-1, :], np.asarray(self[self.sim]['s'][1 : Ns - 1]).flatten(), method='cubic')
            BM3new[0, :] = 0
            BM3new[-1, :] = BM3new[-2, :]
            BM3 = copy.deepcopy(BM3new)
        self['BPLASMA'] = xarray.Dataset()
        self['BPLASMA']['BM1'] = xarray.DataArray(BM1, dims=['s', 'Mm'], coords={'s': self[self.sim]['s'][:Ns], 'Mm': Mm})
        self['BPLASMA']['BM2'] = xarray.DataArray(BM2, dims=['s', 'Mm'], coords={'s': self[self.sim]['s'][:Ns], 'Mm': Mm})
        self['BPLASMA']['BM3'] = xarray.DataArray(BM3, dims=['s', 'Mm'], coords={'s': self[self.sim]['s'][:Ns], 'Mm': Mm})

    def read_XPLASMA(self, filename, XNORM=1.0):
        """
        Read XPLASMA.OUT file corresponding to perturbed plasma displacement

        :param filename: name of file

        :param XNORM: normalization
        """
        XPLASMA = np.loadtxt(filename)
        # Here Ns is the number of grid points in plasma (what elsewhere is Ns1)
        Nm1, Ns, n, _, _, _ = map(int, XPLASMA[0, :])
        XPLASMA = XPLASMA[1:, :]
        Mm = XPLASMA[:Nm1, 1].astype(int)
        #
        dPSIds = XPLASMA[Nm1 : Nm1 + Ns, 0]
        T = XPLASMA[Nm1 : Nm1 + Ns, 3]
        XM1 = XPLASMA[Nm1 + Ns :, 0] + 1j * XPLASMA[Nm1 + Ns :, 1]
        XM2 = XPLASMA[Nm1 + Ns :, 2] + 1j * XPLASMA[Nm1 + Ns :, 3]
        XM3 = XPLASMA[Nm1 + Ns :, 4] + 1j * XPLASMA[Nm1 + Ns :, 5]
        XM1 = np.reshape(XM1, (Nm1, Ns)).T
        XM2 = np.reshape(XM2, (Nm1, Ns)).T
        XM3 = np.reshape(XM3, (Nm1, Ns)).T
        XM1 = XM1[0:Ns, :] * XNORM
        XM2 = XM2[0:Ns, :] * XNORM
        XM3 = XM3[0:Ns, :] * XNORM
        # Recalculate XM2 and XM3 at integer points (they are defined at half-points)
        x = np.asarray((self[self.sim]['s'][0 : Ns - 1] + self[self.sim]['s'][1:Ns]) * 0.5)
        # X2
        XM2new = copy.deepcopy(XM2)
        XM2new[1:-1, :] = griddata(x.flatten(), XM2[0:-1, :], np.asarray(self[self.sim]['s'][1 : Ns - 1]).flatten(), method='cubic')
        XM2new[0, :] = 0
        XM2new[-1, :] = XM2new[-2, :]
        XM2 = copy.deepcopy(XM2new)
        # X3
        XM3new = copy.deepcopy(XM3)
        XM3new[1:-1, :] = griddata(x.flatten(), XM3[0:-1, :], np.asarray(self[self.sim]['s'][1 : Ns - 1]).flatten(), method='cubic')
        XM3new[0, :] = 0
        XM3new[-1, :] = XM3new[-2, :]
        XM3 = copy.deepcopy(XM3new)
        # change central points of XM2 (see MacReadVPLASMA)
        XM2[:, 0] = XM2[:, 2]
        XM2[:, 1] = XM2[:, 2]
        self['XPLASMA'] = xarray.Dataset()
        # Displacement only defined within plasma, radial coordinate is 'sp'
        self['XPLASMA']['XM1'] = xarray.DataArray(XM1, dims=['sp', 'Mm'], coords={'sp': self[self.sim]['sp'], 'Mm': Mm})
        self['XPLASMA']['XM2'] = xarray.DataArray(XM2, dims=['sp', 'Mm'], coords={'sp': self[self.sim]['sp'], 'Mm': Mm})
        self['XPLASMA']['XM3'] = xarray.DataArray(XM3, dims=['sp', 'Mm'], coords={'sp': self[self.sim]['sp'], 'Mm': Mm})
        self[self.sim]['dPSIds'] = xarray.DataArray(dPSIds, dims=['sp'], coords={'sp': self[self.sim]['sp']})
        self[self.sim]['T'] = xarray.DataArray(T, dims=['sp'], coords={'sp': self[self.sim]['sp']})

    def read_RESULTS(self, filename):
        with open(filename) as fin:
            lines = fin.read().splitlines()
            tmp = list(map(float, lines[-1].split()))
        if len(tmp):
            self[self.sim]['NITR'] = xarray.DataArray(tmp[1])
            self[self.sim]['TALPHA1'] = xarray.DataArray(complex(tmp[2], tmp[3]))
            self[self.sim]['EIG'] = xarray.DataArray(complex(tmp[4], tmp[5]), attrs={'Description': 'Output eigenvalue', 'units': '-'})

    def read_PROFEQ(self, filename):
        """
        Read equilibrium quantities used for MARS calculation
        Returns profiles in physical units, not MARS normalization

        :param filename: name of MARS output file, usually PROFEQ.OUT

        """
        from scipy.constants import mu_0

        R0 = self[self.sim]['R0EXP'].values.astype(float)
        B0 = self[self.sim]['B0EXP'].values.astype(float)

        data = np.loadtxt(filename)

        SY = [
            ('s_eq', 's equilibrium (no wall included)', None),
            ('q_prof', 'safety factor', None),
            ('j_prof', 'current density', B0 / (mu_0 * R0)),
            ('p_prof', 'pressure', B0 * B0 / mu_0),
            ('n_prof', 'density', None),
            ('v_prof', 'toroidal rotation', None),
            ('eta', 'resistivity=tau_A / tau_R = 1/S', None),
            ('Gamma', 'Gamma', None),
            ('visc_prof', 'viscosity', None),
            ('Ti_prof', 'Ti', None),
            ('Te_prof', 'Te', None),
            ('dpsi/ds', 'dpsi/ds', None),
            ('F', 'F', None),
            ('omega_*i', 'ion dia. drift freq.', None),
            ('omega_*e', 'e- dia. drift freq.', None),
            ('CSV', 'CSV', None),
            ('erot_prof', 'electron rotation', None),
            ('nu_i', 'ion eff. collisionality', None),
            ('nu_e', 'e- eff. collisionality', None),
            ('zeff', 'Z effective', None),
        ]

        x = data[:, 0]
        self['PROFEQ'] = xarray.Dataset()
        for k, (name, des, units) in enumerate(SY):
            if k < data.shape[1]:
                y = np.array(data[:, k])
                if units is not None:
                    y = y * units
                self['PROFEQ'][name] = xarray.DataArray(y, dims=['s_eq'], coords={'s_eq': x}, attrs={'Description': des})
            else:
                printw('%s information is missing from %s file' % (des, os.path.split(filename)[1]))

    def read_FREQS(self, filename):
        """
        Reads all frequencies related to drift kinetic resonances

        :param filename: name of MARS output file, usually FREQUENCIES.OUT
        """
        data = np.loadtxt(filename)
        s = data[:, 0]
        we = data[:, 1]
        wsni = data[:, 2]
        wsne = data[:, 3]
        wsti = data[:, 4]
        wste = data[:, 5]
        awbp = data[:, 6]
        awbt = data[:, 7]
        awdi = data[:, 8]
        awdi[0] = awdi[2]
        awdi[1] = awdi[2]
        awde = data[:, 9]
        awda = data[:, 10]
        awda[0] = awda[2]
        awda[1] = awda[2]
        fracp = data[:, 11]
        fract = data[:, 12]

        lam1 = data[:, 13]
        lam0 = data[:, 14]
        lam2 = data[:, 15]
        awda1 = data[:, 16]
        awda2 = data[:, 17]

        # Storing data
        self['FREQUENCIES'] = xarray.Dataset()
        self['FREQUENCIES']['s'] = xarray.DataArray(s, dims=['s'], coords={'s': s}, attrs={'Description': 's-coord for FREQUENCIES'})
        self['FREQUENCIES']['we'] = xarray.DataArray(we, dims=['s'], coords={'s': s}, attrs={'Description': 'ExB velocity'})
        self['FREQUENCIES']['wsni'] = xarray.DataArray(
            wsni, dims=['s'], coords={'s': s}, attrs={'Description': 'Diamagnetic frequency - density gradient'}
        )
        self['FREQUENCIES']['wsti'] = xarray.DataArray(
            wsti, dims=['s'], coords={'s': s}, attrs={'Description': 'Diamagnetic frequency - temp. gradient'}
        )
        self['FREQUENCIES']['awbt'] = xarray.DataArray(awbt, dims=['s'], coords={'s': s}, attrs={'Description': 'Bounce - trapped'})
        self['FREQUENCIES']['awbp'] = xarray.DataArray(awbp, dims=['s'], coords={'s': s}, attrs={'Description': 'Bounce - passing'})
        self['FREQUENCIES']['awdi'] = xarray.DataArray(awdi, dims=['s'], coords={'s': s}, attrs={'Description': 'Precession - th ions'})
        self['FREQUENCIES']['awde'] = xarray.DataArray(awde, dims=['s'], coords={'s': s}, attrs={'Description': 'Precession - electrons'})
        self['FREQUENCIES']['awda'] = xarray.DataArray(awda, dims=['s'], coords={'s': s}, attrs={'Description': 'Precession - hot'})

    def read_TIMEEVOL(self, filename, ncase, NORM=False):
        """
        Reads time evolution output from time-stepping runs

        :param filename: name of MARS output file, usually TIMEEVOL.OUT

        :param ncase: input namelist variable defining type of MARS-* run

        :param NORM: toggle normalization to physical units
        """
        if NORM:
            from scipy.constants import mu_0

            R0 = self[self.sim]['R0EXP'].values.astype(float)
            B0 = self[self.sim]['B0EXP'].values.astype(float)
            TAUA0 = 1.0e-7  # Need to parse log_mars to get TAUA0!
            xnorm = R0 * 1.0e3  # displacement [mm]
            bnorm = B0 * 1.0e4  # b-field [Gauss]
            cnorm = R0 * B0 / mu_0  # current [A]
            tdnorm = (B0**2) / mu_0 / np.pi  # torque density [N/m^2]
            ttnorm = tdnorm * (R0**3)  # total torque [Nm]
            tmnorm = TAUA0 * 1.0e3  # time [ms]
            unit_t = 'ms'
            unit_b = 'Gauss'
            unit_c = 'A'
            unit_v = 'A.U.'  # Implement voltage normalization
        else:
            xnorm = 1.0
            bnorm = 1.0
            cnorm = 1.0
            tdnorm = 1.0
            ttnorm = 1.0
            tmnorm = 1.0
            unit_t = 'A.U.'
            unit_b = 'A.U.'
            unit_c = 'A.U.'
            unit_v = 'A.U.'  # Implement voltage normalization
        # tmp = np.atleast_2d(loadtxt(filename, skiprows=0))
        tmp = np.loadtxt(filename)
        ncols = tmp.shape[1]
        self['TIMEEVOL'] = xarray.Dataset()
        if ncase == 3:
            t = np.cumsum(tmp[:, 0]) * tmnorm
            self['TIMEEVOL']['t'] = xarray.DataArray(
                t, dims=['t'], coords={'t': t}, attrs={'Description': 'Time axis', 'Units': '%s' % unit_t}
            )
            # Point-like sensor signal
            self['TIMEEVOL']['PSIS_re'] = xarray.DataArray(
                tmp[:, 1] * bnorm, dims=['t'], coords={'t': t}, attrs={'Description': 'Sensor signal (Re)', 'Units': '%s' % unit_b}
            )
            self['TIMEEVOL']['PSIS_im'] = xarray.DataArray(
                tmp[:, 2] * bnorm, dims=['t'], coords={'t': t}, attrs={'Description': 'Sensor signal (Im)', 'Units': '%s' % unit_b}
            )
            # Get number of columns where AIF is stored
            midcols = tmp.shape[1] - 3
            ncoil = midcols // 4
            # Feedback current
            istart = 3
            for ii in range(ncoil):
                self['TIMEEVOL']['AIF_%d_re' % ii] = xarray.DataArray(
                    tmp[:, istart + ii],
                    dims=['t'],
                    coords={'t': t},
                    attrs={'Description': 'Feedback current coil %s (Re)' % str(ii + 1), 'Units': '%s' % unit_c},
                )
                self['TIMEEVOL']['AIF_%d_im' % ii] = xarray.DataArray(
                    tmp[:, istart + ncoil + ii],
                    dims=['t'],
                    coords={'t': t},
                    attrs={'Description': 'Feedback current coil %s (Im)' % str(ii + 1), 'Units': '%s' % unit_c},
                )
        elif ncase == 4:
            t = np.cumsum(tmp[:, 0]) * tmnorm
            self['TIMEEVOL']['t'] = xarray.DataArray(
                t, dims=['t'], coords={'t': t}, attrs={'Description': 'Time axis', 'Units': '%s' % unit_t}
            )
            # Point-like sensor signal
            self['TIMEEVOL']['PSIS_re'] = xarray.DataArray(
                tmp[:, 1] * bnorm, dims=['t'], coords={'t': t}, attrs={'Description': 'Sensor signal (Re)', 'Units': '%s' % unit_b}
            )
            self['TIMEEVOL']['PSIS_im'] = xarray.DataArray(
                tmp[:, 2] * bnorm, dims=['t'], coords={'t': t}, attrs={'Description': 'Sensor signal (Im)', 'Units': '%s' % unit_b}
            )
            # Sensor noise
            self['TIMEEVOL']['PSISNOISE_re'] = xarray.DataArray(
                tmp[:, -2] * bnorm, dims=['t'], coords={'t': t}, attrs={'Description': 'Sensor noise (Re)', 'Units': '%s' % unit_b}
            )
            self['TIMEEVOL']['PSISNOISE_im'] = xarray.DataArray(
                tmp[:, -1] * bnorm, dims=['t'], coords={'t': t}, attrs={'Description': 'Sensor noise (Im)', 'Units': '%s' % unit_b}
            )
            # Get number of columns where AVF & AIF are stored
            midcols = tmp.shape[1] - 5
            ncoil = midcols // 4
            # Feedback voltages
            istart = 3
            for ii in range(ncoil):
                self['TIMEEVOL']['AVF_%d_re' % ii] = xarray.DataArray(
                    tmp[:, istart + ii],
                    dims=['t'],
                    coords={'t': t},
                    attrs={'Description': 'Feedback voltage coil %s (Re)' % str(ii + 1), 'Units': '%s' % unit_v},
                )
                self['TIMEEVOL']['AVF_%d_im' % ii] = xarray.DataArray(
                    tmp[:, istart + ncoil + ii],
                    dims=['t'],
                    coords={'t': t},
                    attrs={'Description': 'Feedback voltage coil %s (Im)' % str(ii + 1), 'Units': '%s' % unit_v},
                )
            # Feedback currents
            istart = 3 + 2 * ncoil
            for ii in range(ncoil):
                self['TIMEEVOL']['AIF_%d_re' % ii] = xarray.DataArray(
                    tmp[:, istart + ii],
                    dims=['t'],
                    coords={'t': t},
                    attrs={'Description': 'Feedback current coil %s (Re)' % str(ii + 1), 'Units': '%s' % unit_c},
                )
                self['TIMEEVOL']['AIF_%d_im' % ii] = xarray.DataArray(
                    tmp[:, istart + ncoil + ii],
                    dims=['t'],
                    coords={'t': t},
                    attrs={'Description': 'Feedback current coil %s (Im)' % str(ii + 1), 'Units': '%s' % unit_c},
                )
        else:
            print('NCASE=%s not implemented yet' % ncase)
            return

    def read_dWk_den(self, filename):
        """
        Reads perturbed kinetic energy density

        :param filename: name of MARS output file, usually DWK_ENERGY_DENSITY.OUT
        """
        data = np.loadtxt(filename, comments='%')
        NR = len(data[:, 0])
        n = len(data[0, :]) // 10
        blocks = np.split(data, n, axis=1)
        self['DWK_ENERGY_DENSITY'] = xarray.Dataset()
        self['DWK_ENERGY_DENSITY']['FULL_MATRIX'] = xarray.DataArray(data)
        for l in range(len(blocks)):
            CSM = blocks[l][:, 2]
            KP = int(blocks[l][0, 0])
            I = int(blocks[l][1, 1])
            self['DWK_ENERGY_DENSITY']['%s_%s_REdwppara' % (KP, I)] = xarray.DataArray(
                blocks[l][:, 4],
                dims=['s'],
                coords={'s': CSM},
                attrs={'Description': 'Real parallel dWk for species = %s, type = %s' % (KP, I)},
            )
            self['DWK_ENERGY_DENSITY']['%s_%s_IMdwppara' % (KP, I)] = xarray.DataArray(
                blocks[l][:, 5], dims=['s'], coords={'s': CSM}, attrs={'Description': f'Imag parallel dWk for species = {KP}, type = {I}'}
            )
            self['DWK_ENERGY_DENSITY']['%s_%s_REdwpperp' % (KP, I)] = xarray.DataArray(
                blocks[l][:, 6], dims=['s'], coords={'s': CSM}, attrs={'Description': 'Real perp. dWk for specie = %s, type = %s' % (KP, I)}
            )
            self['DWK_ENERGY_DENSITY']['%s_%s_IMdwpperp' % (KP, I)] = xarray.DataArray(
                blocks[l][:, 7],
                dims=['s'],
                coords={'s': CSM},
                attrs={'Description': 'Imag. perp. dWk for specie = %s, type = %s' % (KP, I)},
            )
            self['DWK_ENERGY_DENSITY']['%s_%s_REdwk' % (KP, I)] = xarray.DataArray(
                blocks[l][:, 8], dims=['s'], coords={'s': CSM}, attrs={'Description': 'Real total dWk for specie = %s, type = %s' % (KP, I)}
            )
            self['DWK_ENERGY_DENSITY']['%s_%s_IMdwk' % (KP, I)] = xarray.DataArray(
                blocks[l][:, 9], dims=['s'], coords={'s': CSM}, attrs={'Description': 'Imag total dWk for specie = %s, type = %s' % (KP, I)}
            )
        return

    def read_PROFNTV(self, filename):
        # commented mu_0 might be needed in future extensions
        # from scipy.constants import mu_0

        # read data
        prof = np.loadtxt(filename)

        # profiles
        rho = prof[:, 0]  # radial coordinate
        q = prof[:, 1]  # safety factor
        eps = prof[:, 2]  # equivalent r/R0 in Shaing's theory
        rhoi = prof[:, 3]  # thermal ion density
        nu = prof[:, 4]  # collisionality, thermal ion or electron depending on ZCHARGE
        wti = prof[:, 5]  # thermal ion transit frequency
        wB0 = prof[:, 6]  # gradB precession drift frequency, depending on ZCHARGE
        qwe = prof[:, 7]  # ExB drift frequency, =q*omega_E
        qws = prof[:, 8]  # diamagnetic drift frequency, =q*omega_*p, depending on ZCHARGE
        qwsT = prof[:, 9]  # grad T drift frequency, =q*omega_*T, depending on ZCHARGE
        dB = prof[:, 10]  # surface averaged |dB|/B0

        psi = rho**2

        # some fix-ups
        dB[0] = dB[2]
        dB[1] = dB[2]
        """
        calculate "boundary"-frequencies between different NTV regimes
        first for non-resonant NTV torque
                nu < nu_n1 : nu-regime
        nu_n1 < nu < nu_n2 : sqrt(nu)-regime
        nu_n2 < nu < nu_n3 : 1/nu-regime
        nu_n3 < nu         : violation of assumptions in Shaing's NTV theory
        """
        nu_n1 = np.abs(qwe / q) * ((dB / eps) ** 2)
        nu_n2 = np.abs(qwe / q)
        nu_n3 = np.sqrt(eps) * wti

        """
        next for resonant NTV torque
                nu < nu_r1 : superbanana-regime
        nu_r1 < nu < nu_r2 : superbanana-plateau-regime
        nu_r2 < nu < nu_r3 : 1/nu-regime
        nu_r3 < nu         : violation of assumptions in Shaing's NTV theory     
        """
        nu_r1 = wB0 * ((dB / eps) ** 1.5)
        nu_r2 = wB0 / eps
        nu_r3 = np.sqrt(eps) * wti

        self['PROFNTV'] = xarray.Dataset()
        self['PROFNTV']['nu_n1'] = xarray.DataArray(
            nu_n1, dims=['psi'], coords={'psi': psi}, attrs={'Description': 'nu < nu_n1 : nu-regime'}
        )
        self['PROFNTV']['nu_n2'] = xarray.DataArray(
            nu_n2, dims=['psi'], coords={'psi': psi}, attrs={'Description': 'nu_n1 < nu < nu_n2 : sqrt(nu)-regime'}
        )
        self['PROFNTV']['nu_n3'] = xarray.DataArray(
            nu_n3, dims=['psi'], coords={'psi': psi}, attrs={'Description': 'nu_n2 < nu < nu_n3 : 1/nu-regime'}
        )
        self['PROFNTV']['nu_r1'] = xarray.DataArray(
            nu_r1, dims=['psi'], coords={'psi': psi}, attrs={'Description': 'nu < nu_r1 : superbanana-regime'}
        )
        self['PROFNTV']['nu_r2'] = xarray.DataArray(
            nu_r2,
            dims=['psi'],
            coords={'psi': psi},
            attrs={'Description': 'nu_r1 < nu < nu_r2 : superbanana-plateau-regime, nu_r2 < nu < nu_r3 : 1/nu-regime'},
        )
        self['PROFNTV']['nu'] = xarray.DataArray(
            nu, dims=['psi'], coords={'psi': psi}, attrs={'Description': 'collisionality, thermal ion or electron depending on ZCHARGE'}
        )
        self['PROFNTV']['eps'] = xarray.DataArray(
            eps, dims=['psi'], coords={'psi': psi}, attrs={'Description': 'equivalent r/R0 in Shaing theory'}
        )
        return

    def read_TORQUENTV(self, filename):
        """
        Read TORQUENTV.OUT file containing NTV torque densities
        """
        torq = np.loadtxt(filename)

        # get NTV torque densities
        s = torq[:, 0]  # radial mesh
        TNTVtot = torq[:, 1]  # total NTV torque density = ions + electrons
        DPNTVTot = torq[:, 2]  # particle flux due to total NTV torque

        DPNTVi = torq[:, 3]  # particle flux due to ion NTV torque
        DPNTVe = torq[:, 4]  # particle flux due to electron NTV torque

        TNTVi = torq[:, 5]  # NTV torque due to ions
        TNTVe = torq[:, 6]  # NTV torque due to electrons

        self['TORQUENTV'] = xarray.Dataset()
        self['TORQUENTV']['NTV_tot'] = xarray.DataArray(
            TNTVtot, dims=['s'], coords={'s': s}, attrs={'Description': 'total NTV torque density = ions + electrons'}
        )
        self['TORQUENTV']['NTV_ion'] = xarray.DataArray(TNTVi, dims=['s'], coords={'s': s}, attrs={'Description': 'NTV torque due to ions'})
        self['TORQUENTV']['NTV_el'] = xarray.DataArray(
            TNTVe, dims=['s'], coords={'s': s}, attrs={'Description': 'NTV torque due to electrons'}
        )

        # Particle flux
        self['TORQUENTV']['DP_NTV_tot'] = xarray.DataArray(
            DPNTVTot, dims=['s'], coords={'s': s}, attrs={'Description': 'particle flux due to total NTV torque'}
        )
        self['TORQUENTV']['DP_NTV_ion'] = xarray.DataArray(
            DPNTVi, dims=['s'], coords={'s': s}, attrs={'Description': 'particle flux due to ion NTV torque'}
        )
        self['TORQUENTV']['DP_NTV_el'] = xarray.DataArray(
            DPNTVe, dims=['s'], coords={'s': s}, attrs={'Description': 'particle flux due to electron NTV torque'}
        )
        return

    def read_NUSTAR(self, filename):
        """
        Read PROFNUSTAR.OUT file containing ion and electron effective collisionality
        """
        # read data
        nu = np.loadtxt(filename)

        s = nu[:, 0]
        nui = nu[:, 1]  # nu* ions
        nue = nu[:, 2]  # nu* electrons
        self['NUSTAR'] = xarray.Dataset()
        self['NUSTAR']['nustar_i'] = xarray.DataArray(
            nui, dims=['s'], coords={'s': s}, attrs={'Description': 'nustar for ions calculated in MARS'}
        )
        self['NUSTAR']['nustar_e'] = xarray.DataArray(
            nue, dims=['s'], coords={'s': s}, attrs={'Description': 'nustar for electrons calculated in MARS'}
        )
        return

    """
    'get' methods, calculate quantities from previously read data
    """

    def get_RZ(self):
        """
        convert RM and ZM into R and Z real space co-ordinates
        """
        Nm2 = self[self.sim]['Nm0'].values.astype(int)
        Nchi = self[self.sim]['Nchi'].values.astype(int)
        chi = np.linspace(np.pi * -1, np.pi, Nchi)
        m = np.arange(0, Nm2, 1)
        m = np.reshape(m, (len(m), 1))
        chi = np.reshape(chi, (len(chi), 1))
        expmchi = np.exp(m * chi.T * 1j)
        R = np.real(np.dot(self[self.sim]['RM'][:, 0:Nm2], expmchi))
        Z = np.real(np.dot(self[self.sim]['ZM'][:, 0:Nm2], expmchi))
        self[self.sim]['R'] = xarray.DataArray(
            R, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
        )
        self[self.sim]['Z'] = xarray.DataArray(
            Z, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
        )
        return R, Z

    def get_SurfS(self, rs, saveCarMadata=False):
        """
        Generate MacSurfS ASCII file containing control surface for Equivalent Surface Current workflow
        :param rs: radius (r/a) of control surface picked from CHEASE vacuum mesh
        :param saveCarMadata: flag to save MacDataS for CarMa coupling
        """
        if 'R' not in self[self.sim]:
            self.get_RZ()
        II = np.argmin(abs(self[self.sim]['s'].values - rs))
        tmp1 = np.array([self[self.sim]['R'].values[II - 1, :], self[self.sim]['Z'].values[II - 1, :]]).T
        tmp2 = np.array([self[self.sim]['R'].values[II, :], self[self.sim]['Z'].values[II, :]]).T
        RZrw_CarMa = np.array([(tmp1 + tmp2) / (2 * self[self.sim]['R0EXP'].values), tmp2 * self[self.sim]['R0EXP'].values])
        RZrw_EF = tmp2 * self[self.sim]['R0EXP'].values
        # Save and load into tree
        np.savetxt('MacSurfS', RZrw_EF)
        self['CouplingSurfS'] = {}
        self['CouplingSurfS']['MacSurfS'] = OMFITascii('./MacSurfS')
        self['CouplingSurfS']['Rs'] = self[self.sim]['R'].values[II, :]
        self['CouplingSurfS']['Zs'] = self[self.sim]['Z'].values[II, :]
        self['CouplingSurfS']['s'] = rs
        if saveCarMadata:
            np.savetxt('MacDataS', RZrw_CarMa)
            self['CouplingDataS'] = {}
            self['CouplingDataS']['MacDataS'] = OMFITascii('./MacDataS')
            self['CouplingDataS']['RZrw_CarMa'] = RZrw_CarMa
            return RZrw_EF, RZrw_CarMa
        else:
            return RZrw_EF

    def get_UnitVec(self, vacFlag=False, IIgrid=None):
        """
        Get unit vectors e_s and e_chi and jacobian from real space R,Z
        :param vacFlag: flag to calculate metric elements in all domain (plasma+vacuum)
        :param IIgrid: specify the radial mesh index to calculate vectors within
        """
        from scipy.interpolate import InterpolatedUnivariateSpline

        if 'R' not in self[self.sim]:
            self.get_RZ()
        Ls = len(self[self.sim]['R'][:, 0])
        Lchi = len(self[self.sim]['R'][0, :])
        dRds = copy.deepcopy(self[self.sim]['R'].values)
        dZds = copy.deepcopy(self[self.sim]['Z'].values)
        dRdchi = copy.deepcopy(self[self.sim]['R'].values)
        dZdchi = copy.deepcopy(self[self.sim]['Z'].values)
        jacobian = copy.deepcopy(self[self.sim]['R'].values)
        # Number of mesh points in plasma
        Ns1 = self[self.sim]['Ns1'].values.astype(int)
        # Number of mesh points in vacuum
        Ns2 = self[self.sim]['Ns2'].values.astype(int)
        # indexes of full domain: first couple is vacuum, second is plasma
        domain = [(Ns1, Ns1 + Ns2), (0, Ns1)]
        if isinstance(IIgrid, int):
            II = IIgrid
        else:
            II = Ns1
        # Loop over vacuum and plasma
        for ii, kk in domain:
            if ii == Ns1:
                printi('Partial derivatives in vacuum')
                s0 = self[self.sim]['svac'].values
            elif ii == 0:
                printi('Partial derivatives in plasma')
                s0 = self[self.sim]['sp'].values
            else:
                printi('ERROR! Check Jacobian calculation')
                return
            II1 = ii
            II2 = kk
            R0 = self[self.sim]['R'].isel(s=range(II1, II2))
            Z0 = self[self.sim]['Z'].isel(s=range(II1, II2))
            Nchi = self[self.sim]['Nchi'].values.astype(int)
            chi0 = np.linspace(np.pi * -1, np.pi, Nchi)
            hs = 0.5 * ((s0[1:] - s0[:-1]).min())
            hs = min(hs, 2e-5)
            hchi = 0.5 * ((chi0[1:] - chi0[:-1]).min())
            hchi = min(hchi, 1e-4)
            s1 = s0 - hs
            s2 = s0 + hs
            chi1 = chi0 - hchi
            chi2 = chi0 + hchi

            # compute dR/ds using R(s,chi) and spline
            R1 = np.zeros(np.shape(R0))
            R2 = np.zeros(np.shape(R0))
            for k in range(len(R0[0, :])):
                R1[:, k] = InterpolatedUnivariateSpline(s0, R0[:, k], bbox=[s1[0], s0[-1]])(s1)
                R2[:, k] = InterpolatedUnivariateSpline(s0, R0[:, k], bbox=[s0[0], s2[-1]])(s2)
            dRds[II1:II2, :] = (R2 - R1) / (2.0 * hs)

            # compute dZ/ds using Z(s,chi) and spline
            Z1 = np.zeros(np.shape(Z0))
            Z2 = np.zeros(np.shape(Z0))
            for k in range(len(R0[0, :])):
                Z1[:, k] = InterpolatedUnivariateSpline(s0, Z0[:, k], bbox=[s1[0], s0[-1]])(s1)
                Z2[:, k] = InterpolatedUnivariateSpline(s0, Z0[:, k], bbox=[s0[0], s2[-1]])(s2)
            dZds[II1:II2, :] = (Z2 - Z1) / (2.0 * hs)

            # compute dR/dchi using R(s,chi) and spline
            R1 = np.zeros(np.shape(R0))
            R2 = np.zeros(np.shape(R0))
            for k in range(len(R0[:, 0])):
                R1[k, :] = InterpolatedUnivariateSpline(chi0, R0[k, :], bbox=[chi1[0], chi0[-1]])(chi1)
                R2[k, :] = InterpolatedUnivariateSpline(chi0, R0[k, :], bbox=[chi0[0], chi2[-1]])(chi2)
            R1[:, 0] = R1[:, -1]
            R2[:, -1] = R2[:, 0]
            dRdchi[II1:II2, :] = (R2 - R1) / (2.0 * hchi)

            # compute dR/dchi using R(s,chi) and spline
            Z1 = np.zeros(np.shape(Z0))
            Z2 = np.zeros(np.shape(Z0))
            for k in range(len(R0[:, 0])):
                Z1[k, :] = InterpolatedUnivariateSpline(chi0, Z0[k, :], bbox=[chi1[0], chi0[-1]])(chi1)
                Z2[k, :] = InterpolatedUnivariateSpline(chi0, Z0[k, :], bbox=[chi0[0], chi2[-1]])(chi2)
            Z1[:, 0] = Z1[:, -1]
            Z2[:, -1] = Z2[:, 0]
            dZdchi[II1:II2, :] = (Z2 - Z1) / (2.0 * hchi)
        # Calculate Jacobian
        J = (self[self.sim]['R'].values) * (-dRdchi * dZds + dRds * dZdchi)
        J[0, :] = J[1, :]
        if vacFlag:
            # Calculate metric elements in both plasma and vacuum
            G11 = np.square(dRds) + np.square(dZds)
            G12 = np.multiply(dRds, dRdchi) + np.multiply(dZds, dZdchi)
            G22 = np.square(dRdchi) + np.square(dZdchi)
            G22[0, :] = G22[1, :]
            G33 = np.square(self[self.sim]['R'].values)
        else:
            # Calculate metric elements inside the plasma
            G11 = np.square(dRds[0:II, :]) + np.square(dZds[0:II, :])
            G12 = np.multiply(dRds[0:II, :], dRdchi[0:II, :]) + np.multiply(dZds[0:II, :], dZdchi[0:II, :])
            G22 = np.square(dRdchi[0:II, :]) + np.square(dZdchi[0:II, :])
            G22[0, :] = G22[1, :]
            G33 = np.square(self[self.sim]['R'].values[0:II, :])
        # Store data
        self['UnitVector'] = xarray.Dataset()
        self['UnitVector']['dRds'] = xarray.DataArray(
            dRds, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
        )
        self['UnitVector']['dZds'] = xarray.DataArray(
            dZds, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
        )
        self['UnitVector']['dRdchi'] = xarray.DataArray(
            dRdchi, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
        )
        self['UnitVector']['dZdchi'] = xarray.DataArray(
            dZdchi, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
        )
        self['UnitVector']['Jacobian'] = xarray.DataArray(
            J, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
        )
        self['Metric'] = xarray.Dataset()
        if vacFlag:
            self['Metric']['G11'] = xarray.DataArray(
                G11, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
            )
            self['Metric']['G12'] = xarray.DataArray(
                G12, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
            )
            self['Metric']['G22'] = xarray.DataArray(
                G22, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
            )
            self['Metric']['G33'] = xarray.DataArray(
                G33, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s']}
            )
        else:
            self['Metric']['G11'] = xarray.DataArray(
                G11, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s'][0:II]}
            )
            self['Metric']['G12'] = xarray.DataArray(
                G12, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s'][0:II]}
            )
            self['Metric']['G22'] = xarray.DataArray(
                G22, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s'][0:II]}
            )
            self['Metric']['G33'] = xarray.DataArray(
                G33, dims=['s', 'chi'], coords={'chi': np.linspace(np.pi * -1, np.pi, Nchi), 's': self[self.sim]['s'][0:II]}
            )
        return dRds, dZds, dRdchi, dZdchi, jacobian

    def get_X123(self):
        """
        Inverse Fourier transorm of plasma displacement and projection along Chi and Phi
        """
        if 'UnitVector' not in self:
            self.get_UnitVec()
        expmchi = np.exp(self['XPLASMA']['Mm'] * self[self.sim]['chi'] * 1j)
        expmchi_inv = np.exp(-self[self.sim]['chi'] * self['XPLASMA']['Mm'] * 1j)
        chione = np.ones((1, len(self[self.sim]['chi'])))
        Ns1 = self[self.sim]['Ns1'].values
        X1a = np.dot(self['XPLASMA']['XM1'].values, expmchi)
        X2a = np.dot(self['XPLASMA']['XM2'].values, expmchi)
        X3a = np.dot(self['XPLASMA']['XM3'].values, expmchi)
        if np.size(self['Metric']['G22'], 0) != np.size(X1a, 0):
            self.get_UnitVec(vacFlag=False)
        # Calculate X1 along e_s
        X1 = X1a
        # Calculate X2 along e_chi
        dPSIds = np.array(self[self.sim]['dPSIds'].values).reshape((len(self[self.sim]['dPSIds'].values), 1))
        J = self['UnitVector']['Jacobian'].isel(s=range(Ns1)).values
        T = np.array(self[self.sim]['T'].values).reshape((len(self[self.sim]['T']), 1))
        Bchi = np.divide(np.dot(dPSIds, chione), J)
        Bphi = np.divide(np.dot(T, chione), np.square(self[self.sim]['R'].values[0:Ns1, :]))
        B2 = np.multiply(np.square(Bchi), self['Metric']['G22']) + np.multiply(np.square(Bphi), self['Metric']['G33'])
        X2 = (
            np.divide(np.multiply(-X1, np.multiply(self['Metric']['G12'], np.square(Bchi))), B2)
            + np.divide(np.multiply(X2a, np.multiply(Bphi, self['Metric']['G33'])), B2)
            - np.multiply(X3a, Bchi)
        )
        # Calculate X3 along e_phi
        X3 = (
            np.divide(np.multiply(-X1, np.multiply(self['Metric']['G12'], np.multiply(Bchi, Bphi))), B2)
            + np.divide(np.multiply(X2a, np.multiply(Bchi, self['Metric']['G22'])), B2)
            - np.multiply(X3a, Bphi)
        )
        # Calculate normal plasma displacement
        Xn = np.divide(np.multiply(X1a, J), np.sqrt(np.multiply(self['Metric']['G33'], self['Metric']['G22'])))
        # Fourier transorm of Xn
        XnM = np.dot(Xn, expmchi_inv) * (self[self.sim]['chi'].values[1] - self[self.sim]['chi'].values[0]) / (2 * np.pi)
        # Radial coordinate name 's' is retained for compatibility, here 's' is 'sp' (within plasma)
        self['XPLASMA']['Bchi'] = xarray.DataArray(
            Bchi, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']}
        )
        self['XPLASMA']['Bphi'] = xarray.DataArray(
            Bphi, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']}
        )
        self['XPLASMA']['B2'] = xarray.DataArray(B2, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']})
        self['XPLASMA']['X1'] = xarray.DataArray(X1, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']})
        self['XPLASMA']['X2'] = xarray.DataArray(X2, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']})
        self['XPLASMA']['X3'] = xarray.DataArray(X3, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']})
        self['XPLASMA']['Xn'] = xarray.DataArray(Xn, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']})
        self['XPLASMA']['XnM'] = xarray.DataArray(XnM, dims=['sp', 'Mm'], coords={'sp': self[self.sim]['sp'], 'Mm': self['XPLASMA']['Mm']})
        self['XPLASMA']['X1a'] = xarray.DataArray(
            X1a, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']}
        )
        self['XPLASMA']['X2a'] = xarray.DataArray(
            X2a, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']}
        )
        self['XPLASMA']['X3a'] = xarray.DataArray(
            X3a, dims=['sp', 'chi'], coords={'sp': self[self.sim]['sp'], 'chi': self[self.sim]['chi']}
        )

    def get_B123(self):
        """
        Inverse Fourier transorm of perturbed magnetic field and calculate Bn
        """
        if 'UnitVector' not in self:
            self.get_UnitVec()
        # Check metric element size
        # This is needed when IIgrid=None and NV(MARS) != NV(CHEASE)
        II = np.size(self['BPLASMA']['BM1'], 0)
        if np.size(self['Metric']['G22'], 0) != II:
            print("WARNING: NV(MARS) != NV(CHEASE). Calculating metric elements with b-field radial grid size.")
            self.get_UnitVec(IIgrid=II)
        # Define DFT matrices
        expmchi = np.exp(self['BPLASMA']['Mm'] * self[self.sim]['chi'] * 1j)
        expmchi_inv = np.exp(-self[self.sim]['chi'] * self['BPLASMA']['Mm'] * 1j)
        chione = np.ones((1, len(self[self.sim]['chi'])))
        # Calculate inverse Fourier transorm
        B1 = np.dot(self['BPLASMA']['BM1'].isel(s=range(II)), expmchi)
        B2 = np.dot(self['BPLASMA']['BM2'].isel(s=range(II)), expmchi)
        B3 = np.dot(self['BPLASMA']['BM3'].isel(s=range(II)), expmchi)
        # Calculate normal perturbeb magnetic field
        Bn = np.divide(B1, np.multiply(np.sqrt(self['Metric']['G22']), self[self.sim]['R'].isel(s=range(II))))
        # Fourier transorm of Bn
        BnM = np.dot(Bn, expmchi_inv) * (self[self.sim]['chi'].values[1] - self[self.sim]['chi'].values[0]) / (2 * np.pi)
        # Store data
        self['BPLASMA']['B1'] = xarray.DataArray(B1, dims=['s', 'chi'], coords={'s': self['BPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['BPLASMA']['B2'] = xarray.DataArray(B2, dims=['s', 'chi'], coords={'s': self['BPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['BPLASMA']['B3'] = xarray.DataArray(B3, dims=['s', 'chi'], coords={'s': self['BPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['BPLASMA']['Bn'] = xarray.DataArray(Bn, dims=['s', 'chi'], coords={'s': self['BPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['BPLASMA']['BnM'] = xarray.DataArray(BnM, dims=['s', 'Mm'], coords={'s': self['BPLASMA']['s'], 'Mm': self['BPLASMA']['Mm']})

    def get_J123(self):
        """
        Inverse Fourier transorm of perturbed current
        """
        if 'UnitVector' not in self:
            self.get_UnitVec()
        # Check metric element size
        # This is needed when IIgrid=None and NV(MARS) != NV(CHEASE)
        II = np.size(self['JPLASMA']['JM1'], 0)
        if np.size(self['Metric']['G22'], 0) != II:
            print("WARNING: NV(MARS) != NV(CHEASE). Calculating metric elements with b-field radial grid size.")
            self.get_UnitVec(IIgrid=II)
        # Define DFT matrices
        expmchi = np.exp(self['JPLASMA']['Mm'] * self[self.sim]['chi'] * 1j)
        expmchi_inv = np.exp(-self[self.sim]['chi'] * self['JPLASMA']['Mm'] * 1j)
        chione = np.ones((1, len(self[self.sim]['chi'])))
        # Calculate inverse Fourier transorm
        J1 = np.dot(self['JPLASMA']['JM1'].isel(s=range(II)), expmchi)
        J2 = np.dot(self['JPLASMA']['JM2'].isel(s=range(II)), expmchi)
        J3 = np.dot(self['JPLASMA']['JM3'].isel(s=range(II)), expmchi)
        # Store data
        self['JPLASMA']['J1'] = xarray.DataArray(J1, dims=['s', 'chi'], coords={'s': self['JPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['JPLASMA']['J2'] = xarray.DataArray(J2, dims=['s', 'chi'], coords={'s': self['JPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['JPLASMA']['J3'] = xarray.DataArray(J3, dims=['s', 'chi'], coords={'s': self['JPLASMA']['s'], 'chi': self[self.sim]['chi']})

    def get_Bcyl(self):
        """
        Get B-field components in cylindrical coordinates
        """
        print('GET: calculating B-field cylindrical components')
        if 'B1' not in self['BPLASMA']:
            self.get_B123()
        if 'R' not in self[self.sim]:
            self.get_RZ()
        II = np.size(self['BPLASMA']['BM1'], 0)
        J = self['UnitVector']['Jacobian'].isel(s=range(II))
        dRds = self['UnitVector']['dRds'].isel(s=range(II))
        dRdchi = self['UnitVector']['dRdchi'].isel(s=range(II))
        dZds = self['UnitVector']['dZds'].isel(s=range(II))
        dZdchi = self['UnitVector']['dZdchi'].isel(s=range(II))
        R0 = self[self.sim]['R'].isel(s=range(II))
        # Calculate Br,z,phi
        Br = (self['BPLASMA']['B1'] * dRds + self['BPLASMA']['B2'] * dRdchi) / J
        Br[0:2, :] = Br[2, :]
        Bz = (self['BPLASMA']['B1'] * dZds + self['BPLASMA']['B2'] * dZdchi) / J
        Bz[0:2, :] = Bz[2, :]
        Bphi = (self['BPLASMA']['B3'] * R0) / J
        Bphi[0:2, :] = Bphi[2, :]
        self['BPLASMA']['Br'] = xarray.DataArray(Br, dims=['s', 'chi'], coords={'s': self['BPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['BPLASMA']['Bz'] = xarray.DataArray(Bz, dims=['s', 'chi'], coords={'s': self['BPLASMA']['s'], 'chi': self[self.sim]['chi']})
        self['BPLASMA']['Bphi'] = xarray.DataArray(
            Bphi, dims=['s', 'chi'], coords={'s': self['BPLASMA']['s'], 'chi': self[self.sim]['chi']}
        )

    def get_Xcyl(self):
        """
        Get displacement components in cylindrical coordinates
        """
        print('GET: calculating plasma displacement cylindrical components')
        if 'X1' not in self['XPLASMA']:
            self.get_X123()
        if 'R' not in self[self.sim]:
            self.get_RZ()
        II = np.size(self['XPLASMA']['XM1'], 0)
        J = self['UnitVector']['Jacobian'].isel(s=range(II))
        dRds = self['UnitVector']['dRds'].isel(s=range(II))
        dRdchi = self['UnitVector']['dRdchi'].isel(s=range(II))
        dZds = self['UnitVector']['dZds'].isel(s=range(II))
        dZdchi = self['UnitVector']['dZdchi'].isel(s=range(II))
        R0 = self[self.sim]['R'].isel(s=range(II))
        # Calculate Xr,z,phi
        Xr = self['XPLASMA']['X1'].values * dRds.values + self['XPLASMA']['X2'].values * dRdchi.values
        Xr[0:2, :] = Xr[2, :]
        Xz = self['XPLASMA']['X1'].values * dZds.values + self['XPLASMA']['X2'].values * dZdchi.values
        Xz[0:2, :] = Xz[2, :]
        Xphi = self['XPLASMA']['X3'].values * R0.values
        Xphi[0:2, :] = Xphi[2, :]
        self['XPLASMA']['Xr'] = xarray.DataArray(Xr, dims=['sp', 'chi'], coords={'sp': self['XPLASMA']['sp'], 'chi': self[self.sim]['chi']})
        self['XPLASMA']['Xz'] = xarray.DataArray(Xz, dims=['sp', 'chi'], coords={'sp': self['XPLASMA']['sp'], 'chi': self[self.sim]['chi']})
        self['XPLASMA']['Xphi'] = xarray.DataArray(
            Xphi, dims=['sp', 'chi'], coords={'sp': self['XPLASMA']['sp'], 'chi': self[self.sim]['chi']}
        )

    def get_dWk(self, NFIT=3):
        """
        Calculate dWk components from DWK_ENERGY_DENSITY

        :param NFIT: integral of energy density skips the first NFIT+1 points
        """
        print('GET: calculating dWk components')
        if 'DWK_ENERGY_DENSITY' not in self:
            self.read_dWk_den()
        den = self['DWK_ENERGY_DENSITY']['FULL_MATRIX']
        NR = len(den[:, 0])
        n = len(den[0, :]) // 10
        blocks = np.split(den, n, axis=1)
        DWK = np.zeros((n, 8))
        for l in range(len(blocks)):
            REdwppara = 0
            IMdwppara = 0
            REdwpperp = 0
            IMdwpperp = 0
            REdwk = 0
            IMdwk = 0
            # Storing KP (=1...NSPECIES, 0=total)
            DWK[l, 0] = blocks[l][0, 0]
            # Storing I (=1...5)
            DWK[l, 1] = blocks[l][1, 1]
            for j in range(NFIT + 1, NR):
                REdwppara = REdwppara + blocks[l][j, 4] * blocks[l][j, 3]
                IMdwppara = IMdwppara + blocks[l][j, 5] * blocks[l][j, 3]
                REdwpperp = REdwpperp + blocks[l][j, 6] * blocks[l][j, 3]
                IMdwpperp = IMdwpperp + blocks[l][j, 7] * blocks[l][j, 3]
                REdwk = REdwk + blocks[l][j, 8] * blocks[l][j, 3]
                IMdwk = IMdwk + blocks[l][j, 9] * blocks[l][j, 3]
            DWK[l, 2] = REdwppara
            DWK[l, 3] = IMdwppara
            DWK[l, 4] = REdwpperp
            DWK[l, 5] = IMdwpperp
            DWK[l, 6] = REdwk
            DWK[l, 7] = IMdwk
        # Total dWk
        K_tot = []
        # Non-adiabatic Trapped precession Drift
        K_I_NTD = []
        K_e_NTD = []
        # Non-adiabatic Trapped Bounce
        K_I_NTB = []
        K_e_NTB = []
        # Non-adiabatic Passing
        K_I_NP = []
        K_e_NP = []
        species = np.unique(DWK[:, 0])
        Nspecies = len(species) - 1
        self['DWK_COMPONENTS'] = xarray.Dataset()
        self['DWK_COMPONENTS']['NSPECIES'] = Nspecies
        for P in species:
            if P == 0:
                # Storing total kinetic contribution
                (i,) = np.where(DWK[:, 0] == 0.0)
                (j,) = np.where(DWK[i, 1] == 0.0)

                K_tot = complex(DWK[i[j], 6], DWK[i[j], 7])
                self['DWK_COMPONENTS']['K_tot'] = K_tot
            else:
                if P == 1:
                    # ions
                    particle = 'I'
                elif P == 2:
                    # electrons
                    particle = 'e'
                elif P > 2:
                    # Other particle species
                    particle = str(P)
                (l,) = np.where(DWK[:, 0] == P)
                (p,) = np.where(DWK[l, 1] == 3.0)
                (b,) = np.where(DWK[l, 1] == 4.0)
                (d,) = np.where(DWK[l, 1] == 5.0)

                if not p:
                    K_NP = complex(0.0, 0.0)
                else:
                    K_NP = complex(DWK[l[p], 6], DWK[l[p], 7])

                if not b:
                    K_NTB = complex(0.0, 0.0)
                else:
                    K_NTB = complex(DWK[l[b], 6], DWK[l[b], 7])

                if not d:
                    K_NTD = complex(0.0, 0.0)
                else:
                    K_NTD = complex(DWK[l[d], 6], DWK[l[d], 7])
                self['DWK_COMPONENTS']['K_%s_NTD' % particle] = K_NTD
                self['DWK_COMPONENTS']['K_%s_NTB' % particle] = K_NTB
                self['DWK_COMPONENTS']['K_%s_NP' % particle] = K_NP

    def get_BatSurf(self, rsurf, kdR=False):
        """
        Calculate normal and tangential components of BPLASMA on given surface (e.g. wall)
        Calculate Fourier decomposition of Bn,t,phi
        Method used in CarMa Forward Coupling
        :param rsurf: normalized radius of surface
        :param kdR: flag for alternative calculation of unit vectors (default=False)
        """
        print('GET: calculating B-field on r=%s surface' % (rsurf))
        if 'B1' not in self['BPLASMA']:
            self.get_B123()
        if 'R' not in self[self.sim]:
            self.get_RZ()
        if 'Br' not in self['BPLASMA']:
            self.get_Bcyl()
        mm = self['BPLASMA']['Mm'].values

        # Find wall surface index
        IIsurf = np.argmin(np.abs(self[self.sim]['s'].values - rsurf))

        Rw = self[self.sim]['R'].isel(s=IIsurf)
        Zw = self[self.sim]['Z'].isel(s=IIsurf)
        Cw = self[self.sim]['chi'].values

        R = self[self.sim]['R']
        Z = self[self.sim]['Z']

        Tw = np.arctan2(Zw - Z[0, 0], Rw - R[0, 0])
        KK = np.where(np.diff(Tw) < -np.pi)[0]
        if (len(KK) == 1) & (2 * KK > len(Tw)):
            Tw[KK[0] + 1 :] = Tw[KK[0] + 1 :] + 2 * np.pi
        if (len(KK) == 1) & (2 * KK < len(Tw)):
            Tw[0 : KK[0]] = Tw[0 : KK[0]] - 2 * np.pi
        Tw = np.sort(Tw)
        JJ = np.argsort(Tw)
        try:
            Bwr = self['BPLASMA']['Br'].isel(s=IIsurf)
            Bwz = self['BPLASMA']['Bz'].isel(s=IIsurf)
            Bwphi = self['BPLASMA']['Bphi'].isel(s=IIsurf)
        except IndexError:
            print('ERROR: Selected index is out of BPLASMA calculation domain')
            return

        # clean Tw,Rw,Zw,Bwr,Bwz,Bwphi
        [Tw, JJ] = np.unique(Tw, return_index=True)
        Rw = Rw[JJ]
        Zw = Zw[JJ]
        Cw = Cw[JJ]
        Bwr = Bwr[JJ]
        Bwz = Bwz[JJ]
        Bwphi = Bwphi[JJ]
        # get Gauss quadrature points for Fourier decomposition
        z, w = np.polynomial.legendre.leggauss(2)
        x0 = (Tw[:-1] + Tw[1:]) * 0.5
        h2 = np.diff(Tw) * 0.5
        xx = z[:, np.newaxis] * h2[np.newaxis, :] + np.ones(z.shape)[:, np.newaxis] * x0[np.newaxis, :]
        wh = w[:, np.newaxis] * h2[np.newaxis, :]
        xx = xx.reshape(-1, 1)
        wh = wh.reshape(-1, 1)

        if kdR == True:
            # Fourier decompose (Rw,Zw) in Tw-angle
            expmt = np.exp(-1j * xx * mm) / (2 * np.pi)

            Rx = scipy.interpolate.pchip(Tw, Rw)(xx) * wh
            Zx = scipy.interpolate.pchip(Tw, Zw)(xx) * wh
            Rm = np.dot(Rx.T, expmt)
            Zm = np.dot(Zx.T, expmt)

            # compute (dR/dTw,dZ/dTw) via Fourier harmonics
            expmt = np.exp(1j * mm * Tw[:, np.newaxis])
            dR = 1j * np.dot(mm * Rm, expmt.T)
            dZ = 1j * np.dot(mm * Zm, expmt.T)
            # res = [dR(:)  dZ(:)]
            dR = np.squeeze(dR.real)
            dZ = np.squeeze(dZ.real)

        else:
            # another way to compute dR,dZ
            dRT = np.diff(Rw) / np.diff(Tw)
            x = (Tw[1:] + Tw[0:-1]) * 0.5
            x = np.concatenate([[x[-1] - 2 * np.pi], x, [x[0] + 2 * np.pi]])
            dRT = np.concatenate([[dRT[-1]], dRT, [dRT[0]]])
            dR = scipy.interpolate.pchip(x, dRT)(Tw)
            dZT = np.diff(Zw) / np.diff(Tw)
            dZT = np.concatenate([[dZT[-1]], dZT, [dZT[0]]])
            dZ = scipy.interpolate.pchip(x, dZT)(Tw)

        # compute physical Bn & Bt from Bwr & Bwz
        nA = np.sqrt(dR**2 + dZ**2)
        Bn = (Bwr * dZ - Bwz * dR) / nA
        Bt = (Bwr * dR + Bwz * dZ) / nA

        # Fourier decompose Bn, Bt & Bphi along Tw angle
        expmt = np.exp(-1j * xx * mm) / (2 * np.pi)

        Bnx = scipy.interpolate.pchip(Tw, Bn.values)(xx) * wh
        Btx = scipy.interpolate.pchip(Tw, Bt.values)(xx) * wh
        Bpx = scipy.interpolate.pchip(Tw, Bwphi.values)(xx) * wh
        Bnm = np.dot(Bnx.T, expmt).T
        Btm = np.dot(Btx.T, expmt).T
        Bpm = np.dot(Bpx.T, expmt).T

        # Store results
        self['BPLASMA']['Bn_s'] = xarray.DataArray(Bn, dims=['Tw'], coords={'Tw': Tw})
        self['BPLASMA']['Bt_s'] = xarray.DataArray(Bt, dims=['Tw'], coords={'Tw': Tw})
        self['BPLASMA']['Bphi_s'] = xarray.DataArray(Bwphi, dims=['Tw'], coords={'Tw': Tw})
        self['BPLASMA']['Bnm_s'] = xarray.DataArray(np.squeeze(Bnm), dims=['Mm'], coords={'Mm': self['BPLASMA']['Mm']})
        self['BPLASMA']['Btm_s'] = xarray.DataArray(np.squeeze(Btm), dims=['Mm'], coords={'Mm': self['BPLASMA']['Mm']})
        self['BPLASMA']['Bpm_s'] = xarray.DataArray(np.squeeze(Bpm), dims=['Mm'], coords={'Mm': self['BPLASMA']['Mm']})

        return Bnm, Btm, Bpm

    @dynaLoad
    def load(self):
        self[self.sim] = xarray.Dataset()
        mapper = OrderedDict(
            (
                ('RMZM_F.OUT', self.read_RMZM),
                ('RMZM_F', self.read_RMZM),
                ('JPLASMA.OUT', self.read_JPLASMA),
                ('JPLASMA', self.read_JPLASMA),
                ('RESULT.OUT', self.read_RESULTS),
                ('RESULT', self.read_RESULTS),
                ('BPLASMA.OUT', self.read_BPLASMA),
                ('BPLASMA', self.read_BPLASMA),
                ('PROFEQ.OUT', self.read_PROFEQ),
                ('PROFEQ', self.read_PROFEQ),
                ('XPLASMA.OUT', self.read_XPLASMA),
                ('XPLASMA', self.read_XPLASMA),
                ('FREQUENCIES.OUT', self.read_FREQS),
                ('DWK_ENERGY_DENSITY.OUT', self.read_dWk_den),
                ('PROFNTV.OUT', self.read_PROFNTV),
                ('TORQUENTV.OUT', self.read_TORQUENTV),
                ('PROFNUSTAR.OUT', self.read_NUSTAR),
            )
        )
        for item in mapper:
            if os.path.exists(self.filename + os.sep + item):
                try:
                    mapper[item](self.filename + os.sep + item)
                except Exception as _excp:
                    print(f'Problem parsing {item}: {_excp}')

    """
    Plotting methods
    """

    def plot_RMZM(self, fig=None):
        """
        Plot RM-ZM grid
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)
        ax1 = pyplot.subplot(2, 2, 1)
        ax1.plot(self[self.sim]['s'], np.real(self[self.sim]['RM']))
        ax1.set_ylabel('Re(R_m)')

        ax2 = pyplot.subplot(2, 2, 2)
        ax2.plot(self[self.sim]['s'], np.imag(self[self.sim]['RM']))
        ax2.set_ylabel('Im(R_m)')

        ax3 = pyplot.subplot(2, 2, 3)
        ax3.plot(self[self.sim]['s'], np.real(self[self.sim]['ZM']))
        ax3.set_ylabel('Re(Z_m)')
        ax3.set_xlabel('s')

        ax4 = pyplot.subplot(2, 2, 4)
        ax4.plot(self[self.sim]['s'], np.imag(self[self.sim]['ZM']))
        ax4.set_ylabel('Im(Z_m)')
        ax4.set_xlabel('s')
        fig.tight_layout()

    def plot_RZ(self, fig=None):
        """
        Plot R-Z grid
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)
        Ns = self[self.sim]['Ns1'].values.astype(int) + self[self.sim]['Ns2'].values.astype(int)
        Rplot = self[self.sim]['R'][0:Ns, :].values
        Zplot = self[self.sim]['Z'][0:Ns, :].values
        ax.plot(Rplot.T * self[self.sim]['R0EXP'].values, Zplot.T * self[self.sim]['R0EXP'].values, 'g-')
        ax.plot(Rplot * self[self.sim]['R0EXP'].values, Zplot * self[self.sim]['R0EXP'].values, 'b-')
        ax.axis('equal')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('Z [m]')
        fig.tight_layout()

    def plot_SurfS(self, fig=None):
        """
        Plot surface stored in ['CouplingSurfS']
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)
        Ns = self[self.sim]['Ns1'].values.astype(int) + self[self.sim]['Ns2'].values.astype(int)
        Ns1 = self[self.sim]['Ns1'].values.astype(int)
        Rtot = self[self.sim]['R'][0:Ns, :].values
        Ztot = self[self.sim]['Z'][0:Ns, :].values
        if 'CouplingSurfS' not in self:
            self.get_SurfS()
        Rs = self['CouplingSurfS']['Rs']
        Zs = self['CouplingSurfS']['Zs']
        Rplasma = self[self.sim]['R'][Ns1, :].values
        Zplasma = self[self.sim]['Z'][Ns1, :].values
        # Plot all surfaces
        ax.plot(Rtot.T * self[self.sim]['R0EXP'].values, Ztot.T * self[self.sim]['R0EXP'].values, color='g')
        # Plot SurfS
        ax.plot(Rs * self[self.sim]['R0EXP'].values, Zs * self[self.sim]['R0EXP'].values, linewidth=3, color='r')
        ax.plot(
            Rplasma * self[self.sim]['R0EXP'].values, Zplasma * self[self.sim]['R0EXP'].values, linestyle='dashed', linewidth=2, color='b'
        )
        ax.axis('equal')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('Z [m]')
        fig.tight_layout()

    def plot_JPLASMA(self, Mmax=5, fig=None):
        """
        Plot perturbed current components j1,j2,j3
        The MARS variable "J*j" is shown, not the physical quantity "j"
        :param fig: specify target figure
        """
        from matplotlib import pyplot
        from labellines import labelLine, labelLines

        if fig is None:
            fig = pyplot.figure()
        ax = None
        label = 'JPLASMA'
        MM = self[label]['Mm'].values
        labelstring = [str(m) for m in MM]
        for k, c in enumerate(['JM1', 'JM2', 'JM3']):
            ax = ax1 = fig.use_subplot(3, 2, 2 * k + 1, sharex=ax)
            ax1.plot(self[label]['s'], np.real(self[label][c]))
            for i, line in enumerate(ax1.lines):
                line.set_label(labelstring[i])
            lines1 = ax1.get_lines()
            labelLines(lines1[np.abs(np.min(MM)) + 1 : np.abs(np.min(MM)) + Mmax + 1], xvals=(0.0, 1.0), align=False)
            ax1.set_title('Re($J\cdot j^%d_m$)' % (k + 1), y=0.8)
            ax2 = fig.use_subplot(3, 2, 2 * (k + 1), sharex=ax)
            ax2.plot(self[label]['s'], np.imag(self[label][c]))
            for i, line in enumerate(ax2.lines):
                line.set_label(labelstring[i])
            lines2 = ax2.get_lines()
            labelLines(lines2[np.abs(np.min(MM)) + 1 : np.abs(np.min(MM)) + Mmax + 1], xvals=(0.0, 1.0), align=False)
            ax2.set_title('Im($J\cdot j^%d_m$)' % (k + 1), y=0.8)
        ax1.set_xlabel('s')
        ax2.set_xlabel('s')
        fig.tight_layout()

    def plot_FREQUENCIES(self, fig=None):
        """
        Plot frequencies related to drift kinetic resonances
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)
        label = 'FREQUENCIES'
        ax.plot(self[label]['s'], self[label]['we'], 'k-', label=r'$\omega_E$')
        ax.plot(self[label]['s'], self[label]['wsni'] + self[label]['wsti'], 'g-', label=r'$\omega_*^{thi}$')
        ax.plot(self[label]['s'], self[label]['awbt'], 'b-', label=r'$\omega_b^{thi}$')
        ax.plot(self[label]['s'], self[label]['awdi'], 'r-', label=r'$\omega_d^{thi}$')
        ax.plot(self[label]['s'], self[label]['awda'], 'r--', label=r'$\omega_d^{hot}$')
        ax.set_xlabel('s')
        ax.set_ylabel('Frequencies')
        ax.legend(loc=0)
        fig.tight_layout()

    def plot_BPLASMA(self, Mmax=5, fig=None):
        """
        Plot perturbed field components b1,b2,b3
        The MARS variable "J*b" is shown, not the physical quantity "b"
        :param Mmax: upper poloidal harmonic for labeling
        :param fig: specify target figure
        """
        from matplotlib import pyplot
        from labellines import labelLine, labelLines

        if fig is None:
            fig = pyplot.figure()
        ax = None
        label = 'BPLASMA'
        MM = self[label]['Mm'].values
        labelstring = [str(m) for m in MM]
        for k, c in enumerate(['BM1', 'BM2', 'BM3']):
            ax = ax1 = fig.use_subplot(3, 2, 2 * k + 1, sharex=ax)
            ax1.plot(self[label]['s'], np.real(self[label][c]))
            for i, line in enumerate(ax1.lines):
                line.set_label(labelstring[i])
            lines1 = ax1.get_lines()
            labelLines(lines1[np.abs(np.min(MM)) + 1 : np.abs(np.min(MM)) + Mmax + 1], xvals=(0.0, 1.0), align=False)
            ax1.set_title('Re($J\cdot b^%d_m$)' % (k + 1), y=0.8)
            ax2 = fig.use_subplot(3, 2, 2 * (k + 1), sharex=ax)
            ax2.plot(self[label]['s'], np.imag(self[label][c]))
            for i, line in enumerate(ax2.lines):
                line.set_label(labelstring[i])
            lines2 = ax2.get_lines()
            labelLines(lines2[np.abs(np.min(MM)) + 1 : np.abs(np.min(MM)) + Mmax + 1], xvals=(0.0, 1.0), align=False)
            ax2.set_title('Im($J\cdot b^%d_m$)' % (k + 1), y=0.8)
        ax1.set_xlabel('s')
        ax2.set_xlabel('s')
        fig.tight_layout()

    def plot_XPLASMA(self, Mmax=5, fig=None):
        """
        Plot plasma displacement components X1,X2,X3
        :param Mmax: upper poloidal harmonic for labeling
        :param fig: specify target figure
        """
        from matplotlib import pyplot
        from labellines import labelLine, labelLines

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = None
        label = 'XPLASMA'
        MM = self[label]['Mm'].values
        labelstring = [str(m) for m in MM]
        for k, c in enumerate(['XM1', 'XM2', 'XM3']):
            ax1 = pyplot.subplot(3, 2, 2 * k + 1, sharex=ax)
            ax1.plot(self[label]['sp'], np.real(self[label][c]))
            for i, line in enumerate(ax1.lines):
                line.set_label(labelstring[i])
            lines1 = ax1.get_lines()
            labelLines(lines1[np.abs(np.min(MM)) + 1 : np.abs(np.min(MM)) + Mmax + 1], xvals=(0.0, 1.0), align=False)
            ax1.set_title('Re($X^%d_m$)' % (k + 1), y=0.8)
            ax2 = pyplot.subplot(3, 2, 2 * (k + 1), sharex=ax)
            ax2.plot(self[label]['sp'], np.imag(self[label][c]))
            for i, line in enumerate(ax2.lines):
                line.set_label(labelstring[i])
            lines2 = ax2.get_lines()
            labelLines(lines2[np.abs(np.min(MM)) + 1 : np.abs(np.min(MM)) + Mmax + 1], xvals=(0.0, 1.0), align=False)
            ax2.set_title('Im($X^%d_m$)' % (k + 1), y=0.8)
        ax1.set_xlabel('sp')
        ax2.set_xlabel('sp')
        fig.tight_layout()

    def plot_Xn(self, fig=None):
        """
        Plot normal plasma displacement
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)

        label = 'XPLASMA'
        if 'R' not in self[self.sim]:
            self.get_RZ()
        if 'Xn' not in self[label]:
            self.get_X123()

        Irat = self[self.sim]['Iratsurf']
        # Plasma displacement defined within plasma boundary
        Ns1 = self[self.sim]['Ns1'].values
        R = self[self.sim]['R'].isel(s=range(Ns1)) * self[self.sim]['R0EXP']
        Z = self[self.sim]['Z'].isel(s=range(Ns1)) * self[self.sim]['R0EXP']
        C = np.real(self[label]['Xn'])
        pc = ax.pcolormesh(R, Z, C, cmap='jet', antialiased=True)
        for I in Irat.values:
            ax.plot(R[I, :], Z[I, :], linestyle='dashed', linewidth=2, color='w')
        ax.set_aspect('equal', adjustable='box')
        fig.colorbar(pc, ax=ax)
        ax.set_title('Re($\\xi_n$)')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('Z [m]')
        fig.tight_layout()

    def plot_Bn(self, II=False, fig=None):
        """
        Plot normal field perturbation
        :param II: plot up to II radial grid index (default is plasma boundary)
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)

        label = 'BPLASMA'
        if 'R' not in self[self.sim]:
            self.get_RZ()
        if 'Bn' not in self[label]:
            self.get_B123()

        Irat = self[self.sim]['Iratsurf']
        # Pick last s-grid point for Bn plotting
        if II:
            Ns = II
        else:
            Ns = self[self.sim]['Ns1'].values
        R = self[self.sim]['R'].isel(s=range(Ns)) * self[self.sim]['R0EXP']
        Z = self[self.sim]['Z'].isel(s=range(Ns)) * self[self.sim]['R0EXP']
        C = np.real(self[label]['Bn'].isel(s=range(Ns)))
        pc = ax.pcolormesh(R, Z, C, cmap='jet', antialiased=True)
        for I in Irat.values:
            ax.plot(R[I, :], Z[I, :], linestyle='dashed', linewidth=2, color='w')
        ax.set_aspect('equal', adjustable='box')
        fig.colorbar(pc, ax=ax)
        ax.set_title('Re($B_n$)')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('Z [m]')
        fig.tight_layout()

    def plot_BrzSurf(self, II=False, rsurf=False, fig=None):
        """
        Plot Br Bz (cyl. coords.) along specified surface
        :param II: plot on II radial grid index (default is plasma boundary)
        :param rsurf: normalized radius of surface
        :param fig: specify target figure
        """
        # Pick last s-grid point for Bn plotting
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        if II:
            Ns = II
        elif rsurf:
            # Find surface index
            Ns = np.argmin(np.abs(self[self.sim]['s'].values - rsurf))
        else:
            Ns = self[self.sim]['Ns1'].values
        R = (self[self.sim]['R'].values) * self[self.sim]['R0EXP'].values
        Z = (self[self.sim]['Z'].values) * self[self.sim]['R0EXP'].values
        Rw = R[Ns, :]
        Zw = Z[Ns, :]
        Tw = np.arctan2(Zw - Z[0, 0], Rw - R[0, 0]) * (180 / np.pi)
        KK = np.where(np.diff(Tw) < -180)[0]
        if (len(KK) == 1) & (2 * KK > len(Tw)):
            Tw[KK[0] + 1 :] = Tw[KK[0] + 1 :] + 360
        if (len(KK) == 1) & (2 * KK < len(Tw)):
            Tw[0 : KK[0]] = Tw[0 : KK[0]] - 360
        Tw = np.sort(Tw)
        JJ = np.argsort(Tw)
        label = 'BPLASMA'
        BR = self[label]['Br'].values
        BZ = self[label]['Bz'].values
        ax1 = pyplot.subplot(2, 2, 1)
        ax1.plot(Tw, np.real(BR[Ns, JJ]), linewidth=2)
        ax1.set_ylabel('Re($\delta B_R$)')

        ax2 = pyplot.subplot(2, 2, 2)
        ax2.plot(Tw, np.imag(BR[Ns, JJ]), linewidth=2)
        ax2.set_ylabel('Im($\delta B_R$)')

        ax3 = pyplot.subplot(2, 2, 3)
        ax3.plot(Tw, np.real(BZ[Ns, JJ]), linewidth=2)
        ax3.set_ylabel('Re($\delta B_Z$)')
        ax3.set_xlabel('GEOM angle')

        ax4 = pyplot.subplot(2, 2, 4)
        ax4.plot(Tw, np.imag(BZ[Ns, JJ]), linewidth=2)
        ax4.set_ylabel('Im($\delta B_Z$)')
        ax4.set_xlabel('GEOM angle')
        fig.suptitle(r'$B_r$, $B_z$ vs poloidal angle at s(%s)=%s' % (Ns, self[self.sim]['s'][Ns].values))
        fig.tight_layout()

    def plot_BrzAbs(self, fig=None):
        """
        Plot |B| along poloidal angle at plasma surface
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)
        Ns = self[self.sim]['Ns1'].values
        chi = self[self.sim]['chi'].values
        label = 'BPLASMA'
        AmpB = np.sqrt(abs(self[label]['Br'].values) ** 2 + abs(self[label]['Bz'].values) ** 2 + abs(self[label]['Bphi'].values) ** 2)
        ax.plot(chi * 180 / np.pi, AmpB[Ns, :], linewidth=2)
        ax.set_ylabel('$|\delta B|$')
        ax.set_xlabel('Poloidal angle $[\circ]$')
        fig.tight_layout()

    def plot_BrzMap(self, fig=None):
        """
        Plot |B| (R,Z) map inside plasma
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)

        Ns = self[self.sim]['Ns1'].values
        label = 'BPLASMA'

        Br = self[label]['Br'].isel(s=range(Ns)).values
        Bz = self[label]['Bz'].isel(s=range(Ns)).values
        Bphi = self[label]['Bphi'].isel(s=range(Ns)).values
        AmpB = np.sqrt(abs(Br) ** 2 + abs(Bz) ** 2 + abs(Bphi) ** 2)
        R = self[self.sim]['R'].isel(s=range(Ns)) * self[self.sim]['R0EXP']
        Z = self[self.sim]['Z'].isel(s=range(Ns)) * self[self.sim]['R0EXP']
        pc = ax.pcolormesh(R, Z, AmpB, cmap='jet', antialiased=True)
        ax.set_aspect('equal', adjustable='box')
        fig.colorbar(pc, ax=ax)
        ax.set_title('$|\delta B|$')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('Z [m]')
        fig.tight_layout()

    def plot_XrzMap(self, fig=None):
        """
        Plot |X| (R,Z) map inside plasma
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        Ns = self[self.sim]['Ns1'].values
        label = 'XPLASMA'
        ax = fig.use_subplot(1, 1, 1)
        Xr = self[label]['Xr'].isel(sp=range(Ns)).values.real
        # Xz = self[label]['Xz'].isel(sp=range(Ns)).values
        # Xphi = self[label]['Xphi'].isel(sp=range(Ns)).values
        # AmpX = np.sqrt(abs(Xr) ** 2 + abs(Xz) ** 2 + abs(Xphi) ** 2) * self[self.sim]['R0EXP'].values * 1.0e3
        R = self[self.sim]['R'].isel(s=range(Ns)) * self[self.sim]['R0EXP']
        Z = self[self.sim]['Z'].isel(s=range(Ns)) * self[self.sim]['R0EXP']
        pc = ax.pcolormesh(R, Z, Xr, cmap='jet', antialiased=True)
        ax.set_aspect('equal', adjustable='box')
        fig.colorbar(pc, ax=ax)
        ax.set_title('Radial displacement $X_r$')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('Z [m]')
        fig.tight_layout()

    def plot_dWkDen(self, fig=None):
        """
        Plot total dWk energy density profiles
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)

        label = 'DWK_ENERGY_DENSITY'
        csm = self[label]['s']
        dWki_re = self[label]['0_0_REdwk']
        dWki_im = self[label]['0_0_IMdwk']

        pyplot.plot(csm, dWki_re, 'bo-', label=r'Re($\delta W_k$) total')
        pyplot.plot(csm, dWki_im, 'rs--', label=r'Im($\delta W_k$) total')
        ax.set_xlabel('s')
        ax.set_ylabel('dWk energy density')
        ax.legend(loc=0)
        fig.tight_layout()

    def plot_dWkComp(self, fig=None):
        """
        Plot dWk components (integral of energy density)
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        else:
            pyplot.figure(num=fig.number)

        ax = pyplot.subplot(1, 1, 1)

        NSPECIES = self['DWK_COMPONENTS']['NSPECIES'].values
        labels = ['NTD', 'NTB', 'NP']
        ions = [self['DWK_COMPONENTS']['K_I_NTD'], self['DWK_COMPONENTS']['K_I_NTB'], self['DWK_COMPONENTS']['K_I_NP']]
        electrons = [self['DWK_COMPONENTS']['K_e_NTD'], self['DWK_COMPONENTS']['K_e_NTB'], self['DWK_COMPONENTS']['K_e_NP']]
        if NSPECIES > 2:
            SP_DICT = {}
            for II in range(NSPECIES - 2):
                #  +2 to skip ions and electrons, +1 to start counting from 1
                P = II + 2 + 1
                SP_DICT[P] = [
                    self['DWK_COMPONENTS']['K_%s_NTD' % float(P)],
                    self['DWK_COMPONENTS']['K_%s_NTB' % float(P)],
                    self['DWK_COMPONENTS']['K_%s_NP' % float(P)],
                ]
        x = np.arange(len(labels))
        width = 0.35
        ax.bar(x - width / 2, ions, width, label='Ions')
        ax.bar(x + width / 2, electrons, width, label='Electrons')
        if NSPECIES > 2:
            for II in range(NSPECIES - 2):
                P = II + 2 + 1
                ax.bar(x - width / 2, SP_DICT[P], width, label='Specie %s' % P)
        ax.set_ylabel('dWk')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(loc=0)
        fig.tight_layout()

    def plot_BntpSurf(self, fig=None):
        """
        Plot Bn, Bt, Bphi on surface calculated by get_BatSurf
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        Tw = self['BPLASMA']['Tw']
        ax1 = fig.use_subplot(3, 2, 1)
        ax1.plot(Tw * 180 / np.pi, np.real(self['BPLASMA']['Bn_s']), 'b-')
        ax1.set_ylabel('Re(Bn)')

        ax2 = fig.use_subplot(3, 2, 2)
        ax2.plot(Tw * 180 / np.pi, np.imag(self['BPLASMA']['Bn_s']), 'b-')
        ax2.set_ylabel('Im(Bn)')

        ax3 = fig.use_subplot(3, 2, 3)
        ax3.plot(Tw * 180 / np.pi, np.real(self['BPLASMA']['Bt_s']), 'b-')
        ax3.set_ylabel('Re(Bt)')

        ax4 = fig.use_subplot(3, 2, 4)
        ax4.plot(Tw * 180 / np.pi, np.imag(self['BPLASMA']['Bt_s']), 'b-')
        ax4.set_ylabel('Im(Bt)')

        ax5 = fig.use_subplot(3, 2, 5)
        ax5.plot(Tw * 180 / np.pi, np.real(self['BPLASMA']['Bphi_s']), 'b-')
        ax5.set_ylabel(r'Re($B_{\phi}$)')
        ax5.set_xlabel(r'$\theta$ [$^{\circ}$]')

        ax6 = fig.use_subplot(3, 2, 6)
        ax6.plot(Tw * 180 / np.pi, np.imag(self['BPLASMA']['Bphi_s']), 'b-')
        ax6.set_ylabel(r'Im($B_{\phi}$)')
        ax6.set_xlabel(r'$\theta$ [$^{\circ}$]')
        fig.tight_layout()

    def plot_BntpSurfMm(self, fig=None):
        """
        Plot poloidal Fourier harmonics of Bn, Bt, Bphi on surface calculated by get_BatSurf
        :param fig: specify target figure
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        Tw = self['BPLASMA']['Tw']
        ax1 = fig.use_subplot(3, 2, 1)
        ax1.plot(self['BPLASMA']['Mm'], np.real(self['BPLASMA']['Bnm_s']), 'bo')
        ax1.set_ylabel(r'$Re(B^m_n)$')
        ax1.grid()

        ax2 = fig.use_subplot(3, 2, 2)
        ax2.plot(self['BPLASMA']['Mm'], np.imag(self['BPLASMA']['Bnm_s']), 'bo')
        ax2.set_ylabel(r'$Im(B^m_n)$')
        ax2.grid()

        ax3 = fig.use_subplot(3, 2, 3)
        ax3.plot(self['BPLASMA']['Mm'], np.real(self['BPLASMA']['Btm_s']), 'bo')
        ax3.set_ylabel(r'$Re(B^m_t)$')
        ax3.grid()

        ax4 = fig.use_subplot(3, 2, 4)
        ax4.plot(self['BPLASMA']['Mm'], np.imag(self['BPLASMA']['Btm_s']), 'bo')
        ax4.set_ylabel(r'$Im(B^m_t)$')
        ax4.grid()

        ax5 = fig.use_subplot(3, 2, 5)
        ax5.plot(self['BPLASMA']['Mm'], np.real(self['BPLASMA']['Bpm_s']), 'bo')
        ax5.set_ylabel(r'Re($B^m_{\phi}$)')
        ax5.set_xlabel('m')
        ax5.grid()

        ax6 = fig.use_subplot(3, 2, 6)
        ax6.plot(self['BPLASMA']['Mm'], np.imag(self['BPLASMA']['Bpm_s']), 'bo')
        ax6.set_ylabel(r'Im($B^m_{\phi}$)')
        ax6.set_xlabel('m')
        ax6.grid()
        fig.tight_layout()

    def plot_BatSurf3D(self, fig=None, rsurf=1.0, ntor=-1):
        """
        Plot Bn on surface calculated by get_BatSurf, normalized and reconstructed in (chi,phi) real space
        :param fig: specify target figure
        :param rsurf: normalized surface radius for plotting, default is plasma boundary
        :param n: toroidal mode number for inverse Fourier transorm in toroidal angle
        """
        from matplotlib import pyplot
        from matplotlib.colors import BoundaryNorm
        from matplotlib.ticker import MaxNLocator

        if fig is None:
            fig = pyplot.figure()
        try:
            Bn = self['BPLASMA']['Bn_s']
        except KeyError:
            raise ('ERROR: calculate B on surface before plotting')
        Tw = self['BPLASMA']['Tw']
        phi = np.linspace(0, 2 * np.pi, self[self.sim]['Nchi'].values)
        expnphi = np.exp(1j * ntor * phi)
        Bna = np.real(np.dot(expnphi[:, np.newaxis], Bn.values[np.newaxis, :])).T / np.max(np.abs(Bn.values))
        [pp, cc] = np.meshgrid(phi, Tw)
        pp = pp * 180 / np.pi
        cc = cc * 180 / np.pi
        # Find surface index
        IIsurf = np.argmin(np.abs(self[self.sim]['s'].values - rsurf))

        levels = MaxNLocator(nbins=25).tick_values(Bna.min(), Bna.max())
        cmap = pyplot.get_cmap('jet')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        ax0 = pyplot.gca()
        cf = ax0.contourf(pp, cc, Bna, levels=levels, cmap=cmap)
        cf2 = ax0.contour(cf, levels=cf.levels[::2], colors='k')
        cbar = fig.colorbar(cf, ax=ax0)
        cbar.ax.set_ylabel(r'[A.U.]')
        ax0.set_title(r'$B_{n}$ n=%s - at r/a = %s' % (ntor, str(self[self.sim]['s'][IIsurf].values)))
        ax0.set_xlabel(r'$\Phi [^\circ]$')
        ax0.set_ylabel(r'$\Theta [^\circ]$')

        # Find index of HFS, LFS, TOP, BOT
        k = self[self.sim]['R'].isel(s=IIsurf).argmin(dim='chi').values
        chi_HFS = Tw[k] * 180 / np.pi
        k = self[self.sim]['R'].isel(s=IIsurf).argmax(dim='chi').values
        chi_LFS = Tw[k] * 180 / np.pi
        k = self[self.sim]['Z'].isel(s=IIsurf).argmin(dim='chi').values
        chi_bot = Tw[k] * 180 / np.pi
        k = self[self.sim]['Z'].isel(s=IIsurf).argmax(dim='chi').values
        chi_top = Tw[k] * 180 / np.pi

        ax0.text(10, chi_HFS, 'HFS', bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 5})
        ax0.text(10, chi_LFS, 'LFS', bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 5})
        ax0.text(10, chi_top, 'TOP', bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 5})
        ax0.text(10, chi_bot, 'BOT', bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 5})

        pyplot.tight_layout()

    def plot_Bwarp(self, fig=None, rsurf=1.0):
        """
        Visualize B-field perturbation on specific surface
        :param fig: specify target figure
        :param rsurf: normalized surface radius for plotting, default is plasma boundary
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        if 'Br' not in self['BPLASMA']:
            self.get_Bcyl()

        # Find surface index
        IIsurf = np.argmin(np.abs(self[self.sim]['s'].values - rsurf))

        Rw = self[self.sim]['R'].isel(s=IIsurf)
        Zw = self[self.sim]['Z'].isel(s=IIsurf)

        try:
            Bwr = self['BPLASMA']['Br'].isel(s=IIsurf)
            Bwz = self['BPLASMA']['Bz'].isel(s=IIsurf)
        except IndexError:
            print('ERROR: Selected index is out of BPLASMA calculation domain')
            return
        B0 = self[self.sim]['B0EXP'].values
        R0 = self[self.sim]['R0EXP'].values
        h = B0 / self[self.sim]['Ns1'].values
        Bwr_r = np.real(Bwr)
        Bwz_r = np.real(Bwz)
        Bt = np.sqrt(Bwr_r**2 + Bwz_r**2)
        Bt[np.where(Bt == 0.0)] = 1.0
        R1 = Rw + h * Bwr_r / Bt
        Z1 = Zw + h * Bwz_r / Bt
        R2 = np.vstack((Rw, R1))
        Z2 = np.vstack((Zw, Z1))
        pyplot.plot(Rw * R0, Zw * R0, 'c-')
        pyplot.plot(R2 * R0, Z2 * R0, 'b-')
        pyplot.axis('equal')
        pyplot.xlabel('R [m]')
        pyplot.ylabel('Z [m]')

    def plot_Xwarp(self, fig=None, rsurf=1.0):
        """
        Visualize displacement perturbation on specific surface
        :param fig: specify target figure
        :param rsurf: normalized surface radius for plotting, default is plasma boundary
        """
        from matplotlib import pyplot

        if fig is None:
            fig = pyplot.figure()
        if 'Xr' not in self['XPLASMA']:
            self.get_Xcyl()

        # Find wall surface index
        IIsurf = np.argmin(np.abs(self[self.sim]['s'].values - rsurf))

        Rw = self[self.sim]['R'].isel(s=IIsurf)
        Zw = self[self.sim]['Z'].isel(s=IIsurf)

        try:
            Xwr = self['XPLASMA']['Xr'].isel(sp=IIsurf)
            Xwz = self['XPLASMA']['Xz'].isel(sp=IIsurf)
        except IndexError:
            print('ERROR: Selected index is out of XPLASMA calculation domain')
            return
        B0 = self[self.sim]['B0EXP'].values
        R0 = self[self.sim]['R0EXP'].values
        h = R0 / self[self.sim]['Ns1'].values
        Xwr_r = np.real(Xwr)
        Xwz_r = np.real(Xwz)
        Xt = np.sqrt(Xwr_r**2 + Xwz_r**2)
        Xt[np.where(Xt == 0.0)] = 1.0
        R1 = Rw + h * Xwr_r / Xt
        Z1 = Zw + h * Xwz_r / Xt
        R2 = np.vstack((Rw, R1))
        Z2 = np.vstack((Zw, Z1))
        pyplot.plot(Rw * R0, Zw * R0, 'c-')
        pyplot.plot(R2 * R0, Z2 * R0, 'b-')
        pyplot.axis('equal')
        pyplot.xlabel('R [m]')
        pyplot.ylabel('Z [m]')
        return R1, Z1

    def plot_PROFNTV(self, fig=None):
        """
        Plot "boundary"-frequencies between different NTV regimes
        :param fig: specify target figure
        """
        from labellines import labelLines

        if fig is None:
            fig = pyplot.figure()
        ax = fig.gca()
        pyplot.semilogy(self['PROFNTV']['psi'], self['PROFNTV']['nu_n1'], 'b:', linewidth=1, label=r'$|\omega_E| (\delta B /\epsilon)^{2}$')
        pyplot.semilogy(self['PROFNTV']['psi'], self['PROFNTV']['nu_n2'], 'b--', linewidth=2, label=r'$|\omega_E|$')
        pyplot.semilogy(self['PROFNTV']['psi'], self['PROFNTV']['nu_n3'], 'b-', linewidth=3, label=r'$\sqrt{\epsilon}\omega_{ti}$')
        pyplot.semilogy(
            self['PROFNTV']['psi'], self['PROFNTV']['nu_r1'], 'r:', linewidth=1, label=r'$\omega_{B0}(\delta B /\epsilon)^{3/2}$'
        )
        pyplot.semilogy(self['PROFNTV']['psi'], self['PROFNTV']['nu_r2'], 'r--', linewidth=2, label=r'$\omega_{B0} / \epsilon$')
        pyplot.semilogy(self['PROFNTV']['psi'], self['PROFNTV']['nu'] / self['PROFNTV']['eps'], 'k-', linewidth=4, label=r'$\nu /\epsilon$')
        lines = ax.get_lines()
        labelLines(lines, yoffsets=0.01, align=False, backgroundcolor="none")
        pyplot.xlabel(r'$\psi_p$')
        pyplot.ylabel(r'$freq. / \epsilon$ for NTV regimes [rad/s]')

    def plot_NUSTAR(self, fig=None, kplot=2):
        """
        Plot effective collisionality for ions and electrons
        :param fig: specify target figure
        :param kplot: =2 to use logscale, =1 to use linear y-axis
        """
        from labellines import labelLines

        if fig is None:
            fig = pyplot.figure()
        ax = fig.gca()
        if kplot == 2:
            pyplot.semilogy(self['NUSTAR']['s'], self['NUSTAR']['nustar_i'], 'r--', linewidth=3, label=r'$\nu^*$ ions')
            pyplot.semilogy(self['NUSTAR']['s'], self['NUSTAR']['nustar_e'], 'b-', linewidth=3, label=r'$\nu^*$ electrons')
        else:
            pyplot.plot(self['NUSTAR']['s'], self['NUSTAR']['nustar_i'], 'r--', linewidth=3, label=r'$\nu^*$ ions')
            pyplot.plot(self['NUSTAR']['s'], self['NUSTAR']['nustar_e'], 'b-', linewidth=3, label=r'$\nu^*$ electrons')
        pyplot.xlabel(r'$s=\sqrt{\psi_p}$')
        pyplot.ylabel(r'$\nu^*$')
        pyplot.legend(loc=0)


class OMFITnColumns(SortedDict, OMFITascii):
    r"""
    OMFIT class used to interface with n-columns input files

    :param filename: filename passed to OMFITascii class

    :param \**kw: keyword dictionary passed to OMFITascii class
    """

    def __init__(self, filename, **kw):
        SortedDict.__init__(self)
        OMFITascii.__init__(self, filename, **kw)
        self.dynaLoad = True

    @dynaLoad
    def load(self):
        with open(self.filename, 'r') as f:
            header = f.readline()
        if not len(header):
            return
        tmp = np.atleast_2d(np.loadtxt(self.filename, skiprows=1))
        self['x'] = tmp[:, 0]
        for k in range(1, tmp.shape[1]):
            self['y_%d' % k] = tmp[:, k]

    @dynaSave
    def save(self):
        with open(self.filename, 'w') as f:
            if not len(self):
                f.write('0 0')
                return
            tmp = np.vstack(list(self.values())).T
            shape = list(tmp.shape)
            shape[1] = shape[1] - 1
            f.write(' '.join(map(str, shape)) + '\n')
            for k in range(tmp.shape[0]):
                f.write(' '.join(['%5.9e' % x for x in tmp[k, :]]) + '\n')

    def plot(self):
        from matplotlib import pyplot

        tmp = np.vstack(list(self.values())).T
        fignum = pyplot.get_fignums()[-1]
        for k in range(tmp.shape[1]):
            # condition to avoid plotting first columnt vs. itself
            if k == 0:
                continue
            pyplot.figure(k + fignum)
            pyplot.plot(tmp[:, 0], tmp[:, k])
            pyplot.ylabel(self._OMFITkeyName)
            pyplot.tight_layout()


class OMFITmarsProfile(OMFITnColumns):
    pass


############################################
if '__main__' == __name__:
    test_classes_main_header()

    if os.path.exists('/home/pigatto/Work_2020/RFX-mod2/OUTPUTS/'):
        tmp = OMFITmars('/home/pigatto/Work_2020/RFX-mod2/OUTPUTS/')
        tmp.load()
        print(tmp)
        tmp.plot_RMZM()
        tmp.plot_JPLASMA()
        from matplotlib import pyplot

        pyplot.show()
