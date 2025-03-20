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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack1l11l11l1ll_opy_ as bstack1l11l11ll11_opy_, EVENTS
from bstack_utils.bstack11ll111111_opy_ import bstack11ll111111_opy_
from bstack_utils.helper import bstack111ll1l1l_opy_, bstack11l111l1l1_opy_, bstack1l111111ll_opy_, bstack1l11l111l11_opy_, \
  bstack1l111lll1ll_opy_, bstack1l11111l1_opy_, get_host_info, bstack1l11l111lll_opy_, bstack11lllll1l_opy_, bstack111llll1l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1lll111ll_opy_ import get_logger
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
logger = get_logger(__name__)
bstack1ll1l1lll1_opy_ = bstack1lll1ll1l11_opy_()
@bstack111llll1l1_opy_(class_method=False)
def _1l111lll111_opy_(driver, bstack111l1l1111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l11l_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫᒅ"): caps.get(bstack1l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᒆ"), None),
        bstack1l11l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᒇ"): bstack111l1l1111_opy_.get(bstack1l11l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᒈ"), None),
        bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᒉ"): caps.get(bstack1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᒊ"), None),
        bstack1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᒋ"): caps.get(bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᒌ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᒍ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᒎ"), None) is None or os.environ[bstack1l11l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᒏ")] == bstack1l11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᒐ"):
        return False
    return True
