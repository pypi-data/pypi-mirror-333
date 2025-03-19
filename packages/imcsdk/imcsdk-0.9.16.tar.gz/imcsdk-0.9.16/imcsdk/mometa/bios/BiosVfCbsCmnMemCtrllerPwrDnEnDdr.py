"""This module contains the general information for BiosVfCbsCmnMemCtrllerPwrDnEnDdr ManagedObject."""

from ...imcmo import ManagedObject
from ...imccoremeta import MoPropertyMeta, MoMeta
from ...imcmeta import VersionMeta


class BiosVfCbsCmnMemCtrllerPwrDnEnDdrConsts:
    VP_CBS_CMN_MEM_CTRLLER_PWR_DN_EN_DDR_AUTO = "Auto"
    VP_CBS_CMN_MEM_CTRLLER_PWR_DN_EN_DDR_DISABLED = "Disabled"
    VP_CBS_CMN_MEM_CTRLLER_PWR_DN_EN_DDR_ENABLED = "Enabled"
    _VP_CBS_CMN_MEM_CTRLLER_PWR_DN_EN_DDR_DISABLED = "disabled"
    _VP_CBS_CMN_MEM_CTRLLER_PWR_DN_EN_DDR_ENABLED = "enabled"
    VP_CBS_CMN_MEM_CTRLLER_PWR_DN_EN_DDR_PLATFORM_DEFAULT = "platform-default"


class BiosVfCbsCmnMemCtrllerPwrDnEnDdr(ManagedObject):
    """This is BiosVfCbsCmnMemCtrllerPwrDnEnDdr class."""

    consts = BiosVfCbsCmnMemCtrllerPwrDnEnDdrConsts()
    naming_props = set([])

    mo_meta = {
        "classic": MoMeta("BiosVfCbsCmnMemCtrllerPwrDnEnDdr", "biosVfCbsCmnMemCtrllerPwrDnEnDdr", "Power_Down_Enable", VersionMeta.Version434_240077, "InputOutput", 0x1f, [], ["admin"], ['biosPlatformDefaults', 'biosSettings'], [], [None]),
    }


    prop_meta = {

        "classic": {
            "child_action": MoPropertyMeta("child_action", "childAction", "string", VersionMeta.Version434_240077, MoPropertyMeta.INTERNAL, None, None, None, None, [], []),
            "dn": MoPropertyMeta("dn", "dn", "string", VersionMeta.Version434_240077, MoPropertyMeta.READ_WRITE, 0x2, 0, 255, None, [], []),
            "rn": MoPropertyMeta("rn", "rn", "string", VersionMeta.Version434_240077, MoPropertyMeta.READ_WRITE, 0x4, 0, 255, None, [], []),
            "status": MoPropertyMeta("status", "status", "string", VersionMeta.Version434_240077, MoPropertyMeta.READ_WRITE, 0x8, None, None, None, ["", "created", "deleted", "modified", "removed"], []),
            "vp_cbs_cmn_mem_ctrller_pwr_dn_en_ddr": MoPropertyMeta("vp_cbs_cmn_mem_ctrller_pwr_dn_en_ddr", "vpCbsCmnMemCtrllerPwrDnEnDdr", "string", VersionMeta.Version434_240077, MoPropertyMeta.READ_WRITE, 0x10, None, None, None, ["Auto", "Disabled", "Enabled", "disabled", "enabled", "platform-default"], []),
        },

    }

    prop_map = {

        "classic": {
            "childAction": "child_action", 
            "dn": "dn", 
            "rn": "rn", 
            "status": "status", 
            "vpCbsCmnMemCtrllerPwrDnEnDdr": "vp_cbs_cmn_mem_ctrller_pwr_dn_en_ddr", 
        },

    }

    def __init__(self, parent_mo_or_dn, **kwargs):
        self._dirty_mask = 0
        self.child_action = None
        self.status = None
        self.vp_cbs_cmn_mem_ctrller_pwr_dn_en_ddr = None

        ManagedObject.__init__(self, "BiosVfCbsCmnMemCtrllerPwrDnEnDdr", parent_mo_or_dn, **kwargs)

