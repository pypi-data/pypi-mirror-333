# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack1l11_opy_ = 2048
bstack111l_opy_ = 7
def bstack11_opy_ (bstack111_opy_):
    global bstack111ll1l_opy_
    bstack1llll1l_opy_ = ord (bstack111_opy_ [-1])
    bstack11ll1ll_opy_ = bstack111_opy_ [:-1]
    bstack11l1l1_opy_ = bstack1llll1l_opy_ % len (bstack11ll1ll_opy_)
    bstack111111_opy_ = bstack11ll1ll_opy_ [:bstack11l1l1_opy_] + bstack11ll1ll_opy_ [bstack11l1l1_opy_:]
    if bstack11ll1l1_opy_:
        bstack1ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11_opy_ - (bstack11l1lll_opy_ + bstack1llll1l_opy_) % bstack111l_opy_) for bstack11l1lll_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1ll111_opy_ = str () .join ([chr (ord (char) - bstack1l11_opy_ - (bstack11l1lll_opy_ + bstack1llll1l_opy_) % bstack111l_opy_) for bstack11l1lll_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1ll111_opy_)
from browserstack_sdk.bstack1l1111lll1_opy_ import bstack11l11l1ll_opy_
from browserstack_sdk.bstack111lllllll_opy_ import RobotHandler
def bstack11111l1l_opy_(framework):
    if framework.lower() == bstack11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᢋ"):
        return bstack11l11l1ll_opy_.version()
    elif framework.lower() == bstack11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᢌ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᢍ"):
        import behave
        return behave.__version__
    else:
        return bstack11_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᢎ")
def bstack111l11l11_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᢏ"))
        framework_version.append(importlib.metadata.version(bstack11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᢐ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᢑ"))
        framework_version.append(importlib.metadata.version(bstack11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᢒ")))
    except:
        pass
    return {
        bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢓ"): bstack11_opy_ (u"࠭࡟ࠨᢔ").join(framework_name),
        bstack11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᢕ"): bstack11_opy_ (u"ࠨࡡࠪᢖ").join(framework_version)
    }