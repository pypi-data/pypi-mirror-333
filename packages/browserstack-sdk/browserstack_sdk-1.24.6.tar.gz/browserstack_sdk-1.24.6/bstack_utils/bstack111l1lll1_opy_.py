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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1l11l11llll_opy_, bstack1ll1ll111_opy_, get_host_info, bstack11lllll1l11_opy_, \
 bstack1ll11ll1l1_opy_, bstack1llllll111_opy_, bstack111lll1lll_opy_, bstack11lll11111l_opy_, bstack1lllll11ll_opy_
import bstack_utils.accessibility as bstack1111l1111_opy_
from bstack_utils.bstack11l11l1l1l_opy_ import bstack1ll11l1l1_opy_
from bstack_utils.percy import bstack111ll1l1l_opy_
from bstack_utils.config import Config
bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
logger = logging.getLogger(__name__)
percy = bstack111ll1l1l_opy_()
@bstack111lll1lll_opy_(class_method=False)
def bstack111lll1ll1l_opy_(bs_config, bstack1l1l1lll_opy_):
  try:
    data = {
        bstack11_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ᶸ"): bstack11_opy_ (u"ࠧ࡫ࡵࡲࡲࠬᶹ"),
        bstack11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧᶺ"): bs_config.get(bstack11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᶻ"), bstack11_opy_ (u"ࠪࠫᶼ")),
        bstack11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᶽ"): bs_config.get(bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᶾ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᶿ"): bs_config.get(bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᷀")),
        bstack11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᷁"): bs_config.get(bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲ᷂ࠬ"), bstack11_opy_ (u"ࠪࠫ᷃")),
        bstack11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᷄"): bstack1lllll11ll_opy_(),
        bstack11_opy_ (u"ࠬࡺࡡࡨࡵࠪ᷅"): bstack11lllll1l11_opy_(bs_config),
        bstack11_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩ᷆"): get_host_info(),
        bstack11_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ᷇"): bstack1ll1ll111_opy_(),
        bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᷈"): os.environ.get(bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ᷉")),
        bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ᷊"): os.environ.get(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ᷋"), False),
        bstack11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ᷌"): bstack1l11l11llll_opy_(),
        bstack11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᷍"): bstack111ll11llll_opy_(),
        bstack11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶ᷎ࠫ"): bstack111ll11l11l_opy_(bstack1l1l1lll_opy_),
        bstack11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ᷏࠭"): bstack1llllll11l_opy_(bs_config, bstack1l1l1lll_opy_.get(bstack11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦ᷐ࠪ"), bstack11_opy_ (u"ࠪࠫ᷑"))),
        bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᷒"): bstack1ll11ll1l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨᷓ").format(str(error)))
    return None
def bstack111ll11l11l_opy_(framework):
  return {
    bstack11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᷔ"): framework.get(bstack11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᷕ"), bstack11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᷖ")),
    bstack11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᷗ"): framework.get(bstack11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᷘ")),
    bstack11_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᷙ"): framework.get(bstack11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᷚ")),
    bstack11_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᷛ"): bstack11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᷜ"),
    bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᷝ"): framework.get(bstack11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᷞ"))
  }
def bstack1llllll11l_opy_(bs_config, framework):
  bstack1ll1111l1l_opy_ = False
  bstack1ll11l11_opy_ = False
  bstack111ll11l1l1_opy_ = False
  if bstack11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᷟ") in bs_config:
    bstack111ll11l1l1_opy_ = True
  elif bstack11_opy_ (u"ࠫࡦࡶࡰࠨᷠ") in bs_config:
    bstack1ll1111l1l_opy_ = True
  else:
    bstack1ll11l11_opy_ = True
  bstack11llll1l_opy_ = {
    bstack11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᷡ"): bstack1ll11l1l1_opy_.bstack111ll11ll1l_opy_(bs_config, framework),
    bstack11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᷢ"): bstack1111l1111_opy_.bstack1l11l1111l1_opy_(bs_config),
    bstack11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᷣ"): bs_config.get(bstack11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᷤ"), False),
    bstack11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᷥ"): bstack1ll11l11_opy_,
    bstack11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᷦ"): bstack1ll1111l1l_opy_,
    bstack11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᷧ"): bstack111ll11l1l1_opy_
  }
  return bstack11llll1l_opy_
@bstack111lll1lll_opy_(class_method=False)
def bstack111ll11llll_opy_():
  try:
    bstack111ll1l1111_opy_ = json.loads(os.getenv(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᷨ"), bstack11_opy_ (u"࠭ࡻࡾࠩᷩ")))
    return {
        bstack11_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᷪ"): bstack111ll1l1111_opy_
    }
  except Exception as error:
    logger.error(bstack11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢᷫ").format(str(error)))
    return {}
def bstack111ll1l1l11_opy_(array, bstack111ll1l11ll_opy_, bstack111ll1l111l_opy_):
  result = {}
  for o in array:
    key = o[bstack111ll1l11ll_opy_]
    result[key] = o[bstack111ll1l111l_opy_]
  return result
def bstack111ll1ll11l_opy_(bstack11llll111_opy_=bstack11_opy_ (u"ࠩࠪᷬ")):
  bstack111ll11lll1_opy_ = bstack1111l1111_opy_.on()
  bstack111ll11ll11_opy_ = bstack1ll11l1l1_opy_.on()
  bstack111ll1l11l1_opy_ = percy.bstack111ll11l_opy_()
  if bstack111ll1l11l1_opy_ and not bstack111ll11ll11_opy_ and not bstack111ll11lll1_opy_:
    return bstack11llll111_opy_ not in [bstack11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᷭ"), bstack11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᷮ")]
  elif bstack111ll11lll1_opy_ and not bstack111ll11ll11_opy_:
    return bstack11llll111_opy_ not in [bstack11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᷯ"), bstack11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᷰ"), bstack11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᷱ")]
  return bstack111ll11lll1_opy_ or bstack111ll11ll11_opy_ or bstack111ll1l11l1_opy_
@bstack111lll1lll_opy_(class_method=False)
def bstack111ll1lll1l_opy_(bstack11llll111_opy_, test=None):
  bstack111ll11l1ll_opy_ = bstack1111l1111_opy_.on()
  if not bstack111ll11l1ll_opy_ or bstack11llll111_opy_ not in [bstack11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᷲ")] or test == None:
    return None
  return {
    bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᷳ"): bstack111ll11l1ll_opy_ and bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᷴ"), None) == True and bstack1111l1111_opy_.bstack11ll1lllll_opy_(test[bstack11_opy_ (u"ࠫࡹࡧࡧࡴࠩ᷵")])
  }