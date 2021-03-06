from os.path import join
from viscojapan.pollitz.pollitz_wrapper import \
     decay, vtordep, decay4m, vsphm, decay4, vsphdep
from ..utils import timeit

__all__=['ComputeEarthModelVISCO1D','ComputeEarthModelVISCO1DNonGravity']

class ComputeEarthModelVISCO1D(object):
    def __init__(self,
                 earth_file,
                 l_max,
                 outputs_dir,
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):
        self.earth_file = earth_file
        self.outputs_dir = outputs_dir
        self.l_max = l_max
        self.if_skip_on_existing_output = if_skip_on_existing_output
        self.stdout = stdout
        self.stderr = stderr

        self.decay_out = join(self.outputs_dir, 'decay.out')
        self.vtor_out = join(self.outputs_dir, 'vtor.out')
        self.decay4_out = join(self.outputs_dir, 'decay4.out')
        self.vsph_out = join(self.outputs_dir, 'vsph.out')

    @timeit
    def _decay(self):
        print("decay is running ... ")
        cmd = decay(
            earth_model = self.earth_file,
            decay_out = self.decay_out,
            l_min = 2,
            l_max = self.l_max,
            if_skip_on_existing_output = self.if_skip_on_existing_output,
            stdout = self.stdout,
            stderr = self.stderr,
            )
        cmd()

    @timeit
    def _vtordep(self):
        print("vtordep is running ... ")
        cmd = vtordep(
            earth_model = self.earth_file,
            decay_out = self.decay_out,
            vtor_out = self.vtor_out,
            obs_dep = 0.0,
            if_skip_on_existing_output = self.if_skip_on_existing_output,
            stdout = self.stdout,
            stderr = self.stderr)
        cmd()

    @timeit
    def _decay4m(self):
        print("decay4m is running ... ")
        cmd = decay4m(
            earth_model = self.earth_file,
            decay4_out = self.decay4_out,
            l_min = 2,
            l_max = self.l_max,
            if_skip_on_existing_output = self.if_skip_on_existing_output,
            stdout = self.stdout,
            stderr = self.stderr)
        cmd()

    @timeit
    def _vsphm(self):
        print("vsphm is running ... ")
        cmd = vsphm(
            earth_model = self.earth_file,
            decay4_out = self.decay4_out,
            vsph_out = self.vsph_out,
            obs_dep = 0.0,
            if_skip_on_existing_output = self.if_skip_on_existing_output,
            stdout = self.stdout,
            stderr = self.stderr)
        cmd()

    def run(self):
        self._decay()
        self._vtordep()
        self._decay4m()
        self._vsphm()
        
        
class ComputeEarthModelVISCO1DNonGravity(ComputeEarthModelVISCO1D):
    def __init__(self,
                 earth_file,
                 l_max,
                 outputs_dir,
                 if_skip_on_existing_output = True,
                 stdout = None,
                 stderr = None,
                 ):
        super().__init__(
            earth_file = earth_file,
            l_max = l_max,
            outputs_dir = outputs_dir,
            if_skip_on_existing_output = if_skip_on_existing_output,
            stdout = stdout,
            stderr = stderr,)
        
    @timeit
    def _decay4(self):
        print("decay4 is running ... ")
        cmd = decay4(
            earth_model = self.earth_file,
            decay4_out = self.decay4_out,
            l_min = 2,
            l_max = self.l_max,
            if_skip_on_existing_output = self.if_skip_on_existing_output,
            stdout = self.stdout,
            stderr = self.stderr)
        cmd()

    @timeit
    def _vsphdep(self):
        print("vsphdep is running ... ")
        cmd = vsphdep(
            earth_model = self.earth_file,
            decay4_out = self.decay4_out,
            vsph_out = self.vsph_out,
            obs_dep = 0.0,
            if_skip_on_existing_output = self.if_skip_on_existing_output,
            stdout = self.stdout,
            stderr = self.stderr)
        cmd()

    def run(self):
        self._decay()
        self._vtordep()
        self._decay4()
        self._vsphdep()
         
