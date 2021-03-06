import viscojapan as vj

__all__=['PlotCoseismicDisp']

class PlotCoseismicDisp(object):
    def __init__(self,
                 d_obs,
                 d_pred,                 
                 sites,
                 fault_file = None,
                 fault_slip = None,
                 ):
        self.d_obs = d_obs
        self.d_pred = d_pred
        self.sites = sites
        self.sites_subset = None
        self.fault_file =  fault_file
        self.fault_slip = fault_slip

        self.basemap = None

    def _plot_fault(self):
        if self.fault_file is not None:
            mplt = vj.MapPlotFault(self.fault_file,
                                   basemap = self.basemap)
            mplt.plot_slip(self.fault_slip)
    def _plot_trench_top(self):
        mplt = vj.MapPlotSlab(self.basemap)
        mplt.plot_top()

    def _set_basemap(self, region_code):
        self.basemap = vj.MyBasemap(region_code=region_code)

    def _plot_d(self, scale, X, Y, U, label_len, sites_subset=None):
        mplt = vj.MapPlotDisplacement(self.basemap)
        mplt.plot_disp(self.d_obs, self.sites, sites_subset=sites_subset,
                       scale=scale, X=X, Y=Y, U=U, label='obs. '+label_len)
        mplt.plot_disp(self.d_pred, self.sites, sites_subset=sites_subset,
                       scale=scale, color='red',
                       X=X, Y=Y+0.08, U=U, label='pred. '+label_len)

    def _mark_seafloor_sites(self):
        mplt = vj.MapPlotDisplacement(self.basemap)
        mplt.plot_sites_seafloor()
        
    def plot_at_I(self):
        self._set_basemap('I')
        scale = 0.4
        X = 0.15
        Y = 0.1
        U = 0.03
        label_len = '%dcm'%int(U*100)
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )

    def plot_at_H(self):
        self._set_basemap('H')
        scale = 1.3
        X = 0.15
        Y = 0.7
        U = 0.08
        label_len = '%dcm'%int(U*100)
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )

    def plot_at_E(self):
        self._set_basemap('E')
        scale = .8
        X = 0.8
        Y = 0.8
        U = 0.04
        label_len = '%dcm'%int(U*100)
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )
        
    def plot_at_C(self):
        self._set_basemap('C')
        scale = 18
        X = 0.10
        Y = 0.7
        U = 1
        label_len = '%dm'%int(U)
        self._plot_fault()
        self._plot_trench_top()
        self._mark_seafloor_sites()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )

    def plot_at_A(self):
        self._set_basemap('A')
        scale = 15
        X = 0.10
        Y = 0.7
        U = 1
        label_len = '%dm'%int(U)
        self._plot_fault()
        self._plot_trench_top()
        self._mark_seafloor_sites()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )        

    def plot_at_near(self):
        self._set_basemap('near')
        scale = 20
        X = 0.10
        Y = 0.7
        U = 1
        label_len = '%dm'%int(U)
        self._plot_fault()
        self._plot_trench_top()
        self._mark_seafloor_sites()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )

    def plot_at_seafloor(self):
        self._set_basemap('seafloor')
        scale = 80
        X = 0.10
        Y = 0.7
        U = 1
        label_len = '%dm'%int(U)
        self._plot_fault()
        self._plot_trench_top()
        self._mark_seafloor_sites()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )

    def plot_at_all(self):        
        self._set_basemap('all')
        scale = 80
        X = 0.10
        Y = 0.7
        U = 1
        label_len = '%dm'%int(U)
        self._plot_fault()
        self._plot_trench_top()
        self._mark_seafloor_sites()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )

    def plot_at_ryukyu(self):
        self._set_basemap('ryukyu')
        scale = .1
        X = 0.5
        Y = 0.7
        U = .005
        label_len = '%dmm'%int(U*1000)
        self._plot_trench_top()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len
                     )

    def plot_at_oceanward(self):
        self._set_basemap('oceanward')
        sites_subset = vj.get_sites_in_box(self.basemap.region_box)
        scale = .05
        X = 0.85
        Y = 0.1
        U = .005
        label_len = '%dmm'%int(U*1000)
        self._plot_trench_top()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len,
                     sites_subset = sites_subset
                     )

    def plot_at(self, region_code):
        getattr(self, 'plot_at_'+region_code)()

    def plot_far_field(self, sites_far_field):
        self.sites_subset = sites_far_field
        self._set_basemap('all')
        scale = .2
        X = 0.15
        Y = 0.7
        U = .01
        label_len = '%dmm'%int(U*1000)
        self._plot_fault()
        self._plot_trench_top()
        self._mark_seafloor_sites()
        self._plot_d(scale = scale,
                     X = X, Y = Y, U = U, label_len=label_len,
                     sites_subset = sites_far_field
                     )
        
    

