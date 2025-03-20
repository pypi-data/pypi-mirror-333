# coding: UTF-8
import sys
bstack11lll_opy_ = sys.version_info [0] == 2
bstack1l_opy_ = 2048
bstack1l11lll_opy_ = 7
def bstack1l11l_opy_ (bstack11l11_opy_):
    global bstack111ll1_opy_
    bstack1111l1_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1ll1ll_opy_ = bstack11l11_opy_ [:-1]
    bstack1111111_opy_ = bstack1111l1_opy_ % len (bstack1ll1ll_opy_)
    bstack1lll_opy_ = bstack1ll1ll_opy_ [:bstack1111111_opy_] + bstack1ll1ll_opy_ [bstack1111111_opy_:]
    if bstack11lll_opy_:
        bstack1111ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l_opy_ - (bstack1ll1lll_opy_ + bstack1111l1_opy_) % bstack1l11lll_opy_) for bstack1ll1lll_opy_, char in enumerate (bstack1lll_opy_)])
    else:
        bstack1111ll1_opy_ = str () .join ([chr (ord (char) - bstack1l_opy_ - (bstack1ll1lll_opy_ + bstack1111l1_opy_) % bstack1l11lll_opy_) for bstack1ll1lll_opy_, char in enumerate (bstack1lll_opy_)])
    return eval (bstack1111ll1_opy_)
from browserstack_sdk.bstack1l1lllll11_opy_ import bstack1ll111ll_opy_
from browserstack_sdk.bstack111llll1ll_opy_ import RobotHandler
def bstack1lll1ll1l_opy_(framework):
    if framework.lower() == bstack1l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᢊ"):
        return bstack1ll111ll_opy_.version()
    elif framework.lower() == bstack1l11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᢋ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᢌ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11l_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᢍ")
def bstack1ll1l111_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l11l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᢎ"))
        framework_version.append(importlib.metadata.version(bstack1l11l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᢏ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l11l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᢐ"))
        framework_version.append(importlib.metadata.version(bstack1l11l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᢑ")))
    except:
        pass
    return {
        bstack1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᢒ"): bstack1l11l_opy_ (u"ࠬࡥࠧᢓ").join(framework_name),
        bstack1l11l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᢔ"): bstack1l11l_opy_ (u"ࠧࡠࠩᢕ").join(framework_version)
    }