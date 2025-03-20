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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack1l11l11ll11_opy_ as bstack1l111lll111_opy_, EVENTS
from bstack_utils.bstack1l11l11l11_opy_ import bstack1l11l11l11_opy_
from bstack_utils.helper import bstack1lllll11ll_opy_, bstack11l111l1l1_opy_, bstack1ll11ll1l1_opy_, bstack1l11l1l1111_opy_, \
  bstack1l11l11l1l1_opy_, bstack1ll1ll111_opy_, get_host_info, bstack1l11l11llll_opy_, bstack111111ll_opy_, bstack111lll1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11l11l1l_opy_ import get_logger
from bstack_utils.bstack1l1ll1111_opy_ import bstack11111111l1_opy_
logger = get_logger(__name__)
bstack1l1ll1111_opy_ = bstack11111111l1_opy_()
@bstack111lll1lll_opy_(class_method=False)
def _1l111llll1l_opy_(driver, bstack111ll11111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬᒆ"): caps.get(bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᒇ"), None),
        bstack11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᒈ"): bstack111ll11111_opy_.get(bstack11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᒉ"), None),
        bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᒊ"): caps.get(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᒋ"), None),
        bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᒌ"): caps.get(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᒍ"), None)
    }
  except Exception as error:
    logger.debug(bstack11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᒎ") + str(error))
  return response
def on():
    if os.environ.get(bstack11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᒏ"), None) is None or os.environ[bstack11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᒐ")] == bstack11_opy_ (u"ࠣࡰࡸࡰࡱࠨᒑ"):
        return False
    return True
