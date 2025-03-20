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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1l11111111l_opy_, bstack1111111l1_opy_, bstack1llllll111_opy_, bstack11lll11l1_opy_, \
    bstack11lll1lll1l_opy_
from bstack_utils.measure import measure
def bstack11lll1l1l1_opy_(bstack11l111111ll_opy_):
    for driver in bstack11l111111ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l111111ll_opy_, stage=STAGE.bstack1lll11111l_opy_)
def bstack1l111l111_opy_(driver, status, reason=bstack11_opy_ (u"ࠬ࠭᱋")):
    bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
    if bstack1l1l1lll1_opy_.bstack111l1lll11_opy_():
        return
    bstack1lll11l1_opy_ = bstack1l1ll1llll_opy_(bstack11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ᱌"), bstack11_opy_ (u"ࠧࠨᱍ"), status, reason, bstack11_opy_ (u"ࠨࠩᱎ"), bstack11_opy_ (u"ࠩࠪᱏ"))
    driver.execute_script(bstack1lll11l1_opy_)
@measure(event_name=EVENTS.bstack1l111111ll_opy_, stage=STAGE.bstack1lll11111l_opy_)
def bstack1ll11ll1ll_opy_(page, status, reason=bstack11_opy_ (u"ࠪࠫ᱐")):
    try:
        if page is None:
            return
        bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
        if bstack1l1l1lll1_opy_.bstack111l1lll11_opy_():
            return
        bstack1lll11l1_opy_ = bstack1l1ll1llll_opy_(bstack11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ᱑"), bstack11_opy_ (u"ࠬ࠭᱒"), status, reason, bstack11_opy_ (u"࠭ࠧ᱓"), bstack11_opy_ (u"ࠧࠨ᱔"))
        page.evaluate(bstack11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ᱕"), bstack1lll11l1_opy_)
    except Exception as e:
        print(bstack11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ᱖"), e)
def bstack1l1ll1llll_opy_(type, name, status, reason, bstack11ll11l1ll_opy_, bstack1l1lll1l_opy_):
    bstack1ll1ll1lll_opy_ = {
        bstack11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ᱗"): type,
        bstack11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᱘"): {}
    }
    if type == bstack11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ᱙"):
        bstack1ll1ll1lll_opy_[bstack11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᱚ")][bstack11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᱛ")] = bstack11ll11l1ll_opy_
        bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᱜ")][bstack11_opy_ (u"ࠩࡧࡥࡹࡧࠧᱝ")] = json.dumps(str(bstack1l1lll1l_opy_))
    if type == bstack11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᱞ"):
        bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᱟ")][bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᱠ")] = name
    if type == bstack11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᱡ"):
        bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᱢ")][bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᱣ")] = status
        if status == bstack11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᱤ") and str(reason) != bstack11_opy_ (u"ࠥࠦᱥ"):
            bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᱦ")][bstack11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᱧ")] = json.dumps(str(reason))
    bstack1lll1l11l1_opy_ = bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᱨ").format(json.dumps(bstack1ll1ll1lll_opy_))
    return bstack1lll1l11l1_opy_
def bstack11l1lll1l_opy_(url, config, logger, bstack11l1lll1l1_opy_=False):
    hostname = bstack1111111l1_opy_(url)
    is_private = bstack11lll11l1_opy_(hostname)
    try:
        if is_private or bstack11l1lll1l1_opy_:
            file_path = bstack1l11111111l_opy_(bstack11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᱩ"), bstack11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᱪ"), logger)
            if os.environ.get(bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᱫ")) and eval(
                    os.environ.get(bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᱬ"))):
                return
            if (bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᱭ") in config and not config[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᱮ")]):
                os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᱯ")] = str(True)
                bstack11l111111l1_opy_ = {bstack11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᱰ"): hostname}
                bstack11lll1lll1l_opy_(bstack11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᱱ"), bstack11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᱲ"), bstack11l111111l1_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l1ll1l_opy_(caps, bstack11l11111l11_opy_):
    if bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᱳ") in caps:
        caps[bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᱴ")][bstack11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᱵ")] = True
        if bstack11l11111l11_opy_:
            caps[bstack11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᱶ")][bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᱷ")] = bstack11l11111l11_opy_
    else:
        caps[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᱸ")] = True
        if bstack11l11111l11_opy_:
            caps[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᱹ")] = bstack11l11111l11_opy_
def bstack11l11l11111_opy_(bstack111llllll1_opy_):
    bstack11l11111l1l_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᱺ"), bstack11_opy_ (u"ࠫࠬᱻ"))
    if bstack11l11111l1l_opy_ == bstack11_opy_ (u"ࠬ࠭ᱼ") or bstack11l11111l1l_opy_ == bstack11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᱽ"):
        threading.current_thread().testStatus = bstack111llllll1_opy_
    else:
        if bstack111llllll1_opy_ == bstack11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᱾"):
            threading.current_thread().testStatus = bstack111llllll1_opy_