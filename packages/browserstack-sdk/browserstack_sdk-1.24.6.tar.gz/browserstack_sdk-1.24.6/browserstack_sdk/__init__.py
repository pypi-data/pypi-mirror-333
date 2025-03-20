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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.measure import bstack1l1ll1111_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from browserstack_sdk.bstack1l1l111l_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1l111111_opy_ import bstack11l1llllll_opy_
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack11l1ll1l_opy_():
  global CONFIG
  headers = {
        bstack11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11l1ll11_opy_(CONFIG, bstack11llll1ll1_opy_)
  try:
    response = requests.get(bstack11llll1ll1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l11111l_opy_ = response.json()[bstack11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1ll11l1lll_opy_.format(response.json()))
      return bstack1l11111l_opy_
    else:
      logger.debug(bstack11ll1l11_opy_.format(bstack11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11ll1l11_opy_.format(e))
def bstack11ll1l1111_opy_(hub_url):
  global CONFIG
  url = bstack11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11l1ll11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1ll1ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l111l1ll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l1l111l1_opy_, stage=STAGE.bstack1lll11111l_opy_)
def bstack1lll1lllll_opy_():
  try:
    global bstack1ll111ll1_opy_
    bstack1l11111l_opy_ = bstack11l1ll1l_opy_()
    bstack11111lll_opy_ = []
    results = []
    for bstack1l111lll_opy_ in bstack1l11111l_opy_:
      bstack11111lll_opy_.append(bstack11ll11l11l_opy_(target=bstack11ll1l1111_opy_,args=(bstack1l111lll_opy_,)))
    for t in bstack11111lll_opy_:
      t.start()
    for t in bstack11111lll_opy_:
      results.append(t.join())
    bstack1l1l11l1l_opy_ = {}
    for item in results:
      hub_url = item[bstack11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1l11l1l_opy_[hub_url] = latency
    bstack1ll11l1ll1_opy_ = min(bstack1l1l11l1l_opy_, key= lambda x: bstack1l1l11l1l_opy_[x])
    bstack1ll111ll1_opy_ = bstack1ll11l1ll1_opy_
    logger.debug(bstack1l11l1l1ll_opy_.format(bstack1ll11l1ll1_opy_))
  except Exception as e:
    logger.debug(bstack1l11ll1l1l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack11l11l1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11ll1111ll_opy_, bstack111111ll_opy_, bstack11l1l1ll1l_opy_, bstack1llllll111_opy_, \
  bstack1ll11ll1l1_opy_, \
  Notset, bstack11111111_opy_, \
  bstack1lll1l1l1l_opy_, bstack1l11l1l1_opy_, bstack1111l1ll1_opy_, bstack1ll1ll111_opy_, bstack11l1ll11ll_opy_, bstack1ll11l11l1_opy_, \
  bstack111l1l111_opy_, \
  bstack1l1ll11ll_opy_, bstack11ll111l1_opy_, bstack1llll1lll_opy_, bstack1l11lll11_opy_, \
  bstack11111ll1l_opy_, bstack1ll1lll1_opy_, bstack11l1l1l11_opy_, bstack11lll111l_opy_
from bstack_utils.bstack11l1llll_opy_ import bstack11111l1l_opy_, bstack111l11l11_opy_
from bstack_utils.bstack1lllllll11_opy_ import bstack1lll1111ll_opy_
from bstack_utils.bstack1l111l11ll_opy_ import bstack1l111l111_opy_, bstack1ll11ll1ll_opy_
from bstack_utils.bstack1l11l11l11_opy_ import bstack1l11l11l11_opy_
from bstack_utils.proxy import bstack11l11llll_opy_, bstack11l1ll11_opy_, bstack111111l11_opy_, bstack1l111lll1_opy_
from browserstack_sdk.bstack1l1111lll1_opy_ import *
from browserstack_sdk.bstack1ll1llllll_opy_ import *
from bstack_utils.bstack1ll11ll11l_opy_ import bstack11lll1llll_opy_
from browserstack_sdk.sdk_cli.bstack11ll1l1ll1_opy_ import bstack11ll1l1ll1_opy_, bstack11lllll111_opy_, bstack1l111l1l1l_opy_, bstack1l1lll1l1_opy_
from browserstack_sdk.bstack111lll1l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack11l11l1l_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1llll1l1_opy_, stage=STAGE.bstack1lll11111l_opy_)
def bstack111llll11_opy_():
    global bstack1ll111ll1_opy_
    try:
        bstack11l1l11l_opy_ = bstack11ll1llll1_opy_()
        bstack1ll1l1lll_opy_(bstack11l1l11l_opy_)
        hub_url = bstack11l1l11l_opy_.get(bstack11_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack11_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack11_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack11_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1ll111ll1_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack11ll1llll1_opy_():
    global CONFIG
    bstack11llll11ll_opy_ = CONFIG.get(bstack11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack11_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack11_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack11llll11ll_opy_, str):
        raise ValueError(bstack11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack11l1l11l_opy_ = bstack111l1l1l1_opy_(bstack11llll11ll_opy_)
        return bstack11l1l11l_opy_
    except Exception as e:
        logger.error(bstack11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack111l1l1l1_opy_(bstack11llll11ll_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack11_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1l11ll1l1_opy_ + bstack11llll11ll_opy_
        auth = (CONFIG[bstack11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack111l111ll_opy_ = json.loads(response.text)
            return bstack111l111ll_opy_
    except ValueError as ve:
        logger.error(bstack11_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1ll1l1lll_opy_(bstack111l1l11_opy_):
    global CONFIG
    if bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack11_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack11_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack111l1l11_opy_:
        bstack111ll1111_opy_ = CONFIG.get(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack11_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack111ll1111_opy_)
        bstack11ll11ll1_opy_ = bstack111l1l11_opy_.get(bstack11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1ll1111l1_opy_ = bstack11_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack11ll11ll1_opy_)
        logger.debug(bstack11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1ll1111l1_opy_)
        bstack11ll111l_opy_ = {
            bstack11_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack11_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack11_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1ll1111l1_opy_
        }
        bstack111ll1111_opy_.update(bstack11ll111l_opy_)
        logger.debug(bstack11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack111ll1111_opy_)
        CONFIG[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack111ll1111_opy_
        logger.debug(bstack11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack11l1111l_opy_():
    bstack11l1l11l_opy_ = bstack11ll1llll1_opy_()
    if not bstack11l1l11l_opy_[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack11l1l11l_opy_[bstack11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack11_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1ll1111lll_opy_, stage=STAGE.bstack1lll11111l_opy_)
def bstack1llll1ll1l_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1ll11111l_opy_
        logger.debug(bstack11_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l1lll11l1_opy_ = json.loads(response.text)
                bstack1ll1111ll_opy_ = bstack1l1lll11l1_opy_.get(bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1ll1111ll_opy_:
                    bstack1l1ll11l_opy_ = bstack1ll1111ll_opy_[0]
                    build_hashed_id = bstack1l1ll11l_opy_.get(bstack11_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack11l1lll1ll_opy_ = bstack11l1ll1l1l_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11l1lll1ll_opy_])
                    logger.info(bstack1lll1lll1_opy_.format(bstack11l1lll1ll_opy_))
                    bstack1l11l1l111_opy_ = CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l11l1l111_opy_ += bstack11_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l11l1l111_opy_ != bstack1l1ll11l_opy_.get(bstack11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11l1l1ll_opy_.format(bstack1l1ll11l_opy_.get(bstack11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l11l1l111_opy_))
                    return result
                else:
                    logger.debug(bstack11_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack11_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack11_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack11_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
import bstack_utils.bstack111l1lll1_opy_ as bstack1ll11l111l_opy_
import bstack_utils.bstack11llllll1_opy_ as bstack1l1111l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
if os.getenv(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack111111ll1_opy_()
else:
  os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack11lllll1ll_opy_ = bstack11_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1111lllll_opy_ = bstack11_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1lll1ll1_opy_ = None
CONFIG = {}
bstack1ll111l1_opy_ = {}
bstack1ll11ll1_opy_ = {}
bstack11l111l1_opy_ = None
bstack1lll1l1ll_opy_ = None
bstack1ll111lll1_opy_ = None
bstack11lllll11_opy_ = -1
bstack1l1l1lll11_opy_ = 0
bstack11l11ll11_opy_ = bstack1l111111_opy_
bstack11ll11lll_opy_ = 1
bstack11llll11_opy_ = False
bstack1lll11ll_opy_ = False
bstack1l1ll111ll_opy_ = bstack11_opy_ (u"ࠬ࠭ࢾ")
bstack1l11l111_opy_ = bstack11_opy_ (u"࠭ࠧࢿ")
bstack1111ll1l_opy_ = False
bstack1111l1l1l_opy_ = True
bstack1l111l1l_opy_ = bstack11_opy_ (u"ࠧࠨࣀ")
bstack1l1lll1ll_opy_ = []
bstack1ll111ll1_opy_ = bstack11_opy_ (u"ࠨࠩࣁ")
bstack1l11111l1l_opy_ = False
bstack1l11lllll1_opy_ = None
bstack111ll1lll_opy_ = None
bstack1l111ll111_opy_ = None
bstack11ll1l11ll_opy_ = -1
bstack1l1l1111l1_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠩࢁࠫࣂ")), bstack11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack11_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1ll1lll111_opy_ = 0
bstack11ll11ll11_opy_ = 0
bstack11lllllll_opy_ = []
bstack1ll111lll_opy_ = []
bstack1lllll11l1_opy_ = []
bstack1l1l1111_opy_ = []
bstack11ll1ll1_opy_ = bstack11_opy_ (u"ࠬ࠭ࣅ")
bstack1lll1ll111_opy_ = bstack11_opy_ (u"࠭ࠧࣆ")
bstack1l11llll_opy_ = False
bstack1ll111ll_opy_ = False
bstack1l1lll111l_opy_ = {}
bstack1lll111111_opy_ = None
bstack11ll1ll11l_opy_ = None
bstack1111llll_opy_ = None
bstack1lllll1l1_opy_ = None
bstack1lll1l1111_opy_ = None
bstack1l11llll11_opy_ = None
bstack1llll1l1l_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack11l1llll11_opy_ = None
bstack1lll1lll11_opy_ = None
bstack1ll11l1l_opy_ = None
bstack1ll1l1l1l1_opy_ = None
bstack1ll1l11l1l_opy_ = None
bstack1111ll1ll_opy_ = None
bstack1ll1ll111l_opy_ = None
bstack1l1lll1ll1_opy_ = None
bstack11l1ll11l1_opy_ = None
bstack11lll1ll1_opy_ = None
bstack1l1lll1l1l_opy_ = None
bstack1llll1llll_opy_ = None
bstack111l11ll_opy_ = None
bstack1l11ll11ll_opy_ = None
bstack11ll1l1l_opy_ = None
bstack11l1l11ll_opy_ = False
bstack1ll1ll11l_opy_ = bstack11_opy_ (u"ࠢࠣࣇ")
logger = bstack11l11l1l_opy_.get_logger(__name__, bstack11l11ll11_opy_)
bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
percy = bstack111ll1l1l_opy_()
bstack1111111ll_opy_ = bstack11l1llllll_opy_()
bstack1ll1ll1l1l_opy_ = bstack111lll1l_opy_()
def bstack1l11llll1_opy_():
  global CONFIG
  global bstack1l11llll_opy_
  global bstack1l1l1lll1_opy_
  bstack1lll1llll1_opy_ = bstack1lllll111l_opy_(CONFIG)
  if bstack1ll11ll1l1_opy_(CONFIG):
    if (bstack11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in bstack1lll1llll1_opy_ and str(bstack1lll1llll1_opy_[bstack11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1l11llll_opy_ = True
    bstack1l1l1lll1_opy_.bstack1lll1ll11l_opy_(bstack1lll1llll1_opy_.get(bstack11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1l11llll_opy_ = True
    bstack1l1l1lll1_opy_.bstack1lll1ll11l_opy_(True)
def bstack111ll1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111l111l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11111lll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack11_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l111l1l_opy_
      bstack1l111l1l_opy_ += bstack11_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack111l1111l_opy_ = re.compile(bstack11_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack11111ll11_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111l1111l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack11_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack1l1l1l1l1l_opy_():
  global bstack11ll1l1l_opy_
  if bstack11ll1l1l_opy_ is None:
        bstack11ll1l1l_opy_ = bstack11111lll1_opy_()
  bstack1ll1l1l11_opy_ = bstack11ll1l1l_opy_
  if bstack1ll1l1l11_opy_ and os.path.exists(os.path.abspath(bstack1ll1l1l11_opy_)):
    fileName = bstack1ll1l1l11_opy_
  if bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack11_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack11_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack1l1l_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1l_opy_ = bstack11_opy_ (u"ࠩࠪࣗ")
  bstack1l11l1ll_opy_ = os.getcwd()
  bstack1l1l11l1_opy_ = bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack1l1l1ll1ll_opy_ = bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack1l1l_opy_)) and bstack1l11l1ll_opy_ != bstack11_opy_ (u"ࠧࠨࣚ"):
    bstack1l1l_opy_ = os.path.join(bstack1l11l1ll_opy_, bstack1l1l11l1_opy_)
    if not os.path.exists(bstack1l1l_opy_):
      bstack1l1l_opy_ = os.path.join(bstack1l11l1ll_opy_, bstack1l1l1ll1ll_opy_)
    if bstack1l11l1ll_opy_ != os.path.dirname(bstack1l11l1ll_opy_):
      bstack1l11l1ll_opy_ = os.path.dirname(bstack1l11l1ll_opy_)
    else:
      bstack1l11l1ll_opy_ = bstack11_opy_ (u"ࠨࠢࣛ")
  bstack11ll1l1l_opy_ = bstack1l1l_opy_ if os.path.exists(bstack1l1l_opy_) else None
  return bstack11ll1l1l_opy_
def bstack1l11ll111l_opy_():
  bstack1l1l_opy_ = bstack1l1l1l1l1l_opy_()
  if not os.path.exists(bstack1l1l_opy_):
    bstack1l1l11ll1_opy_(
      bstack1l11ll1l_opy_.format(os.getcwd()))
  try:
    with open(bstack1l1l_opy_, bstack11_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack11_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack111l1111l_opy_)
      yaml.add_constructor(bstack11_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack11111ll11_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l1l_opy_, bstack11_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l1l11ll1_opy_(bstack11ll1l11l_opy_.format(str(exc)))
def bstack1ll1l11ll_opy_(config):
  bstack1l11111l1_opy_ = bstack1l11lll11l_opy_(config)
  for option in list(bstack1l11111l1_opy_):
    if option.lower() in bstack1l1l1l1lll_opy_ and option != bstack1l1l1l1lll_opy_[option.lower()]:
      bstack1l11111l1_opy_[bstack1l1l1l1lll_opy_[option.lower()]] = bstack1l11111l1_opy_[option]
      del bstack1l11111l1_opy_[option]
  return config
def bstack1ll1lllll_opy_():
  global bstack1ll11ll1_opy_
  for key, bstack111l1111_opy_ in bstack1llllllll_opy_.items():
    if isinstance(bstack111l1111_opy_, list):
      for var in bstack111l1111_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll11ll1_opy_[key] = os.environ[var]
          break
    elif bstack111l1111_opy_ in os.environ and os.environ[bstack111l1111_opy_] and str(os.environ[bstack111l1111_opy_]).strip():
      bstack1ll11ll1_opy_[key] = os.environ[bstack111l1111_opy_]
  if bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack1ll11ll1_opy_[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack1ll11ll1_opy_[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack1ll1ll1111_opy_():
  global bstack1ll111l1_opy_
  global bstack1l111l1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack1ll111l1_opy_[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack1ll111l1_opy_[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lllll1lll_opy_ in bstack1l111l1l11_opy_.items():
    if isinstance(bstack1lllll1lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lllll1lll_opy_:
          if idx < len(sys.argv) and bstack11_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack1ll111l1_opy_:
            bstack1ll111l1_opy_[key] = sys.argv[idx + 1]
            bstack1l111l1l_opy_ += bstack11_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack11_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack1lllll1lll_opy_.lower() == val.lower() and not key in bstack1ll111l1_opy_:
          bstack1ll111l1_opy_[key] = sys.argv[idx + 1]
          bstack1l111l1l_opy_ += bstack11_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack1lllll1lll_opy_ + bstack11_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll1llll11_opy_(config):
  bstack1lllll11_opy_ = config.keys()
  for bstack11ll1111_opy_, bstack1l1ll11lll_opy_ in bstack1ll1lll11l_opy_.items():
    if bstack1l1ll11lll_opy_ in bstack1lllll11_opy_:
      config[bstack11ll1111_opy_] = config[bstack1l1ll11lll_opy_]
      del config[bstack1l1ll11lll_opy_]
  for bstack11ll1111_opy_, bstack1l1ll11lll_opy_ in bstack1l1llll11l_opy_.items():
    if isinstance(bstack1l1ll11lll_opy_, list):
      for bstack11ll11lll1_opy_ in bstack1l1ll11lll_opy_:
        if bstack11ll11lll1_opy_ in bstack1lllll11_opy_:
          config[bstack11ll1111_opy_] = config[bstack11ll11lll1_opy_]
          del config[bstack11ll11lll1_opy_]
          break
    elif bstack1l1ll11lll_opy_ in bstack1lllll11_opy_:
      config[bstack11ll1111_opy_] = config[bstack1l1ll11lll_opy_]
      del config[bstack1l1ll11lll_opy_]
  for bstack11ll11lll1_opy_ in list(config):
    for bstack1lll1l11_opy_ in bstack1l111llll1_opy_:
      if bstack11ll11lll1_opy_.lower() == bstack1lll1l11_opy_.lower() and bstack11ll11lll1_opy_ != bstack1lll1l11_opy_:
        config[bstack1lll1l11_opy_] = config[bstack11ll11lll1_opy_]
        del config[bstack11ll11lll1_opy_]
  bstack11lll111ll_opy_ = [{}]
  if not config.get(bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack11lll111ll_opy_ = config[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack11lll111ll_opy_:
    for bstack11ll11lll1_opy_ in list(platform):
      for bstack1lll1l11_opy_ in bstack1l111llll1_opy_:
        if bstack11ll11lll1_opy_.lower() == bstack1lll1l11_opy_.lower() and bstack11ll11lll1_opy_ != bstack1lll1l11_opy_:
          platform[bstack1lll1l11_opy_] = platform[bstack11ll11lll1_opy_]
          del platform[bstack11ll11lll1_opy_]
  for bstack11ll1111_opy_, bstack1l1ll11lll_opy_ in bstack1l1llll11l_opy_.items():
    for platform in bstack11lll111ll_opy_:
      if isinstance(bstack1l1ll11lll_opy_, list):
        for bstack11ll11lll1_opy_ in bstack1l1ll11lll_opy_:
          if bstack11ll11lll1_opy_ in platform:
            platform[bstack11ll1111_opy_] = platform[bstack11ll11lll1_opy_]
            del platform[bstack11ll11lll1_opy_]
            break
      elif bstack1l1ll11lll_opy_ in platform:
        platform[bstack11ll1111_opy_] = platform[bstack1l1ll11lll_opy_]
        del platform[bstack1l1ll11lll_opy_]
  for bstack1lllllll1l_opy_ in bstack1l111l11_opy_:
    if bstack1lllllll1l_opy_ in config:
      if not bstack1l111l11_opy_[bstack1lllllll1l_opy_] in config:
        config[bstack1l111l11_opy_[bstack1lllllll1l_opy_]] = {}
      config[bstack1l111l11_opy_[bstack1lllllll1l_opy_]].update(config[bstack1lllllll1l_opy_])
      del config[bstack1lllllll1l_opy_]
  for platform in bstack11lll111ll_opy_:
    for bstack1lllllll1l_opy_ in bstack1l111l11_opy_:
      if bstack1lllllll1l_opy_ in list(platform):
        if not bstack1l111l11_opy_[bstack1lllllll1l_opy_] in platform:
          platform[bstack1l111l11_opy_[bstack1lllllll1l_opy_]] = {}
        platform[bstack1l111l11_opy_[bstack1lllllll1l_opy_]].update(platform[bstack1lllllll1l_opy_])
        del platform[bstack1lllllll1l_opy_]
  config = bstack1ll1l11ll_opy_(config)
  return config
def bstack1l111ll1ll_opy_(config):
  global bstack1l11l111_opy_
  bstack11lll1lll_opy_ = False
  if bstack11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack11l1l11l_opy_ = bstack11ll1llll1_opy_()
      if bstack11_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack11l1l11l_opy_:
        if not bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack11_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack11lll1lll_opy_ = True
        bstack1l11l111_opy_ = config[bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack1ll11ll1l1_opy_(config) and bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack11lll1lll_opy_:
    if not bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack11_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1lllll11ll_opy_ = datetime.datetime.now()
      bstack11lllll1l1_opy_ = bstack1lllll11ll_opy_.strftime(bstack11_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack11ll111ll_opy_ = bstack11_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack11lllll1l1_opy_, hostname, bstack11ll111ll_opy_)
      config[bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack1l11l111_opy_ = config[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1l1l1ll111_opy_():
  bstack1l11l1l11_opy_ =  bstack1ll1ll111_opy_()[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack1l11l1l11_opy_ if bstack1l11l1l11_opy_ else -1
def bstack11l11lll1_opy_(bstack1l11l1l11_opy_):
  global CONFIG
  if not bstack11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack11_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack1l11l1l11_opy_)
  )
def bstack1lllll111_opy_():
  global CONFIG
  if not bstack11_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1lllll11ll_opy_ = datetime.datetime.now()
  bstack11lllll1l1_opy_ = bstack1lllll11ll_opy_.strftime(bstack11_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack11lllll1l1_opy_
  )
def bstack11l111lll_opy_():
  global CONFIG
  if bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack11_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack11_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack1lllll111_opy_()
    os.environ[bstack11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack11_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack1l11l1l11_opy_ = bstack11_opy_ (u"ࠧࠨऩ")
  bstack1lll11l1ll_opy_ = bstack1l1l1ll111_opy_()
  if bstack1lll11l1ll_opy_ != -1:
    bstack1l11l1l11_opy_ = bstack11_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack1lll11l1ll_opy_)
  if bstack1l11l1l11_opy_ == bstack11_opy_ (u"ࠩࠪफ"):
    bstack1l111lllll_opy_ = bstack1ll11ll1l_opy_(CONFIG[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack1l111lllll_opy_ != -1:
      bstack1l11l1l11_opy_ = str(bstack1l111lllll_opy_)
  if bstack1l11l1l11_opy_:
    bstack11l11lll1_opy_(bstack1l11l1l11_opy_)
    os.environ[bstack11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack1l1l11lll1_opy_(bstack1111ll1l1_opy_, bstack1llll1l11_opy_, path):
  bstack1l11ll1lll_opy_ = {
    bstack11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1llll1l11_opy_
  }
  if os.path.exists(path):
    bstack11111111l_opy_ = json.load(open(path, bstack11_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack11111111l_opy_ = {}
  bstack11111111l_opy_[bstack1111ll1l1_opy_] = bstack1l11ll1lll_opy_
  with open(path, bstack11_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack11111111l_opy_, outfile)
def bstack1ll11ll1l_opy_(bstack1111ll1l1_opy_):
  bstack1111ll1l1_opy_ = str(bstack1111ll1l1_opy_)
  bstack11llllll1l_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠩࢁࠫल")), bstack11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack11llllll1l_opy_):
      os.makedirs(bstack11llllll1l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠫࢃ࠭ऴ")), bstack11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack11_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack11_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11_opy_ (u"ࠩࡵࠫह")) as bstack11lll1ll11_opy_:
      bstack111111l1_opy_ = json.load(bstack11lll1ll11_opy_)
    if bstack1111ll1l1_opy_ in bstack111111l1_opy_:
      bstack1l1ll1lll_opy_ = bstack111111l1_opy_[bstack1111ll1l1_opy_][bstack11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack111lll111_opy_ = int(bstack1l1ll1lll_opy_) + 1
      bstack1l1l11lll1_opy_(bstack1111ll1l1_opy_, bstack111lll111_opy_, file_path)
      return bstack111lll111_opy_
    else:
      bstack1l1l11lll1_opy_(bstack1111ll1l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll111ll1_opy_.format(str(e)))
    return -1
def bstack1l1111ll1_opy_(config):
  if not config[bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack11ll1l111l_opy_(config, index=0):
  global bstack1111ll1l_opy_
  bstack1llll11111_opy_ = {}
  caps = bstack111llll1_opy_ + bstack1l11111lll_opy_
  if config.get(bstack11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack1llll11111_opy_[bstack11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack1llll11111_opy_[bstack11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack1111ll1l_opy_:
    caps += bstack1l11l1l11l_opy_
  for key in config:
    if key in caps + [bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack1llll11111_opy_[key] = config[key]
  if bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack1l11l1111l_opy_ in config[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack1l11l1111l_opy_ in caps:
        continue
      bstack1llll11111_opy_[bstack1l11l1111l_opy_] = config[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack1l11l1111l_opy_]
  bstack1llll11111_opy_[bstack11_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack1llll11111_opy_:
    del (bstack1llll11111_opy_[bstack11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack1llll11111_opy_
def bstack1l1llll11_opy_(config):
  global bstack1111ll1l_opy_
  bstack1l1111111_opy_ = {}
  caps = bstack1l11111lll_opy_
  if bstack1111ll1l_opy_:
    caps += bstack1l11l1l11l_opy_
  for key in caps:
    if key in config:
      bstack1l1111111_opy_[key] = config[key]
  return bstack1l1111111_opy_
def bstack1l11lllll_opy_(bstack1llll11111_opy_, bstack1l1111111_opy_):
  bstack1l11l1ll1_opy_ = {}
  for key in bstack1llll11111_opy_.keys():
    if key in bstack1ll1lll11l_opy_:
      bstack1l11l1ll1_opy_[bstack1ll1lll11l_opy_[key]] = bstack1llll11111_opy_[key]
    else:
      bstack1l11l1ll1_opy_[key] = bstack1llll11111_opy_[key]
  for key in bstack1l1111111_opy_:
    if key in bstack1ll1lll11l_opy_:
      bstack1l11l1ll1_opy_[bstack1ll1lll11l_opy_[key]] = bstack1l1111111_opy_[key]
    else:
      bstack1l11l1ll1_opy_[key] = bstack1l1111111_opy_[key]
  return bstack1l11l1ll1_opy_
def bstack1l1l1lll1l_opy_(config, index=0):
  global bstack1111ll1l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l1l11l1ll_opy_ = bstack11ll1111ll_opy_(bstack1l1ll1l1_opy_, config, logger)
  bstack1l1111111_opy_ = bstack1l1llll11_opy_(config)
  bstack1l1l111ll1_opy_ = bstack1l11111lll_opy_
  bstack1l1l111ll1_opy_ += bstack1l1l11llll_opy_
  bstack1l1111111_opy_ = update(bstack1l1111111_opy_, bstack1l1l11l1ll_opy_)
  if bstack1111ll1l_opy_:
    bstack1l1l111ll1_opy_ += bstack1l11l1l11l_opy_
  if bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack11lll1111_opy_ = bstack11ll1111ll_opy_(bstack1l1ll1l1_opy_, config[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1l1l111ll1_opy_ += list(bstack11lll1111_opy_.keys())
    for bstack1l11111111_opy_ in bstack1l1l111ll1_opy_:
      if bstack1l11111111_opy_ in config[bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack1l11111111_opy_ == bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack11lll1111_opy_[bstack1l11111111_opy_] = str(config[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l11111111_opy_] * 1.0)
          except:
            bstack11lll1111_opy_[bstack1l11111111_opy_] = str(config[bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1l11111111_opy_])
        else:
          bstack11lll1111_opy_[bstack1l11111111_opy_] = config[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1l11111111_opy_]
        del (config[bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack1l11111111_opy_])
    bstack1l1111111_opy_ = update(bstack1l1111111_opy_, bstack11lll1111_opy_)
  bstack1llll11111_opy_ = bstack11ll1l111l_opy_(config, index)
  for bstack11ll11lll1_opy_ in bstack1l11111lll_opy_ + list(bstack1l1l11l1ll_opy_.keys()):
    if bstack11ll11lll1_opy_ in bstack1llll11111_opy_:
      bstack1l1111111_opy_[bstack11ll11lll1_opy_] = bstack1llll11111_opy_[bstack11ll11lll1_opy_]
      del (bstack1llll11111_opy_[bstack11ll11lll1_opy_])
  if bstack11111111_opy_(config):
    bstack1llll11111_opy_[bstack11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack1l1111111_opy_)
    caps[bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack1llll11111_opy_
  else:
    bstack1llll11111_opy_[bstack11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack1l11lllll_opy_(bstack1llll11111_opy_, bstack1l1111111_opy_))
    if bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack111l11ll1_opy_():
  global bstack1ll111ll1_opy_
  global CONFIG
  if bstack111l111l1_opy_() <= version.parse(bstack11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack1ll111ll1_opy_ != bstack11_opy_ (u"ࠬ࠭०"):
      return bstack11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack1ll111ll1_opy_ + bstack11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack1l1ll111l_opy_
  if bstack1ll111ll1_opy_ != bstack11_opy_ (u"ࠨࠩ३"):
    return bstack11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack1ll111ll1_opy_ + bstack11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack11l1ll1ll_opy_
def bstack11ll1ll11_opy_(options):
  return hasattr(options, bstack11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1111lll1_opy_(options, bstack11l11l11l_opy_):
  for bstack1llll11lll_opy_ in bstack11l11l11l_opy_:
    if bstack1llll11lll_opy_ in [bstack11_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack1llll11lll_opy_ in options._experimental_options:
      options._experimental_options[bstack1llll11lll_opy_] = update(options._experimental_options[bstack1llll11lll_opy_],
                                                         bstack11l11l11l_opy_[bstack1llll11lll_opy_])
    else:
      options.add_experimental_option(bstack1llll11lll_opy_, bstack11l11l11l_opy_[bstack1llll11lll_opy_])
  if bstack11_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack11l11l11l_opy_:
    for arg in bstack11l11l11l_opy_[bstack11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack11l11l11l_opy_[bstack11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack11l11l11l_opy_:
    for ext in bstack11l11l11l_opy_[bstack11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11l11l11l_opy_[bstack11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack1l11l11ll_opy_(options, bstack1l1ll1l1l1_opy_):
  if bstack11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack1l1ll1l1l1_opy_:
    for bstack1ll1l11ll1_opy_ in bstack1l1ll1l1l1_opy_[bstack11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack1ll1l11ll1_opy_ in options._preferences:
        options._preferences[bstack1ll1l11ll1_opy_] = update(options._preferences[bstack1ll1l11ll1_opy_], bstack1l1ll1l1l1_opy_[bstack11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack1ll1l11ll1_opy_])
      else:
        options.set_preference(bstack1ll1l11ll1_opy_, bstack1l1ll1l1l1_opy_[bstack11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack1ll1l11ll1_opy_])
  if bstack11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1l1ll1l1l1_opy_:
    for arg in bstack1l1ll1l1l1_opy_[bstack11_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1ll111l1l1_opy_(options, bstack1lll111l1_opy_):
  if bstack11_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack1lll111l1_opy_:
    options.use_webview(bool(bstack1lll111l1_opy_[bstack11_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack1111lll1_opy_(options, bstack1lll111l1_opy_)
def bstack111ll1ll_opy_(options, bstack111l1ll1_opy_):
  for bstack1l1ll1l1l_opy_ in bstack111l1ll1_opy_:
    if bstack1l1ll1l1l_opy_ in [bstack11_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack1l1ll1l1l_opy_, bstack111l1ll1_opy_[bstack1l1ll1l1l_opy_])
  if bstack11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack111l1ll1_opy_:
    for arg in bstack111l1ll1_opy_[bstack11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack111l1ll1_opy_:
    options.bstack1l1111llll_opy_(bool(bstack111l1ll1_opy_[bstack11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack1l1l11111l_opy_(options, bstack111llllll_opy_):
  for bstack11ll1111l_opy_ in bstack111llllll_opy_:
    if bstack11ll1111l_opy_ in [bstack11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack11_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack11ll1111l_opy_] = bstack111llllll_opy_[bstack11ll1111l_opy_]
  if bstack11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack111llllll_opy_:
    for bstack1ll11ll11_opy_ in bstack111llllll_opy_[bstack11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1l1l1l1ll1_opy_(
        bstack1ll11ll11_opy_, bstack111llllll_opy_[bstack11_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack1ll11ll11_opy_])
  if bstack11_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack111llllll_opy_:
    for arg in bstack111llllll_opy_[bstack11_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack1l1l11111_opy_(options, caps):
  if not hasattr(options, bstack11_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ") and options.KEY in caps:
    bstack1111lll1_opy_(options, caps[bstack11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ")])
  elif options.KEY == bstack11_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack1l11l11ll_opy_(options, caps[bstack11_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬএ") and options.KEY in caps:
    bstack111ll1ll_opy_(options, caps[bstack11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ")])
  elif options.KEY == bstack11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack1ll111l1l1_opy_(options, caps[bstack11_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧও") and options.KEY in caps:
    bstack1l1l11111l_opy_(options, caps[bstack11_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ")])
def bstack1llll111l_opy_(caps):
  global bstack1111ll1l_opy_
  if isinstance(os.environ.get(bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫক")), str):
    bstack1111ll1l_opy_ = eval(os.getenv(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")))
  if bstack1111ll1l_opy_:
    if bstack111ll1l1_opy_() < version.parse(bstack11_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫগ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ঘ")
    if bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬঙ") in caps:
      browser = caps[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ")]
    elif bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪছ") in caps:
      browser = caps[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ")]
    browser = str(browser).lower()
    if browser == bstack11_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫঝ") or browser == bstack11_opy_ (u"ࠬ࡯ࡰࡢࡦࠪঞ"):
      browser = bstack11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ট")
    if browser == bstack11_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨঠ"):
      browser = bstack11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨড")
    if browser not in [bstack11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ"), bstack11_opy_ (u"ࠪࡩࡩ࡭ࡥࠨণ"), bstack11_opy_ (u"ࠫ࡮࡫ࠧত"), bstack11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬথ"), bstack11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧদ")]:
      return None
    try:
      package = bstack11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩধ").format(browser)
      name = bstack11_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩন")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll1ll11_opy_(options):
        return None
      for bstack11ll11lll1_opy_ in caps.keys():
        options.set_capability(bstack11ll11lll1_opy_, caps[bstack11ll11lll1_opy_])
      bstack1l1l11111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll11lll1_opy_(options, bstack1llll1l11l_opy_):
  if not bstack11ll1ll11_opy_(options):
    return
  for bstack11ll11lll1_opy_ in bstack1llll1l11l_opy_.keys():
    if bstack11ll11lll1_opy_ in bstack1l1l11llll_opy_:
      continue
    if bstack11ll11lll1_opy_ in options._caps and type(options._caps[bstack11ll11lll1_opy_]) in [dict, list]:
      options._caps[bstack11ll11lll1_opy_] = update(options._caps[bstack11ll11lll1_opy_], bstack1llll1l11l_opy_[bstack11ll11lll1_opy_])
    else:
      options.set_capability(bstack11ll11lll1_opy_, bstack1llll1l11l_opy_[bstack11ll11lll1_opy_])
  bstack1l1l11111_opy_(options, bstack1llll1l11l_opy_)
  if bstack11_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ঩") in options._caps:
    if options._caps[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨপ")] and options._caps[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")].lower() != bstack11_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ব"):
      del options._caps[bstack11_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬভ")]
def bstack1l111l1ll1_opy_(proxy_config):
  if bstack11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম") in proxy_config:
    proxy_config[bstack11_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪয")] = proxy_config[bstack11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র")]
    del (proxy_config[bstack11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")])
  if bstack11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল") in proxy_config and proxy_config[bstack11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳")].lower() != bstack11_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঴"):
    proxy_config[bstack11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack11_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨশ")
  if bstack11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧষ") in proxy_config:
    proxy_config[bstack11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭স")] = bstack11_opy_ (u"ࠫࡵࡧࡣࠨহ")
  return proxy_config
def bstack1llll11l1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺") in config:
    return proxy
  config[bstack11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻")] = bstack1l111l1ll1_opy_(config[bstack11_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")])
  if proxy == None:
    proxy = Proxy(config[bstack11_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  return proxy
def bstack11ll11l1l1_opy_(self):
  global CONFIG
  global bstack1ll1l1l1l1_opy_
  try:
    proxy = bstack111111l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧা")):
        proxies = bstack11l11llll_opy_(proxy, bstack111l11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll11l1l_opy_ = proxies.popitem()
          if bstack11_opy_ (u"ࠥ࠾࠴࠵ࠢি") in bstack1l1ll11l1l_opy_:
            return bstack1l1ll11l1l_opy_
          else:
            return bstack11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧী") + bstack1l1ll11l1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤু").format(str(e)))
  return bstack1ll1l1l1l1_opy_(self)
def bstack1l11ll111_opy_():
  global CONFIG
  return bstack1l111lll1_opy_(CONFIG) and bstack1ll11l11l1_opy_() and bstack111l111l1_opy_() >= version.parse(bstack111l111l_opy_)
def bstack11ll1lll11_opy_():
  global CONFIG
  return (bstack11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩূ") in CONFIG or bstack11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ") in CONFIG) and bstack111l1l111_opy_()
def bstack1l11lll11l_opy_(config):
  bstack1l11111l1_opy_ = {}
  if bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬৄ") in config:
    bstack1l11111l1_opy_ = config[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅")]
  if bstack11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৆") in config:
    bstack1l11111l1_opy_ = config[bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে")]
  proxy = bstack111111l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack11_opy_ (u"ࠬ࠴ࡰࡢࡥࠪৈ")) and os.path.isfile(proxy):
      bstack1l11111l1_opy_[bstack11_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ৉")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")):
        proxies = bstack11l1ll11_opy_(config, bstack111l11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll11l1l_opy_ = proxies.popitem()
          if bstack11_opy_ (u"ࠣ࠼࠲࠳ࠧো") in bstack1l1ll11l1l_opy_:
            parsed_url = urlparse(bstack1l1ll11l1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") + bstack1l1ll11l1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l11111l1_opy_[bstack11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ্࠭")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l11111l1_opy_[bstack11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৎ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l11111l1_opy_[bstack11_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ৏")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l11111l1_opy_[bstack11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ৐")] = str(parsed_url.password)
  return bstack1l11111l1_opy_
def bstack1lllll111l_opy_(config):
  if bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ৑") in config:
    return config[bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒")]
  return {}
def bstack1l1l1ll1l_opy_(caps):
  global bstack1l11l111_opy_
  if bstack11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓") in caps:
    caps[bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔")][bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ৕")] = True
    if bstack1l11l111_opy_:
      caps[bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨৗ")] = bstack1l11l111_opy_
  else:
    caps[bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ৘")] = True
    if bstack1l11l111_opy_:
      caps[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৙")] = bstack1l11l111_opy_
@measure(event_name=EVENTS.bstack1llllll11_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l1l11lll_opy_():
  global CONFIG
  if not bstack1ll11ll1l1_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭৚") in CONFIG and bstack11l1l1l11_opy_(CONFIG[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛")]):
    if (
      bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨড়") in CONFIG
      and bstack11l1l1l11_opy_(CONFIG[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়")].get(bstack11_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪ৞")))
    ):
      logger.debug(bstack11_opy_ (u"ࠢࡍࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࡧࡧࠤࡦࡹࠠࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤࠣয়"))
      return
    bstack1l11111l1_opy_ = bstack1l11lll11l_opy_(CONFIG)
    bstack111ll111l_opy_(CONFIG[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫৠ")], bstack1l11111l1_opy_)
def bstack111ll111l_opy_(key, bstack1l11111l1_opy_):
  global bstack1lll1ll1_opy_
  logger.info(bstack11111l1ll_opy_)
  try:
    bstack1lll1ll1_opy_ = Local()
    bstack111l1l1l_opy_ = {bstack11_opy_ (u"ࠩ࡮ࡩࡾ࠭ৡ"): key}
    bstack111l1l1l_opy_.update(bstack1l11111l1_opy_)
    logger.debug(bstack11lll1l11_opy_.format(str(bstack111l1l1l_opy_)).replace(key, bstack11_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧৢ")))
    bstack1lll1ll1_opy_.start(**bstack111l1l1l_opy_)
    if bstack1lll1ll1_opy_.isRunning():
      logger.info(bstack1l1lllll_opy_)
  except Exception as e:
    bstack1l1l11ll1_opy_(bstack1ll1l11l11_opy_.format(str(e)))
def bstack1l11l1l1l1_opy_():
  global bstack1lll1ll1_opy_
  if bstack1lll1ll1_opy_.isRunning():
    logger.info(bstack11l1ll1ll1_opy_)
    bstack1lll1ll1_opy_.stop()
  bstack1lll1ll1_opy_ = None
def bstack111llll1l_opy_(bstack1l11l11l1l_opy_=[]):
  global CONFIG
  bstack1l11l1ll1l_opy_ = []
  bstack11l1lll11l_opy_ = [bstack11_opy_ (u"ࠫࡴࡹࠧৣ"), bstack11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৤"), bstack11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ৥"), bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ০"), bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭১"), bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ২")]
  try:
    for err in bstack1l11l11l1l_opy_:
      bstack11l1l1l1_opy_ = {}
      for k in bstack11l1lll11l_opy_:
        val = CONFIG[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৩")][int(err[bstack11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ৪")])].get(k)
        if val:
          bstack11l1l1l1_opy_[k] = val
      if(err[bstack11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")] != bstack11_opy_ (u"࠭ࠧ৬")):
        bstack11l1l1l1_opy_[bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭৭")] = {
          err[bstack11_opy_ (u"ࠨࡰࡤࡱࡪ࠭৮")]: err[bstack11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৯")]
        }
        bstack1l11l1ll1l_opy_.append(bstack11l1l1l1_opy_)
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬৰ") + str(e))
  finally:
    return bstack1l11l1ll1l_opy_
def bstack11111l111_opy_(file_name):
  bstack1l1lllllll_opy_ = []
  try:
    bstack11l1ll11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11l1ll11l_opy_):
      with open(bstack11l1ll11l_opy_) as f:
        bstack1ll111l1ll_opy_ = json.load(f)
        bstack1l1lllllll_opy_ = bstack1ll111l1ll_opy_
      os.remove(bstack11l1ll11l_opy_)
    return bstack1l1lllllll_opy_
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ৱ") + str(e))
    return bstack1l1lllllll_opy_
def bstack1l1l1111l_opy_():
  try:
      from bstack_utils.constants import bstack11ll111l1l_opy_, EVENTS
      from bstack_utils.helper import bstack111111ll_opy_, get_host_info, bstack1l1l1lll1_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack11lll1l1_opy_ = os.path.join(os.getcwd(), bstack11_opy_ (u"ࠬࡲ࡯ࡨࠩ৲"), bstack11_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ৳"))
      lock = FileLock(bstack11lll1l1_opy_+bstack11_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ৴"))
      def bstack111111111_opy_():
          try:
              with lock:
                  with open(bstack11lll1l1_opy_, bstack11_opy_ (u"ࠣࡴࠥ৵"), encoding=bstack11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ৶")) as file:
                      data = json.load(file)
                      config = {
                          bstack11_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ৷"): {
                              bstack11_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥ৸"): bstack11_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣ৹"),
                          }
                      }
                      bstack11l1ll111_opy_ = datetime.utcnow()
                      bstack1lllll11ll_opy_ = bstack11l1ll111_opy_.strftime(bstack11_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠦࡕࡕࡅࠥ৺"))
                      bstack11ll1ll111_opy_ = os.environ.get(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ৻")) if os.environ.get(bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) else bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ৽"))
                      payload = {
                          bstack11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠢ৾"): bstack11_opy_ (u"ࠦࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣ৿"),
                          bstack11_opy_ (u"ࠧࡪࡡࡵࡣࠥ਀"): {
                              bstack11_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠧਁ"): bstack11ll1ll111_opy_,
                              bstack11_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࡠࡦࡤࡽࠧਂ"): bstack1lllll11ll_opy_,
                              bstack11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧਃ"): bstack11_opy_ (u"ࠤࡖࡈࡐࡌࡥࡢࡶࡸࡶࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࠥ਄"),
                              bstack11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡ࡭ࡷࡴࡴࠢਅ"): {
                                  bstack11_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࡸࠨਆ"): data,
                                  bstack11_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਇ"): bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"))
                              },
                              bstack11_opy_ (u"ࠢࡶࡵࡨࡶࡤࡪࡡࡵࡣࠥਉ"): bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਊ")),
                              bstack11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠧ਋"): get_host_info()
                          }
                      }
                      response = bstack111111ll_opy_(bstack11_opy_ (u"ࠥࡔࡔ࡙ࡔࠣ਌"), bstack11ll111l1l_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack11_opy_ (u"ࠦࡉࡧࡴࡢࠢࡶࡩࡳࡺࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡴࡰࠢࡾࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡࠡࡽࢀࠦ਍").format(bstack11ll111l1l_opy_, payload))
                      else:
                          logger.debug(bstack11_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧ਎").format(bstack11ll111l1l_opy_, payload))
          except Exception as e:
              logger.debug(bstack11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠࡼࡿࠥਏ").format(e))
      bstack111111111_opy_()
      bstack1l11l1l1_opy_(bstack11lll1l1_opy_, logger)
  except:
    pass
def bstack11lll1l1l1_opy_():
  global bstack1ll1ll11l_opy_
  global bstack1l1lll1ll_opy_
  global bstack11lllllll_opy_
  global bstack1ll111lll_opy_
  global bstack1lllll11l1_opy_
  global bstack1lll1ll111_opy_
  global CONFIG
  bstack1ll11lll1l_opy_ = os.environ.get(bstack11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਐ"))
  if bstack1ll11lll1l_opy_ in [bstack11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ਑"), bstack11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ਒")]:
    bstack11llll111l_opy_()
  percy.shutdown()
  if bstack1ll1ll11l_opy_:
    logger.warning(bstack11l1l1ll1_opy_.format(str(bstack1ll1ll11l_opy_)))
  else:
    try:
      bstack11111111l_opy_ = bstack1lll1l1l1l_opy_(bstack11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩਓ"), logger)
      if bstack11111111l_opy_.get(bstack11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਔ")) and bstack11111111l_opy_.get(bstack11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਕ")).get(bstack11_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਖ")):
        logger.warning(bstack11l1l1ll1_opy_.format(str(bstack11111111l_opy_[bstack11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਗ")][bstack11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਘ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.bstack1ll1l11l1_opy_)
  logger.info(bstack1111l1ll_opy_)
  global bstack1lll1ll1_opy_
  if bstack1lll1ll1_opy_:
    bstack1l11l1l1l1_opy_()
  try:
    for driver in bstack1l1lll1ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l11l1lll_opy_)
  if bstack1lll1ll111_opy_ == bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ"):
    bstack1lllll11l1_opy_ = bstack11111l111_opy_(bstack11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਚ"))
  if bstack1lll1ll111_opy_ == bstack11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਛ") and len(bstack1ll111lll_opy_) == 0:
    bstack1ll111lll_opy_ = bstack11111l111_opy_(bstack11_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਜ"))
    if len(bstack1ll111lll_opy_) == 0:
      bstack1ll111lll_opy_ = bstack11111l111_opy_(bstack11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਝ"))
  bstack1lll11lll_opy_ = bstack11_opy_ (u"ࠧࠨਞ")
  if len(bstack11lllllll_opy_) > 0:
    bstack1lll11lll_opy_ = bstack111llll1l_opy_(bstack11lllllll_opy_)
  elif len(bstack1ll111lll_opy_) > 0:
    bstack1lll11lll_opy_ = bstack111llll1l_opy_(bstack1ll111lll_opy_)
  elif len(bstack1lllll11l1_opy_) > 0:
    bstack1lll11lll_opy_ = bstack111llll1l_opy_(bstack1lllll11l1_opy_)
  elif len(bstack1l1l1111_opy_) > 0:
    bstack1lll11lll_opy_ = bstack111llll1l_opy_(bstack1l1l1111_opy_)
  if bool(bstack1lll11lll_opy_):
    bstack11l11111_opy_(bstack1lll11lll_opy_)
  else:
    bstack11l11111_opy_()
  bstack1l11l1l1_opy_(bstack1lllllll1_opy_, logger)
  if bstack1ll11lll1l_opy_ not in [bstack11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩਟ")]:
    bstack1l1l1111l_opy_()
  bstack11l11l1l_opy_.bstack1l1l11ll11_opy_(CONFIG)
  if len(bstack1lllll11l1_opy_) > 0:
    sys.exit(len(bstack1lllll11l1_opy_))
def bstack1l1ll11ll1_opy_(bstack111111lll_opy_, frame):
  global bstack1l1l1lll1_opy_
  logger.error(bstack1ll1111111_opy_)
  bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬਠ"), bstack111111lll_opy_)
  if hasattr(signal, bstack11_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫਡ")):
    bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਢ"), signal.Signals(bstack111111lll_opy_).name)
  else:
    bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ"), bstack11_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਤ"))
  if cli.is_running():
    bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.bstack1ll1l11l1_opy_)
  bstack1ll11lll1l_opy_ = os.environ.get(bstack11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਥ"))
  if bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਦ") and not cli.is_enabled(CONFIG):
    bstack111lllll1_opy_.stop(bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ")))
  bstack11lll1l1l1_opy_()
  sys.exit(1)
def bstack1l1l11ll1_opy_(err):
  logger.critical(bstack1ll111l11_opy_.format(str(err)))
  bstack11l11111_opy_(bstack1ll111l11_opy_.format(str(err)), True)
  atexit.unregister(bstack11lll1l1l1_opy_)
  bstack11llll111l_opy_()
  sys.exit(1)
def bstack11ll1l1lll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11l11111_opy_(message, True)
  atexit.unregister(bstack11lll1l1l1_opy_)
  bstack11llll111l_opy_()
  sys.exit(1)
def bstack11ll1l11l1_opy_():
  global CONFIG
  global bstack1ll111l1_opy_
  global bstack1ll11ll1_opy_
  global bstack1111l1l1l_opy_
  CONFIG = bstack1l11ll111l_opy_()
  load_dotenv(CONFIG.get(bstack11_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਨ")))
  bstack1ll1lllll_opy_()
  bstack1ll1ll1111_opy_()
  CONFIG = bstack1ll1llll11_opy_(CONFIG)
  update(CONFIG, bstack1ll11ll1_opy_)
  update(CONFIG, bstack1ll111l1_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1l111ll1ll_opy_(CONFIG)
  bstack1111l1l1l_opy_ = bstack1ll11ll1l1_opy_(CONFIG)
  os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ਩")] = bstack1111l1l1l_opy_.__str__().lower()
  bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਪ"), bstack1111l1l1l_opy_)
  if (bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਫ") in CONFIG and bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") in bstack1ll111l1_opy_) or (
          bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਭ") in CONFIG and bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") not in bstack1ll11ll1_opy_):
    if os.getenv(bstack11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਯ")):
      CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਰ")] = os.getenv(bstack11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਱"))
    else:
      if not CONFIG.get(bstack11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤਲ"), bstack11_opy_ (u"ࠢࠣਲ਼")) in bstack1lll1111l1_opy_:
        bstack11l111lll_opy_()
  elif (bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਴") not in CONFIG and bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ") in CONFIG) or (
          bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in bstack1ll11ll1_opy_ and bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") not in bstack1ll111l1_opy_):
    del (CONFIG[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਸ")])
  if bstack1l1111ll1_opy_(CONFIG):
    bstack1l1l11ll1_opy_(bstack1l111ll1l1_opy_)
  Config.bstack11l111l11_opy_().bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਹ"), CONFIG[bstack11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ਺")])
  bstack1l11l11l_opy_()
  bstack1ll1ll11l1_opy_()
  if bstack1111ll1l_opy_ and not CONFIG.get(bstack11_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ਻"), bstack11_opy_ (u"ࠤ਼ࠥ")) in bstack1lll1111l1_opy_:
    CONFIG[bstack11_opy_ (u"ࠪࡥࡵࡶࠧ਽")] = bstack1l1l1ll11_opy_(CONFIG)
    logger.info(bstack11lll1l11l_opy_.format(CONFIG[bstack11_opy_ (u"ࠫࡦࡶࡰࠨਾ")]))
  if not bstack1111l1l1l_opy_:
    CONFIG[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਿ")] = [{}]
def bstack11lll1ll1l_opy_(config, bstack1llllll1l_opy_):
  global CONFIG
  global bstack1111ll1l_opy_
  CONFIG = config
  bstack1111ll1l_opy_ = bstack1llllll1l_opy_
def bstack1ll1ll11l1_opy_():
  global CONFIG
  global bstack1111ll1l_opy_
  if bstack11_opy_ (u"࠭ࡡࡱࡲࠪੀ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11l1l1111_opy_)
    bstack1111ll1l_opy_ = True
    bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ੁ"), True)
def bstack1l1l1ll11_opy_(config):
  bstack11llll1111_opy_ = bstack11_opy_ (u"ࠨࠩੂ")
  app = config[bstack11_opy_ (u"ࠩࡤࡴࡵ࠭੃")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l11ll1l_opy_:
      if os.path.exists(app):
        bstack11llll1111_opy_ = bstack1lllll1l1l_opy_(config, app)
      elif bstack1ll1l1lll1_opy_(app):
        bstack11llll1111_opy_ = app
      else:
        bstack1l1l11ll1_opy_(bstack11l1llll1l_opy_.format(app))
    else:
      if bstack1ll1l1lll1_opy_(app):
        bstack11llll1111_opy_ = app
      elif os.path.exists(app):
        bstack11llll1111_opy_ = bstack1lllll1l1l_opy_(app)
      else:
        bstack1l1l11ll1_opy_(bstack11l1ll111l_opy_)
  else:
    if len(app) > 2:
      bstack1l1l11ll1_opy_(bstack111l11111_opy_)
    elif len(app) == 2:
      if bstack11_opy_ (u"ࠪࡴࡦࡺࡨࠨ੄") in app and bstack11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੅") in app:
        if os.path.exists(app[bstack11_opy_ (u"ࠬࡶࡡࡵࡪࠪ੆")]):
          bstack11llll1111_opy_ = bstack1lllll1l1l_opy_(config, app[bstack11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫੇ")], app[bstack11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪੈ")])
        else:
          bstack1l1l11ll1_opy_(bstack11l1llll1l_opy_.format(app))
      else:
        bstack1l1l11ll1_opy_(bstack111l11111_opy_)
    else:
      for key in app:
        if key in bstack1ll11llll_opy_:
          if key == bstack11_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉"):
            if os.path.exists(app[key]):
              bstack11llll1111_opy_ = bstack1lllll1l1l_opy_(config, app[key])
            else:
              bstack1l1l11ll1_opy_(bstack11l1llll1l_opy_.format(app))
          else:
            bstack11llll1111_opy_ = app[key]
        else:
          bstack1l1l11ll1_opy_(bstack1ll1lll1l_opy_)
  return bstack11llll1111_opy_
def bstack1ll1l1lll1_opy_(bstack11llll1111_opy_):
  import re
  bstack1l1l11l11l_opy_ = re.compile(bstack11_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੊"))
  bstack1l1111ll_opy_ = re.compile(bstack11_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢੋ"))
  if bstack11_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪੌ") in bstack11llll1111_opy_ or re.fullmatch(bstack1l1l11l11l_opy_, bstack11llll1111_opy_) or re.fullmatch(bstack1l1111ll_opy_, bstack11llll1111_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1111l111_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1lllll1l1l_opy_(config, path, bstack1l111l1111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11_opy_ (u"ࠬࡸࡢࠨ੍")).read()).hexdigest()
  bstack11l11111l_opy_ = bstack1l1lll111_opy_(md5_hash)
  bstack11llll1111_opy_ = None
  if bstack11l11111l_opy_:
    logger.info(bstack1ll1l111l_opy_.format(bstack11l11111l_opy_, md5_hash))
    return bstack11l11111l_opy_
  bstack11lllll1l_opy_ = datetime.datetime.now()
  bstack11lllll1_opy_ = MultipartEncoder(
    fields={
      bstack11_opy_ (u"࠭ࡦࡪ࡮ࡨࠫ੎"): (os.path.basename(path), open(os.path.abspath(path), bstack11_opy_ (u"ࠧࡳࡤࠪ੏")), bstack11_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ੐")),
      bstack11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬੑ"): bstack1l111l1111_opy_
    }
  )
  response = requests.post(bstack1l11lll1ll_opy_, data=bstack11lllll1_opy_,
                           headers={bstack11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੒"): bstack11lllll1_opy_.content_type},
                           auth=(config[bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੓")], config[bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੔")]))
  try:
    res = json.loads(response.text)
    bstack11llll1111_opy_ = res[bstack11_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧ੕")]
    logger.info(bstack11ll1l1l1l_opy_.format(bstack11llll1111_opy_))
    bstack1l11l11lll_opy_(md5_hash, bstack11llll1111_opy_)
    cli.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ੖"), datetime.datetime.now() - bstack11lllll1l_opy_)
  except ValueError as err:
    bstack1l1l11ll1_opy_(bstack11l11lll_opy_.format(str(err)))
  return bstack11llll1111_opy_
def bstack1l11l11l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11ll11lll_opy_
  bstack1ll11l11l_opy_ = 1
  bstack1ll1l1ll11_opy_ = 1
  if bstack11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੗") in CONFIG:
    bstack1ll1l1ll11_opy_ = CONFIG[bstack11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੘")]
  else:
    bstack1ll1l1ll11_opy_ = bstack11lll11111_opy_(framework_name, args) or 1
  if bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਖ਼") in CONFIG:
    bstack1ll11l11l_opy_ = len(CONFIG[bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")])
  bstack11ll11lll_opy_ = int(bstack1ll1l1ll11_opy_) * int(bstack1ll11l11l_opy_)
def bstack11lll11111_opy_(framework_name, args):
  if framework_name == bstack1111111l_opy_ and args and bstack11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪਜ਼") in args:
      bstack11llll11l_opy_ = args.index(bstack11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫੜ"))
      return int(args[bstack11llll11l_opy_ + 1]) or 1
  return 1
def bstack1l1lll111_opy_(md5_hash):
  bstack1llll11l1_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠧࡿࠩ੝")), bstack11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack11_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੟"))
  if os.path.exists(bstack1llll11l1_opy_):
    bstack1ll11l1l11_opy_ = json.load(open(bstack1llll11l1_opy_, bstack11_opy_ (u"ࠪࡶࡧ࠭੠")))
    if md5_hash in bstack1ll11l1l11_opy_:
      bstack1llll11l11_opy_ = bstack1ll11l1l11_opy_[md5_hash]
      bstack1ll1l11111_opy_ = datetime.datetime.now()
      bstack1l1111l1l1_opy_ = datetime.datetime.strptime(bstack1llll11l11_opy_[bstack11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੡")], bstack11_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੢"))
      if (bstack1ll1l11111_opy_ - bstack1l1111l1l1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1llll11l11_opy_[bstack11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੣")]):
        return None
      return bstack1llll11l11_opy_[bstack11_opy_ (u"ࠧࡪࡦࠪ੤")]
  else:
    return None
def bstack1l11l11lll_opy_(md5_hash, bstack11llll1111_opy_):
  bstack11llllll1l_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠨࢀࠪ੥")), bstack11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੦"))
  if not os.path.exists(bstack11llllll1l_opy_):
    os.makedirs(bstack11llllll1l_opy_)
  bstack1llll11l1_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠪࢂࠬ੧")), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੨"), bstack11_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੩"))
  bstack1ll1llll1l_opy_ = {
    bstack11_opy_ (u"࠭ࡩࡥࠩ੪"): bstack11llll1111_opy_,
    bstack11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ੫"): datetime.datetime.strftime(datetime.datetime.now(), bstack11_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ੬")),
    bstack11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੭"): str(__version__)
  }
  if os.path.exists(bstack1llll11l1_opy_):
    bstack1ll11l1l11_opy_ = json.load(open(bstack1llll11l1_opy_, bstack11_opy_ (u"ࠪࡶࡧ࠭੮")))
  else:
    bstack1ll11l1l11_opy_ = {}
  bstack1ll11l1l11_opy_[md5_hash] = bstack1ll1llll1l_opy_
  with open(bstack1llll11l1_opy_, bstack11_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
    json.dump(bstack1ll11l1l11_opy_, outfile)
def bstack11ll1lll_opy_(self):
  return
def bstack1l111ll11l_opy_(self):
  return
def bstack11lllllll1_opy_(self):
  global bstack1ll1l11l1l_opy_
  bstack1ll1l11l1l_opy_(self)
def bstack1lll1l1ll1_opy_():
  global bstack1l111ll111_opy_
  bstack1l111ll111_opy_ = True
@measure(event_name=EVENTS.bstack1ll1lll1l1_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l11l1111_opy_(self):
  global bstack1l1ll111ll_opy_
  global bstack11l111l1_opy_
  global bstack11ll1ll11l_opy_
  try:
    if bstack11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬੰ") in bstack1l1ll111ll_opy_ and self.session_id != None and bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੱ"), bstack11_opy_ (u"ࠧࠨੲ")) != bstack11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩੳ"):
      bstack11111l11_opy_ = bstack11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩੴ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੵ")
      if bstack11111l11_opy_ == bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੶"):
        bstack11111ll1l_opy_(logger)
      if self != None:
        bstack1l111l111_opy_(self, bstack11111l11_opy_, bstack11_opy_ (u"ࠬ࠲ࠠࠨ੷").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11_opy_ (u"࠭ࠧ੸")
    if bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੹") in bstack1l1ll111ll_opy_ and getattr(threading.current_thread(), bstack11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੺"), None):
      bstack11l11l1ll_opy_.bstack1lll111l_opy_(self, bstack1l1lll111l_opy_, logger, wait=True)
    if bstack11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ੻") in bstack1l1ll111ll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l111l111_opy_(self, bstack11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੼"))
      bstack1l1111l1l_opy_.bstack11lll111l1_opy_(self)
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੽") + str(e))
  bstack11ll1ll11l_opy_(self)
  self.session_id = None
def bstack1l1l11l11_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1ll1l111_opy_
    global bstack1l1ll111ll_opy_
    command_executor = kwargs.get(bstack11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੾"), bstack11_opy_ (u"࠭ࠧ੿"))
    bstack11ll11111l_opy_ = False
    if type(command_executor) == str and bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઀") in command_executor:
      bstack11ll11111l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫઁ") in str(getattr(command_executor, bstack11_opy_ (u"ࠩࡢࡹࡷࡲࠧં"), bstack11_opy_ (u"ࠪࠫઃ"))):
      bstack11ll11111l_opy_ = True
    else:
      return bstack1lll111111_opy_(self, *args, **kwargs)
    if bstack11ll11111l_opy_:
      bstack11llll1l_opy_ = bstack1ll11l111l_opy_.bstack1llllll11l_opy_(CONFIG, bstack1l1ll111ll_opy_)
      if kwargs.get(bstack11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ઄")):
        kwargs[bstack11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭અ")] = bstack1l1ll1l111_opy_(kwargs[bstack11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧઆ")], bstack1l1ll111ll_opy_, bstack11llll1l_opy_)
      elif kwargs.get(bstack11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧઇ")):
        kwargs[bstack11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨઈ")] = bstack1l1ll1l111_opy_(kwargs[bstack11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩઉ")], bstack1l1ll111ll_opy_, bstack11llll1l_opy_)
  except Exception as e:
    logger.error(bstack11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥઊ").format(str(e)))
  return bstack1lll111111_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1ll1l1ll1_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1ll1l1ll_opy_(self, command_executor=bstack11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧઋ"), *args, **kwargs):
  bstack11l11l11_opy_ = bstack1l1l11l11_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1ll11l1l1_opy_.on():
    return bstack11l11l11_opy_
  try:
    logger.debug(bstack11_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩઌ").format(str(command_executor)))
    logger.debug(bstack11_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨઍ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઎") in command_executor._url:
      bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩએ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬઐ") in command_executor):
    bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫઑ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1llll1l1_opy_ = getattr(threading.current_thread(), bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ઒"), None)
  if bstack11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬઓ") in bstack1l1ll111ll_opy_ or bstack11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઔ") in bstack1l1ll111ll_opy_:
    bstack111lllll1_opy_.bstack11ll1ll1ll_opy_(self)
  if bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧક") in bstack1l1ll111ll_opy_ and bstack1l1llll1l1_opy_ and bstack1l1llll1l1_opy_.get(bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ"), bstack11_opy_ (u"ࠩࠪગ")) == bstack11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫઘ"):
    bstack111lllll1_opy_.bstack11ll1ll1ll_opy_(self)
  return bstack11l11l11_opy_
def bstack1l1111l1_opy_(args):
  return bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬઙ") in str(args)
def bstack11lll11lll_opy_(self, driver_command, *args, **kwargs):
  global bstack1llll1llll_opy_
  global bstack11l1l11ll_opy_
  bstack1lll1ll11_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩચ"), None) and bstack1llllll111_opy_(
          threading.current_thread(), bstack11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬછ"), None)
  bstack1ll11111ll_opy_ = getattr(self, bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧજ"), None) != None and getattr(self, bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨઝ"), None) == True
  if not bstack11l1l11ll_opy_ and bstack1111l1l1l_opy_ and bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩઞ") in CONFIG and CONFIG[bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪટ")] == True and bstack1l11l11l11_opy_.bstack1ll11111l1_opy_(driver_command) and (bstack1ll11111ll_opy_ or bstack1lll1ll11_opy_) and not bstack1l1111l1_opy_(args):
    try:
      bstack11l1l11ll_opy_ = True
      logger.debug(bstack11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ઠ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪડ").format(str(err)))
    bstack11l1l11ll_opy_ = False
  response = bstack1llll1llll_opy_(self, driver_command, *args, **kwargs)
  if (bstack11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઢ") in str(bstack1l1ll111ll_opy_).lower() or bstack11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧણ") in str(bstack1l1ll111ll_opy_).lower()) and bstack1ll11l1l1_opy_.on():
    try:
      if driver_command == bstack11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬત"):
        bstack111lllll1_opy_.bstack1l11ll11l1_opy_({
            bstack11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨથ"): response[bstack11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩદ")],
            bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫધ"): bstack111lllll1_opy_.current_test_uuid() if bstack111lllll1_opy_.current_test_uuid() else bstack1ll11l1l1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11l1111ll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1ll1l111l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11l111l1_opy_
  global bstack11lllll11_opy_
  global bstack1ll111lll1_opy_
  global bstack11llll11_opy_
  global bstack1lll11ll_opy_
  global bstack1l1ll111ll_opy_
  global bstack1lll111111_opy_
  global bstack1l1lll1ll_opy_
  global bstack11ll1l11ll_opy_
  global bstack1l1lll111l_opy_
  CONFIG[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧન")] = str(bstack1l1ll111ll_opy_) + str(__version__)
  bstack1l11l1l1l_opy_ = os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ઩")]
  bstack11llll1l_opy_ = bstack1ll11l111l_opy_.bstack1llllll11l_opy_(CONFIG, bstack1l1ll111ll_opy_)
  CONFIG[bstack11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪપ")] = bstack1l11l1l1l_opy_
  CONFIG[bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪફ")] = bstack11llll1l_opy_
  command_executor = bstack111l11ll1_opy_()
  logger.debug(bstack111l1llll_opy_.format(command_executor))
  proxy = bstack1llll11l1l_opy_(CONFIG, proxy)
  bstack1l1l1111ll_opy_ = 0 if bstack11lllll11_opy_ < 0 else bstack11lllll11_opy_
  try:
    if bstack11llll11_opy_ is True:
      bstack1l1l1111ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll11ll_opy_ is True:
      bstack1l1l1111ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1l1111ll_opy_ = 0
  bstack1llll1l11l_opy_ = bstack1l1l1lll1l_opy_(CONFIG, bstack1l1l1111ll_opy_)
  logger.debug(bstack1l111l11l1_opy_.format(str(bstack1llll1l11l_opy_)))
  if bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭બ") in CONFIG and bstack11l1l1l11_opy_(CONFIG[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧભ")]):
    bstack1l1l1ll1l_opy_(bstack1llll1l11l_opy_)
  if bstack1111l1111_opy_.bstack11ll1l1l11_opy_(CONFIG, bstack1l1l1111ll_opy_) and bstack1111l1111_opy_.bstack1111l11ll_opy_(bstack1llll1l11l_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    if cli.accessibility is None or not cli.accessibility.is_enabled():
      bstack1111l1111_opy_.set_capabilities(bstack1llll1l11l_opy_, CONFIG)
  if desired_capabilities:
    bstack1lll1ll1ll_opy_ = bstack1ll1llll11_opy_(desired_capabilities)
    bstack1lll1ll1ll_opy_[bstack11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫમ")] = bstack11111111_opy_(CONFIG)
    bstack1l1l1l111_opy_ = bstack1l1l1lll1l_opy_(bstack1lll1ll1ll_opy_)
    if bstack1l1l1l111_opy_:
      bstack1llll1l11l_opy_ = update(bstack1l1l1l111_opy_, bstack1llll1l11l_opy_)
    desired_capabilities = None
  if options:
    bstack1ll11lll1_opy_(options, bstack1llll1l11l_opy_)
  if not options:
    options = bstack1llll111l_opy_(bstack1llll1l11l_opy_)
  bstack1l1lll111l_opy_ = CONFIG.get(bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨય"))[bstack1l1l1111ll_opy_]
  if proxy and bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ર")):
    options.proxy(proxy)
  if options and bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭઱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111l111l1_opy_() < version.parse(bstack11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧલ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1llll1l11l_opy_)
  logger.info(bstack1lll11lll1_opy_)
  bstack1l1ll1111_opy_.end(EVENTS.bstack1ll1ll1l1_opy_.value, EVENTS.bstack1ll1ll1l1_opy_.value + bstack11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤળ"), EVENTS.bstack1ll1ll1l1_opy_.value + bstack11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ઴"), status=True, failure=None, test_name=bstack1ll111lll1_opy_)
  if bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫવ")):
    bstack1lll111111_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫશ")):
    bstack1lll111111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ષ")):
    bstack1lll111111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll111111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack111lll11l_opy_ = bstack11_opy_ (u"ࠧࠨસ")
    if bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩહ")):
      bstack111lll11l_opy_ = self.caps.get(bstack11_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ઺"))
    else:
      bstack111lll11l_opy_ = self.capabilities.get(bstack11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ઻"))
    if bstack111lll11l_opy_:
      bstack1llll1lll_opy_(bstack111lll11l_opy_)
      if bstack111l111l1_opy_() <= version.parse(bstack11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳઼ࠫ")):
        self.command_executor._url = bstack11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨઽ") + bstack1ll111ll1_opy_ + bstack11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥા")
      else:
        self.command_executor._url = bstack11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤિ") + bstack111lll11l_opy_ + bstack11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤી")
      logger.debug(bstack111ll11l1_opy_.format(bstack111lll11l_opy_))
    else:
      logger.debug(bstack1l11l11l1_opy_.format(bstack11_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥુ")))
  except Exception as e:
    logger.debug(bstack1l11l11l1_opy_.format(e))
  if bstack11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૂ") in bstack1l1ll111ll_opy_:
    bstack111l1l1ll_opy_(bstack11lllll11_opy_, bstack11ll1l11ll_opy_)
  bstack11l111l1_opy_ = self.session_id
  if bstack11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫૃ") in bstack1l1ll111ll_opy_ or bstack11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬૄ") in bstack1l1ll111ll_opy_ or bstack11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬૅ") in bstack1l1ll111ll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l1llll1l1_opy_ = getattr(threading.current_thread(), bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૆"), None)
  if bstack11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨે") in bstack1l1ll111ll_opy_ or bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨૈ") in bstack1l1ll111ll_opy_:
    bstack111lllll1_opy_.bstack11ll1ll1ll_opy_(self)
  if bstack11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪૉ") in bstack1l1ll111ll_opy_ and bstack1l1llll1l1_opy_ and bstack1l1llll1l1_opy_.get(bstack11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૊"), bstack11_opy_ (u"ࠬ࠭ો")) == bstack11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૌ"):
    bstack111lllll1_opy_.bstack11ll1ll1ll_opy_(self)
  bstack1l1lll1ll_opy_.append(self)
  if bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ્ࠪ") in CONFIG and bstack11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭૎") in CONFIG[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૏")][bstack1l1l1111ll_opy_]:
    bstack1ll111lll1_opy_ = CONFIG[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૐ")][bstack1l1l1111ll_opy_][bstack11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૑")]
  logger.debug(bstack1111llll1_opy_.format(bstack11l111l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11l1111l_opy_
    def bstack1ll1l11lll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l11111l1l_opy_
      if(bstack11_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ૒") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11_opy_ (u"࠭ࡾࠨ૓")), bstack11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ૔"), bstack11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ૕")), bstack11_opy_ (u"ࠩࡺࠫ૖")) as fp:
          fp.write(bstack11_opy_ (u"ࠥࠦ૗"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૘")))):
          with open(args[1], bstack11_opy_ (u"ࠬࡸࠧ૙")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬ૚") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11lllll1ll_opy_)
            if bstack11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ૛") in CONFIG and str(CONFIG[bstack11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ૜")]).lower() != bstack11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ૝"):
                bstack1l1llllll_opy_ = bstack11l1111l_opy_()
                bstack1111lllll_opy_ = bstack11_opy_ (u"ࠪࠫࠬࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡁࠊࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡁࠊࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡣࡰࡰࡶࡳࡱ࡫࠮ࡦࡴࡵࡳࡷ࠮ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠤ࠯ࠤࡪࡾࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠࠨࡽࡦࡨࡵ࡛ࡲ࡭ࡿࠪࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭࠱ࠐࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࡿࢀ࠭ࡀࠐࡽࡾ࠽ࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࠧࠨࠩ૞").format(bstack1l1llllll_opy_=bstack1l1llllll_opy_)
            lines.insert(1, bstack1111lllll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૟")), bstack11_opy_ (u"ࠬࡽࠧૠ")) as bstack1lll11llll_opy_:
              bstack1lll11llll_opy_.writelines(lines)
        CONFIG[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨૡ")] = str(bstack1l1ll111ll_opy_) + str(__version__)
        bstack1l11l1l1l_opy_ = os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬૢ")]
        bstack11llll1l_opy_ = bstack1ll11l111l_opy_.bstack1llllll11l_opy_(CONFIG, bstack1l1ll111ll_opy_)
        CONFIG[bstack11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫૣ")] = bstack1l11l1l1l_opy_
        CONFIG[bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૤")] = bstack11llll1l_opy_
        bstack1l1l1111ll_opy_ = 0 if bstack11lllll11_opy_ < 0 else bstack11lllll11_opy_
        try:
          if bstack11llll11_opy_ is True:
            bstack1l1l1111ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll11ll_opy_ is True:
            bstack1l1l1111ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1l1111ll_opy_ = 0
        CONFIG[bstack11_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ૥")] = False
        CONFIG[bstack11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ૦")] = True
        bstack1llll1l11l_opy_ = bstack1l1l1lll1l_opy_(CONFIG, bstack1l1l1111ll_opy_)
        logger.debug(bstack1l111l11l1_opy_.format(str(bstack1llll1l11l_opy_)))
        if CONFIG.get(bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ૧")):
          bstack1l1l1ll1l_opy_(bstack1llll1l11l_opy_)
        if bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨") in CONFIG and bstack11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૩") in CONFIG[bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૪")][bstack1l1l1111ll_opy_]:
          bstack1ll111lll1_opy_ = CONFIG[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૫")][bstack1l1l1111ll_opy_][bstack11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ૬")]
        args.append(os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠫࢃ࠭૭")), bstack11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ૮"), bstack11_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ૯")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1llll1l11l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ૰"))
      bstack1l11111l1l_opy_ = True
      return bstack1ll1ll111l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11lll1lll1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11lllll11_opy_
    global bstack1ll111lll1_opy_
    global bstack11llll11_opy_
    global bstack1lll11ll_opy_
    global bstack1l1ll111ll_opy_
    CONFIG[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ૱")] = str(bstack1l1ll111ll_opy_) + str(__version__)
    bstack1l11l1l1l_opy_ = os.environ[bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ૲")]
    bstack11llll1l_opy_ = bstack1ll11l111l_opy_.bstack1llllll11l_opy_(CONFIG, bstack1l1ll111ll_opy_)
    CONFIG[bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭૳")] = bstack1l11l1l1l_opy_
    CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭૴")] = bstack11llll1l_opy_
    bstack1l1l1111ll_opy_ = 0 if bstack11lllll11_opy_ < 0 else bstack11lllll11_opy_
    try:
      if bstack11llll11_opy_ is True:
        bstack1l1l1111ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll11ll_opy_ is True:
        bstack1l1l1111ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1l1111ll_opy_ = 0
    CONFIG[bstack11_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ૵")] = True
    bstack1llll1l11l_opy_ = bstack1l1l1lll1l_opy_(CONFIG, bstack1l1l1111ll_opy_)
    logger.debug(bstack1l111l11l1_opy_.format(str(bstack1llll1l11l_opy_)))
    if CONFIG.get(bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ૶")):
      bstack1l1l1ll1l_opy_(bstack1llll1l11l_opy_)
    if bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૷") in CONFIG and bstack11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭૸") in CONFIG[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬૹ")][bstack1l1l1111ll_opy_]:
      bstack1ll111lll1_opy_ = CONFIG[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૺ")][bstack1l1l1111ll_opy_][bstack11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩૻ")]
    import urllib
    import json
    if bstack11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩૼ") in CONFIG and str(CONFIG[bstack11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ૽")]).lower() != bstack11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭૾"):
        bstack11ll1111l1_opy_ = bstack11l1111l_opy_()
        bstack1l1llllll_opy_ = bstack11ll1111l1_opy_ + urllib.parse.quote(json.dumps(bstack1llll1l11l_opy_))
    else:
        bstack1l1llllll_opy_ = bstack11_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ૿") + urllib.parse.quote(json.dumps(bstack1llll1l11l_opy_))
    browser = self.connect(bstack1l1llllll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1lllll1_opy_():
    global bstack1l11111l1l_opy_
    global bstack1l1ll111ll_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11111ll1_opy_
        global bstack1l1l1lll1_opy_
        if not bstack1111l1l1l_opy_:
          global bstack1l11ll11ll_opy_
          if not bstack1l11ll11ll_opy_:
            from bstack_utils.helper import bstack11lll11l11_opy_, bstack1llll1lll1_opy_, bstack1l1ll1l11l_opy_
            bstack1l11ll11ll_opy_ = bstack11lll11l11_opy_()
            bstack1llll1lll1_opy_(bstack1l1ll111ll_opy_)
            bstack11llll1l_opy_ = bstack1ll11l111l_opy_.bstack1llllll11l_opy_(CONFIG, bstack1l1ll111ll_opy_)
            bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦ଀"), bstack11llll1l_opy_)
          BrowserType.connect = bstack1l11111ll1_opy_
          return
        BrowserType.launch = bstack11lll1lll1_opy_
        bstack1l11111l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1l11lll_opy_
      bstack1l11111l1l_opy_ = True
    except Exception as e:
      pass
def bstack1l1l1l11l1_opy_(context, bstack1llll1l1l1_opy_):
  try:
    context.page.evaluate(bstack11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦଁ"), bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨଂ")+ json.dumps(bstack1llll1l1l1_opy_) + bstack11_opy_ (u"ࠧࢃࡽࠣଃ"))
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀ࠾ࠥࢁࡽࠣ଄").format(str(e), traceback.format_exc()))
def bstack1l1lll11_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଅ"), bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଆ") + json.dumps(message) + bstack11_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬଇ") + json.dumps(level) + bstack11_opy_ (u"ࠪࢁࢂ࠭ଈ"))
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦଉ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1l111l11_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l1l1ll11l_opy_(self, url):
  global bstack1111ll1ll_opy_
  try:
    bstack11l1lll1l_opy_(url)
  except Exception as err:
    logger.debug(bstack11lll11l_opy_.format(str(err)))
  try:
    bstack1111ll1ll_opy_(self, url)
  except Exception as e:
    try:
      bstack11111ll1_opy_ = str(e)
      if any(err_msg in bstack11111ll1_opy_ for err_msg in bstack1l11111l11_opy_):
        bstack11l1lll1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11lll11l_opy_.format(str(err)))
    raise e
def bstack11ll1ll1l_opy_(self):
  global bstack111ll1lll_opy_
  bstack111ll1lll_opy_ = self
  return
def bstack1l1l1l1111_opy_(self):
  global bstack1l11lllll1_opy_
  bstack1l11lllll1_opy_ = self
  return
def bstack1ll11lll_opy_(test_name, bstack1l111ll1_opy_):
  global CONFIG
  if percy.bstack111ll11l_opy_() == bstack11_opy_ (u"ࠧࡺࡲࡶࡧࠥଊ"):
    bstack1ll1l1ll1l_opy_ = os.path.relpath(bstack1l111ll1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1ll1l1ll1l_opy_)
    bstack1ll111llll_opy_ = suite_name + bstack11_opy_ (u"ࠨ࠭ࠣଋ") + test_name
    threading.current_thread().percySessionName = bstack1ll111llll_opy_
def bstack1111l11l_opy_(self, test, *args, **kwargs):
  global bstack1111llll_opy_
  test_name = None
  bstack1l111ll1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l111ll1_opy_ = str(test.source)
  bstack1ll11lll_opy_(test_name, bstack1l111ll1_opy_)
  bstack1111llll_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1ll1l111ll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l1ll111_opy_(driver, bstack1ll111llll_opy_):
  if not bstack1l11llll_opy_ and bstack1ll111llll_opy_:
      bstack1ll1ll1lll_opy_ = {
          bstack11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଌ"): bstack11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ଍"),
          bstack11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ଎"): {
              bstack11_opy_ (u"ࠪࡲࡦࡳࡥࠨଏ"): bstack1ll111llll_opy_
          }
      }
      bstack1lll1l11l1_opy_ = bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩଐ").format(json.dumps(bstack1ll1ll1lll_opy_))
      driver.execute_script(bstack1lll1l11l1_opy_)
  if bstack1lll1l1ll_opy_:
      bstack1l111l1lll_opy_ = {
          bstack11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ଑"): bstack11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ଒"),
          bstack11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଓ"): {
              bstack11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ଔ"): bstack1ll111llll_opy_ + bstack11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫକ"),
              bstack11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଖ"): bstack11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩଗ")
          }
      }
      if bstack1lll1l1ll_opy_.status == bstack11_opy_ (u"ࠬࡖࡁࡔࡕࠪଘ"):
          bstack1l11l11111_opy_ = bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫଙ").format(json.dumps(bstack1l111l1lll_opy_))
          driver.execute_script(bstack1l11l11111_opy_)
          bstack1l111l111_opy_(driver, bstack11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଚ"))
      elif bstack1lll1l1ll_opy_.status == bstack11_opy_ (u"ࠨࡈࡄࡍࡑ࠭ଛ"):
          reason = bstack11_opy_ (u"ࠤࠥଜ")
          bstack111l11l1l_opy_ = bstack1ll111llll_opy_ + bstack11_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫଝ")
          if bstack1lll1l1ll_opy_.message:
              reason = str(bstack1lll1l1ll_opy_.message)
              bstack111l11l1l_opy_ = bstack111l11l1l_opy_ + bstack11_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫଞ") + reason
          bstack1l111l1lll_opy_[bstack11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଟ")] = {
              bstack11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬଠ"): bstack11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ଡ"),
              bstack11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ଢ"): bstack111l11l1l_opy_
          }
          bstack1l11l11111_opy_ = bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧଣ").format(json.dumps(bstack1l111l1lll_opy_))
          driver.execute_script(bstack1l11l11111_opy_)
          bstack1l111l111_opy_(driver, bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪତ"), reason)
          bstack1ll1lll1_opy_(reason, str(bstack1lll1l1ll_opy_), str(bstack11lllll11_opy_), logger)
@measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1ll1lllll1_opy_(driver, test):
  if percy.bstack111ll11l_opy_() == bstack11_opy_ (u"ࠦࡹࡸࡵࡦࠤଥ") and percy.bstack1l1lll11l_opy_() == bstack11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢଦ"):
      bstack1111l111l_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଧ"), None)
      bstack1111l1l1_opy_(driver, bstack1111l111l_opy_, test)
  if bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫନ"), None) and bstack1llllll111_opy_(
          threading.current_thread(), bstack11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ଩"), None):
      logger.info(bstack11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤପ"))
      bstack1111l1111_opy_.bstack1l1llll1l_opy_(driver, name=test.name, path=test.source)
def bstack1ll1l1l111_opy_(test, bstack1ll111llll_opy_):
    try:
      bstack11lllll1l_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11_opy_ (u"ࠪࡲࡦࡳࡥࠨଫ")] = bstack1ll111llll_opy_
      if bstack1lll1l1ll_opy_:
        if bstack1lll1l1ll_opy_.status == bstack11_opy_ (u"ࠫࡕࡇࡓࡔࠩବ"):
          data[bstack11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬଭ")] = bstack11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ମ")
        elif bstack1lll1l1ll_opy_.status == bstack11_opy_ (u"ࠧࡇࡃࡌࡐࠬଯ"):
          data[bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨର")] = bstack11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଱")
          if bstack1lll1l1ll_opy_.message:
            data[bstack11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪଲ")] = str(bstack1lll1l1ll_opy_.message)
      user = CONFIG[bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ଳ")]
      key = CONFIG[bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ଴")]
      url = bstack11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫଵ").format(user, key, bstack11l111l1_opy_)
      headers = {
        bstack11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ଶ"): bstack11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫଷ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲࡧࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸࠨସ"), datetime.datetime.now() - bstack11lllll1l_opy_)
    except Exception as e:
      logger.error(bstack1l11ll1ll_opy_.format(str(e)))
def bstack1l1l1lllll_opy_(test, bstack1ll111llll_opy_):
  global CONFIG
  global bstack1l11lllll1_opy_
  global bstack111ll1lll_opy_
  global bstack11l111l1_opy_
  global bstack1lll1l1ll_opy_
  global bstack1ll111lll1_opy_
  global bstack1lllll1l1_opy_
  global bstack1lll1l1111_opy_
  global bstack1l11llll11_opy_
  global bstack111l11ll_opy_
  global bstack1l1lll1ll_opy_
  global bstack1l1lll111l_opy_
  try:
    if not bstack11l111l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠪࢂࠬହ")), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ଺"), bstack11_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ଻"))) as f:
        bstack1ll11l111_opy_ = json.loads(bstack11_opy_ (u"ࠨࡻ଼ࠣ") + f.read().strip() + bstack11_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩଽ") + bstack11_opy_ (u"ࠣࡿࠥା"))
        bstack11l111l1_opy_ = bstack1ll11l111_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1lll1ll_opy_:
    for driver in bstack1l1lll1ll_opy_:
      if bstack11l111l1_opy_ == driver.session_id:
        if test:
          bstack1ll1lllll1_opy_(driver, test)
        bstack1l1ll111_opy_(driver, bstack1ll111llll_opy_)
  elif bstack11l111l1_opy_:
    bstack1ll1l1l111_opy_(test, bstack1ll111llll_opy_)
  if bstack1l11lllll1_opy_:
    bstack1lll1l1111_opy_(bstack1l11lllll1_opy_)
  if bstack111ll1lll_opy_:
    bstack1l11llll11_opy_(bstack111ll1lll_opy_)
  if bstack1l111ll111_opy_:
    bstack111l11ll_opy_()
def bstack1l1l1llll1_opy_(self, test, *args, **kwargs):
  bstack1ll111llll_opy_ = None
  if test:
    bstack1ll111llll_opy_ = str(test.name)
  bstack1l1l1lllll_opy_(test, bstack1ll111llll_opy_)
  bstack1lllll1l1_opy_(self, test, *args, **kwargs)
def bstack11l1111l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll1l1l_opy_
  global CONFIG
  global bstack1l1lll1ll_opy_
  global bstack11l111l1_opy_
  bstack11l1ll1111_opy_ = None
  try:
    if bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨି"), None):
      try:
        if not bstack11l111l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠪࢂࠬୀ")), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫୁ"), bstack11_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧୂ"))) as f:
            bstack1ll11l111_opy_ = json.loads(bstack11_opy_ (u"ࠨࡻࠣୃ") + f.read().strip() + bstack11_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩୄ") + bstack11_opy_ (u"ࠣࡿࠥ୅"))
            bstack11l111l1_opy_ = bstack1ll11l111_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l1lll1ll_opy_:
        for driver in bstack1l1lll1ll_opy_:
          if bstack11l111l1_opy_ == driver.session_id:
            bstack11l1ll1111_opy_ = driver
    bstack11l1lllll1_opy_ = bstack1111l1111_opy_.bstack11ll1lllll_opy_(test.tags)
    if bstack11l1ll1111_opy_:
      threading.current_thread().isA11yTest = bstack1111l1111_opy_.bstack1111ll111_opy_(bstack11l1ll1111_opy_, bstack11l1lllll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l1lllll1_opy_
  except:
    pass
  bstack1llll1l1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1lll1l1ll_opy_
  try:
    bstack1lll1l1ll_opy_ = self._test
  except:
    bstack1lll1l1ll_opy_ = self.test
def bstack1lllll1ll1_opy_():
  global bstack1l1l1111l1_opy_
  try:
    if os.path.exists(bstack1l1l1111l1_opy_):
      os.remove(bstack1l1l1111l1_opy_)
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ୆") + str(e))
def bstack1l11l111l1_opy_():
  global bstack1l1l1111l1_opy_
  bstack11111111l_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1l1111l1_opy_):
      with open(bstack1l1l1111l1_opy_, bstack11_opy_ (u"ࠪࡻࠬେ")):
        pass
      with open(bstack1l1l1111l1_opy_, bstack11_opy_ (u"ࠦࡼ࠱ࠢୈ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1l1111l1_opy_):
      bstack11111111l_opy_ = json.load(open(bstack1l1l1111l1_opy_, bstack11_opy_ (u"ࠬࡸࡢࠨ୉")))
  except Exception as e:
    logger.debug(bstack11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୊") + str(e))
  finally:
    return bstack11111111l_opy_
def bstack111l1l1ll_opy_(platform_index, item_index):
  global bstack1l1l1111l1_opy_
  try:
    bstack11111111l_opy_ = bstack1l11l111l1_opy_()
    bstack11111111l_opy_[item_index] = platform_index
    with open(bstack1l1l1111l1_opy_, bstack11_opy_ (u"ࠢࡸ࠭ࠥୋ")) as outfile:
      json.dump(bstack11111111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ୌ") + str(e))
def bstack1llllll1ll_opy_(bstack1llll1ll_opy_):
  global CONFIG
  bstack1l11lll1l_opy_ = bstack11_opy_ (u"୍ࠩࠪ")
  if not bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୎") in CONFIG:
    logger.info(bstack11_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ୏"))
  try:
    platform = CONFIG[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୐")][bstack1llll1ll_opy_]
    if bstack11_opy_ (u"࠭࡯ࡴࠩ୑") in platform:
      bstack1l11lll1l_opy_ += str(platform[bstack11_opy_ (u"ࠧࡰࡵࠪ୒")]) + bstack11_opy_ (u"ࠨ࠮ࠣࠫ୓")
    if bstack11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ୔") in platform:
      bstack1l11lll1l_opy_ += str(platform[bstack11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୕")]) + bstack11_opy_ (u"ࠫ࠱ࠦࠧୖ")
    if bstack11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩୗ") in platform:
      bstack1l11lll1l_opy_ += str(platform[bstack11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ୘")]) + bstack11_opy_ (u"ࠧ࠭ࠢࠪ୙")
    if bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ୚") in platform:
      bstack1l11lll1l_opy_ += str(platform[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ୛")]) + bstack11_opy_ (u"ࠪ࠰ࠥ࠭ଡ଼")
    if bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଢ଼") in platform:
      bstack1l11lll1l_opy_ += str(platform[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୞")]) + bstack11_opy_ (u"࠭ࠬࠡࠩୟ")
    if bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨୠ") in platform:
      bstack1l11lll1l_opy_ += str(platform[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩୡ")]) + bstack11_opy_ (u"ࠩ࠯ࠤࠬୢ")
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪୣ") + str(e))
  finally:
    if bstack1l11lll1l_opy_[len(bstack1l11lll1l_opy_) - 2:] == bstack11_opy_ (u"ࠫ࠱ࠦࠧ୤"):
      bstack1l11lll1l_opy_ = bstack1l11lll1l_opy_[:-2]
    return bstack1l11lll1l_opy_
def bstack1lll11ll1_opy_(path, bstack1l11lll1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1l11l111_opy_ = ET.parse(path)
    bstack11lll11ll_opy_ = bstack1l1l11l111_opy_.getroot()
    bstack1ll111111_opy_ = None
    for suite in bstack11lll11ll_opy_.iter(bstack11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୥")):
      if bstack11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭୦") in suite.attrib:
        suite.attrib[bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ୧")] += bstack11_opy_ (u"ࠨࠢࠪ୨") + bstack1l11lll1l_opy_
        bstack1ll111111_opy_ = suite
    bstack1lllll1ll_opy_ = None
    for robot in bstack11lll11ll_opy_.iter(bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ୩")):
      bstack1lllll1ll_opy_ = robot
    bstack1ll1llll1_opy_ = len(bstack1lllll1ll_opy_.findall(bstack11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ୪")))
    if bstack1ll1llll1_opy_ == 1:
      bstack1lllll1ll_opy_.remove(bstack1lllll1ll_opy_.findall(bstack11_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ୫"))[0])
      bstack11ll1l1ll_opy_ = ET.Element(bstack11_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୬"), attrib={bstack11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ୭"): bstack11_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ୮"), bstack11_opy_ (u"ࠨ࡫ࡧࠫ୯"): bstack11_opy_ (u"ࠩࡶ࠴ࠬ୰")})
      bstack1lllll1ll_opy_.insert(1, bstack11ll1l1ll_opy_)
      bstack1l1llllll1_opy_ = None
      for suite in bstack1lllll1ll_opy_.iter(bstack11_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩୱ")):
        bstack1l1llllll1_opy_ = suite
      bstack1l1llllll1_opy_.append(bstack1ll111111_opy_)
      bstack11l111l1l_opy_ = None
      for status in bstack1ll111111_opy_.iter(bstack11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ୲")):
        bstack11l111l1l_opy_ = status
      bstack1l1llllll1_opy_.append(bstack11l111l1l_opy_)
    bstack1l1l11l111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪ୳") + str(e))
def bstack1l1ll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11lll1ll1_opy_
  global CONFIG
  if bstack11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥ୴") in options:
    del options[bstack11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦ୵")]
  bstack1l11ll1lll_opy_ = bstack1l11l111l1_opy_()
  for bstack1llllllll1_opy_ in bstack1l11ll1lll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11_opy_ (u"ࠨࡲࡤࡦࡴࡺ࡟ࡳࡧࡶࡹࡱࡺࡳࠨ୶"), str(bstack1llllllll1_opy_), bstack11_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭୷"))
    bstack1lll11ll1_opy_(path, bstack1llllll1ll_opy_(bstack1l11ll1lll_opy_[bstack1llllllll1_opy_]))
  bstack1lllll1ll1_opy_()
  return bstack11lll1ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1l1ll1_opy_(self, ff_profile_dir):
  global bstack1l1l1l1l_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1l1l1l_opy_(self, ff_profile_dir)
def bstack1ll1l1111l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l11l111_opy_
  bstack1l1llll111_opy_ = []
  if bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୸") in CONFIG:
    bstack1l1llll111_opy_ = CONFIG[bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୹")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨ୺")],
      pabot_args[bstack11_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢ୻")],
      argfile,
      pabot_args.get(bstack11_opy_ (u"ࠢࡩ࡫ࡹࡩࠧ୼")),
      pabot_args[bstack11_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦ୽")],
      platform[0],
      bstack1l11l111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤ୾")] or [(bstack11_opy_ (u"ࠥࠦ୿"), None)]
    for platform in enumerate(bstack1l1llll111_opy_)
  ]
def bstack1l11lll111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1l1111_opy_=bstack11_opy_ (u"ࠫࠬ஀")):
  global bstack1lll1lll11_opy_
  self.platform_index = platform_index
  self.bstack11l11ll1_opy_ = bstack1ll1l1111_opy_
  bstack1lll1lll11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l1l11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll11l1l_opy_
  global bstack1l111l1l_opy_
  bstack11lll1111l_opy_ = copy.deepcopy(item)
  if not bstack11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ஁") in item.options:
    bstack11lll1111l_opy_.options[bstack11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨஂ")] = []
  bstack1l111l1l1_opy_ = bstack11lll1111l_opy_.options[bstack11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩஃ")].copy()
  for v in bstack11lll1111l_opy_.options[bstack11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ஄")]:
    if bstack11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨஅ") in v:
      bstack1l111l1l1_opy_.remove(v)
    if bstack11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪஆ") in v:
      bstack1l111l1l1_opy_.remove(v)
    if bstack11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨஇ") in v:
      bstack1l111l1l1_opy_.remove(v)
  bstack1l111l1l1_opy_.insert(0, bstack11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧஈ").format(bstack11lll1111l_opy_.platform_index))
  bstack1l111l1l1_opy_.insert(0, bstack11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭உ").format(bstack11lll1111l_opy_.bstack11l11ll1_opy_))
  bstack11lll1111l_opy_.options[bstack11_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩஊ")] = bstack1l111l1l1_opy_
  if bstack1l111l1l_opy_:
    bstack11lll1111l_opy_.options[bstack11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ஋")].insert(0, bstack11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬ஌").format(bstack1l111l1l_opy_))
  return bstack1ll11l1l_opy_(caller_id, datasources, is_last, bstack11lll1111l_opy_, outs_dir)
def bstack1l1111lll_opy_(command, item_index):
  if bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ஍")):
    os.environ[bstack11_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬஎ")] = json.dumps(CONFIG[bstack11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨஏ")][item_index % bstack1l1l1lll11_opy_])
  global bstack1l111l1l_opy_
  if bstack1l111l1l_opy_:
    command[0] = command[0].replace(bstack11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬஐ"), bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ஑") + str(
      item_index) + bstack11_opy_ (u"ࠨࠢࠪஒ") + bstack1l111l1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨஓ"),
                                    bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧஔ") + str(item_index), 1)
def bstack1l111ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1llll11_opy_
  bstack1l1111lll_opy_(command, item_index)
  return bstack11l1llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1lllll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1llll11_opy_
  bstack1l1111lll_opy_(command, item_index)
  return bstack11l1llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1llll11_opy_
  bstack1l1111lll_opy_(command, item_index)
  return bstack11l1llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack111ll1l11_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1l11ll1l_opy_
  bstack1l11ll1ll1_opy_ = bstack1l1l11ll1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫக")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩ஖")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l11ll1ll1_opy_
def bstack11lll1l1l_opy_(runner, hook_name, context, element, bstack1111l1l11_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1ll1l1l_opy_.bstack1ll11l1ll_opy_(hook_name, element)
    bstack1111l1l11_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll1ll1l1l_opy_.bstack111111l1l_opy_(element)
      if hook_name not in [bstack11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ஗"), bstack11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ஘")] and args and hasattr(args[0], bstack11_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨங")):
        args[0].error_message = bstack11_opy_ (u"ࠩࠪச")
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬ஛").format(str(e)))
@measure(event_name=EVENTS.bstack1lll11l11_opy_, stage=STAGE.bstack1lll11111l_opy_, hook_type=bstack11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢஜ"), bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l1lll1111_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    if runner.hooks.get(bstack11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ஝")).__name__ != bstack11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤஞ"):
      bstack11lll1l1l_opy_(runner, name, context, runner, bstack1111l1l11_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l1l1l111l_opy_(bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ட")) else context.browser
      runner.driver_initialised = bstack11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ஠")
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭஡").format(str(e)))
def bstack1111ll11l_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    bstack11lll1l1l_opy_(runner, name, context, context.feature, bstack1111l1l11_opy_, *args)
    try:
      if not bstack1l11llll_opy_:
        bstack11l1ll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l111l_opy_(bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ஢")) else context.browser
        if is_driver_active(bstack11l1ll1111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧண")
          bstack1llll1l1l1_opy_ = str(runner.feature.name)
          bstack1l1l1l11l1_opy_(context, bstack1llll1l1l1_opy_)
          bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪத") + json.dumps(bstack1llll1l1l1_opy_) + bstack11_opy_ (u"࠭ࡽࡾࠩ஥"))
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ஦").format(str(e)))
def bstack11111l11l_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    if hasattr(context, bstack11_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ஧")):
        bstack1ll1ll1l1l_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫந")) else context.feature
    bstack11lll1l1l_opy_(runner, name, context, target, bstack1111l1l11_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l111lll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1lll111lll_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll1ll1l1l_opy_.start_test(context)
    bstack11lll1l1l_opy_(runner, name, context, context.scenario, bstack1111l1l11_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1111l1l_opy_.bstack111ll111_opy_(context, *args)
    try:
      bstack11l1ll1111_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩன"), context.browser)
      if is_driver_active(bstack11l1ll1111_opy_):
        bstack111lllll1_opy_.bstack11ll1ll1ll_opy_(bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪப"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ஫")
        if (not bstack1l11llll_opy_):
          scenario_name = args[0].name
          feature_name = bstack1llll1l1l1_opy_ = str(runner.feature.name)
          bstack1llll1l1l1_opy_ = feature_name + bstack11_opy_ (u"࠭ࠠ࠮ࠢࠪ஬") + scenario_name
          if runner.driver_initialised == bstack11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ஭"):
            bstack1l1l1l11l1_opy_(context, bstack1llll1l1l1_opy_)
            bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ம") + json.dumps(bstack1llll1l1l1_opy_) + bstack11_opy_ (u"ࠩࢀࢁࠬய"))
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫர").format(str(e)))
@measure(event_name=EVENTS.bstack1lll11l11_opy_, stage=STAGE.bstack1lll11111l_opy_, hook_type=bstack11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡗࡹ࡫ࡰࠣற"), bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack111l1lll_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    bstack11lll1l1l_opy_(runner, name, context, args[0], bstack1111l1l11_opy_, *args)
    try:
      bstack11l1ll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l111l_opy_(bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫல")) else context.browser
      if is_driver_active(bstack11l1ll1111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦள")
        bstack1ll1ll1l1l_opy_.bstack1lllll11l_opy_(args[0])
        if runner.driver_initialised == bstack11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧழ"):
          feature_name = bstack1llll1l1l1_opy_ = str(runner.feature.name)
          bstack1llll1l1l1_opy_ = feature_name + bstack11_opy_ (u"ࠨࠢ࠰ࠤࠬவ") + context.scenario.name
          bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧஶ") + json.dumps(bstack1llll1l1l1_opy_) + bstack11_opy_ (u"ࠪࢁࢂ࠭ஷ"))
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨஸ").format(str(e)))
@measure(event_name=EVENTS.bstack1lll11l11_opy_, stage=STAGE.bstack1lll11111l_opy_, hook_type=bstack11_opy_ (u"ࠧࡧࡦࡵࡧࡵࡗࡹ࡫ࡰࠣஹ"), bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1l1l1l11l_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
  bstack1ll1ll1l1l_opy_.bstack1ll1ll1l_opy_(args[0])
  try:
    bstack11l1l111_opy_ = args[0].status.name
    bstack11l1ll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ஺") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack11l1ll1111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ஻")
        feature_name = bstack1llll1l1l1_opy_ = str(runner.feature.name)
        bstack1llll1l1l1_opy_ = feature_name + bstack11_opy_ (u"ࠨࠢ࠰ࠤࠬ஼") + context.scenario.name
        bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ஽") + json.dumps(bstack1llll1l1l1_opy_) + bstack11_opy_ (u"ࠪࢁࢂ࠭ா"))
    if str(bstack11l1l111_opy_).lower() == bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫி"):
      bstack1l1l111ll_opy_ = bstack11_opy_ (u"ࠬ࠭ீ")
      bstack11lll1l111_opy_ = bstack11_opy_ (u"࠭ࠧு")
      bstack11lll11ll1_opy_ = bstack11_opy_ (u"ࠧࠨூ")
      try:
        import traceback
        bstack1l1l111ll_opy_ = runner.exception.__class__.__name__
        bstack1lll11l111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11lll1l111_opy_ = bstack11_opy_ (u"ࠨࠢࠪ௃").join(bstack1lll11l111_opy_)
        bstack11lll11ll1_opy_ = bstack1lll11l111_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1lll1_opy_.format(str(e)))
      bstack1l1l111ll_opy_ += bstack11lll11ll1_opy_
      bstack1l1lll11_opy_(context, json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௄") + str(bstack11lll1l111_opy_)),
                          bstack11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௅"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤெ"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11_opy_ (u"ࠬࡶࡡࡨࡧࠪே"), None), bstack11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨை"), bstack1l1l111ll_opy_)
        bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௉") + json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢொ") + str(bstack11lll1l111_opy_)) + bstack11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩோ"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣௌ"):
        bstack1l111l111_opy_(bstack11l1ll1111_opy_, bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧ்ࠫ"), bstack11_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ௎") + str(bstack1l1l111ll_opy_))
    else:
      bstack1l1lll11_opy_(context, bstack11_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ௏"), bstack11_opy_ (u"ࠢࡪࡰࡩࡳࠧௐ"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ௑"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௒"), None), bstack11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ௓"))
      bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௔") + json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ௕")) + bstack11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ௖"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧௗ"):
        bstack1l111l111_opy_(bstack11l1ll1111_opy_, bstack11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ௘"))
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ௙").format(str(e)))
  bstack11lll1l1l_opy_(runner, name, context, args[0], bstack1111l1l11_opy_, *args)
@measure(event_name=EVENTS.bstack1lll11l1l1_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1ll111l11l_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
  bstack1ll1ll1l1l_opy_.end_test(args[0])
  try:
    bstack11ll11l111_opy_ = args[0].status.name
    bstack11l1ll1111_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௚"), context.browser)
    bstack1l1111l1l_opy_.bstack11lll111l1_opy_(bstack11l1ll1111_opy_)
    if str(bstack11ll11l111_opy_).lower() == bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௛"):
      bstack1l1l111ll_opy_ = bstack11_opy_ (u"ࠬ࠭௜")
      bstack11lll1l111_opy_ = bstack11_opy_ (u"࠭ࠧ௝")
      bstack11lll11ll1_opy_ = bstack11_opy_ (u"ࠧࠨ௞")
      try:
        import traceback
        bstack1l1l111ll_opy_ = runner.exception.__class__.__name__
        bstack1lll11l111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11lll1l111_opy_ = bstack11_opy_ (u"ࠨࠢࠪ௟").join(bstack1lll11l111_opy_)
        bstack11lll11ll1_opy_ = bstack1lll11l111_opy_[-1]
      except Exception as e:
        logger.debug(bstack11ll1lll1_opy_.format(str(e)))
      bstack1l1l111ll_opy_ += bstack11lll11ll1_opy_
      bstack1l1lll11_opy_(context, json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௠") + str(bstack11lll1l111_opy_)),
                          bstack11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௡"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௢") or runner.driver_initialised == bstack11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௣"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11_opy_ (u"࠭ࡰࡢࡩࡨࠫ௤"), None), bstack11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ௥"), bstack1l1l111ll_opy_)
        bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭௦") + json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௧") + str(bstack11lll1l111_opy_)) + bstack11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ௨"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௩") or runner.driver_initialised == bstack11_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௪"):
        bstack1l111l111_opy_(bstack11l1ll1111_opy_, bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௫"), bstack11_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ௬") + str(bstack1l1l111ll_opy_))
    else:
      bstack1l1lll11_opy_(context, bstack11_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ௭"), bstack11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ௮"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௯") or runner.driver_initialised == bstack11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ௰"):
        bstack1ll11ll1ll_opy_(getattr(context, bstack11_opy_ (u"ࠬࡶࡡࡨࡧࠪ௱"), None), bstack11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௲"))
      bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௳") + json.dumps(str(args[0].name) + bstack11_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ௴")) + bstack11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ௵"))
      if runner.driver_initialised == bstack11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௶") or runner.driver_initialised == bstack11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ௷"):
        bstack1l111l111_opy_(bstack11l1ll1111_opy_, bstack11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ௸"))
  except Exception as e:
    logger.debug(bstack11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ௹").format(str(e)))
  bstack11lll1l1l_opy_(runner, name, context, context.scenario, bstack1111l1l11_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1ll111ll11_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    target = context.scenario if hasattr(context, bstack11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ௺")) else context.feature
    bstack11lll1l1l_opy_(runner, name, context, target, bstack1111l1l11_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l1l1ll1l1_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    try:
      bstack11l1ll1111_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௻"), context.browser)
      bstack1l1111ll11_opy_ = bstack11_opy_ (u"ࠩࠪ௼")
      if context.failed is True:
        bstack1l1l1l1l1_opy_ = []
        bstack11ll11l11_opy_ = []
        bstack1ll11111_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1l1l1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1lll11l111_opy_ = traceback.format_tb(exc_tb)
            bstack1lll11111_opy_ = bstack11_opy_ (u"ࠪࠤࠬ௽").join(bstack1lll11l111_opy_)
            bstack11ll11l11_opy_.append(bstack1lll11111_opy_)
            bstack1ll11111_opy_.append(bstack1lll11l111_opy_[-1])
        except Exception as e:
          logger.debug(bstack11ll1lll1_opy_.format(str(e)))
        bstack1l1l111ll_opy_ = bstack11_opy_ (u"ࠫࠬ௾")
        for i in range(len(bstack1l1l1l1l1_opy_)):
          bstack1l1l111ll_opy_ += bstack1l1l1l1l1_opy_[i] + bstack1ll11111_opy_[i] + bstack11_opy_ (u"ࠬࡢ࡮ࠨ௿")
        bstack1l1111ll11_opy_ = bstack11_opy_ (u"࠭ࠠࠨఀ").join(bstack11ll11l11_opy_)
        if runner.driver_initialised in [bstack11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఁ"), bstack11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧం")]:
          bstack1l1lll11_opy_(context, bstack1l1111ll11_opy_, bstack11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣః"))
          bstack1ll11ll1ll_opy_(getattr(context, bstack11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨఄ"), None), bstack11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఅ"), bstack1l1l111ll_opy_)
          bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪఆ") + json.dumps(bstack1l1111ll11_opy_) + bstack11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ఇ"))
          bstack1l111l111_opy_(bstack11l1ll1111_opy_, bstack11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢఈ"), bstack11_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨఉ") + str(bstack1l1l111ll_opy_))
          bstack1lllll1111_opy_ = bstack1l11lll11_opy_(bstack1l1111ll11_opy_, runner.feature.name, logger)
          if (bstack1lllll1111_opy_ != None):
            bstack1l1l1111_opy_.append(bstack1lllll1111_opy_)
      else:
        if runner.driver_initialised in [bstack11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥఊ"), bstack11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢఋ")]:
          bstack1l1lll11_opy_(context, bstack11_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢఌ") + str(runner.feature.name) + bstack11_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ఍"), bstack11_opy_ (u"ࠨࡩ࡯ࡨࡲࠦఎ"))
          bstack1ll11ll1ll_opy_(getattr(context, bstack11_opy_ (u"ࠧࡱࡣࡪࡩࠬఏ"), None), bstack11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣఐ"))
          bstack11l1ll1111_opy_.execute_script(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ఑") + json.dumps(bstack11_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨఒ") + str(runner.feature.name) + bstack11_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨఓ")) + bstack11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫఔ"))
          bstack1l111l111_opy_(bstack11l1ll1111_opy_, bstack11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭క"))
          bstack1lllll1111_opy_ = bstack1l11lll11_opy_(bstack1l1111ll11_opy_, runner.feature.name, logger)
          if (bstack1lllll1111_opy_ != None):
            bstack1l1l1111_opy_.append(bstack1lllll1111_opy_)
    except Exception as e:
      logger.debug(bstack11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩఖ").format(str(e)))
    bstack11lll1l1l_opy_(runner, name, context, context.feature, bstack1111l1l11_opy_, *args)
@measure(event_name=EVENTS.bstack1lll11l11_opy_, stage=STAGE.bstack1lll11111l_opy_, hook_type=bstack11_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥగ"), bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack11llllll_opy_(runner, name, context, bstack1111l1l11_opy_, *args):
    bstack11lll1l1l_opy_(runner, name, context, runner, bstack1111l1l11_opy_, *args)
def bstack11l1lll1_opy_(self, name, context, *args):
  if bstack1111l1l1l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l1l1lll11_opy_
    bstack1lll111l1l_opy_ = CONFIG[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬఘ")][platform_index]
    os.environ[bstack11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫఙ")] = json.dumps(bstack1lll111l1l_opy_)
  global bstack1111l1l11_opy_
  if not hasattr(self, bstack11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩచ")):
    self.driver_initialised = None
  bstack1ll1l111_opy_ = {
      bstack11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩఛ"): bstack1l1lll1111_opy_,
      bstack11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧజ"): bstack1111ll11l_opy_,
      bstack11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫఝ"): bstack11111l11l_opy_,
      bstack11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪఞ"): bstack1lll111lll_opy_,
      bstack11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧట"): bstack111l1lll_opy_,
      bstack11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧఠ"): bstack1l1l1l11l_opy_,
      bstack11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬడ"): bstack1ll111l11l_opy_,
      bstack11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨఢ"): bstack1ll111ll11_opy_,
      bstack11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ణ"): bstack1l1l1ll1l1_opy_,
      bstack11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪత"): bstack11llllll_opy_
  }
  handler = bstack1ll1l111_opy_.get(name, bstack1111l1l11_opy_)
  handler(self, name, context, bstack1111l1l11_opy_, *args)
  if name in [bstack11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨథ"), bstack11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪద"), bstack11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ధ")]:
    try:
      bstack11l1ll1111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l111l_opy_(bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪన")) else context.browser
      bstack1ll11l11ll_opy_ = (
        (name == bstack11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ఩") and self.driver_initialised == bstack11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥప")) or
        (name == bstack11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧఫ") and self.driver_initialised == bstack11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤబ")) or
        (name == bstack11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪభ") and self.driver_initialised in [bstack11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧమ"), bstack11_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦయ")]) or
        (name == bstack11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩర") and self.driver_initialised == bstack11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦఱ"))
      )
      if bstack1ll11l11ll_opy_:
        self.driver_initialised = None
        bstack11l1ll1111_opy_.quit()
    except Exception:
      pass
def bstack11l1l1l1l_opy_(config, startdir):
  return bstack11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧల").format(bstack11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢళ"))
notset = Notset()
def bstack1ll11lllll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1lll1ll1_opy_
  if str(name).lower() == bstack11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩఴ"):
    return bstack11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤవ")
  else:
    return bstack1l1lll1ll1_opy_(self, name, default, skip)
def bstack1l1l1l1ll_opy_(item, when):
  global bstack11l1ll11l1_opy_
  try:
    bstack11l1ll11l1_opy_(item, when)
  except Exception as e:
    pass
def bstack11l1lll111_opy_():
  return
def bstack1l1ll1llll_opy_(type, name, status, reason, bstack11ll11l1ll_opy_, bstack1l1lll1l_opy_):
  bstack1ll1ll1lll_opy_ = {
    bstack11_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫశ"): type,
    bstack11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨష"): {}
  }
  if type == bstack11_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨస"):
    bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪహ")][bstack11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ఺")] = bstack11ll11l1ll_opy_
    bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ఻")][bstack11_opy_ (u"ࠪࡨࡦࡺࡡࠨ఼")] = json.dumps(str(bstack1l1lll1l_opy_))
  if type == bstack11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఽ"):
    bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨా")][bstack11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫి")] = name
  if type == bstack11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪీ"):
    bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫు")][bstack11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩూ")] = status
    if status == bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪృ"):
      bstack1ll1ll1lll_opy_[bstack11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౄ")][bstack11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ౅")] = json.dumps(str(reason))
  bstack1lll1l11l1_opy_ = bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫె").format(json.dumps(bstack1ll1ll1lll_opy_))
  return bstack1lll1l11l1_opy_
def bstack111lll11_opy_(driver_command, response):
    if driver_command == bstack11_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫే"):
        bstack111lllll1_opy_.bstack1l11ll11l1_opy_({
            bstack11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧై"): response[bstack11_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ౉")],
            bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪొ"): bstack111lllll1_opy_.current_test_uuid()
        })
def bstack11ll11ll1l_opy_(item, call, rep):
  global bstack1l1lll1l1l_opy_
  global bstack1l1lll1ll_opy_
  global bstack1l11llll_opy_
  name = bstack11_opy_ (u"ࠫࠬో")
  try:
    if rep.when == bstack11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪౌ"):
      bstack11l111l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l11llll_opy_:
          name = str(rep.nodeid)
          bstack1lll11l1_opy_ = bstack1l1ll1llll_opy_(bstack11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫్ࠧ"), name, bstack11_opy_ (u"ࠧࠨ౎"), bstack11_opy_ (u"ࠨࠩ౏"), bstack11_opy_ (u"ࠩࠪ౐"), bstack11_opy_ (u"ࠪࠫ౑"))
          threading.current_thread().bstack1lll1lll_opy_ = name
          for driver in bstack1l1lll1ll_opy_:
            if bstack11l111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11l1_opy_)
      except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ౒").format(str(e)))
      try:
        bstack11lll1llll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭౓"):
          status = bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౔") if rep.outcome.lower() == bstack11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪౕࠧ") else bstack11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨౖ")
          reason = bstack11_opy_ (u"ࠩࠪ౗")
          if status == bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪౘ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩౙ") if status == bstack11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬౚ") else bstack11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ౛")
          data = name + bstack11_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ౜") if status == bstack11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨౝ") else name + bstack11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ౞") + reason
          bstack1lll11ll11_opy_ = bstack1l1ll1llll_opy_(bstack11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ౟"), bstack11_opy_ (u"ࠫࠬౠ"), bstack11_opy_ (u"ࠬ࠭ౡ"), bstack11_opy_ (u"࠭ࠧౢ"), level, data)
          for driver in bstack1l1lll1ll_opy_:
            if bstack11l111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1lll11ll11_opy_)
      except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫౣ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ౤").format(str(e)))
  bstack1l1lll1l1l_opy_(item, call, rep)
def bstack1111l1l1_opy_(driver, bstack11llll11l1_opy_, test=None):
  global bstack11lllll11_opy_
  if test != None:
    bstack1l11111ll_opy_ = getattr(test, bstack11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౥"), None)
    bstack1ll1111l11_opy_ = getattr(test, bstack11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ౦"), None)
    PercySDK.screenshot(driver, bstack11llll11l1_opy_, bstack1l11111ll_opy_=bstack1l11111ll_opy_, bstack1ll1111l11_opy_=bstack1ll1111l11_opy_, bstack1ll1ll1ll_opy_=bstack11lllll11_opy_)
  else:
    PercySDK.screenshot(driver, bstack11llll11l1_opy_)
@measure(event_name=EVENTS.bstack11l1lll11_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1ll1111l_opy_(driver):
  if bstack1111111ll_opy_.bstack1ll1l1l1ll_opy_() is True or bstack1111111ll_opy_.capturing() is True:
    return
  bstack1111111ll_opy_.bstack1llll11l_opy_()
  while not bstack1111111ll_opy_.bstack1ll1l1l1ll_opy_():
    bstack1l111ll11_opy_ = bstack1111111ll_opy_.bstack1lll111ll_opy_()
    bstack1111l1l1_opy_(driver, bstack1l111ll11_opy_)
  bstack1111111ll_opy_.bstack11l1l111l_opy_()
def bstack1l111111l_opy_(sequence, driver_command, response = None, bstack1ll111l1l_opy_ = None, args = None):
    try:
      if sequence != bstack11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ౧"):
        return
      if percy.bstack111ll11l_opy_() == bstack11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ౨"):
        return
      bstack1l111ll11_opy_ = bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ౩"), None)
      for command in bstack1lll1l11l_opy_:
        if command == driver_command:
          for driver in bstack1l1lll1ll_opy_:
            bstack1ll1111l_opy_(driver)
      bstack11llll1ll_opy_ = percy.bstack1l1lll11l_opy_()
      if driver_command in bstack1ll11llll1_opy_[bstack11llll1ll_opy_]:
        bstack1111111ll_opy_.bstack111ll1ll1_opy_(bstack1l111ll11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1ll1ll1_opy_(framework_name):
  if bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ౪")):
      return
  bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ౫"), True)
  global bstack1l1ll111ll_opy_
  global bstack1l11111l1l_opy_
  global bstack1ll111ll_opy_
  bstack1l1ll111ll_opy_ = framework_name
  logger.info(bstack1lll1l1lll_opy_.format(bstack1l1ll111ll_opy_.split(bstack11_opy_ (u"ࠩ࠰ࠫ౬"))[0]))
  bstack1l11llll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1111l1l1l_opy_:
      Service.start = bstack11ll1lll_opy_
      Service.stop = bstack1l111ll11l_opy_
      webdriver.Remote.get = bstack1l1l1ll11l_opy_
      WebDriver.close = bstack11lllllll1_opy_
      WebDriver.quit = bstack1l11l1111_opy_
      webdriver.Remote.__init__ = bstack1ll1l111l1_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1111l1l1l_opy_:
        webdriver.Remote.__init__ = bstack1ll1l1ll_opy_
    WebDriver.execute = bstack11lll11lll_opy_
    bstack1l11111l1l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1111l1l1l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll1l1ll1_opy_
  except Exception as e:
    pass
  bstack1l1lllll1_opy_()
  if not bstack1l11111l1l_opy_:
    bstack11ll1l1lll_opy_(bstack11_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ౭"), bstack11l1llll1_opy_)
  if bstack1l11ll111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._11llll1lll_opy_ = bstack11ll11l1l1_opy_
    except Exception as e:
      logger.error(bstack11l1ll1l1_opy_.format(str(e)))
  if bstack11ll1lll11_opy_():
    bstack1l1ll11ll_opy_(CONFIG, logger)
  if (bstack11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౮") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack111ll11l_opy_() == bstack11_opy_ (u"ࠧࡺࡲࡶࡧࠥ౯"):
          bstack1lll1111ll_opy_(bstack1l111111l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1l1ll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1l1l1111_opy_
      except Exception as e:
        logger.warn(bstack11l11l111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11ll1ll1l_opy_
      except Exception as e:
        logger.debug(bstack11l1l1llll_opy_ + str(e))
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11l11l111_opy_)
    Output.start_test = bstack1111l11l_opy_
    Output.end_test = bstack1l1l1llll1_opy_
    TestStatus.__init__ = bstack11l1111l1_opy_
    QueueItem.__init__ = bstack1l11lll111_opy_
    pabot._create_items = bstack1ll1l1111l_opy_
    try:
      from pabot import __version__ as bstack1lll1ll1l1_opy_
      if version.parse(bstack1lll1ll1l1_opy_) >= version.parse(bstack11_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭౰")):
        pabot._run = bstack1llll1111_opy_
      elif version.parse(bstack1lll1ll1l1_opy_) >= version.parse(bstack11_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧ౱")):
        pabot._run = bstack1l1lllll11_opy_
      else:
        pabot._run = bstack1l111ll1l_opy_
    except Exception as e:
      pabot._run = bstack1l111ll1l_opy_
    pabot._create_command_for_execution = bstack1l1l1l11_opy_
    pabot._report_results = bstack1l1ll11l1_opy_
  if bstack11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ౲") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11ll11llll_opy_)
    Runner.run_hook = bstack11l1lll1_opy_
    Step.run = bstack111ll1l11_opy_
  if bstack11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౳") in str(framework_name).lower():
    if not bstack1111l1l1l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l1l1l1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack11l1lll111_opy_
      Config.getoption = bstack1ll11lllll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11ll11ll1l_opy_
    except Exception as e:
      pass
def bstack1lll11l11l_opy_():
  global CONFIG
  if bstack11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ౴") in CONFIG and int(CONFIG[bstack11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ౵")]) > 1:
    logger.warn(bstack111lllll_opy_)
def bstack1l1lllll1l_opy_(arg, bstack1l1ll1l11_opy_, bstack1l1lllllll_opy_=None):
  global CONFIG
  global bstack1ll111ll1_opy_
  global bstack1111ll1l_opy_
  global bstack1111l1l1l_opy_
  global bstack1l1l1lll1_opy_
  bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ౶")
  if bstack1l1ll1l11_opy_ and isinstance(bstack1l1ll1l11_opy_, str):
    bstack1l1ll1l11_opy_ = eval(bstack1l1ll1l11_opy_)
  CONFIG = bstack1l1ll1l11_opy_[bstack11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭౷")]
  bstack1ll111ll1_opy_ = bstack1l1ll1l11_opy_[bstack11_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ౸")]
  bstack1111ll1l_opy_ = bstack1l1ll1l11_opy_[bstack11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ౹")]
  bstack1111l1l1l_opy_ = bstack1l1ll1l11_opy_[bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ౺")]
  bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ౻"), bstack1111l1l1l_opy_)
  os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭౼")] = bstack1ll11lll1l_opy_
  os.environ[bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ౽")] = json.dumps(CONFIG)
  os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭౾")] = bstack1ll111ll1_opy_
  os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ౿")] = str(bstack1111ll1l_opy_)
  os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧಀ")] = str(True)
  if bstack1111l1ll1_opy_(arg, [bstack11_opy_ (u"ࠩ࠰ࡲࠬಁ"), bstack11_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫಂ")]) != -1:
    os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬಃ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll11ll111_opy_)
    return
  bstack11ll1llll_opy_()
  global bstack11ll11lll_opy_
  global bstack11lllll11_opy_
  global bstack1l11l111_opy_
  global bstack1l111l1l_opy_
  global bstack1ll111lll_opy_
  global bstack1ll111ll_opy_
  global bstack11llll11_opy_
  arg.append(bstack11_opy_ (u"ࠧ࠳ࡗࠣ಄"))
  arg.append(bstack11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤಅ"))
  arg.append(bstack11_opy_ (u"ࠢ࠮࡙ࠥಆ"))
  arg.append(bstack11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡖ࡫ࡩࠥ࡮࡯ࡰ࡭࡬ࡱࡵࡲࠢಇ"))
  global bstack1lll111111_opy_
  global bstack11ll1ll11l_opy_
  global bstack1llll1llll_opy_
  global bstack1llll1l1l_opy_
  global bstack1l1l1l1l_opy_
  global bstack1lll1lll11_opy_
  global bstack1ll11l1l_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1111ll1ll_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1l1lll1ll1_opy_
  global bstack11l1ll11l1_opy_
  global bstack1l1lll1l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll111111_opy_ = webdriver.Remote.__init__
    bstack11ll1ll11l_opy_ = WebDriver.quit
    bstack1ll1l11l1l_opy_ = WebDriver.close
    bstack1111ll1ll_opy_ = WebDriver.get
    bstack1llll1llll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l111lll1_opy_(CONFIG) and bstack1ll11l11l1_opy_():
    if bstack111l111l1_opy_() < version.parse(bstack111l111l_opy_):
      logger.error(bstack11l1l11l1_opy_.format(bstack111l111l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll1l1l1l1_opy_ = RemoteConnection._11llll1lll_opy_
      except Exception as e:
        logger.error(bstack11l1ll1l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1lll1ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack11l1ll11l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1llll111ll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1lll1l1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪಈ"))
  bstack1l11l111_opy_ = CONFIG.get(bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧಉ"), {}).get(bstack11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ಊ"))
  bstack11llll11_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1ll111ll1l_opy_():
      bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.CONNECT, bstack1l1lll1l1_opy_())
    platform_index = int(os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಋ"), bstack11_opy_ (u"࠭࠰ࠨಌ")))
  else:
    bstack1l1ll1ll1_opy_(bstack1ll1llll_opy_)
  os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ಍")] = CONFIG[bstack11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪಎ")]
  os.environ[bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬಏ")] = CONFIG[bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಐ")]
  os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ಑")] = bstack1111l1l1l_opy_.__str__()
  from _pytest.config import main as bstack111l11l1_opy_
  bstack1111lll11_opy_ = []
  try:
    bstack11llllll11_opy_ = bstack111l11l1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l1111l11_opy_()
    if bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩಒ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1l1l11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1111lll11_opy_.append(bstack1ll1l1l11l_opy_)
    try:
      bstack11111llll_opy_ = (bstack1111lll11_opy_, int(bstack11llllll11_opy_))
      bstack1l1lllllll_opy_.append(bstack11111llll_opy_)
    except:
      bstack1l1lllllll_opy_.append((bstack1111lll11_opy_, bstack11llllll11_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1111lll11_opy_.append({bstack11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಓ"): bstack11_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩಔ") + os.environ.get(bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨಕ")), bstack11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨಖ"): traceback.format_exc(), bstack11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩಗ"): int(os.environ.get(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫಘ")))})
    bstack1l1lllllll_opy_.append((bstack1111lll11_opy_, 1))
def bstack1l1111l111_opy_(arg):
  global bstack11ll11ll11_opy_
  bstack1l1ll1ll1_opy_(bstack1111l11l1_opy_)
  os.environ[bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ಙ")] = str(bstack1111ll1l_opy_)
  from behave.__main__ import main as bstack11ll111ll1_opy_
  status_code = bstack11ll111ll1_opy_(arg)
  if status_code != 0:
    bstack11ll11ll11_opy_ = status_code
def bstack11ll111l11_opy_():
  logger.info(bstack1l1111ll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬಚ"), help=bstack11_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨಛ"))
  parser.add_argument(bstack11_opy_ (u"ࠨ࠯ࡸࠫಜ"), bstack11_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭ಝ"), help=bstack11_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩಞ"))
  parser.add_argument(bstack11_opy_ (u"ࠫ࠲ࡱࠧಟ"), bstack11_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫಠ"), help=bstack11_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧಡ"))
  parser.add_argument(bstack11_opy_ (u"ࠧ࠮ࡨࠪಢ"), bstack11_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಣ"), help=bstack11_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨತ"))
  bstack1l11l1llll_opy_ = parser.parse_args()
  try:
    bstack1lll1l1l_opy_ = bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧಥ")
    if bstack1l11l1llll_opy_.framework and bstack1l11l1llll_opy_.framework not in (bstack11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫದ"), bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ಧ")):
      bstack1lll1l1l_opy_ = bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬನ")
    bstack111l1ll11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l1l_opy_)
    bstack1ll11l1l1l_opy_ = open(bstack111l1ll11_opy_, bstack11_opy_ (u"ࠧࡳࠩ಩"))
    bstack1l111111l1_opy_ = bstack1ll11l1l1l_opy_.read()
    bstack1ll11l1l1l_opy_.close()
    if bstack1l11l1llll_opy_.username:
      bstack1l111111l1_opy_ = bstack1l111111l1_opy_.replace(bstack11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨಪ"), bstack1l11l1llll_opy_.username)
    if bstack1l11l1llll_opy_.key:
      bstack1l111111l1_opy_ = bstack1l111111l1_opy_.replace(bstack11_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫಫ"), bstack1l11l1llll_opy_.key)
    if bstack1l11l1llll_opy_.framework:
      bstack1l111111l1_opy_ = bstack1l111111l1_opy_.replace(bstack11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಬ"), bstack1l11l1llll_opy_.framework)
    file_name = bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧಭ")
    file_path = os.path.abspath(file_name)
    bstack1l111llll_opy_ = open(file_path, bstack11_opy_ (u"ࠬࡽࠧಮ"))
    bstack1l111llll_opy_.write(bstack1l111111l1_opy_)
    bstack1l111llll_opy_.close()
    logger.info(bstack11ll11l1l_opy_)
    try:
      os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಯ")] = bstack1l11l1llll_opy_.framework if bstack1l11l1llll_opy_.framework != None else bstack11_opy_ (u"ࠢࠣರ")
      config = yaml.safe_load(bstack1l111111l1_opy_)
      config[bstack11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨಱ")] = bstack11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨಲ")
      bstack11l11l1l1_opy_(bstack1llllll1l1_opy_, config)
    except Exception as e:
      logger.debug(bstack11lll111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l1llll1ll_opy_.format(str(e)))
def bstack11l11l1l1_opy_(bstack11llll111_opy_, config, bstack11ll11l1_opy_={}):
  global bstack1111l1l1l_opy_
  global bstack1lll1ll111_opy_
  global bstack1l1l1lll1_opy_
  if not config:
    return
  bstack111l1ll1l_opy_ = bstack11llll1l1l_opy_ if not bstack1111l1l1l_opy_ else (
    bstack1l1l11ll_opy_ if bstack11_opy_ (u"ࠪࡥࡵࡶࠧಳ") in config else (
        bstack1l1ll1111l_opy_ if config.get(bstack11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ಴")) else bstack111l11lll_opy_
    )
)
  bstack1ll1111l1l_opy_ = False
  bstack1ll11l11_opy_ = False
  if bstack1111l1l1l_opy_ is True:
      if bstack11_opy_ (u"ࠬࡧࡰࡱࠩವ") in config:
          bstack1ll1111l1l_opy_ = True
      else:
          bstack1ll11l11_opy_ = True
  bstack11llll1l_opy_ = bstack1ll11l111l_opy_.bstack1llllll11l_opy_(config, bstack1lll1ll111_opy_)
  bstack11ll1l1l1_opy_ = bstack111l11l11_opy_()
  data = {
    bstack11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨಶ"): config[bstack11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩಷ")],
    bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಸ"): config[bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬಹ")],
    bstack11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ಺"): bstack11llll111_opy_,
    bstack11_opy_ (u"ࠫࡩ࡫ࡴࡦࡥࡷࡩࡩࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ಻"): os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ಼ࠧ"), bstack1lll1ll111_opy_),
    bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨಽ"): bstack11ll1ll1_opy_,
    bstack11_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭ࠩಾ"): bstack11ll111l1_opy_(),
    bstack11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫಿ"): {
      bstack11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೀ"): str(config[bstack11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪು")]) if bstack11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫೂ") in config else bstack11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨೃ"),
      bstack11_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡗࡧࡵࡷ࡮ࡵ࡮ࠨೄ"): sys.version,
      bstack11_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩ೅"): bstack11ll11111_opy_(os.environ.get(bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೆ"), bstack1lll1ll111_opy_)),
      bstack11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫೇ"): bstack11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪೈ"),
      bstack11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ೉"): bstack111l1ll1l_opy_,
      bstack11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪೊ"): bstack11llll1l_opy_,
      bstack11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠬೋ"): os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬೌ")],
      bstack11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮್ࠫ"): os.environ.get(bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ೎"), bstack1lll1ll111_opy_),
      bstack11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೏"): bstack11111l1l_opy_(os.environ.get(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೐"), bstack1lll1ll111_opy_)),
      bstack11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ೑"): bstack11ll1l1l1_opy_.get(bstack11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೒")),
      bstack11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೓"): bstack11ll1l1l1_opy_.get(bstack11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ೔")),
      bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೕ"): config[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೖ")] if config[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೗")] else bstack11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ೘"),
      bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೙"): str(config[bstack11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೚")]) if bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೛") in config else bstack11_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ೜"),
      bstack11_opy_ (u"ࠪࡳࡸ࠭ೝ"): sys.platform,
      bstack11_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ೞ"): socket.gethostname(),
      bstack11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ೟"): bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨೠ"))
    }
  }
  if not bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧೡ")) is None:
    data[bstack11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫೢ")][bstack11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡑࡪࡺࡡࡥࡣࡷࡥࠬೣ")] = {
      bstack11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ೤"): bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ೥"),
      bstack11_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬ೦"): bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭೧")),
      bstack11_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࡎࡶ࡯ࡥࡩࡷ࠭೨"): bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡐࡲࠫ೩"))
    }
  if bstack11llll111_opy_ == bstack11l111111_opy_:
    data[bstack11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೪")][bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࠨ೫")] = bstack11lll111l_opy_(config)
    data[bstack11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೬")][bstack11_opy_ (u"ࠬ࡯ࡳࡑࡧࡵࡧࡾࡇࡵࡵࡱࡈࡲࡦࡨ࡬ࡦࡦࠪ೭")] = percy.bstack1ll11lll11_opy_
    data[bstack11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ೮")][bstack11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡈࡵࡪ࡮ࡧࡍࡩ࠭೯")] = percy.percy_build_id
  update(data[bstack11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ೰")], bstack11ll11l1_opy_)
  try:
    response = bstack111111ll_opy_(bstack11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧೱ"), bstack11l1l1ll1l_opy_(bstack1l11l111ll_opy_), data, {
      bstack11_opy_ (u"ࠪࡥࡺࡺࡨࠨೲ"): (config[bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೳ")], config[bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೴")])
    })
    if response:
      logger.debug(bstack1l111l111l_opy_.format(bstack11llll111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lll1ll1l_opy_.format(str(e)))
def bstack11ll11111_opy_(framework):
  return bstack11_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ೵").format(str(framework), __version__) if framework else bstack11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ೶").format(
    __version__)
def bstack11ll1llll_opy_():
  global CONFIG
  global bstack11l11ll11_opy_
  if bool(CONFIG):
    return
  try:
    bstack11ll1l11l1_opy_()
    logger.debug(bstack111l1l11l_opy_.format(str(CONFIG)))
    bstack11l11ll11_opy_ = bstack11l11l1l_opy_.bstack1lll11ll1l_opy_(CONFIG, bstack11l11ll11_opy_)
    bstack1l11llll1_opy_()
  except Exception as e:
    logger.error(bstack11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧ೷") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1ll1l1ll_opy_
  atexit.register(bstack11lll1l1l1_opy_)
  signal.signal(signal.SIGINT, bstack1l1ll11ll1_opy_)
  signal.signal(signal.SIGTERM, bstack1l1ll11ll1_opy_)
def bstack1l1ll1l1ll_opy_(exctype, value, traceback):
  global bstack1l1lll1ll_opy_
  try:
    for driver in bstack1l1lll1ll_opy_:
      bstack1l111l111_opy_(driver, bstack11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ೸"), bstack11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ೹") + str(value))
  except Exception:
    pass
  logger.info(bstack11llllllll_opy_)
  bstack11l11111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11l11111_opy_(message=bstack11_opy_ (u"ࠫࠬ೺"), bstack1llll111_opy_ = False):
  global CONFIG
  bstack1l11llll1l_opy_ = bstack11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧ೻") if bstack1llll111_opy_ else bstack11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ೼")
  try:
    if message:
      bstack11ll11l1_opy_ = {
        bstack1l11llll1l_opy_ : str(message)
      }
      bstack11l11l1l1_opy_(bstack11l111111_opy_, CONFIG, bstack11ll11l1_opy_)
    else:
      bstack11l11l1l1_opy_(bstack11l111111_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1ll1ll1l_opy_.format(str(e)))
def bstack1ll111l111_opy_(bstack1l1ll11l11_opy_, size):
  bstack1l11l111l_opy_ = []
  while len(bstack1l1ll11l11_opy_) > size:
    bstack1l1lll1lll_opy_ = bstack1l1ll11l11_opy_[:size]
    bstack1l11l111l_opy_.append(bstack1l1lll1lll_opy_)
    bstack1l1ll11l11_opy_ = bstack1l1ll11l11_opy_[size:]
  bstack1l11l111l_opy_.append(bstack1l1ll11l11_opy_)
  return bstack1l11l111l_opy_
def bstack11lll1ll_opy_(args):
  if bstack11_opy_ (u"ࠧ࠮࡯ࠪ೽") in args and bstack11_opy_ (u"ࠨࡲࡧࡦࠬ೾") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1ll1ll1l1_opy_, stage=STAGE.bstack1l11l1lll1_opy_)
def run_on_browserstack(bstack1ll1lll1ll_opy_=None, bstack1l1lllllll_opy_=None, bstack11111l1l1_opy_=False):
  global CONFIG
  global bstack1ll111ll1_opy_
  global bstack1111ll1l_opy_
  global bstack1lll1ll111_opy_
  global bstack1l1l1lll1_opy_
  bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠩࠪ೿")
  bstack1l11l1l1_opy_(bstack1lllllll1_opy_, logger)
  if bstack1ll1lll1ll_opy_ and isinstance(bstack1ll1lll1ll_opy_, str):
    bstack1ll1lll1ll_opy_ = eval(bstack1ll1lll1ll_opy_)
  if bstack1ll1lll1ll_opy_:
    CONFIG = bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪഀ")]
    bstack1ll111ll1_opy_ = bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬഁ")]
    bstack1111ll1l_opy_ = bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧം")]
    bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨഃ"), bstack1111ll1l_opy_)
    bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഄ")
  bstack1l1l1lll1_opy_.bstack11ll1lll1l_opy_(bstack11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪഅ"), uuid4().__str__())
  logger.info(bstack11_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧആ") + bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬഇ")));
  logger.debug(bstack11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩࡃࠧഈ") + bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧഉ")))
  if not bstack11111l1l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll11ll111_opy_)
      return
    if sys.argv[1] == bstack11_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩഊ") or sys.argv[1] == bstack11_opy_ (u"ࠧ࠮ࡸࠪഋ"):
      logger.info(bstack11_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨഌ").format(__version__))
      return
    if sys.argv[1] == bstack11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ഍"):
      bstack11ll111l11_opy_()
      return
  args = sys.argv
  bstack11ll1llll_opy_()
  global bstack11ll11lll_opy_
  global bstack1l1l1lll11_opy_
  global bstack11llll11_opy_
  global bstack1lll11ll_opy_
  global bstack11lllll11_opy_
  global bstack1l11l111_opy_
  global bstack1l111l1l_opy_
  global bstack11lllllll_opy_
  global bstack1ll111lll_opy_
  global bstack1ll111ll_opy_
  global bstack1ll1lll111_opy_
  bstack1l1l1lll11_opy_ = len(CONFIG.get(bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭എ"), []))
  if not bstack1ll11lll1l_opy_:
    if args[1] == bstack11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫഏ") or args[1] == bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ഐ"):
      bstack1ll11lll1l_opy_ = bstack11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭഑")
      args = args[2:]
    elif args[1] == bstack11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ഒ"):
      bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧഓ")
      args = args[2:]
    elif args[1] == bstack11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨഔ"):
      bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩക")
      args = args[2:]
    elif args[1] == bstack11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬഖ"):
      bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ഗ")
      args = args[2:]
    elif args[1] == bstack11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ഘ"):
      bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧങ")
      args = args[2:]
    elif args[1] == bstack11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨച"):
      bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഛ")
      args = args[2:]
    else:
      if not bstack11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ജ") in CONFIG or str(CONFIG[bstack11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഝ")]).lower() in [bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഞ"), bstack11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧട")]:
        bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഠ")
        args = args[1:]
      elif str(CONFIG[bstack11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഡ")]).lower() == bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨഢ"):
        bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩണ")
        args = args[1:]
      elif str(CONFIG[bstack11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧത")]).lower() == bstack11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫഥ"):
        bstack1ll11lll1l_opy_ = bstack11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬദ")
        args = args[1:]
      elif str(CONFIG[bstack11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪധ")]).lower() == bstack11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨന"):
        bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഩ")
        args = args[1:]
      elif str(CONFIG[bstack11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭പ")]).lower() == bstack11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഫ"):
        bstack1ll11lll1l_opy_ = bstack11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬബ")
        args = args[1:]
      else:
        os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨഭ")] = bstack1ll11lll1l_opy_
        bstack1l1l11ll1_opy_(bstack1l1l1l11ll_opy_)
  os.environ[bstack11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨമ")] = bstack1ll11lll1l_opy_
  bstack1lll1ll111_opy_ = bstack1ll11lll1l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack111lll1l1_opy_ = bstack1ll1ll11ll_opy_[bstack11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬയ")] if bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩര") and bstack11l1ll11ll_opy_() else bstack1ll11lll1l_opy_
      bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.bstack1l11lll1l1_opy_, bstack1l111l1l1l_opy_(
        sdk_version=__version__,
        path_config=bstack1l1l1l1l1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack111lll1l1_opy_,
        frameworks=[bstack111lll1l1_opy_],
        framework_versions={
          bstack111lll1l1_opy_: bstack11111l1l_opy_(bstack11_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩറ") if bstack1ll11lll1l_opy_ in [bstack11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪല"), bstack11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫള"), bstack11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧഴ")] else bstack1ll11lll1l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤവ"), None):
        CONFIG[bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥശ")] = cli.config.get(bstack11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦഷ"), None)
    except Exception as e:
      bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.bstack1l1111l11l_opy_, e.__traceback__, 1)
    if bstack1111ll1l_opy_:
      CONFIG[bstack11_opy_ (u"ࠥࡥࡵࡶࠢസ")] = cli.config[bstack11_opy_ (u"ࠦࡦࡶࡰࠣഹ")]
      logger.info(bstack11lll1l11l_opy_.format(CONFIG[bstack11_opy_ (u"ࠬࡧࡰࡱࠩഺ")]))
  else:
    bstack11ll1l1ll1_opy_.clear()
  global bstack1ll1ll111l_opy_
  global bstack1l11ll11ll_opy_
  if bstack1ll1lll1ll_opy_:
    try:
      bstack11lllll1l_opy_ = datetime.datetime.now()
      os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ഻")] = bstack1ll11lll1l_opy_
      bstack11l11l1l1_opy_(bstack11l1ll1lll_opy_, CONFIG)
      cli.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡹࡤ࡬ࡡࡷࡩࡸࡺ࡟ࡢࡶࡷࡩࡲࡶࡴࡦࡦ഼ࠥ"), datetime.datetime.now() - bstack11lllll1l_opy_)
    except Exception as e:
      logger.debug(bstack1llll11ll_opy_.format(str(e)))
  global bstack1lll111111_opy_
  global bstack11ll1ll11l_opy_
  global bstack1111llll_opy_
  global bstack1lllll1l1_opy_
  global bstack1l11llll11_opy_
  global bstack1lll1l1111_opy_
  global bstack1llll1l1l_opy_
  global bstack1l1l1l1l_opy_
  global bstack11l1llll11_opy_
  global bstack1lll1lll11_opy_
  global bstack1ll11l1l_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1111l1l11_opy_
  global bstack1l1l11ll1l_opy_
  global bstack1111ll1ll_opy_
  global bstack1ll1l1l1l1_opy_
  global bstack1l1lll1ll1_opy_
  global bstack11l1ll11l1_opy_
  global bstack11lll1ll1_opy_
  global bstack1l1lll1l1l_opy_
  global bstack1llll1llll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll111111_opy_ = webdriver.Remote.__init__
    bstack11ll1ll11l_opy_ = WebDriver.quit
    bstack1ll1l11l1l_opy_ = WebDriver.close
    bstack1111ll1ll_opy_ = WebDriver.get
    bstack1llll1llll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1ll111l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11lll11l11_opy_
    bstack1l11ll11ll_opy_ = bstack11lll11l11_opy_()
  except Exception as e:
    pass
  try:
    global bstack111l11ll_opy_
    from QWeb.keywords import browser
    bstack111l11ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l111lll1_opy_(CONFIG) and bstack1ll11l11l1_opy_():
    if bstack111l111l1_opy_() < version.parse(bstack111l111l_opy_):
      logger.error(bstack11l1l11l1_opy_.format(bstack111l111l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll1l1l1l1_opy_ = RemoteConnection._11llll1lll_opy_
      except Exception as e:
        logger.error(bstack11l1ll1l1_opy_.format(str(e)))
  if not CONFIG.get(bstack11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪഽ"), False) and not bstack1ll1lll1ll_opy_:
    logger.info(bstack1l11ll11_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ാ") in CONFIG and str(CONFIG[bstack11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧി")]).lower() != bstack11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪീ"):
      bstack111llll11_opy_()
    elif bstack1ll11lll1l_opy_ != bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬു") or (bstack1ll11lll1l_opy_ == bstack11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ൂ") and not bstack1ll1lll1ll_opy_):
      bstack1lll1lllll_opy_()
  if (bstack1ll11lll1l_opy_ in [bstack11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ൃ"), bstack11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧൄ"), bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൅")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1l1ll1_opy_
        bstack1lll1l1111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l11l111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l11llll11_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11l1l1llll_opy_ + str(e))
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11l11l111_opy_)
    if bstack1ll11lll1l_opy_ != bstack11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫെ"):
      bstack1lllll1ll1_opy_()
    bstack1111llll_opy_ = Output.start_test
    bstack1lllll1l1_opy_ = Output.end_test
    bstack1llll1l1l_opy_ = TestStatus.__init__
    bstack11l1llll11_opy_ = pabot._run
    bstack1lll1lll11_opy_ = QueueItem.__init__
    bstack1ll11l1l_opy_ = pabot._create_command_for_execution
    bstack11lll1ll1_opy_ = pabot._report_results
  if bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫേ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11ll11llll_opy_)
    bstack1111l1l11_opy_ = Runner.run_hook
    bstack1l1l11ll1l_opy_ = Step.run
  if bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬൈ"):
    try:
      from _pytest.config import Config
      bstack1l1lll1ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack11l1ll11l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1llll111ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1lll1l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ൉"))
  try:
    framework_name = bstack11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൊ") if bstack1ll11lll1l_opy_ in [bstack11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧോ"), bstack11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൌ"), bstack11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯്ࠫ")] else bstack1l1ll11111_opy_(bstack1ll11lll1l_opy_)
    bstack1l1l1lll_opy_ = {
      bstack11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬൎ"): bstack11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ൏") if bstack1ll11lll1l_opy_ == bstack11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൐") and bstack11l1ll11ll_opy_() else framework_name,
      bstack11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ൑"): bstack11111l1l_opy_(framework_name),
      bstack11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭൒"): __version__,
      bstack11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ൓"): bstack1ll11lll1l_opy_
    }
    if bstack1ll11lll1l_opy_ in bstack1ll1l1l1l_opy_:
      if bstack1111l1l1l_opy_ and bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪൔ") in CONFIG and CONFIG[bstack11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫൕ")] == True:
        if bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬൖ") in CONFIG:
          os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧൗ")] = os.getenv(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ൘"), json.dumps(CONFIG[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൙")]))
          CONFIG[bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ൚")].pop(bstack11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ൛"), None)
          CONFIG[bstack11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ൜")].pop(bstack11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ൝"), None)
        bstack1l1l1lll_opy_[bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൞")] = {
          bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬൟ"): bstack11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪൠ"),
          bstack11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪൡ"): str(bstack111l111l1_opy_())
        }
    if bstack1ll11lll1l_opy_ not in [bstack11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൢ")] and not cli.is_running():
      bstack11lll1l1ll_opy_ = bstack111lllll1_opy_.launch(CONFIG, bstack1l1l1lll_opy_)
  except Exception as e:
    logger.debug(bstack1l1llll1_opy_.format(bstack11_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦࠬൣ"), str(e)))
  if bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൤"):
    bstack11llll11_opy_ = True
    if bstack1ll1lll1ll_opy_ and bstack11111l1l1_opy_:
      bstack1l11l111_opy_ = CONFIG.get(bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ൥"), {}).get(bstack11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ൦"))
      bstack1l1ll1ll1_opy_(bstack1lll11l1l_opy_)
    elif bstack1ll1lll1ll_opy_:
      bstack1l11l111_opy_ = CONFIG.get(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ൧"), {}).get(bstack11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൨"))
      global bstack1l1lll1ll_opy_
      try:
        if bstack11lll1ll_opy_(bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭൩")]) and multiprocessing.current_process().name == bstack11_opy_ (u"ࠫ࠵࠭൪"):
          bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൫")].remove(bstack11_opy_ (u"࠭࠭࡮ࠩ൬"))
          bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൭")].remove(bstack11_opy_ (u"ࠨࡲࡧࡦࠬ൮"))
          bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ൯")] = bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭൰")][0]
          with open(bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ൱")], bstack11_opy_ (u"ࠬࡸࠧ൲")) as f:
            bstack1lll1lll1l_opy_ = f.read()
          bstack11ll11ll_opy_ = bstack11_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࠣࡁࠥࡹࡴࡳࠪ࡬ࡲࡹ࠮ࡡࡳࡩࠬ࠯࠶࠶ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤ൳").format(str(bstack1ll1lll1ll_opy_))
          bstack1l111lll1l_opy_ = bstack11ll11ll_opy_ + bstack1lll1lll1l_opy_
          bstack1l1111111l_opy_ = bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൴")] + bstack11_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪ൵")
          with open(bstack1l1111111l_opy_, bstack11_opy_ (u"ࠩࡺࠫ൶")):
            pass
          with open(bstack1l1111111l_opy_, bstack11_opy_ (u"ࠥࡻ࠰ࠨ൷")) as f:
            f.write(bstack1l111lll1l_opy_)
          import subprocess
          bstack1llll1111l_opy_ = subprocess.run([bstack11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦ൸"), bstack1l1111111l_opy_])
          if os.path.exists(bstack1l1111111l_opy_):
            os.unlink(bstack1l1111111l_opy_)
          os._exit(bstack1llll1111l_opy_.returncode)
        else:
          if bstack11lll1ll_opy_(bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൹")]):
            bstack1ll1lll1ll_opy_[bstack11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩൺ")].remove(bstack11_opy_ (u"ࠧ࠮࡯ࠪൻ"))
            bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫർ")].remove(bstack11_opy_ (u"ࠩࡳࡨࡧ࠭ൽ"))
            bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ൾ")] = bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧൿ")][0]
          bstack1l1ll1ll1_opy_(bstack1lll11l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ඀")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨඁ")] = bstack11_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩං")
          mod_globals[bstack11_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪඃ")] = os.path.abspath(bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඄")])
          exec(open(bstack1ll1lll1ll_opy_[bstack11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭අ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫආ").format(str(e)))
          for driver in bstack1l1lll1ll_opy_:
            bstack1l1lllllll_opy_.append({
              bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඇ"): bstack1ll1lll1ll_opy_[bstack11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඈ")],
              bstack11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ඉ"): str(e),
              bstack11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧඊ"): multiprocessing.current_process().name
            })
            bstack1l111l111_opy_(driver, bstack11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩඋ"), bstack11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨඌ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1lll1ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1111ll1l_opy_, CONFIG, logger)
      bstack1l1l11lll_opy_()
      bstack1lll11l11l_opy_()
      bstack1l1ll1l11_opy_ = {
        bstack11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඍ"): args[0],
        bstack11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬඎ"): CONFIG,
        bstack11_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧඏ"): bstack1ll111ll1_opy_,
        bstack11_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩඐ"): bstack1111ll1l_opy_
      }
      percy.bstack1111ll11_opy_()
      if bstack11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫඑ") in CONFIG:
        bstack1llll1ll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1l1l11_opy_ = manager.list()
        if bstack11lll1ll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬඒ")]):
            if index == 0:
              bstack1l1ll1l11_opy_[bstack11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඓ")] = args
            bstack1llll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1ll1l11_opy_, bstack1lll1l1l11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧඔ")]):
            bstack1llll1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1ll1l11_opy_, bstack1lll1l1l11_opy_)))
        for t in bstack1llll1ll1_opy_:
          t.start()
        for t in bstack1llll1ll1_opy_:
          t.join()
        bstack11lllllll_opy_ = list(bstack1lll1l1l11_opy_)
      else:
        if bstack11lll1ll_opy_(args):
          bstack1l1ll1l11_opy_[bstack11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඕ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1ll1l11_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1ll1ll1_opy_(bstack1lll11l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨඖ")] = bstack11_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ඗")
          mod_globals[bstack11_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪ඘")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ඙") or bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩක"):
    percy.init(bstack1111ll1l_opy_, CONFIG, logger)
    percy.bstack1111ll11_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11l11l111_opy_)
    bstack1l1l11lll_opy_()
    bstack1l1ll1ll1_opy_(bstack1111111l_opy_)
    if bstack1111l1l1l_opy_:
      bstack1l11l11l_opy_(bstack1111111l_opy_, args)
      if bstack11_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩඛ") in args:
        i = args.index(bstack11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪග"))
        args.pop(i)
        args.pop(i)
      if bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඝ") not in CONFIG:
        CONFIG[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඞ")] = [{}]
        bstack1l1l1lll11_opy_ = 1
      if bstack11ll11lll_opy_ == 0:
        bstack11ll11lll_opy_ = 1
      args.insert(0, str(bstack11ll11lll_opy_))
      args.insert(0, str(bstack11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ඟ")))
    if bstack111lllll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11ll1ll1l1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1lll11_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤච"),
        ).parse_args(bstack11ll1ll1l1_opy_)
        bstack1ll1l11l_opy_ = args.index(bstack11ll1ll1l1_opy_[0]) if len(bstack11ll1ll1l1_opy_) > 0 else len(args)
        args.insert(bstack1ll1l11l_opy_, str(bstack11_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧඡ")))
        args.insert(bstack1ll1l11l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨජ"))))
        if bstack11l1l1l11_opy_(os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪඣ"))) and str(os.environ.get(bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪඤ"), bstack11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬඥ"))) != bstack11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ඦ"):
          for bstack11l1ll1l11_opy_ in bstack1ll1lll11_opy_:
            args.remove(bstack11l1ll1l11_opy_)
          bstack1ll1l1llll_opy_ = os.environ.get(bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ට")).split(bstack11_opy_ (u"ࠪ࠰ࠬඨ"))
          for bstack1ll111111l_opy_ in bstack1ll1l1llll_opy_:
            args.append(bstack1ll111111l_opy_)
      except Exception as e:
        logger.error(bstack11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࠢඩ").format(e))
    pabot.main(args)
  elif bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ඪ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11l11l111_opy_)
    for a in args:
      if bstack11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬණ") in a:
        bstack11lllll11_opy_ = int(a.split(bstack11_opy_ (u"ࠧ࠻ࠩඬ"))[1])
      if bstack11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬත") in a:
        bstack1l11l111_opy_ = str(a.split(bstack11_opy_ (u"ࠩ࠽ࠫථ"))[1])
      if bstack11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪද") in a:
        bstack1l111l1l_opy_ = str(a.split(bstack11_opy_ (u"ࠫ࠿࠭ධ"))[1])
    bstack1l11l1ll11_opy_ = None
    if bstack11_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫන") in args:
      i = args.index(bstack11_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ඲"))
      args.pop(i)
      bstack1l11l1ll11_opy_ = args.pop(i)
    if bstack1l11l1ll11_opy_ is not None:
      global bstack11ll1l11ll_opy_
      bstack11ll1l11ll_opy_ = bstack1l11l1ll11_opy_
    bstack1l1ll1ll1_opy_(bstack1111111l_opy_)
    run_cli(args)
    if bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫඳ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1l1l11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1lllllll_opy_.append(bstack1ll1l1l11l_opy_)
  elif bstack1ll11lll1l_opy_ == bstack11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨප"):
    bstack1l1ll1ll_opy_ = bstack11l11l1ll_opy_(args, logger, CONFIG, bstack1111l1l1l_opy_)
    bstack1l1ll1ll_opy_.bstack1l11ll1111_opy_()
    bstack1l1l11lll_opy_()
    bstack1lll11ll_opy_ = True
    bstack1ll111ll_opy_ = bstack1l1ll1ll_opy_.bstack1l11ll1l11_opy_()
    bstack1l1ll1ll_opy_.bstack1l1ll1l11_opy_(bstack1l11llll_opy_)
    bstack11l1l1lll_opy_ = bstack1l1ll1ll_opy_.bstack1lll1111_opy_(bstack1l1lllll1l_opy_, {
      bstack11_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪඵ"): bstack1ll111ll1_opy_,
      bstack11_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬබ"): bstack1111ll1l_opy_,
      bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧභ"): bstack1111l1l1l_opy_
    })
    try:
      bstack1111lll11_opy_, bstack1111lll1l_opy_ = map(list, zip(*bstack11l1l1lll_opy_))
      bstack1ll111lll_opy_ = bstack1111lll11_opy_[0]
      for status_code in bstack1111lll1l_opy_:
        if status_code != 0:
          bstack1ll1lll111_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥම").format(str(e)))
  elif bstack1ll11lll1l_opy_ == bstack11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඹ"):
    try:
      from behave.__main__ import main as bstack11ll111ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11ll1l1lll_opy_(e, bstack11ll11llll_opy_)
    bstack1l1l11lll_opy_()
    bstack1lll11ll_opy_ = True
    bstack1l1l111l1l_opy_ = 1
    if bstack11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧය") in CONFIG:
      bstack1l1l111l1l_opy_ = CONFIG[bstack11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨර")]
    if bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ඼") in CONFIG:
      bstack11ll1l111_opy_ = int(bstack1l1l111l1l_opy_) * int(len(CONFIG[bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ල")]))
    else:
      bstack11ll1l111_opy_ = int(bstack1l1l111l1l_opy_)
    config = Configuration(args)
    bstack1lllllllll_opy_ = config.paths
    if len(bstack1lllllllll_opy_) == 0:
      import glob
      pattern = bstack11_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪ඾")
      bstack11ll111111_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll111111_opy_)
      config = Configuration(args)
      bstack1lllllllll_opy_ = config.paths
    bstack1lllll1l11_opy_ = [os.path.normpath(item) for item in bstack1lllllllll_opy_]
    bstack11l1l1lll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1llll1ll11_opy_ = [item for item in bstack11l1l1lll1_opy_ if item not in bstack1lllll1l11_opy_]
    import platform as pf
    if pf.system().lower() == bstack11_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭඿"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lllll1l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll11l_opy_)))
                    for bstack1l11ll11l_opy_ in bstack1lllll1l11_opy_]
    bstack1lll1l1l1_opy_ = []
    for spec in bstack1lllll1l11_opy_:
      bstack11lllll11l_opy_ = []
      bstack11lllll11l_opy_ += bstack1llll1ll11_opy_
      bstack11lllll11l_opy_.append(spec)
      bstack1lll1l1l1_opy_.append(bstack11lllll11l_opy_)
    execution_items = []
    for bstack11lllll11l_opy_ in bstack1lll1l1l1_opy_:
      if bstack11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩව") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪශ")]):
          item = {}
          item[bstack11_opy_ (u"ࠨࡣࡵ࡫ࠬෂ")] = bstack11_opy_ (u"ࠩࠣࠫස").join(bstack11lllll11l_opy_)
          item[bstack11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩහ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11_opy_ (u"ࠫࡦࡸࡧࠨළ")] = bstack11_opy_ (u"ࠬࠦࠧෆ").join(bstack11lllll11l_opy_)
        item[bstack11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෇")] = 0
        execution_items.append(item)
    bstack1ll1ll11_opy_ = bstack1ll111l111_opy_(execution_items, bstack11ll1l111_opy_)
    for execution_item in bstack1ll1ll11_opy_:
      bstack1llll1ll1_opy_ = []
      for item in execution_item:
        bstack1llll1ll1_opy_.append(bstack11ll11l11l_opy_(name=str(item[bstack11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭෈")]),
                                             target=bstack1l1111l111_opy_,
                                             args=(item[bstack11_opy_ (u"ࠨࡣࡵ࡫ࠬ෉")],)))
      for t in bstack1llll1ll1_opy_:
        t.start()
      for t in bstack1llll1ll1_opy_:
        t.join()
  else:
    bstack1l1l11ll1_opy_(bstack1l1l1l11ll_opy_)
  if not bstack1ll1lll1ll_opy_:
    bstack11llll111l_opy_()
    if(bstack1ll11lll1l_opy_ in [bstack11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ්ࠩ"), bstack11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෋")]):
      bstack1l1l1111l_opy_()
  bstack11l11l1l_opy_.bstack1l1ll111l1_opy_()
def browserstack_initialize(bstack1ll11l1111_opy_=None):
  logger.info(bstack11_opy_ (u"ࠫࡗࡻ࡮࡯࡫ࡱ࡫࡙ࠥࡄࡌࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡷ࠿ࠦࠧ෌") + str(bstack1ll11l1111_opy_))
  run_on_browserstack(bstack1ll11l1111_opy_, None, True)
@measure(event_name=EVENTS.bstack111lll1ll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack11llll111l_opy_():
  global CONFIG
  global bstack1lll1ll111_opy_
  global bstack1ll1lll111_opy_
  global bstack11ll11ll11_opy_
  global bstack1l1l1lll1_opy_
  if cli.is_running():
    bstack11ll1l1ll1_opy_.invoke(bstack11lllll111_opy_.bstack1ll1l11l1_opy_)
  if bstack1lll1ll111_opy_ == bstack11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෍"):
    if not cli.is_enabled(CONFIG):
      bstack111lllll1_opy_.stop()
  else:
    bstack111lllll1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1ll11l1l1_opy_.bstack1l11lll1_opy_()
  if bstack11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ෎") in CONFIG and str(CONFIG[bstack11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫා")]).lower() != bstack11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧැ"):
    bstack1l1lll11ll_opy_, bstack11l1lll1ll_opy_ = bstack1llll1ll1l_opy_()
  else:
    bstack1l1lll11ll_opy_, bstack11l1lll1ll_opy_ = get_build_link()
  bstack11llll1l11_opy_(bstack1l1lll11ll_opy_)
  logger.info(bstack11_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡩࡳࡷࠦࡩࡥ࠼ࠪෑ") + bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬි"), bstack11_opy_ (u"ࠫࠬී")) + bstack11_opy_ (u"ࠬ࠲ࠠࡵࡧࡶࡸ࡭ࡻࡢࠡ࡫ࡧ࠾ࠥ࠭ු") + os.getenv(bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ෕"), bstack11_opy_ (u"ࠧࠨූ")))
  if bstack1l1lll11ll_opy_ is not None and bstack1l1l1ll111_opy_() != -1:
    sessions = bstack1llll1l111_opy_(bstack1l1lll11ll_opy_)
    bstack11ll111lll_opy_(sessions, bstack11l1lll1ll_opy_)
  if bstack1lll1ll111_opy_ == bstack11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෗") and bstack1ll1lll111_opy_ != 0:
    sys.exit(bstack1ll1lll111_opy_)
  if bstack1lll1ll111_opy_ == bstack11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ") and bstack11ll11ll11_opy_ != 0:
    sys.exit(bstack11ll11ll11_opy_)
def bstack11llll1l11_opy_(new_id):
    global bstack11ll1ll1_opy_
    bstack11ll1ll1_opy_ = new_id
def bstack1l1ll11111_opy_(bstack1lll111l11_opy_):
  if bstack1lll111l11_opy_:
    return bstack1lll111l11_opy_.capitalize()
  else:
    return bstack11_opy_ (u"ࠪࠫෙ")
@measure(event_name=EVENTS.bstack1l11llllll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack11l1lllll_opy_(bstack1l1111l1ll_opy_):
  if bstack11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩේ") in bstack1l1111l1ll_opy_ and bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪෛ")] != bstack11_opy_ (u"࠭ࠧො"):
    return bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬෝ")]
  else:
    bstack1ll111llll_opy_ = bstack11_opy_ (u"ࠣࠤෞ")
    if bstack11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩෟ") in bstack1l1111l1ll_opy_ and bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ෠")] != None:
      bstack1ll111llll_opy_ += bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ෡")] + bstack11_opy_ (u"ࠧ࠲ࠠࠣ෢")
      if bstack1l1111l1ll_opy_[bstack11_opy_ (u"࠭࡯ࡴࠩ෣")] == bstack11_opy_ (u"ࠢࡪࡱࡶࠦ෤"):
        bstack1ll111llll_opy_ += bstack11_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ෥")
      bstack1ll111llll_opy_ += (bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭෦")] or bstack11_opy_ (u"ࠪࠫ෧"))
      return bstack1ll111llll_opy_
    else:
      bstack1ll111llll_opy_ += bstack1l1ll11111_opy_(bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ෨")]) + bstack11_opy_ (u"ࠧࠦࠢ෩") + (
              bstack1l1111l1ll_opy_[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෪")] or bstack11_opy_ (u"ࠧࠨ෫")) + bstack11_opy_ (u"ࠣ࠮ࠣࠦ෬")
      if bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠩࡲࡷࠬ෭")] == bstack11_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ෮"):
        bstack1ll111llll_opy_ += bstack11_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ෯")
      bstack1ll111llll_opy_ += bstack1l1111l1ll_opy_[bstack11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෰")] or bstack11_opy_ (u"࠭ࠧ෱")
      return bstack1ll111llll_opy_
@measure(event_name=EVENTS.bstack1l111111ll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack1llll111l1_opy_(bstack1ll1l1l1_opy_):
  if bstack1ll1l1l1_opy_ == bstack11_opy_ (u"ࠢࡥࡱࡱࡩࠧෲ"):
    return bstack11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫෳ")
  elif bstack1ll1l1l1_opy_ == bstack11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ෴"):
    return bstack11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭෵")
  elif bstack1ll1l1l1_opy_ == bstack11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ෶"):
    return bstack11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෷")
  elif bstack1ll1l1l1_opy_ == bstack11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ෸"):
    return bstack11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ෹")
  elif bstack1ll1l1l1_opy_ == bstack11_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ෺"):
    return bstack11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ෻")
  elif bstack1ll1l1l1_opy_ == bstack11_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦ෼"):
    return bstack11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෽")
  else:
    return bstack11_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩ෾") + bstack1l1ll11111_opy_(
      bstack1ll1l1l1_opy_) + bstack11_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෿")
def bstack1111l1lll_opy_(session):
  return bstack11_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧ฀").format(
    session[bstack11_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬก")], bstack11l1lllll_opy_(session), bstack1llll111l1_opy_(session[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨข")]),
    bstack1llll111l1_opy_(session[bstack11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪฃ")]),
    bstack1l1ll11111_opy_(session[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬค")] or session[bstack11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬฅ")] or bstack11_opy_ (u"࠭ࠧฆ")) + bstack11_opy_ (u"ࠢࠡࠤง") + (session[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪจ")] or bstack11_opy_ (u"ࠩࠪฉ")),
    session[bstack11_opy_ (u"ࠪࡳࡸ࠭ช")] + bstack11_opy_ (u"ࠦࠥࠨซ") + session[bstack11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩฌ")], session[bstack11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨญ")] or bstack11_opy_ (u"ࠧࠨฎ"),
    session[bstack11_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬฏ")] if session[bstack11_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ฐ")] else bstack11_opy_ (u"ࠪࠫฑ"))
@measure(event_name=EVENTS.bstack1l111l11l_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def bstack11ll111lll_opy_(sessions, bstack11l1lll1ll_opy_):
  try:
    bstack1l1l1llll_opy_ = bstack11_opy_ (u"ࠦࠧฒ")
    if not os.path.exists(bstack1l111lll11_opy_):
      os.mkdir(bstack1l111lll11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪณ")), bstack11_opy_ (u"࠭ࡲࠨด")) as f:
      bstack1l1l1llll_opy_ = f.read()
    bstack1l1l1llll_opy_ = bstack1l1l1llll_opy_.replace(bstack11_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫต"), str(len(sessions)))
    bstack1l1l1llll_opy_ = bstack1l1l1llll_opy_.replace(bstack11_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨถ"), bstack11l1lll1ll_opy_)
    bstack1l1l1llll_opy_ = bstack1l1l1llll_opy_.replace(bstack11_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪท"),
                                              sessions[0].get(bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧธ")) if sessions[0] else bstack11_opy_ (u"ࠫࠬน"))
    with open(os.path.join(bstack1l111lll11_opy_, bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩบ")), bstack11_opy_ (u"࠭ࡷࠨป")) as stream:
      stream.write(bstack1l1l1llll_opy_.split(bstack11_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫผ"))[0])
      for session in sessions:
        stream.write(bstack1111l1lll_opy_(session))
      stream.write(bstack1l1l1llll_opy_.split(bstack11_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬฝ"))[1])
    logger.info(bstack11_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬพ").format(bstack1l111lll11_opy_));
  except Exception as e:
    logger.debug(bstack1ll1ll1l11_opy_.format(str(e)))
def bstack1llll1l111_opy_(bstack1l1lll11ll_opy_):
  global CONFIG
  try:
    bstack11lllll1l_opy_ = datetime.datetime.now()
    host = bstack11_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ฟ") if bstack11_opy_ (u"ࠫࡦࡶࡰࠨภ") in CONFIG else bstack11_opy_ (u"ࠬࡧࡰࡪࠩม")
    user = CONFIG[bstack11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨย")]
    key = CONFIG[bstack11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪร")]
    bstack1lll1111l_opy_ = bstack11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧฤ") if bstack11_opy_ (u"ࠩࡤࡴࡵ࠭ล") in CONFIG else (bstack11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧฦ") if CONFIG.get(bstack11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨว")) else bstack11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧศ"))
    url = bstack11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫษ").format(user, key, host, bstack1lll1111l_opy_,
                                                                                bstack1l1lll11ll_opy_)
    headers = {
      bstack11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ส"): bstack11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫห"),
    }
    proxies = bstack11l1ll11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࡥ࡬ࡪࡵࡷࠦฬ"), datetime.datetime.now() - bstack11lllll1l_opy_)
      return list(map(lambda session: session[bstack11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨอ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1lll1l11_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11l111ll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def get_build_link():
  global CONFIG
  global bstack11ll1ll1_opy_
  try:
    if bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧฮ") in CONFIG:
      bstack11lllll1l_opy_ = datetime.datetime.now()
      host = bstack11_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨฯ") if bstack11_opy_ (u"࠭ࡡࡱࡲࠪะ") in CONFIG else bstack11_opy_ (u"ࠧࡢࡲ࡬ࠫั")
      user = CONFIG[bstack11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪา")]
      key = CONFIG[bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬำ")]
      bstack1lll1111l_opy_ = bstack11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩิ") if bstack11_opy_ (u"ࠫࡦࡶࡰࠨี") in CONFIG else bstack11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧึ")
      url = bstack11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭ื").format(user, key, host, bstack1lll1111l_opy_)
      headers = {
        bstack11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪุ࠭"): bstack11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱูࠫ"),
      }
      if bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵฺࠫ") in CONFIG:
        params = {bstack11_opy_ (u"ࠪࡲࡦࡳࡥࠨ฻"): CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ฼")], bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ฽"): CONFIG[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ฾")]}
      else:
        params = {bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ฿"): CONFIG[bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫเ")]}
      proxies = bstack11l1ll11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11lll11l1l_opy_ = response.json()[0][bstack11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬแ")]
        if bstack11lll11l1l_opy_:
          bstack11l1lll1ll_opy_ = bstack11lll11l1l_opy_[bstack11_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧโ")].split(bstack11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪใ"))[0] + bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ไ") + bstack11lll11l1l_opy_[
            bstack11_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩๅ")]
          logger.info(bstack1lll1lll1_opy_.format(bstack11l1lll1ll_opy_))
          bstack11ll1ll1_opy_ = bstack11lll11l1l_opy_[bstack11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪๆ")]
          bstack1l11l1l111_opy_ = CONFIG[bstack11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ็")]
          if bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ่ࠫ") in CONFIG:
            bstack1l11l1l111_opy_ += bstack11_opy_ (u"ࠪࠤ้ࠬ") + CONFIG[bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ๊࠭")]
          if bstack1l11l1l111_opy_ != bstack11lll11l1l_opy_[bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧ๋ࠪ")]:
            logger.debug(bstack11l1l1ll_opy_.format(bstack11lll11l1l_opy_[bstack11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ์")], bstack1l11l1l111_opy_))
          cli.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡥࡹ࡮ࡲࡤࡠ࡮࡬ࡲࡰࠨํ"), datetime.datetime.now() - bstack11lllll1l_opy_)
          return [bstack11lll11l1l_opy_[bstack11_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ๎")], bstack11l1lll1ll_opy_]
    else:
      logger.warn(bstack1l1l1l1l11_opy_)
  except Exception as e:
    logger.debug(bstack1ll1111ll1_opy_.format(str(e)))
  return [None, None]
def bstack11l1lll1l_opy_(url, bstack11l1lll1l1_opy_=False):
  global CONFIG
  global bstack1ll1ll11l_opy_
  if not bstack1ll1ll11l_opy_:
    hostname = bstack1111111l1_opy_(url)
    is_private = bstack11lll11l1_opy_(hostname)
    if (bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭๏") in CONFIG and not bstack11l1l1l11_opy_(CONFIG[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ๐")])) and (is_private or bstack11l1lll1l1_opy_):
      bstack1ll1ll11l_opy_ = hostname
def bstack1111111l1_opy_(url):
  return urlparse(url).hostname
def bstack11lll11l1_opy_(hostname):
  for bstack1llll11ll1_opy_ in bstack1llll1l1ll_opy_:
    regex = re.compile(bstack1llll11ll1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1l1l111l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack111ll11ll_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11lllll11_opy_
  bstack1lll1l111_opy_ = not (bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ๑"), None) and bstack1llllll111_opy_(
          threading.current_thread(), bstack11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ๒"), None))
  bstack1l11l11ll1_opy_ = getattr(driver, bstack11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭๓"), None) != True
  if not bstack1111l1111_opy_.bstack11ll1l1l11_opy_(CONFIG, bstack11lllll11_opy_) or (bstack1l11l11ll1_opy_ and bstack1lll1l111_opy_):
    logger.warning(bstack11_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ๔"))
    return {}
  try:
    logger.debug(bstack11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ๕"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l11l11l11_opy_.bstack1lll1l111l_opy_)
    return results
  except Exception:
    logger.error(bstack11_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ๖"))
    return {}
@measure(event_name=EVENTS.bstack11l111ll1_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11lllll11_opy_
  bstack1lll1l111_opy_ = not (bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ๗"), None) and bstack1llllll111_opy_(
          threading.current_thread(), bstack11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๘"), None))
  bstack1l11l11ll1_opy_ = getattr(driver, bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ๙"), None) != True
  if not bstack1111l1111_opy_.bstack11ll1l1l11_opy_(CONFIG, bstack11lllll11_opy_) or (bstack1l11l11ll1_opy_ and bstack1lll1l111_opy_):
    logger.warning(bstack11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥ๚"))
    return {}
  try:
    logger.debug(bstack11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ๛"))
    logger.debug(perform_scan(driver))
    bstack1l1ll1lll1_opy_ = driver.execute_async_script(bstack1l11l11l11_opy_.bstack1l1l11l1l1_opy_)
    return bstack1l1ll1lll1_opy_
  except Exception:
    logger.error(bstack11_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ๜"))
    return {}
@measure(event_name=EVENTS.bstack11llll1l1_opy_, stage=STAGE.bstack1lll11111l_opy_, bstack1ll111llll_opy_=bstack1ll111lll1_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11lllll11_opy_
  bstack1lll1l111_opy_ = not (bstack1llllll111_opy_(threading.current_thread(), bstack11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭๝"), None) and bstack1llllll111_opy_(
          threading.current_thread(), bstack11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๞"), None))
  bstack1l11l11ll1_opy_ = getattr(driver, bstack11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ๟"), None) != True
  if not bstack1111l1111_opy_.bstack11ll1l1l11_opy_(CONFIG, bstack11lllll11_opy_) or (bstack1l11l11ll1_opy_ and bstack1lll1l111_opy_):
    logger.warning(bstack11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢ๠"))
    return {}
  try:
    bstack1lll1l11ll_opy_ = driver.execute_async_script(bstack1l11l11l11_opy_.perform_scan, {bstack11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭๡"): kwargs.get(bstack11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡱࡰࡱࡦࡴࡤࠨ๢"), None) or bstack11_opy_ (u"ࠨࠩ๣")})
    return bstack1lll1l11ll_opy_
  except Exception:
    logger.error(bstack11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣ๤"))
    return {}