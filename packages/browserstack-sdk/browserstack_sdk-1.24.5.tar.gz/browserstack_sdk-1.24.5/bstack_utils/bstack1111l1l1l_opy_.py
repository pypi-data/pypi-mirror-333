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
import re
from bstack_utils.bstack11l11111l_opy_ import bstack11l111ll1ll_opy_
def bstack11l111llll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰐ")):
        return bstack1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᰑ")
    elif fixture_name.startswith(bstack1l11l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰒ")):
        return bstack1l11l_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᰓ")
    elif fixture_name.startswith(bstack1l11l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰔ")):
        return bstack1l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᰕ")
    elif fixture_name.startswith(bstack1l11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᰖ")):
        return bstack1l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᰗ")
def bstack11l111lll1l_opy_(fixture_name):
    return bool(re.match(bstack1l11l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᰘ"), fixture_name))
def bstack11l111ll111_opy_(fixture_name):
    return bool(re.match(bstack1l11l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᰙ"), fixture_name))
def bstack11l111lll11_opy_(fixture_name):
    return bool(re.match(bstack1l11l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᰚ"), fixture_name))
def bstack11l11l1111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᰛ")):
        return bstack1l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᰜ"), bstack1l11l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᰝ")
    elif fixture_name.startswith(bstack1l11l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᰞ")):
        return bstack1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᰟ"), bstack1l11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᰠ")
    elif fixture_name.startswith(bstack1l11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᰡ")):
        return bstack1l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᰢ"), bstack1l11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᰣ")
    elif fixture_name.startswith(bstack1l11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰤ")):
        return bstack1l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᰥ"), bstack1l11l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᰦ")
    return None, None
def bstack11l111ll11l_opy_(hook_name):
    if hook_name in [bstack1l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᰧ"), bstack1l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᰨ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11l111l1lll_opy_(hook_name):
    if hook_name in [bstack1l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᰩ"), bstack1l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᰪ")]:
        return bstack1l11l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᰫ")
    elif hook_name in [bstack1l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᰬ"), bstack1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᰭ")]:
        return bstack1l11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᰮ")
    elif hook_name in [bstack1l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᰯ"), bstack1l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᰰ")]:
        return bstack1l11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᰱ")
    elif hook_name in [bstack1l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᰲ"), bstack1l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᰳ")]:
        return bstack1l11l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᰴ")
    return hook_name
def bstack11l111l1ll1_opy_(node, scenario):
    if hasattr(node, bstack1l11l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᰵ")):
        parts = node.nodeid.rsplit(bstack1l11l_opy_ (u"ࠧࡡࠢᰶ"))
        params = parts[-1]
        return bstack1l11l_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨ᰷").format(scenario.name, params)
    return scenario.name
def bstack11l111l1l1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l11l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩ᰸")):
            examples = list(node.callspec.params[bstack1l11l_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧ᰹")].values())
        return examples
    except:
        return []
def bstack11l11l111l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l11l11111_opy_(report):
    try:
        status = bstack1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᰺")
        if report.passed or (report.failed and hasattr(report, bstack1l11l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ᰻"))):
            status = bstack1l11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᰼")
        elif report.skipped:
            status = bstack1l11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᰽")
        bstack11l111ll1ll_opy_(status)
    except:
        pass
def bstack1l111l1lll_opy_(status):
    try:
        bstack11l111ll1l1_opy_ = bstack1l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᰾")
        if status == bstack1l11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᰿"):
            bstack11l111ll1l1_opy_ = bstack1l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᱀")
        elif status == bstack1l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ᱁"):
            bstack11l111ll1l1_opy_ = bstack1l11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᱂")
        bstack11l111ll1ll_opy_(bstack11l111ll1l1_opy_)
    except:
        pass
def bstack11l111lllll_opy_(item=None, report=None, summary=None, extra=None):
    return