def bstack1l11l1111l1_opy_(config):
  return config.get(bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᒒ"), False) or any([p.get(bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᒓ"), False) == True for p in config.get(bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᒔ"), [])])
def bstack11ll1l1l11_opy_(config, bstack1l1l1111ll_opy_):
  try:
    if not bstack1ll11ll1l1_opy_(config):
      return False
    bstack1l11l11l11l_opy_ = config.get(bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᒕ"), False)
    if int(bstack1l1l1111ll_opy_) < len(config.get(bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᒖ"), [])) and config[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᒗ")][bstack1l1l1111ll_opy_]:
      bstack1l11l11l111_opy_ = config[bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᒘ")][bstack1l1l1111ll_opy_].get(bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᒙ"), None)
    else:
      bstack1l11l11l111_opy_ = config.get(bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᒚ"), None)
    if bstack1l11l11l111_opy_ != None:
      bstack1l11l11l11l_opy_ = bstack1l11l11l111_opy_
    bstack1l11l1111ll_opy_ = os.getenv(bstack11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᒛ")) is not None and len(os.getenv(bstack11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᒜ"))) > 0 and os.getenv(bstack11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᒝ")) != bstack11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᒞ")
    return bstack1l11l11l11l_opy_ and bstack1l11l1111ll_opy_
  except Exception as error:
    logger.debug(bstack11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᒟ") + str(error))
  return False
def bstack11ll1lllll_opy_(test_tags):
  bstack1ll1llll1ll_opy_ = os.getenv(bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᒠ"))
  if bstack1ll1llll1ll_opy_ is None:
    return True
  bstack1ll1llll1ll_opy_ = json.loads(bstack1ll1llll1ll_opy_)
  try:
    include_tags = bstack1ll1llll1ll_opy_[bstack11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᒡ")] if bstack11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᒢ") in bstack1ll1llll1ll_opy_ and isinstance(bstack1ll1llll1ll_opy_[bstack11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᒣ")], list) else []
    exclude_tags = bstack1ll1llll1ll_opy_[bstack11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᒤ")] if bstack11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᒥ") in bstack1ll1llll1ll_opy_ and isinstance(bstack1ll1llll1ll_opy_[bstack11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᒦ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᒧ") + str(error))
  return False
def bstack1l11l111lll_opy_(config, bstack1l111ll1lll_opy_, bstack1l11l11111l_opy_, bstack1l11l11l1ll_opy_):
  bstack1l111lll1ll_opy_ = bstack1l11l1l1111_opy_(config)
  bstack1l111lllll1_opy_ = bstack1l11l11l1l1_opy_(config)
  if bstack1l111lll1ll_opy_ is None or bstack1l111lllll1_opy_ is None:
    logger.error(bstack11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᒨ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᒩ"), bstack11_opy_ (u"ࠬࢁࡽࠨᒪ")))
    data = {
        bstack11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᒫ"): config[bstack11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᒬ")],
        bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᒭ"): config.get(bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᒮ"), os.path.basename(os.getcwd())),
        bstack11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᒯ"): bstack1lllll11ll_opy_(),
        bstack11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᒰ"): config.get(bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᒱ"), bstack11_opy_ (u"࠭ࠧᒲ")),
        bstack11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᒳ"): {
            bstack11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᒴ"): bstack1l111ll1lll_opy_,
            bstack11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᒵ"): bstack1l11l11111l_opy_,
            bstack11_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᒶ"): __version__,
            bstack11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᒷ"): bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᒸ"),
            bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᒹ"): bstack11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᒺ"),
            bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᒻ"): bstack1l11l11l1ll_opy_
        },
        bstack11_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᒼ"): settings,
        bstack11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᒽ"): bstack1l11l11llll_opy_(),
        bstack11_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᒾ"): bstack1ll1ll111_opy_(),
        bstack11_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᒿ"): get_host_info(),
        bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᓀ"): bstack1ll11ll1l1_opy_(config)
    }
    headers = {
        bstack11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᓁ"): bstack11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᓂ"),
    }
    config = {
        bstack11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᓃ"): (bstack1l111lll1ll_opy_, bstack1l111lllll1_opy_),
        bstack11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᓄ"): headers
    }
    response = bstack111111ll_opy_(bstack11_opy_ (u"ࠫࡕࡕࡓࡕࠩᓅ"), bstack1l111lll111_opy_ + bstack11_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᓆ"), data, config)
    bstack1l11l111l11_opy_ = response.json()
    if bstack1l11l111l11_opy_[bstack11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᓇ")]:
      parsed = json.loads(os.getenv(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᓈ"), bstack11_opy_ (u"ࠨࡽࢀࠫᓉ")))
      parsed[bstack11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᓊ")] = bstack1l11l111l11_opy_[bstack11_opy_ (u"ࠪࡨࡦࡺࡡࠨᓋ")][bstack11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᓌ")]
      os.environ[bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᓍ")] = json.dumps(parsed)
      bstack1l11l11l11_opy_.bstack1l111lll1l1_opy_(bstack1l11l111l11_opy_[bstack11_opy_ (u"࠭ࡤࡢࡶࡤࠫᓎ")][bstack11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᓏ")])
      bstack1l11l11l11_opy_.bstack1l111lll11l_opy_(bstack1l11l111l11_opy_[bstack11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᓐ")][bstack11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᓑ")])
      bstack1l11l11l11_opy_.store()
      return bstack1l11l111l11_opy_[bstack11_opy_ (u"ࠪࡨࡦࡺࡡࠨᓒ")][bstack11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᓓ")], bstack1l11l111l11_opy_[bstack11_opy_ (u"ࠬࡪࡡࡵࡣࠪᓔ")][bstack11_opy_ (u"࠭ࡩࡥࠩᓕ")]
    else:
      logger.error(bstack11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᓖ") + bstack1l11l111l11_opy_[bstack11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓗ")])
      if bstack1l11l111l11_opy_[bstack11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓘ")] == bstack11_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᓙ"):
        for bstack1l11l11lll1_opy_ in bstack1l11l111l11_opy_[bstack11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᓚ")]:
          logger.error(bstack1l11l11lll1_opy_[bstack11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᓛ")])
      return None, None
  except Exception as error:
    logger.error(bstack11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᓜ") +  str(error))
    return None, None
def bstack1l11l111l1l_opy_():
  if os.getenv(bstack11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᓝ")) is None:
    return {
        bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᓞ"): bstack11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᓟ"),
        bstack11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓠ"): bstack11_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᓡ")
    }
  data = {bstack11_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᓢ"): bstack1lllll11ll_opy_()}
  headers = {
      bstack11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᓣ"): bstack11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᓤ") + os.getenv(bstack11_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᓥ")),
      bstack11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᓦ"): bstack11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᓧ")
  }
  response = bstack111111ll_opy_(bstack11_opy_ (u"ࠫࡕ࡛ࡔࠨᓨ"), bstack1l111lll111_opy_ + bstack11_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᓩ"), data, { bstack11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᓪ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᓫ") + bstack11l111l1l1_opy_().isoformat() + bstack11_opy_ (u"ࠨ࡜ࠪᓬ"))
      return {bstack11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᓭ"): bstack11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᓮ"), bstack11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᓯ"): bstack11_opy_ (u"ࠬ࠭ᓰ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᓱ") + str(error))
    return {
        bstack11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᓲ"): bstack11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᓳ"),
        bstack11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓴ"): str(error)
    }
def bstack1111l11ll_opy_(caps, options, desired_capabilities={}):
  try:
    bstack1lll1111111_opy_ = caps.get(bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᓵ"), {}).get(bstack11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᓶ"), caps.get(bstack11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᓷ"), bstack11_opy_ (u"࠭ࠧᓸ")))
    if bstack1lll1111111_opy_:
      logger.warn(bstack11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᓹ"))
      return False
    if options:
      bstack1l11l11ll1l_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack1l11l11ll1l_opy_ = desired_capabilities
    else:
      bstack1l11l11ll1l_opy_ = {}
    browser = caps.get(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᓺ"), bstack11_opy_ (u"ࠩࠪᓻ")).lower() or bstack1l11l11ll1l_opy_.get(bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᓼ"), bstack11_opy_ (u"ࠫࠬᓽ")).lower()
    if browser != bstack11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᓾ"):
      logger.warning(bstack11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᓿ"))
      return False
    browser_version = caps.get(bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔀ")) or caps.get(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᔁ")) or bstack1l11l11ll1l_opy_.get(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᔂ")) or bstack1l11l11ll1l_opy_.get(bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᔃ"), {}).get(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᔄ")) or bstack1l11l11ll1l_opy_.get(bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᔅ"), {}).get(bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔆ"))
    if browser_version and browser_version != bstack11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᔇ") and int(browser_version.split(bstack11_opy_ (u"ࠨ࠰ࠪᔈ"))[0]) <= 98:
      logger.warning(bstack11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠽࠴ࠢᔉ"))
      return False
    if not options:
      bstack1ll1ll1llll_opy_ = caps.get(bstack11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᔊ")) or bstack1l11l11ll1l_opy_.get(bstack11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᔋ"), {})
      if bstack11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᔌ") in bstack1ll1ll1llll_opy_.get(bstack11_opy_ (u"࠭ࡡࡳࡩࡶࠫᔍ"), []):
        logger.warn(bstack11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᔎ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᔏ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1lll1l1ll11_opy_ = config.get(bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᔐ"), {})
    bstack1lll1l1ll11_opy_[bstack11_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᔑ")] = os.getenv(bstack11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᔒ"))
    bstack1l11l111ll1_opy_ = json.loads(os.getenv(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᔓ"), bstack11_opy_ (u"࠭ࡻࡾࠩᔔ"))).get(bstack11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔕ"))
    caps[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᔖ")] = True
    if bstack11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᔗ") in caps:
      caps[bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᔘ")][bstack11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᔙ")] = bstack1lll1l1ll11_opy_
      caps[bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᔚ")][bstack11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᔛ")][bstack11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔜ")] = bstack1l11l111ll1_opy_
    else:
      caps[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᔝ")] = bstack1lll1l1ll11_opy_
      caps[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᔞ")][bstack11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᔟ")] = bstack1l11l111ll1_opy_
  except Exception as error:
    logger.debug(bstack11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧᔠ") +  str(error))
def bstack1111ll111_opy_(driver, bstack1l111llllll_opy_):
  try:
    setattr(driver, bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᔡ"), True)
    session = driver.session_id
    if session:
      bstack1l11l1l111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1l11l1l111l_opy_ = False
      bstack1l11l1l111l_opy_ = url.scheme in [bstack11_opy_ (u"ࠨࡨࡵࡶࡳࠦᔢ"), bstack11_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᔣ")]
      if bstack1l11l1l111l_opy_:
        if bstack1l111llllll_opy_:
          logger.info(bstack11_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣᔤ"))
      return bstack1l111llllll_opy_
  except Exception as e:
    logger.error(bstack11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᔥ") + str(e))
    return False
def bstack1l1llll1l_opy_(driver, name, path):
  try:
    bstack1ll1ll11l11_opy_ = {
        bstack11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᔦ"): threading.current_thread().current_test_uuid,
        bstack11_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᔧ"): os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᔨ"), bstack11_opy_ (u"࠭ࠧᔩ")),
        bstack11_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫᔪ"): os.environ.get(bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᔫ"), bstack11_opy_ (u"ࠩࠪᔬ"))
    }
    bstack1ll1l1llll1_opy_ = bstack1l1ll1111_opy_.bstack1ll1ll11111_opy_(EVENTS.bstack11llll1l1_opy_.value)
    logger.debug(bstack11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᔭ"))
    try:
      logger.debug(driver.execute_async_script(bstack1l11l11l11_opy_.perform_scan, {bstack11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᔮ"): name}))
      bstack1l1ll1111_opy_.end(EVENTS.bstack11llll1l1_opy_.value, bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔯ"), bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔰ"), True, None)
    except Exception as error:
      bstack1l1ll1111_opy_.end(EVENTS.bstack11llll1l1_opy_.value, bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᔱ"), bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᔲ"), False, str(error))
    bstack1ll1l1llll1_opy_ = bstack1l1ll1111_opy_.bstack1l11l111111_opy_(EVENTS.bstack1lll111lll1_opy_.value)
    bstack1l1ll1111_opy_.mark(bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᔳ"))
    try:
      logger.debug(driver.execute_async_script(bstack1l11l11l11_opy_.bstack1l111llll11_opy_, bstack1ll1ll11l11_opy_))
      bstack1l1ll1111_opy_.end(bstack1ll1l1llll1_opy_, bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᔴ"), bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᔵ"),True, None)
    except Exception as error:
      bstack1l1ll1111_opy_.end(bstack1ll1l1llll1_opy_, bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔶ"), bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔷ"),False, str(error))
    logger.info(bstack11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᔸ"))
  except Exception as bstack1ll1lll1111_opy_:
    logger.error(bstack11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᔹ") + str(path) + bstack11_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᔺ") + str(bstack1ll1lll1111_opy_))