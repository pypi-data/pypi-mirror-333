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
import threading
import logging
import bstack_utils.accessibility as bstack11lll111l_opy_
from bstack_utils.helper import bstack1llll1llll_opy_
logger = logging.getLogger(__name__)
def bstack111111l1l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1111l11ll_opy_(context, *args):
    tags = getattr(args[0], bstack1l11l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᕏ"), [])
    bstack1ll1l1lll_opy_ = bstack11lll111l_opy_.bstack1l1111l111_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll1l1lll_opy_
    try:
      bstack11llllll11_opy_ = threading.current_thread().bstackSessionDriver if bstack111111l1l_opy_(bstack1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᕐ")) else context.browser
      if bstack11llllll11_opy_ and bstack11llllll11_opy_.session_id and bstack1ll1l1lll_opy_ and bstack1llll1llll_opy_(
              threading.current_thread(), bstack1l11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᕑ"), None):
          threading.current_thread().isA11yTest = bstack11lll111l_opy_.bstack11ll1111l_opy_(bstack11llllll11_opy_, bstack1ll1l1lll_opy_)
    except Exception as e:
       logger.debug(bstack1l11l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡢ࠳࠴ࡽࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬᕒ").format(str(e)))
def bstack1l1lllll1_opy_(bstack11llllll11_opy_):
    if bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᕓ"), None) and bstack1llll1llll_opy_(
      threading.current_thread(), bstack1l11l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᕔ"), None) and not bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࠫᕕ"), False):
      threading.current_thread().a11y_stop = True
      bstack11lll111l_opy_.bstack1l11l1l1_opy_(bstack11llllll11_opy_, name=bstack1l11l_opy_ (u"ࠤࠥᕖ"), path=bstack1l11l_opy_ (u"ࠥࠦᕗ"))