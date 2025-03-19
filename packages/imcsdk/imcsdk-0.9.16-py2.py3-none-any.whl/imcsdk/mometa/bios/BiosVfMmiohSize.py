"""This module contains the general information for BiosVfMmiohSize ManagedObject."""

from ...imcmo import ManagedObject
from ...imccoremeta import MoPropertyMeta, MoMeta
from ...imcmeta import VersionMeta


class BiosVfMmiohSizeConsts:
    VP_MMIOH_SIZE_1024_G = "1024G"
    VP_MMIOH_SIZE_16_G = "16G"
    VP_MMIOH_SIZE_1_G = "1G"
    VP_MMIOH_SIZE_256_G = "256G"
    VP_MMIOH_SIZE_4_G = "4G"
    VP_MMIOH_SIZE_64_G = "64G"
    VP_MMIOH_SIZE_PLATFORM_DEFAULT = "platform-default"


class BiosVfMmiohSize(ManagedObject):
    """This is BiosVfMmiohSize class."""

    consts = BiosVfMmiohSizeConsts()
    naming_props = set([])

    mo_meta = {
        "classic": MoMeta("BiosVfMmiohSize", "biosVfMmiohSize", "MMIO-High-Granularity-Size", VersionMeta.Version433_240024, "InputOutput", 0x1f, [], ["admin"], ['biosPlatformDefaults', 'biosSettings'], [], [None]),
    }


    prop_meta = {

        "classic": {
            "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version433_240024, MoPropertyMeta.INTERNAL, None, None, None, None, [], []),
            "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version433_240024, MoPropertyMeta.READ_WRITE, 0x2, 0, 255, None, [], []),
            "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version433_240024, MoPropertyMeta.READ_WRITE, 0x4, 0, 255, None, [], []),
            "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version433_240024, MoPropertyMeta.READ_WRITE, 0x8, None, None, None, ["", "created", "deleted", "modified", "removed"], []),
            "vp_mmioh_size": MoPropertyMeta("vp_mmioh_size", "vpMmiohSize", "string", VersionMeta.Version433_240024, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["1024G", "16G", "1G", "256G", "4G", "64G", "platform-default"], []),
        },

    }

    prop_map = {

        "classic": {
            "childAction": "child_action", 
            "dn": "dn", 
            "rn": "rn", 
            "status": "status", 
            "vpMmiohSize": "vp_mmioh_size", 
        },

    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.child_action = None
        self.status = None
        self.vp_mmioh_size = None

        ManagedObject.__init__(self, "BiosVfMmiohSize", parent_mo_or_dn, **kwargs)

