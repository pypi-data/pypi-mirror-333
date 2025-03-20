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
import os
import threading
from bstack_utils.helper import bstack11l1l1l11_opy_
from bstack_utils.constants import bstack1l1111ll1l1_opy_, EVENTS, STAGE
from bstack_utils.bstack11l11l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack1ll11l1l1_opy_:
    bstack11l1111llll_opy_ = None
    @classmethod
    def bstack1l11lll1_opy_(cls):
        if cls.on() and os.getenv(bstack11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ᷶")):
            logger.info(
                bstack11_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯᷷ࠩ").format(os.getenv(bstack11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᷸ࠧ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘ᷹ࠬ"), None) is None or os.environ[bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ᷺࡛࡙࠭")] == bstack11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ᷻"):
            return False
        return True
    @classmethod
    def bstack111ll11ll1l_opy_(cls, bs_config, framework=bstack11_opy_ (u"ࠦࠧ᷼")):
        bstack1l111l1ll11_opy_ = False
        for fw in bstack1l1111ll1l1_opy_:
            if fw in framework:
                bstack1l111l1ll11_opy_ = True
        return bstack11l1l1l11_opy_(bs_config.get(bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ᷽ࠩ"), bstack1l111l1ll11_opy_))
    @classmethod
    def bstack111ll111l1l_opy_(cls, framework):
        return framework in bstack1l1111ll1l1_opy_
    @classmethod
    def bstack111ll1lll11_opy_(cls, bs_config, framework):
        return cls.bstack111ll11ll1l_opy_(bs_config, framework) is True and cls.bstack111ll111l1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ᷾"), None)
    @staticmethod
    def bstack11l11llll1_opy_():
        if getattr(threading.current_thread(), bstack11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧ᷿ࠫ"), None):
            return {
                bstack11_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ḁ"): bstack11_opy_ (u"ࠩࡷࡩࡸࡺࠧḁ"),
                bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪḂ"): getattr(threading.current_thread(), bstack11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨḃ"), None)
            }
        if getattr(threading.current_thread(), bstack11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩḄ"), None):
            return {
                bstack11_opy_ (u"࠭ࡴࡺࡲࡨࠫḅ"): bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬḆ"),
                bstack11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨḇ"): getattr(threading.current_thread(), bstack11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭Ḉ"), None)
            }
        return None
    @staticmethod
    def bstack111ll11l111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll11l1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l11111l1_opy_(test, hook_name=None):
        bstack111ll111ll1_opy_ = test.parent
        if hook_name in [bstack11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨḉ"), bstack11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬḊ"), bstack11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫḋ"), bstack11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨḌ")]:
            bstack111ll111ll1_opy_ = test
        scope = []
        while bstack111ll111ll1_opy_ is not None:
            scope.append(bstack111ll111ll1_opy_.name)
            bstack111ll111ll1_opy_ = bstack111ll111ll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack111ll111lll_opy_(hook_type):
        if hook_type == bstack11_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧḍ"):
            return bstack11_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧḎ")
        elif hook_type == bstack11_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨḏ"):
            return bstack11_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥḐ")
    @staticmethod
    def bstack111ll111l11_opy_(bstack1lllll1l11_opy_):
        try:
            if not bstack1ll11l1l1_opy_.on():
                return bstack1lllll1l11_opy_
            if os.environ.get(bstack11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤḑ"), None) == bstack11_opy_ (u"ࠧࡺࡲࡶࡧࠥḒ"):
                tests = os.environ.get(bstack11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥḓ"), None)
                if tests is None or tests == bstack11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧḔ"):
                    return bstack1lllll1l11_opy_
                bstack1lllll1l11_opy_ = tests.split(bstack11_opy_ (u"ࠨ࠮ࠪḕ"))
                return bstack1lllll1l11_opy_
        except Exception as exc:
            logger.debug(bstack11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥḖ") + str(str(exc)) + bstack11_opy_ (u"ࠥࠦḗ"))
        return bstack1lllll1l11_opy_