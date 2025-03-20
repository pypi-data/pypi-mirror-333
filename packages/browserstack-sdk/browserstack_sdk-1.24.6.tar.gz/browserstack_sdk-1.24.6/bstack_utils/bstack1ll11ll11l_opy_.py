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
import re
from bstack_utils.bstack1l111l11ll_opy_ import bstack11l11l11111_opy_
def bstack11l111l1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᰑ")):
        return bstack11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᰒ")
    elif fixture_name.startswith(bstack11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᰓ")):
        return bstack11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᰔ")
    elif fixture_name.startswith(bstack11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᰕ")):
        return bstack11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᰖ")
    elif fixture_name.startswith(bstack11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᰗ")):
        return bstack11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᰘ")
def bstack11l111lllll_opy_(fixture_name):
    return bool(re.match(bstack11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᰙ"), fixture_name))
def bstack11l111ll1ll_opy_(fixture_name):
    return bool(re.match(bstack11_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᰚ"), fixture_name))
def bstack11l11l111l1_opy_(fixture_name):
    return bool(re.match(bstack11_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᰛ"), fixture_name))
def bstack11l111lll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᰜ")):
        return bstack11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᰝ"), bstack11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᰞ")
    elif fixture_name.startswith(bstack11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᰟ")):
        return bstack11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᰠ"), bstack11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᰡ")
    elif fixture_name.startswith(bstack11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰢ")):
        return bstack11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᰣ"), bstack11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᰤ")
    elif fixture_name.startswith(bstack11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᰥ")):
        return bstack11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᰦ"), bstack11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᰧ")
    return None, None
def bstack11l111llll1_opy_(hook_name):
    if hook_name in [bstack11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᰨ"), bstack11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᰩ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11l111l1ll1_opy_(hook_name):
    if hook_name in [bstack11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᰪ"), bstack11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᰫ")]:
        return bstack11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᰬ")
    elif hook_name in [bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᰭ"), bstack11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᰮ")]:
        return bstack11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᰯ")
    elif hook_name in [bstack11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᰰ"), bstack11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᰱ")]:
        return bstack11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᰲ")
    elif hook_name in [bstack11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᰳ"), bstack11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᰴ")]:
        return bstack11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᰵ")
    return hook_name
def bstack11l11l1111l_opy_(node, scenario):
    if hasattr(node, bstack11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᰶ")):
        parts = node.nodeid.rsplit(bstack11_opy_ (u"ࠨ᰷࡛ࠣ"))
        params = parts[-1]
        return bstack11_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢ᰸").format(scenario.name, params)
    return scenario.name
def bstack11l111ll11l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ᰹")):
            examples = list(node.callspec.params[bstack11_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨ᰺")].values())
        return examples
    except:
        return []
def bstack11l111lll11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l111l1l1l_opy_(report):
    try:
        status = bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᰻")
        if report.passed or (report.failed and hasattr(report, bstack11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ᰼"))):
            status = bstack11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᰽")
        elif report.skipped:
            status = bstack11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᰾")
        bstack11l11l11111_opy_(status)
    except:
        pass
def bstack11lll1llll_opy_(status):
    try:
        bstack11l111ll111_opy_ = bstack11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᰿")
        if status == bstack11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᱀"):
            bstack11l111ll111_opy_ = bstack11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᱁")
        elif status == bstack11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᱂"):
            bstack11l111ll111_opy_ = bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ᱃")
        bstack11l11l11111_opy_(bstack11l111ll111_opy_)
    except:
        pass
def bstack11l111ll1l1_opy_(item=None, report=None, summary=None, extra=None):
    return