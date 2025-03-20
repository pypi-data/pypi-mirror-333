import numpy as np, os
from mpi4py import MPI
from scalapack4py import ScaLAPACK4py
from numpy.random import rand
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

m = 4
n = 6
dtype=np.float64

a = np.arange(m*n, dtype=dtype).reshape((4,6), order='F') * (MPI.COMM_WORLD.rank+1) if MPI.COMM_WORLD.rank==0 else None
a = a.astype(dtype=dtype, order='F') if MPI.COMM_WORLD.rank==0 else None

print(a)

size = min(m, n)

MP, NP = 2,1
ctx = sl.make_blacs_context(sl.get_default_system_context(), MP, NP)
descr_a = sl.make_blacs_desc(ctx, m, n)
descr_u = sl.make_blacs_desc(ctx, m, m)
descr_vt = sl.make_blacs_desc(ctx, n, n)

b = np.zeros((descr_a.locrow, descr_a.loccol), dtype=dtype, order='F')
sl.scatter_numpy(a, POINTER(c_int)(descr_a), b.ctypes.data_as(POINTER(c_double)), b.dtype)

s = np.zeros(size, dtype=dtype, order='F')
u = np.zeros((descr_u.locrow, descr_u.loccol), dtype=dtype, order='F')
vt = np.zeros((descr_vt.locrow, descr_vt.loccol), dtype=dtype, order='F')
work = np.zeros(1, dtype=np.float64, order='F')

# Workspace query for PDGESVD
lwork = -1
rwork = -1
info = -1
sl.pdgesvd("V", "V", m, n, b, 1, 1, descr_a,
         s, u, 1, 1, descr_u, vt, 1, 1, descr_vt,
         work, lwork, info) 

# Execute PDGESVD with optimal workspace
lwork = int(work[0])
work = np.zeros((lwork), dtype=dtype, order='F')
sl.pdgesvd("V", "V", m, n, b, 1, 1, descr_a,
         s, u, 1, 1, descr_u, vt, 1, 1, descr_vt,
         work, lwork, info)

u_gather = sl.gather_numpy(POINTER(c_int)(descr_u), u.ctypes.data_as(POINTER(c_double)), (m, m))
vt_gather = sl.gather_numpy(POINTER(c_int)(descr_vt), vt.ctypes.data_as(POINTER(c_double)), (n, n))

print(f'U: {u_gather}') if MPI.COMM_WORLD.rank==0 else None
print(f'V**T: {vt_gather}') if MPI.COMM_WORLD.rank==0 else None

s_square = np.eye(size) * s 
s_full_array = np.zeros((m,n)) 
s_full_array[:size,:size] = s_square

print(f'S: {s_full_array}') if MPI.COMM_WORLD.rank==0 else None
print(f'U @ S @ V**T: {u_gather @ s_full_array @ vt_gather}') if MPI.COMM_WORLD.rank==0 else None