def bstack1l11l1111l1_opy_(config):
  return config.get(bstack1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᒑ"), False) or any([p.get(bstack1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᒒ"), False) == True for p in config.get(bstack1l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᒓ"), [])])
def bstack1l1llll11l_opy_(config, bstack111ll111l_opy_):
  try:
    if not bstack1l111111ll_opy_(config):
      return False
    bstack1l111lll11l_opy_ = config.get(bstack1l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᒔ"), False)
    if int(bstack111ll111l_opy_) < len(config.get(bstack1l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᒕ"), [])) and config[bstack1l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᒖ")][bstack111ll111l_opy_]:
      bstack1l11l11l1l1_opy_ = config[bstack1l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᒗ")][bstack111ll111l_opy_].get(bstack1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᒘ"), None)
    else:
      bstack1l11l11l1l1_opy_ = config.get(bstack1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᒙ"), None)
    if bstack1l11l11l1l1_opy_ != None:
      bstack1l111lll11l_opy_ = bstack1l11l11l1l1_opy_
    bstack1l111llll11_opy_ = os.getenv(bstack1l11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᒚ")) is not None and len(os.getenv(bstack1l11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᒛ"))) > 0 and os.getenv(bstack1l11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᒜ")) != bstack1l11l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᒝ")
    return bstack1l111lll11l_opy_ and bstack1l111llll11_opy_
  except Exception as error:
    logger.debug(bstack1l11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᒞ") + str(error))
  return False
def bstack1l1111l111_opy_(test_tags):
  bstack1ll1lll1ll1_opy_ = os.getenv(bstack1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᒟ"))
  if bstack1ll1lll1ll1_opy_ is None:
    return True
  bstack1ll1lll1ll1_opy_ = json.loads(bstack1ll1lll1ll1_opy_)
  try:
    include_tags = bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᒠ")] if bstack1l11l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᒡ") in bstack1ll1lll1ll1_opy_ and isinstance(bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᒢ")], list) else []
    exclude_tags = bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᒣ")] if bstack1l11l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᒤ") in bstack1ll1lll1ll1_opy_ and isinstance(bstack1ll1lll1ll1_opy_[bstack1l11l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᒥ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᒦ") + str(error))
  return False
def bstack1l11l11llll_opy_(config, bstack1l11l1l111l_opy_, bstack1l11l111l1l_opy_, bstack1l111ll1lll_opy_):
  bstack1l11l11ll1l_opy_ = bstack1l11l111l11_opy_(config)
  bstack1l11l1111ll_opy_ = bstack1l111lll1ll_opy_(config)
  if bstack1l11l11ll1l_opy_ is None or bstack1l11l1111ll_opy_ is None:
    logger.error(bstack1l11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᒧ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᒨ"), bstack1l11l_opy_ (u"ࠫࢀࢃࠧᒩ")))
    data = {
        bstack1l11l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᒪ"): config[bstack1l11l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᒫ")],
        bstack1l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᒬ"): config.get(bstack1l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᒭ"), os.path.basename(os.getcwd())),
        bstack1l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬᒮ"): bstack111ll1l1l_opy_(),
        bstack1l11l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᒯ"): config.get(bstack1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᒰ"), bstack1l11l_opy_ (u"ࠬ࠭ᒱ")),
        bstack1l11l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᒲ"): {
            bstack1l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᒳ"): bstack1l11l1l111l_opy_,
            bstack1l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᒴ"): bstack1l11l111l1l_opy_,
            bstack1l11l_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᒵ"): __version__,
            bstack1l11l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᒶ"): bstack1l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᒷ"),
            bstack1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᒸ"): bstack1l11l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᒹ"),
            bstack1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᒺ"): bstack1l111ll1lll_opy_
        },
        bstack1l11l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪᒻ"): settings,
        bstack1l11l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪᒼ"): bstack1l11l111lll_opy_(),
        bstack1l11l_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪᒽ"): bstack1l11111l1_opy_(),
        bstack1l11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭ᒾ"): get_host_info(),
        bstack1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᒿ"): bstack1l111111ll_opy_(config)
    }
    headers = {
        bstack1l11l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᓀ"): bstack1l11l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᓁ"),
    }
    config = {
        bstack1l11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᓂ"): (bstack1l11l11ll1l_opy_, bstack1l11l1111ll_opy_),
        bstack1l11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᓃ"): headers
    }
    response = bstack11lllll1l_opy_(bstack1l11l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᓄ"), bstack1l11l11ll11_opy_ + bstack1l11l_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫᓅ"), data, config)
    bstack1l11l11lll1_opy_ = response.json()
    if bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᓆ")]:
      parsed = json.loads(os.getenv(bstack1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᓇ"), bstack1l11l_opy_ (u"ࠧࡼࡿࠪᓈ")))
      parsed[bstack1l11l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᓉ")] = bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠩࡧࡥࡹࡧࠧᓊ")][bstack1l11l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᓋ")]
      os.environ[bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᓌ")] = json.dumps(parsed)
      bstack11ll111111_opy_.bstack1l11l11111l_opy_(bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠬࡪࡡࡵࡣࠪᓍ")][bstack1l11l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᓎ")])
      bstack11ll111111_opy_.bstack1l11l111111_opy_(bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠧࡥࡣࡷࡥࠬᓏ")][bstack1l11l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᓐ")])
      bstack11ll111111_opy_.store()
      return bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠩࡧࡥࡹࡧࠧᓑ")][bstack1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᓒ")], bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠫࡩࡧࡴࡢࠩᓓ")][bstack1l11l_opy_ (u"ࠬ࡯ࡤࠨᓔ")]
    else:
      logger.error(bstack1l11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧᓕ") + bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᓖ")])
      if bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓗ")] == bstack1l11l_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫᓘ"):
        for bstack1l11l11l11l_opy_ in bstack1l11l11lll1_opy_[bstack1l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᓙ")]:
          logger.error(bstack1l11l11l11l_opy_[bstack1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᓚ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨᓛ") +  str(error))
    return None, None
def bstack1l11l11l111_opy_():
  if os.getenv(bstack1l11l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᓜ")) is None:
    return {
        bstack1l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᓝ"): bstack1l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᓞ"),
        bstack1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓟ"): bstack1l11l_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩᓠ")
    }
  data = {bstack1l11l_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬᓡ"): bstack111ll1l1l_opy_()}
  headers = {
      bstack1l11l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᓢ"): bstack1l11l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧᓣ") + os.getenv(bstack1l11l_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧᓤ")),
      bstack1l11l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᓥ"): bstack1l11l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᓦ")
  }
  response = bstack11lllll1l_opy_(bstack1l11l_opy_ (u"ࠪࡔ࡚࡚ࠧᓧ"), bstack1l11l11ll11_opy_ + bstack1l11l_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ᓨ"), data, { bstack1l11l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᓩ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l11l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢᓪ") + bstack11l111l1l1_opy_().isoformat() + bstack1l11l_opy_ (u"࡛ࠧࠩᓫ"))
      return {bstack1l11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᓬ"): bstack1l11l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᓭ"), bstack1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓮ"): bstack1l11l_opy_ (u"ࠫࠬᓯ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣᓰ") + str(error))
    return {
        bstack1l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᓱ"): bstack1l11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᓲ"),
        bstack1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓳ"): str(error)
    }
def bstack1ll1lll1_opy_(caps, options, desired_capabilities={}):
  try:
    bstack1ll1lll111l_opy_ = caps.get(bstack1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᓴ"), {}).get(bstack1l11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᓵ"), caps.get(bstack1l11l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᓶ"), bstack1l11l_opy_ (u"ࠬ࠭ᓷ")))
    if bstack1ll1lll111l_opy_:
      logger.warn(bstack1l11l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᓸ"))
      return False
    if options:
      bstack1l111lllll1_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack1l111lllll1_opy_ = desired_capabilities
    else:
      bstack1l111lllll1_opy_ = {}
    browser = caps.get(bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᓹ"), bstack1l11l_opy_ (u"ࠨࠩᓺ")).lower() or bstack1l111lllll1_opy_.get(bstack1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᓻ"), bstack1l11l_opy_ (u"ࠪࠫᓼ")).lower()
    if browser != bstack1l11l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᓽ"):
      logger.warning(bstack1l11l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᓾ"))
      return False
    browser_version = caps.get(bstack1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᓿ")) or caps.get(bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᔀ")) or bstack1l111lllll1_opy_.get(bstack1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᔁ")) or bstack1l111lllll1_opy_.get(bstack1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᔂ"), {}).get(bstack1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᔃ")) or bstack1l111lllll1_opy_.get(bstack1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᔄ"), {}).get(bstack1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᔅ"))
    if browser_version and browser_version != bstack1l11l_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᔆ") and int(browser_version.split(bstack1l11l_opy_ (u"ࠧ࠯ࠩᔇ"))[0]) <= 98:
      logger.warning(bstack1l11l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠼࠳ࠨᔈ"))
      return False
    if not options:
      bstack1lll111ll1l_opy_ = caps.get(bstack1l11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᔉ")) or bstack1l111lllll1_opy_.get(bstack1l11l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᔊ"), {})
      if bstack1l11l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᔋ") in bstack1lll111ll1l_opy_.get(bstack1l11l_opy_ (u"ࠬࡧࡲࡨࡵࠪᔌ"), []):
        logger.warn(bstack1l11l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᔍ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᔎ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1llll11111l_opy_ = config.get(bstack1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᔏ"), {})
    bstack1llll11111l_opy_[bstack1l11l_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᔐ")] = os.getenv(bstack1l11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᔑ"))
    bstack1l111llll1l_opy_ = json.loads(os.getenv(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᔒ"), bstack1l11l_opy_ (u"ࠬࢁࡽࠨᔓ"))).get(bstack1l11l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᔔ"))
    caps[bstack1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᔕ")] = True
    if bstack1l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᔖ") in caps:
      caps[bstack1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᔗ")][bstack1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᔘ")] = bstack1llll11111l_opy_
      caps[bstack1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᔙ")][bstack1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᔚ")][bstack1l11l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᔛ")] = bstack1l111llll1l_opy_
    else:
      caps[bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᔜ")] = bstack1llll11111l_opy_
      caps[bstack1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᔝ")][bstack1l11l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᔞ")] = bstack1l111llll1l_opy_
  except Exception as error:
    logger.debug(bstack1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦᔟ") +  str(error))
def bstack11ll1111l_opy_(driver, bstack1l11l1l1111_opy_):
  try:
    setattr(driver, bstack1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᔠ"), True)
    session = driver.session_id
    if session:
      bstack1l11l111ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1l11l111ll1_opy_ = False
      bstack1l11l111ll1_opy_ = url.scheme in [bstack1l11l_opy_ (u"ࠧ࡮ࡴࡵࡲࠥᔡ"), bstack1l11l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᔢ")]
      if bstack1l11l111ll1_opy_:
        if bstack1l11l1l1111_opy_:
          logger.info(bstack1l11l_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢᔣ"))
      return bstack1l11l1l1111_opy_
  except Exception as e:
    logger.error(bstack1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᔤ") + str(e))
    return False
def bstack1l11l1l1_opy_(driver, name, path):
  try:
    bstack1ll1lllll11_opy_ = {
        bstack1l11l_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᔥ"): threading.current_thread().current_test_uuid,
        bstack1l11l_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᔦ"): os.environ.get(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᔧ"), bstack1l11l_opy_ (u"ࠬ࠭ᔨ")),
        bstack1l11l_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪᔩ"): os.environ.get(bstack1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᔪ"), bstack1l11l_opy_ (u"ࠨࠩᔫ"))
    }
    bstack1ll1ll11111_opy_ = bstack1ll1l1lll1_opy_.bstack1lll111l1ll_opy_(EVENTS.bstack1lll1l1ll_opy_.value)
    logger.debug(bstack1l11l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᔬ"))
    try:
      logger.debug(driver.execute_async_script(bstack11ll111111_opy_.perform_scan, {bstack1l11l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥᔭ"): name}))
      bstack1ll1l1lll1_opy_.end(EVENTS.bstack1lll1l1ll_opy_.value, bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᔮ"), bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᔯ"), True, None)
    except Exception as error:
      bstack1ll1l1lll1_opy_.end(EVENTS.bstack1lll1l1ll_opy_.value, bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᔰ"), bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᔱ"), False, str(error))
    bstack1ll1ll11111_opy_ = bstack1ll1l1lll1_opy_.bstack1l111lll1l1_opy_(EVENTS.bstack1ll1ll11lll_opy_.value)
    bstack1ll1l1lll1_opy_.mark(bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᔲ"))
    try:
      logger.debug(driver.execute_async_script(bstack11ll111111_opy_.bstack1l111llllll_opy_, bstack1ll1lllll11_opy_))
      bstack1ll1l1lll1_opy_.end(bstack1ll1ll11111_opy_, bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᔳ"), bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᔴ"),True, None)
    except Exception as error:
      bstack1ll1l1lll1_opy_.end(bstack1ll1ll11111_opy_, bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᔵ"), bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᔶ"),False, str(error))
    logger.info(bstack1l11l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᔷ"))
  except Exception as bstack1lll111l11l_opy_:
    logger.error(bstack1l11l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᔸ") + str(path) + bstack1l11l_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᔹ") + str(bstack1lll111l11l_opy_))