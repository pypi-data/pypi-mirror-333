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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11llll1lll1_opy_, bstack1l1ll1ll_opy_, bstack1llll1llll_opy_, bstack1ll111ll1l_opy_, \
    bstack11ll1lll111_opy_
from bstack_utils.measure import measure
def bstack1l1l1lll11_opy_(bstack11l111111l1_opy_):
    for driver in bstack11l111111l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1l111l_opy_, stage=STAGE.bstack1111111l_opy_)
def bstack1ll1ll1lll_opy_(driver, status, reason=bstack1l11l_opy_ (u"ࠫࠬ᱊")):
    bstack1ll11111ll_opy_ = Config.bstack111lll11_opy_()
    if bstack1ll11111ll_opy_.bstack111l1l1l1l_opy_():
        return
    bstack1l11l1l11_opy_ = bstack1l1lll1111_opy_(bstack1l11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ᱋"), bstack1l11l_opy_ (u"࠭ࠧ᱌"), status, reason, bstack1l11l_opy_ (u"ࠧࠨᱍ"), bstack1l11l_opy_ (u"ࠨࠩᱎ"))
    driver.execute_script(bstack1l11l1l11_opy_)
@measure(event_name=EVENTS.bstack11ll1l111l_opy_, stage=STAGE.bstack1111111l_opy_)
def bstack111ll11l_opy_(page, status, reason=bstack1l11l_opy_ (u"ࠩࠪᱏ")):
    try:
        if page is None:
            return
        bstack1ll11111ll_opy_ = Config.bstack111lll11_opy_()
        if bstack1ll11111ll_opy_.bstack111l1l1l1l_opy_():
            return
        bstack1l11l1l11_opy_ = bstack1l1lll1111_opy_(bstack1l11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭᱐"), bstack1l11l_opy_ (u"ࠫࠬ᱑"), status, reason, bstack1l11l_opy_ (u"ࠬ࠭᱒"), bstack1l11l_opy_ (u"࠭ࠧ᱓"))
        page.evaluate(bstack1l11l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ᱔"), bstack1l11l1l11_opy_)
    except Exception as e:
        print(bstack1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡿࢂࠨ᱕"), e)
def bstack1l1lll1111_opy_(type, name, status, reason, bstack11llll111l_opy_, bstack1llllll1l_opy_):
    bstack11lll111_opy_ = {
        bstack1l11l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ᱖"): type,
        bstack1l11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᱗"): {}
    }
    if type == bstack1l11l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭᱘"):
        bstack11lll111_opy_[bstack1l11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ᱙")][bstack1l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᱚ")] = bstack11llll111l_opy_
        bstack11lll111_opy_[bstack1l11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᱛ")][bstack1l11l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᱜ")] = json.dumps(str(bstack1llllll1l_opy_))
    if type == bstack1l11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᱝ"):
        bstack11lll111_opy_[bstack1l11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᱞ")][bstack1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᱟ")] = name
    if type == bstack1l11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᱠ"):
        bstack11lll111_opy_[bstack1l11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᱡ")][bstack1l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᱢ")] = status
        if status == bstack1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᱣ") and str(reason) != bstack1l11l_opy_ (u"ࠤࠥᱤ"):
            bstack11lll111_opy_[bstack1l11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᱥ")][bstack1l11l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᱦ")] = json.dumps(str(reason))
    bstack1lll1ll11l_opy_ = bstack1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪᱧ").format(json.dumps(bstack11lll111_opy_))
    return bstack1lll1ll11l_opy_
def bstack1l11l111ll_opy_(url, config, logger, bstack1l1ll11ll1_opy_=False):
    hostname = bstack1l1ll1ll_opy_(url)
    is_private = bstack1ll111ll1l_opy_(hostname)
    try:
        if is_private or bstack1l1ll11ll1_opy_:
            file_path = bstack11llll1lll1_opy_(bstack1l11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᱨ"), bstack1l11l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᱩ"), logger)
            if os.environ.get(bstack1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᱪ")) and eval(
                    os.environ.get(bstack1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᱫ"))):
                return
            if (bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᱬ") in config and not config[bstack1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᱭ")]):
                os.environ[bstack1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᱮ")] = str(True)
                bstack11l111111ll_opy_ = {bstack1l11l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨᱯ"): hostname}
                bstack11ll1lll111_opy_(bstack1l11l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᱰ"), bstack1l11l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ᱱ"), bstack11l111111ll_opy_, logger)
    except Exception as e:
        pass
def bstack1l11lll1ll_opy_(caps, bstack11l11111l11_opy_):
    if bstack1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᱲ") in caps:
        caps[bstack1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᱳ")][bstack1l11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪᱴ")] = True
        if bstack11l11111l11_opy_:
            caps[bstack1l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᱵ")][bstack1l11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᱶ")] = bstack11l11111l11_opy_
    else:
        caps[bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬᱷ")] = True
        if bstack11l11111l11_opy_:
            caps[bstack1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᱸ")] = bstack11l11111l11_opy_
def bstack11l111ll1ll_opy_(bstack11l111ll1l_opy_):
    bstack11l11111l1l_opy_ = bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᱹ"), bstack1l11l_opy_ (u"ࠪࠫᱺ"))
    if bstack11l11111l1l_opy_ == bstack1l11l_opy_ (u"ࠫࠬᱻ") or bstack11l11111l1l_opy_ == bstack1l11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᱼ"):
        threading.current_thread().testStatus = bstack11l111ll1l_opy_
    else:
        if bstack11l111ll1l_opy_ == bstack1l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᱽ"):
            threading.current_thread().testStatus = bstack11l111ll1l_opy_