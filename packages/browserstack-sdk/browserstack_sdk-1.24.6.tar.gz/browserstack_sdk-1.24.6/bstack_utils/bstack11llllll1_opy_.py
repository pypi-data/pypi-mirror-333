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
import threading
import logging
import bstack_utils.accessibility as bstack1111l1111_opy_
from bstack_utils.helper import bstack1llllll111_opy_
logger = logging.getLogger(__name__)
def bstack1l1l1l111l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack111ll111_opy_(context, *args):
    tags = getattr(args[0], bstack11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᕐ"), [])
    bstack11l1lllll1_opy_ = bstack1111l1111_opy_.bstack11ll1lllll_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l1lllll1_opy_
    try:
      bstack11l1ll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l111l_opy_(bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᕑ")) else context.browser
      if bstack11l1ll1111_opy_ and bstack11l1ll1111_opy_.session_id and bstack11l1lllll1_opy_ and bstack1llllll111_opy_(
              threading.current_thread(), bstack11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᕒ"), None):
          threading.current_thread().isA11yTest = bstack1111l1111_opy_.bstack1111ll111_opy_(bstack11l1ll1111_opy_, bstack11l1lllll1_opy_)
    except Exception as e:
       logger.debug(bstack11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᕓ").format(str(e)))
def bstack11lll111l1_opy_(bstack11l1ll1111_opy_):
    if bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᕔ"), None) and bstack1llllll111_opy_(
      threading.current_thread(), bstack11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᕕ"), None) and not bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᕖ"), False):
      threading.current_thread().a11y_stop = True
      bstack1111l1111_opy_.bstack1l1llll1l_opy_(bstack11l1ll1111_opy_, name=bstack11_opy_ (u"ࠥࠦᕗ"), path=bstack11_opy_ (u"ࠦࠧᕘ"))