import numpy as np, os
from mpi4py import MPI
from scalapack4py import ScaLAPACK4py
from ctypes import CDLL, RTLD_GLOBAL, POINTER, c_int, c_double

default_scalapack_path = '/usr/lib/x86_64-linux-gnu/libscalapack-openmpi.so'

if os.path.isfile(default_scalapack_path):
    # Try the default path used by most Linux systems
    libpath = '/usr/lib/x86_64-linux-gnu/libscalapack-openmpi.so'
elif 'SCALAPACK_ROOT' in os.environ:
    # ONEAPI Intel MKL case
    libpath = os.environ['SCALAPACK_ROOT']+'libmkl_scalapack_lp64.so'
elif 'SCALAPACK_LIB_PATH' in os.environ:
    # Finally, let user set their own SCALAPACK path
    libpath = os.environ['SCALAPACK_LIB_PATH']
else:
    OSError("Cannot find SCALAPACK library, try installing in the default \n \
    system path with apt-get, installing ONEAPI, or manually setting the \n \
    environmental variable SCALAPACK_LIB_PATH with location of the SCALAPACK \n \
    library.")

sl = ScaLAPACK4py(CDLL(libpath, mode=RTLD_GLOBAL))

n = 5
dtype=np.float64
a = np.arange(n*n, dtype=dtype).reshape((n,n), order='F') * (MPI.COMM_WORLD.rank+1) if MPI.COMM_WORLD.rank==0 else None
print (a)

MP, NP = 2,1

ctx = sl.make_blacs_context(sl.get_default_system_context(), MP, NP)
descr = sl.make_blacs_desc(ctx, n, n)
print("descr", descr, descr.locrow, descr.loccol)

b = np.zeros((descr.locrow, descr.loccol), dtype=dtype)

sl.scatter_numpy(a, POINTER(c_int)(descr), b.ctypes.data_as(POINTER(c_double)), b.dtype)
print (b)

c = sl.gather_numpy(POINTER(c_int)(descr), b, (n, n))
print (c)

