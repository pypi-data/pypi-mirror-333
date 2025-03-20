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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1l11l111l11_opy_, bstack1l111lll1ll_opy_, bstack11lllll1l_opy_, bstack111llll1l1_opy_, bstack11lll1ll11l_opy_, bstack11llll111ll_opy_, bstack11lllll111l_opy_, bstack111ll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l1111l1l1_opy_ import bstack11l111l11l1_opy_
import bstack_utils.bstack11l11ll1_opy_ as bstack1l1l1l111l_opy_
from bstack_utils.bstack11l11l1ll1_opy_ import bstack11l1llllll_opy_
import bstack_utils.accessibility as bstack11lll111l_opy_
from bstack_utils.bstack11ll111111_opy_ import bstack11ll111111_opy_
from bstack_utils.bstack11l1l1l1l1_opy_ import bstack111lll111l_opy_
bstack111lll11111_opy_ = bstack1l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᲽ")
logger = logging.getLogger(__name__)
class bstack1ll1lll11_opy_:
    bstack11l1111l1l1_opy_ = None
    bs_config = None
    bstack1l11l11lll_opy_ = None
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l111l11ll1_opy_, stage=STAGE.bstack1111111l_opy_)
    def launch(cls, bs_config, bstack1l11l11lll_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11l11lll_opy_ = bstack1l11l11lll_opy_
        try:
            cls.bstack111lll111l1_opy_()
            bstack1l11l11ll1l_opy_ = bstack1l11l111l11_opy_(bs_config)
            bstack1l11l1111ll_opy_ = bstack1l111lll1ll_opy_(bs_config)
            data = bstack1l1l1l111l_opy_.bstack111ll1l1lll_opy_(bs_config, bstack1l11l11lll_opy_)
            config = {
                bstack1l11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭Ჾ"): (bstack1l11l11ll1l_opy_, bstack1l11l1111ll_opy_),
                bstack1l11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᲿ"): cls.default_headers()
            }
            response = bstack11lllll1l_opy_(bstack1l11l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ᳀"), cls.request_url(bstack1l11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫ᳁")), data, config)
            if response.status_code != 200:
                bstack1lll1l11ll1_opy_ = response.json()
                if bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭᳂")] == False:
                    cls.bstack111lll11l11_opy_(bstack1lll1l11ll1_opy_)
                    return
                cls.bstack111ll1lll1l_opy_(bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᳃")])
                cls.bstack111ll1l1l1l_opy_(bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᳄")])
                return None
            bstack111ll1lll11_opy_ = cls.bstack111lll11l1l_opy_(response)
            return bstack111ll1lll11_opy_
        except Exception as error:
            logger.error(bstack1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨ᳅").format(str(error)))
            return None
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    def stop(cls, bstack111ll1l1l11_opy_=None):
        if not bstack11l1llllll_opy_.on() and not bstack11lll111l_opy_.on():
            return
        if os.environ.get(bstack1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᳆")) == bstack1l11l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ᳇") or os.environ.get(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᳈")) == bstack1l11l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᳉"):
            logger.error(bstack1l11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ᳊"))
            return {
                bstack1l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ᳋"): bstack1l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᳌"),
                bstack1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᳍"): bstack1l11l_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨ᳎")
            }
        try:
            cls.bstack11l1111l1l1_opy_.shutdown()
            data = {
                bstack1l11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᳏"): bstack111ll1l1l_opy_()
            }
            if not bstack111ll1l1l11_opy_ is None:
                data[bstack1l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ᳐")] = [{
                    bstack1l11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭᳑"): bstack1l11l_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ᳒"),
                    bstack1l11l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ᳓"): bstack111ll1l1l11_opy_
                }]
            config = {
                bstack1l11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵ᳔ࠪ"): cls.default_headers()
            }
            bstack1l111111l1l_opy_ = bstack1l11l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳ᳕ࠫ").format(os.environ[bstack1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ᳖")])
            bstack111ll1l1ll1_opy_ = cls.request_url(bstack1l111111l1l_opy_)
            response = bstack11lllll1l_opy_(bstack1l11l_opy_ (u"ࠬࡖࡕࡕ᳗ࠩ"), bstack111ll1l1ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l11l_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯᳘ࠧ"))
        except Exception as error:
            logger.error(bstack1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼᳙ࠣࠦ") + str(error))
            return {
                bstack1l11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᳚"): bstack1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳛"),
                bstack1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ᳜ࠫ"): str(error)
            }
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    def bstack111lll11l1l_opy_(cls, response):
        bstack1lll1l11ll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack111ll1lll11_opy_ = {}
        if bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"ࠫ࡯ࡽࡴࠨ᳝")) is None:
            os.environ[bstack1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕ᳞ࠩ")] = bstack1l11l_opy_ (u"࠭࡮ࡶ࡮࡯᳟ࠫ")
        else:
            os.environ[bstack1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᳠")] = bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"ࠨ࡬ࡺࡸࠬ᳡"), bstack1l11l_opy_ (u"ࠩࡱࡹࡱࡲ᳢ࠧ"))
        os.environ[bstack1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᳣")] = bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ᳤࠭"), bstack1l11l_opy_ (u"ࠬࡴࡵ࡭࡮᳥ࠪ"))
        logger.info(bstack1l11l_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼᳦ࠣࠫ") + os.getenv(bstack1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᳧ࠬ")));
        if bstack11l1llllll_opy_.bstack111lll1l1ll_opy_(cls.bs_config, cls.bstack1l11l11lll_opy_.get(bstack1l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥ᳨ࠩ"), bstack1l11l_opy_ (u"ࠩࠪᳩ"))) is True:
            bstack111ll1ll1l1_opy_, build_hashed_id, bstack111ll1llll1_opy_ = cls.bstack111lll1llll_opy_(bstack1lll1l11ll1_opy_)
            if bstack111ll1ll1l1_opy_ != None and build_hashed_id != None:
                bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᳪ")] = {
                    bstack1l11l_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧᳫ"): bstack111ll1ll1l1_opy_,
                    bstack1l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᳬ"): build_hashed_id,
                    bstack1l11l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵ᳭ࠪ"): bstack111ll1llll1_opy_
                }
            else:
                bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᳮ")] = {}
        else:
            bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᳯ")] = {}
        if bstack11lll111l_opy_.bstack1l11l1111l1_opy_(cls.bs_config) is True:
            bstack111ll1ll11l_opy_, build_hashed_id = cls.bstack111lll11lll_opy_(bstack1lll1l11ll1_opy_)
            if bstack111ll1ll11l_opy_ != None and build_hashed_id != None:
                bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᳰ")] = {
                    bstack1l11l_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧᳱ"): bstack111ll1ll11l_opy_,
                    bstack1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᳲ"): build_hashed_id,
                }
            else:
                bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᳳ")] = {}
        else:
            bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᳴")] = {}
        if bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᳵ")].get(bstack1l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᳶ")) != None or bstack111ll1lll11_opy_[bstack1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᳷")].get(bstack1l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ᳸")) != None:
            cls.bstack111lll1ll11_opy_(bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"ࠫ࡯ࡽࡴࠨ᳹")), bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᳺ")))
        return bstack111ll1lll11_opy_
    @classmethod
    def bstack111lll1llll_opy_(cls, bstack1lll1l11ll1_opy_):
        if bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᳻")) == None:
            cls.bstack111ll1lll1l_opy_()
            return [None, None, None]
        if bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᳼")][bstack1l11l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ᳽")] != True:
            cls.bstack111ll1lll1l_opy_(bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᳾")])
            return [None, None, None]
        logger.debug(bstack1l11l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧ᳿"))
        os.environ[bstack1l11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᴀ")] = bstack1l11l_opy_ (u"ࠬࡺࡲࡶࡧࠪᴁ")
        if bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"࠭ࡪࡸࡶࠪᴂ")):
            os.environ[bstack1l11l_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫᴃ")] = json.dumps({
                bstack1l11l_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪᴄ"): bstack1l11l111l11_opy_(cls.bs_config),
                bstack1l11l_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫᴅ"): bstack1l111lll1ll_opy_(cls.bs_config)
            })
        if bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᴆ")):
            os.environ[bstack1l11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᴇ")] = bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᴈ")]
        if bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᴉ")].get(bstack1l11l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᴊ"), {}).get(bstack1l11l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᴋ")):
            os.environ[bstack1l11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᴌ")] = str(bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᴍ")][bstack1l11l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᴎ")][bstack1l11l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᴏ")])
        else:
            os.environ[bstack1l11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᴐ")] = bstack1l11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᴑ")
        return [bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠨ࡬ࡺࡸࠬᴒ")], bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᴓ")], os.environ[bstack1l11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᴔ")]]
    @classmethod
    def bstack111lll11lll_opy_(cls, bstack1lll1l11ll1_opy_):
        if bstack1lll1l11ll1_opy_.get(bstack1l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴕ")) == None:
            cls.bstack111ll1l1l1l_opy_()
            return [None, None]
        if bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴖ")][bstack1l11l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᴗ")] != True:
            cls.bstack111ll1l1l1l_opy_(bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴘ")])
            return [None, None]
        if bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴙ")].get(bstack1l11l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᴚ")):
            logger.debug(bstack1l11l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧᴛ"))
            parsed = json.loads(os.getenv(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᴜ"), bstack1l11l_opy_ (u"ࠬࢁࡽࠨᴝ")))
            capabilities = bstack1l1l1l111l_opy_.bstack111lll1lll1_opy_(bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴞ")][bstack1l11l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᴟ")][bstack1l11l_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᴠ")], bstack1l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᴡ"), bstack1l11l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩᴢ"))
            bstack111ll1ll11l_opy_ = capabilities[bstack1l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᴣ")]
            os.environ[bstack1l11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᴤ")] = bstack111ll1ll11l_opy_
            parsed[bstack1l11l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᴥ")] = capabilities[bstack1l11l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᴦ")]
            os.environ[bstack1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᴧ")] = json.dumps(parsed)
            scripts = bstack1l1l1l111l_opy_.bstack111lll1lll1_opy_(bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴨ")][bstack1l11l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᴩ")][bstack1l11l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᴪ")], bstack1l11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᴫ"), bstack1l11l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧᴬ"))
            bstack11ll111111_opy_.bstack1l11l11111l_opy_(scripts)
            commands = bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴭ")][bstack1l11l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᴮ")][bstack1l11l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪᴯ")].get(bstack1l11l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᴰ"))
            bstack11ll111111_opy_.bstack1l11l111111_opy_(commands)
            bstack11ll111111_opy_.store()
        return [bstack111ll1ll11l_opy_, bstack1lll1l11ll1_opy_[bstack1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᴱ")]]
    @classmethod
    def bstack111ll1lll1l_opy_(cls, response=None):
        os.environ[bstack1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᴲ")] = bstack1l11l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᴳ")
        os.environ[bstack1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᴴ")] = bstack1l11l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᴵ")
        os.environ[bstack1l11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᴶ")] = bstack1l11l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᴷ")
        os.environ[bstack1l11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᴸ")] = bstack1l11l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᴹ")
        os.environ[bstack1l11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᴺ")] = bstack1l11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᴻ")
        cls.bstack111lll11l11_opy_(response, bstack1l11l_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣᴼ"))
        return [None, None, None]
    @classmethod
    def bstack111ll1l1l1l_opy_(cls, response=None):
        os.environ[bstack1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᴽ")] = bstack1l11l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᴾ")
        os.environ[bstack1l11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᴿ")] = bstack1l11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᵀ")
        os.environ[bstack1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᵁ")] = bstack1l11l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᵂ")
        cls.bstack111lll11l11_opy_(response, bstack1l11l_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣᵃ"))
        return [None, None, None]
    @classmethod
    def bstack111lll1ll11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᵄ")] = jwt
        os.environ[bstack1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᵅ")] = build_hashed_id
    @classmethod
    def bstack111lll11l11_opy_(cls, response=None, product=bstack1l11l_opy_ (u"ࠦࠧᵆ")):
        if response == None:
            logger.error(product + bstack1l11l_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢᵇ"))
        for error in response[bstack1l11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᵈ")]:
            bstack1l11111111l_opy_ = error[bstack1l11l_opy_ (u"ࠧ࡬ࡧࡼࠫᵉ")]
            error_message = error[bstack1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᵊ")]
            if error_message:
                if bstack1l11111111l_opy_ == bstack1l11l_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣᵋ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l11l_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦᵌ") + product + bstack1l11l_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᵍ"))
    @classmethod
    def bstack111lll111l1_opy_(cls):
        if cls.bstack11l1111l1l1_opy_ is not None:
            return
        cls.bstack11l1111l1l1_opy_ = bstack11l111l11l1_opy_(cls.bstack111lll1l111_opy_)
        cls.bstack11l1111l1l1_opy_.start()
    @classmethod
    def bstack111llll11l_opy_(cls):
        if cls.bstack11l1111l1l1_opy_ is None:
            return
        cls.bstack11l1111l1l1_opy_.shutdown()
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    def bstack111lll1l111_opy_(cls, bstack11l1111lll_opy_, event_url=bstack1l11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᵎ")):
        config = {
            bstack1l11l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᵏ"): cls.default_headers()
        }
        logger.debug(bstack1l11l_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢᵐ").format(bstack1l11l_opy_ (u"ࠨ࠮ࠣࠫᵑ").join([event[bstack1l11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᵒ")] for event in bstack11l1111lll_opy_])))
        response = bstack11lllll1l_opy_(bstack1l11l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᵓ"), cls.request_url(event_url), bstack11l1111lll_opy_, config)
        bstack1l11l11lll1_opy_ = response.json()
    @classmethod
    def bstack1l111l1111_opy_(cls, bstack11l1111lll_opy_, event_url=bstack1l11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᵔ")):
        logger.debug(bstack1l11l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧᵕ").format(bstack11l1111lll_opy_[bstack1l11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᵖ")]))
        if not bstack1l1l1l111l_opy_.bstack111ll1ll111_opy_(bstack11l1111lll_opy_[bstack1l11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᵗ")]):
            logger.debug(bstack1l11l_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨᵘ").format(bstack11l1111lll_opy_[bstack1l11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᵙ")]))
            return
        bstack1111l1lll_opy_ = bstack1l1l1l111l_opy_.bstack111ll1ll1ll_opy_(bstack11l1111lll_opy_[bstack1l11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᵚ")], bstack11l1111lll_opy_.get(bstack1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᵛ")))
        if bstack1111l1lll_opy_ != None:
            if bstack11l1111lll_opy_.get(bstack1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᵜ")) != None:
                bstack11l1111lll_opy_[bstack1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᵝ")][bstack1l11l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᵞ")] = bstack1111l1lll_opy_
            else:
                bstack11l1111lll_opy_[bstack1l11l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᵟ")] = bstack1111l1lll_opy_
        if event_url == bstack1l11l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᵠ"):
            cls.bstack111lll111l1_opy_()
            logger.debug(bstack1l11l_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨᵡ").format(bstack11l1111lll_opy_[bstack1l11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᵢ")]))
            cls.bstack11l1111l1l1_opy_.add(bstack11l1111lll_opy_)
        elif event_url == bstack1l11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᵣ"):
            cls.bstack111lll1l111_opy_([bstack11l1111lll_opy_], event_url)
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    def bstack1111lll1l_opy_(cls, logs):
        bstack111lll1l1l1_opy_ = []
        for log in logs:
            bstack111lll111ll_opy_ = {
                bstack1l11l_opy_ (u"࠭࡫ࡪࡰࡧࠫᵤ"): bstack1l11l_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᵥ"),
                bstack1l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᵦ"): log[bstack1l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᵧ")],
                bstack1l11l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᵨ"): log[bstack1l11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᵩ")],
                bstack1l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᵪ"): {},
                bstack1l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᵫ"): log[bstack1l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᵬ")],
            }
            if bstack1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᵭ") in log:
                bstack111lll111ll_opy_[bstack1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᵮ")] = log[bstack1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᵯ")]
            elif bstack1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵰ") in log:
                bstack111lll111ll_opy_[bstack1l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᵱ")] = log[bstack1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᵲ")]
            bstack111lll1l1l1_opy_.append(bstack111lll111ll_opy_)
        cls.bstack1l111l1111_opy_({
            bstack1l11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᵳ"): bstack1l11l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᵴ"),
            bstack1l11l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᵵ"): bstack111lll1l1l1_opy_
        })
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    def bstack111ll1lllll_opy_(cls, steps):
        bstack111lll11ll1_opy_ = []
        for step in steps:
            bstack111lll1l11l_opy_ = {
                bstack1l11l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᵶ"): bstack1l11l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᵷ"),
                bstack1l11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᵸ"): step[bstack1l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᵹ")],
                bstack1l11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᵺ"): step[bstack1l11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᵻ")],
                bstack1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᵼ"): step[bstack1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᵽ")],
                bstack1l11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᵾ"): step[bstack1l11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᵿ")]
            }
            if bstack1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶀ") in step:
                bstack111lll1l11l_opy_[bstack1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶁ")] = step[bstack1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᶂ")]
            elif bstack1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶃ") in step:
                bstack111lll1l11l_opy_[bstack1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶄ")] = step[bstack1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᶅ")]
            bstack111lll11ll1_opy_.append(bstack111lll1l11l_opy_)
        cls.bstack1l111l1111_opy_({
            bstack1l11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᶆ"): bstack1l11l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᶇ"),
            bstack1l11l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᶈ"): bstack111lll11ll1_opy_
        })
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11lllll1_opy_, stage=STAGE.bstack1111111l_opy_)
    def bstack11111ll1l_opy_(cls, screenshot):
        cls.bstack1l111l1111_opy_({
            bstack1l11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᶉ"): bstack1l11l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᶊ"),
            bstack1l11l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᶋ"): [{
                bstack1l11l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᶌ"): bstack1l11l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᶍ"),
                bstack1l11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᶎ"): datetime.datetime.utcnow().isoformat() + bstack1l11l_opy_ (u"࡛ࠧࠩᶏ"),
                bstack1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᶐ"): screenshot[bstack1l11l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᶑ")],
                bstack1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶒ"): screenshot[bstack1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᶓ")]
            }]
        }, event_url=bstack1l11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᶔ"))
    @classmethod
    @bstack111llll1l1_opy_(class_method=True)
    def bstack1l11111ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111l1111_opy_({
            bstack1l11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᶕ"): bstack1l11l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᶖ"),
            bstack1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᶗ"): {
                bstack1l11l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᶘ"): cls.current_test_uuid(),
                bstack1l11l_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᶙ"): cls.bstack11l11l1lll_opy_(driver)
            }
        })
    @classmethod
    def bstack11l11l11l1_opy_(cls, event: str, bstack11l1111lll_opy_: bstack111lll111l_opy_):
        bstack111ll11l1l_opy_ = {
            bstack1l11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᶚ"): event,
            bstack11l1111lll_opy_.bstack111ll1ll1l_opy_(): bstack11l1111lll_opy_.bstack111ll11lll_opy_(event)
        }
        cls.bstack1l111l1111_opy_(bstack111ll11l1l_opy_)
        result = getattr(bstack11l1111lll_opy_, bstack1l11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᶛ"), None)
        if event == bstack1l11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᶜ"):
            threading.current_thread().bstackTestMeta = {bstack1l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᶝ"): bstack1l11l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᶞ")}
        elif event == bstack1l11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᶟ"):
            threading.current_thread().bstackTestMeta = {bstack1l11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᶠ"): getattr(result, bstack1l11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᶡ"), bstack1l11l_opy_ (u"ࠬ࠭ᶢ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᶣ"), None) is None or os.environ[bstack1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᶤ")] == bstack1l11l_opy_ (u"ࠣࡰࡸࡰࡱࠨᶥ")) and (os.environ.get(bstack1l11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᶦ"), None) is None or os.environ[bstack1l11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᶧ")] == bstack1l11l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᶨ")):
            return False
        return True
    @staticmethod
    def bstack111lll1ll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1lll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᶩ"): bstack1l11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᶪ"),
            bstack1l11l_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪᶫ"): bstack1l11l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᶬ")
        }
        if os.environ.get(bstack1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᶭ"), None):
            headers[bstack1l11l_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᶮ")] = bstack1l11l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᶯ").format(os.environ[bstack1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤᶰ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l11l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᶱ").format(bstack111lll11111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᶲ"), None)
    @staticmethod
    def bstack11l11l1lll_opy_(driver):
        return {
            bstack11lll1ll11l_opy_(): bstack11llll111ll_opy_(driver)
        }
    @staticmethod
    def bstack111lll1111l_opy_(exception_info, report):
        return [{bstack1l11l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᶳ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111l11ll11_opy_(typename):
        if bstack1l11l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᶴ") in typename:
            return bstack1l11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᶵ")
        return bstack1l11l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᶶ")