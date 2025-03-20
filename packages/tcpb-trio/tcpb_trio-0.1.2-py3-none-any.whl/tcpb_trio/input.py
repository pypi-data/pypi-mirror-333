from .msg import terachem_server_pb2 as tcpb2

from pathlib import Path
from itertools import chain
from collections import ChainMap
import numpy as np
import logging

logger = logging.getLogger(__name__)

DEFAULT_OPTS = dict(genscrdata="no")


class JobInput:
    """Wrapper of ``terachem_server_pb2.JobInput``"""

    def __init__(self, jobpb: tcpb2.JobInput):
        self.pb = jobpb

    @classmethod
    def from_file(cls, fname: str) -> "JobInput":
        d = read_tc_input(fname)
        return cls.from_dict(d, Path(fname).parent)

    @classmethod
    def from_dict(cls, d: dict[str, str], cwd: Path = Path(".")) -> "JobInput":
        job = tcpb2.JobInput()

        mol = job.mol
        if "coordinates" in d:
            atmi, geom = read_xyz(cwd / d.pop("coordinates"))
            mol.atoms[:] = atmi
            mol.xyz[:] = list(geom.reshape((-1,)))
        if "units" in d:
            mol.units = tcpb2._MOL_UNITTYPE.values_by_name[
                d.pop("units").upper()
            ].number
        if "charge" in d:
            mol.charge = int(d.pop("charge"))
        if "spinmult" in d:
            mol.multiplicity = int(d.pop("spinmult"))
        match list(d["method"].lower().replace("revpbe", "------")):
            case ["r", "o", *_]:
                mol.closed, mol.restricted, d["method"] = False, True, d["method"][2:]
            case ["r", *_]:
                mol.closed, mol.restricted, d["method"] = True, True, d["method"][1:]
            case ["u", *_]:
                mol.closed, mol.restricted, d["method"] = True, False, d["method"][1:]
            case _:
                mol.closed, mol.restricted = True, True

        job.run = tcpb2._JOBINPUT_RUNTYPE.values_by_name[d.pop("run").upper()].number
        job.method = tcpb2._JOBINPUT_METHODTYPE.values_by_name[
            d.pop("method").upper()
        ].number
        job.basis = d.pop("basis")
        d = ChainMap(d, DEFAULT_OPTS)
        job.user_options[:] = list(chain.from_iterable(d.items()))

        return cls(job)

    def encode(self) -> bytes:
        return self.pb.SerializeToString()

    def with_mol(self, atmi=None, xyz=None, charge=None, multiplicity=None):
        mol = self.pb.mol
        if atmi is not None:
            mol.atoms[:] = atmi
        if xyz is not None:
            mol.xyz[:] = list(np.reshape(xyz, (-1,)))
        if charge is not None:
            mol.charge = charge
        if multiplicity is not None:
            mol.multiplicity = multiplicity
        return self

    def with_point_charge(self, xyz, charges):
        self.pb.qmmm_type = tcpb2._JOBINPUT_QMMMTYPE.values_by_name[
            "POINT_CHARGE"
        ].number
        self.pb.mmatom_position[:] = list(np.reshape(xyz, (-1,)))
        self.pb.mmatom_charge[:] = charges
        return self

    def with_openmm(self, xyz, prmtop, qm_indices):
        self.pb.qmmm_type = tcpb2._JOBINPUT_QMMMTYPE.values_by_name[
            "TC_OPENMM"
        ].number
        self.pb.mmatom_position[:] = list(np.reshape(xyz, (-1,)))
        self.pb.prmtop_path = str(prmtop)
        self.pb.qm_indices[:] = qm_indices
        return self


def read_tc_input(fname: str) -> dict[str, str]:
    d = {}
    with open(fname, "r") as f:
        for l in f:
            l = l.strip()
            if (cpos := l.find("#")) != -1:
                l = l[:cpos]
            if (cpos := l.find("!")) != -1:
                l = l[:cpos]
            if not l:
                continue
            k, v = l.split()
            if k in d:
                logger.warning(f"Duplicate input entry {l!r} is ignored")
                continue
            d[k] = v
    return d


def read_xyz(fname: str) -> tuple[list[str], "NDArray[(N,3), float]"]:
    with open(fname, "r") as xyzf:
        n = int(next(xyzf))
        _ = next(xyzf)
        fields = (l.split() for l in xyzf)
        atmi, geom = zip(*([f[0], [f[1], f[2], f[3]]] for f in fields))
    return atmi, np.array(geom, dtype=float)
