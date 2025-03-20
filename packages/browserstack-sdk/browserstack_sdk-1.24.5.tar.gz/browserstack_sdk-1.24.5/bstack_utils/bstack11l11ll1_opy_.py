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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1l11l111lll_opy_, bstack1l11111l1_opy_, get_host_info, bstack11ll1l1l11l_opy_, \
 bstack1l111111ll_opy_, bstack1llll1llll_opy_, bstack111llll1l1_opy_, bstack11lllll111l_opy_, bstack111ll1l1l_opy_
import bstack_utils.accessibility as bstack11lll111l_opy_
from bstack_utils.bstack11l11l1ll1_opy_ import bstack11l1llllll_opy_
from bstack_utils.percy import bstack1lll111lll_opy_
from bstack_utils.config import Config
bstack1ll11111ll_opy_ = Config.bstack111lll11_opy_()
logger = logging.getLogger(__name__)
percy = bstack1lll111lll_opy_()
@bstack111llll1l1_opy_(class_method=False)
def bstack111ll1l1lll_opy_(bs_config, bstack1l11l11lll_opy_):
  try:
    data = {
        bstack1l11l_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᶷ"): bstack1l11l_opy_ (u"࠭ࡪࡴࡱࡱࠫᶸ"),
        bstack1l11l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᶹ"): bs_config.get(bstack1l11l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᶺ"), bstack1l11l_opy_ (u"ࠩࠪᶻ")),
        bstack1l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨᶼ"): bs_config.get(bstack1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᶽ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᶾ"): bs_config.get(bstack1l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᶿ")),
        bstack1l11l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ᷀"): bs_config.get(bstack1l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᷁"), bstack1l11l_opy_ (u"᷂ࠩࠪ")),
        bstack1l11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᷃"): bstack111ll1l1l_opy_(),
        bstack1l11l_opy_ (u"ࠫࡹࡧࡧࡴࠩ᷄"): bstack11ll1l1l11l_opy_(bs_config),
        bstack1l11l_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨ᷅"): get_host_info(),
        bstack1l11l_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ᷆"): bstack1l11111l1_opy_(),
        bstack1l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᷇"): os.environ.get(bstack1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᷈")),
        bstack1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧ᷉"): os.environ.get(bstack1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ᷊"), False),
        bstack1l11l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭᷋"): bstack1l11l111lll_opy_(),
        bstack1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᷌"): bstack111ll11lll1_opy_(),
        bstack1l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ᷍"): bstack111ll1l11l1_opy_(bstack1l11l11lll_opy_),
        bstack1l11l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴ᷎ࠬ"): bstack1l1l1l1ll1_opy_(bs_config, bstack1l11l11lll_opy_.get(bstack1l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥ᷏ࠩ"), bstack1l11l_opy_ (u"᷐ࠩࠪ"))),
        bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᷑"): bstack1l111111ll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ᷒").format(str(error)))
    return None
def bstack111ll1l11l1_opy_(framework):
  return {
    bstack1l11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᷓ"): framework.get(bstack1l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧᷔ"), bstack1l11l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᷕ")),
    bstack1l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᷖ"): framework.get(bstack1l11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᷗ")),
    bstack1l11l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᷘ"): framework.get(bstack1l11l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᷙ")),
    bstack1l11l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᷚ"): bstack1l11l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᷛ"),
    bstack1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᷜ"): framework.get(bstack1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᷝ"))
  }
def bstack1l1l1l1ll1_opy_(bs_config, framework):
  bstack1ll1ll1l1l_opy_ = False
  bstack1111l1111_opy_ = False
  bstack111ll1l1111_opy_ = False
  if bstack1l11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᷞ") in bs_config:
    bstack111ll1l1111_opy_ = True
  elif bstack1l11l_opy_ (u"ࠪࡥࡵࡶࠧᷟ") in bs_config:
    bstack1ll1ll1l1l_opy_ = True
  else:
    bstack1111l1111_opy_ = True
  bstack1111l1lll_opy_ = {
    bstack1l11l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᷠ"): bstack11l1llllll_opy_.bstack111ll11llll_opy_(bs_config, framework),
    bstack1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᷡ"): bstack11lll111l_opy_.bstack1l11l1111l1_opy_(bs_config),
    bstack1l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᷢ"): bs_config.get(bstack1l11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᷣ"), False),
    bstack1l11l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᷤ"): bstack1111l1111_opy_,
    bstack1l11l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᷥ"): bstack1ll1ll1l1l_opy_,
    bstack1l11l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᷦ"): bstack111ll1l1111_opy_
  }
  return bstack1111l1lll_opy_
@bstack111llll1l1_opy_(class_method=False)
def bstack111ll11lll1_opy_():
  try:
    bstack111ll11ll1l_opy_ = json.loads(os.getenv(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᷧ"), bstack1l11l_opy_ (u"ࠬࢁࡽࠨᷨ")))
    return {
        bstack1l11l_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᷩ"): bstack111ll11ll1l_opy_
    }
  except Exception as error:
    logger.error(bstack1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨᷪ").format(str(error)))
    return {}
def bstack111lll1lll1_opy_(array, bstack111ll11l1l1_opy_, bstack111ll1l111l_opy_):
  result = {}
  for o in array:
    key = o[bstack111ll11l1l1_opy_]
    result[key] = o[bstack111ll1l111l_opy_]
  return result
def bstack111ll1ll111_opy_(bstack11ll111lll_opy_=bstack1l11l_opy_ (u"ࠨࠩᷫ")):
  bstack111ll11l11l_opy_ = bstack11lll111l_opy_.on()
  bstack111ll1l11ll_opy_ = bstack11l1llllll_opy_.on()
  bstack111ll11l1ll_opy_ = percy.bstack1ll11lll_opy_()
  if bstack111ll11l1ll_opy_ and not bstack111ll1l11ll_opy_ and not bstack111ll11l11l_opy_:
    return bstack11ll111lll_opy_ not in [bstack1l11l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᷬ"), bstack1l11l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᷭ")]
  elif bstack111ll11l11l_opy_ and not bstack111ll1l11ll_opy_:
    return bstack11ll111lll_opy_ not in [bstack1l11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᷮ"), bstack1l11l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᷯ"), bstack1l11l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᷰ")]
  return bstack111ll11l11l_opy_ or bstack111ll1l11ll_opy_ or bstack111ll11l1ll_opy_
@bstack111llll1l1_opy_(class_method=False)
def bstack111ll1ll1ll_opy_(bstack11ll111lll_opy_, test=None):
  bstack111ll11ll11_opy_ = bstack11lll111l_opy_.on()
  if not bstack111ll11ll11_opy_ or bstack11ll111lll_opy_ not in [bstack1l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᷱ")] or test == None:
    return None
  return {
    bstack1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᷲ"): bstack111ll11ll11_opy_ and bstack1llll1llll_opy_(threading.current_thread(), bstack1l11l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᷳ"), None) == True and bstack11lll111l_opy_.bstack1l1111l111_opy_(test[bstack1l11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᷴ")])
  }