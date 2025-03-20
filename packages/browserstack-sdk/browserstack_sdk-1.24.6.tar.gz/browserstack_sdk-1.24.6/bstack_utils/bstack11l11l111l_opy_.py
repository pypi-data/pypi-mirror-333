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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1l11l1l1111_opy_, bstack1l11l11l1l1_opy_, bstack111111ll_opy_, bstack111lll1lll_opy_, bstack11lll111111_opy_, bstack11ll1l1l1l1_opy_, bstack11lll11111l_opy_, bstack1lllll11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l1111llll_opy_ import bstack11l1111ll11_opy_
import bstack_utils.bstack111l1lll1_opy_ as bstack1ll11l111l_opy_
from bstack_utils.bstack11l11l1l1l_opy_ import bstack1ll11l1l1_opy_
import bstack_utils.accessibility as bstack1111l1111_opy_
from bstack_utils.bstack1l11l11l11_opy_ import bstack1l11l11l11_opy_
from bstack_utils.bstack11l1l11l1l_opy_ import bstack11l111l11l_opy_
bstack111lll11111_opy_ = bstack11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᲾ")
logger = logging.getLogger(__name__)
class bstack111lllll1_opy_:
    bstack11l1111llll_opy_ = None
    bs_config = None
    bstack1l1l1lll_opy_ = None
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l11111l11l_opy_, stage=STAGE.bstack1lll11111l_opy_)
    def launch(cls, bs_config, bstack1l1l1lll_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1l1lll_opy_ = bstack1l1l1lll_opy_
        try:
            cls.bstack111lll1l1ll_opy_()
            bstack1l111lll1ll_opy_ = bstack1l11l1l1111_opy_(bs_config)
            bstack1l111lllll1_opy_ = bstack1l11l11l1l1_opy_(bs_config)
            data = bstack1ll11l111l_opy_.bstack111lll1ll1l_opy_(bs_config, bstack1l1l1lll_opy_)
            config = {
                bstack11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᲿ"): (bstack1l111lll1ll_opy_, bstack1l111lllll1_opy_),
                bstack11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ᳀"): cls.default_headers()
            }
            response = bstack111111ll_opy_(bstack11_opy_ (u"ࠫࡕࡕࡓࡕࠩ᳁"), cls.request_url(bstack11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬ᳂")), data, config)
            if response.status_code != 200:
                bstack1lll1l1l11l_opy_ = response.json()
                if bstack1lll1l1l11l_opy_[bstack11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ᳃")] == False:
                    cls.bstack111lll1l11l_opy_(bstack1lll1l1l11l_opy_)
                    return
                cls.bstack111lll1ll11_opy_(bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᳄")])
                cls.bstack111ll1l1l1l_opy_(bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᳅")])
                return None
            bstack111lll1llll_opy_ = cls.bstack111lll111l1_opy_(response)
            return bstack111lll1llll_opy_
        except Exception as error:
            logger.error(bstack11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢ᳆").format(str(error)))
            return None
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    def stop(cls, bstack111ll1ll111_opy_=None):
        if not bstack1ll11l1l1_opy_.on() and not bstack1111l1111_opy_.on():
            return
        if os.environ.get(bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ᳇")) == bstack11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᳈") or os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᳉")) == bstack11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ᳊"):
            logger.error(bstack11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪ᳋"))
            return {
                bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᳌"): bstack11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳍"),
                bstack11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᳎"): bstack11_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩ᳏")
            }
        try:
            cls.bstack11l1111llll_opy_.shutdown()
            data = {
                bstack11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᳐"): bstack1lllll11ll_opy_()
            }
            if not bstack111ll1ll111_opy_ is None:
                data[bstack11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪ᳑")] = [{
                    bstack11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ᳒"): bstack11_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭᳓"),
                    bstack11_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭᳔ࠩ"): bstack111ll1ll111_opy_
                }]
            config = {
                bstack11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶ᳕ࠫ"): cls.default_headers()
            }
            bstack1l1111111ll_opy_ = bstack11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴ᳖ࠬ").format(os.environ[bstack11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆ᳗ࠥ")])
            bstack111lll1l111_opy_ = cls.request_url(bstack1l1111111ll_opy_)
            response = bstack111111ll_opy_(bstack11_opy_ (u"࠭ࡐࡖࡖ᳘ࠪ"), bstack111lll1l111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨ᳙"))
        except Exception as error:
            logger.error(bstack11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧ᳚") + str(error))
            return {
                bstack11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᳛"): bstack11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳ᳜ࠩ"),
                bstack11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩ᳝ࠬ"): str(error)
            }
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    def bstack111lll111l1_opy_(cls, response):
        bstack1lll1l1l11l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack111lll1llll_opy_ = {}
        if bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠬࡰࡷࡵ᳞ࠩ")) is None:
            os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖ᳟ࠪ")] = bstack11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ᳠")
        else:
            os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ᳡")] = bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠩ࡭ࡻࡹ᳢࠭"), bstack11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ᳣"))
        os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅ᳤ࠩ")] = bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪ᳥ࠧ"), bstack11_opy_ (u"࠭࡮ࡶ࡮࡯᳦ࠫ"))
        logger.info(bstack11_opy_ (u"ࠧࡕࡧࡶࡸ࡭ࡻࡢࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤ᳧ࠬ") + os.getenv(bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ᳨࠭")));
        if bstack1ll11l1l1_opy_.bstack111ll1lll11_opy_(cls.bs_config, cls.bstack1l1l1lll_opy_.get(bstack11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᳩ"), bstack11_opy_ (u"ࠪࠫᳪ"))) is True:
            bstack111lll11l1l_opy_, build_hashed_id, bstack111lll1lll1_opy_ = cls.bstack111ll1ll1l1_opy_(bstack1lll1l1l11l_opy_)
            if bstack111lll11l1l_opy_ != None and build_hashed_id != None:
                bstack111lll1llll_opy_[bstack11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᳫ")] = {
                    bstack11_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨᳬ"): bstack111lll11l1l_opy_,
                    bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ᳭"): build_hashed_id,
                    bstack11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᳮ"): bstack111lll1lll1_opy_
                }
            else:
                bstack111lll1llll_opy_[bstack11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᳯ")] = {}
        else:
            bstack111lll1llll_opy_[bstack11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᳰ")] = {}
        if bstack1111l1111_opy_.bstack1l11l1111l1_opy_(cls.bs_config) is True:
            bstack111ll1llll1_opy_, build_hashed_id = cls.bstack111ll1ll1ll_opy_(bstack1lll1l1l11l_opy_)
            if bstack111ll1llll1_opy_ != None and build_hashed_id != None:
                bstack111lll1llll_opy_[bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᳱ")] = {
                    bstack11_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨᳲ"): bstack111ll1llll1_opy_,
                    bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᳳ"): build_hashed_id,
                }
            else:
                bstack111lll1llll_opy_[bstack11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᳴")] = {}
        else:
            bstack111lll1llll_opy_[bstack11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᳵ")] = {}
        if bstack111lll1llll_opy_[bstack11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᳶ")].get(bstack11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ᳷")) != None or bstack111lll1llll_opy_[bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᳸")].get(bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᳹")) != None:
            cls.bstack111lll1l1l1_opy_(bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠬࡰࡷࡵࠩᳺ")), bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ᳻")))
        return bstack111lll1llll_opy_
    @classmethod
    def bstack111ll1ll1l1_opy_(cls, bstack1lll1l1l11l_opy_):
        if bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ᳼")) == None:
            cls.bstack111lll1ll11_opy_()
            return [None, None, None]
        if bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᳽")][bstack11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ᳾")] != True:
            cls.bstack111lll1ll11_opy_(bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᳿")])
            return [None, None, None]
        logger.debug(bstack11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᴀ"))
        os.environ[bstack11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᴁ")] = bstack11_opy_ (u"࠭ࡴࡳࡷࡨࠫᴂ")
        if bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠧ࡫ࡹࡷࠫᴃ")):
            os.environ[bstack11_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬᴄ")] = json.dumps({
                bstack11_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫᴅ"): bstack1l11l1l1111_opy_(cls.bs_config),
                bstack11_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬᴆ"): bstack1l11l11l1l1_opy_(cls.bs_config)
            })
        if bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᴇ")):
            os.environ[bstack11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᴈ")] = bstack1lll1l1l11l_opy_[bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᴉ")]
        if bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᴊ")].get(bstack11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᴋ"), {}).get(bstack11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᴌ")):
            os.environ[bstack11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᴍ")] = str(bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᴎ")][bstack11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴏ")][bstack11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᴐ")])
        else:
            os.environ[bstack11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᴑ")] = bstack11_opy_ (u"ࠣࡰࡸࡰࡱࠨᴒ")
        return [bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠩ࡭ࡻࡹ࠭ᴓ")], bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᴔ")], os.environ[bstack11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᴕ")]]
    @classmethod
    def bstack111ll1ll1ll_opy_(cls, bstack1lll1l1l11l_opy_):
        if bstack1lll1l1l11l_opy_.get(bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴖ")) == None:
            cls.bstack111ll1l1l1l_opy_()
            return [None, None]
        if bstack1lll1l1l11l_opy_[bstack11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴗ")][bstack11_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᴘ")] != True:
            cls.bstack111ll1l1l1l_opy_(bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴙ")])
            return [None, None]
        if bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴚ")].get(bstack11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᴛ")):
            logger.debug(bstack11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᴜ"))
            parsed = json.loads(os.getenv(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᴝ"), bstack11_opy_ (u"࠭ࡻࡾࠩᴞ")))
            capabilities = bstack1ll11l111l_opy_.bstack111ll1l1l11_opy_(bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴟ")][bstack11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᴠ")][bstack11_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴡ")], bstack11_opy_ (u"ࠪࡲࡦࡳࡥࠨᴢ"), bstack11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᴣ"))
            bstack111ll1llll1_opy_ = capabilities[bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪᴤ")]
            os.environ[bstack11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᴥ")] = bstack111ll1llll1_opy_
            parsed[bstack11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᴦ")] = capabilities[bstack11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᴧ")]
            os.environ[bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᴨ")] = json.dumps(parsed)
            scripts = bstack1ll11l111l_opy_.bstack111ll1l1l11_opy_(bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴩ")][bstack11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᴪ")][bstack11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᴫ")], bstack11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᴬ"), bstack11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨᴭ"))
            bstack1l11l11l11_opy_.bstack1l111lll1l1_opy_(scripts)
            commands = bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴮ")][bstack11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᴯ")][bstack11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫᴰ")].get(bstack11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᴱ"))
            bstack1l11l11l11_opy_.bstack1l111lll11l_opy_(commands)
            bstack1l11l11l11_opy_.store()
        return [bstack111ll1llll1_opy_, bstack1lll1l1l11l_opy_[bstack11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᴲ")]]
    @classmethod
    def bstack111lll1ll11_opy_(cls, response=None):
        os.environ[bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᴳ")] = bstack11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᴴ")
        os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᴵ")] = bstack11_opy_ (u"ࠩࡱࡹࡱࡲࠧᴶ")
        os.environ[bstack11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᴷ")] = bstack11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᴸ")
        os.environ[bstack11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᴹ")] = bstack11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᴺ")
        os.environ[bstack11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᴻ")] = bstack11_opy_ (u"ࠣࡰࡸࡰࡱࠨᴼ")
        cls.bstack111lll1l11l_opy_(response, bstack11_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᴽ"))
        return [None, None, None]
    @classmethod
    def bstack111ll1l1l1l_opy_(cls, response=None):
        os.environ[bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᴾ")] = bstack11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᴿ")
        os.environ[bstack11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᵀ")] = bstack11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᵁ")
        os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᵂ")] = bstack11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᵃ")
        cls.bstack111lll1l11l_opy_(response, bstack11_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᵄ"))
        return [None, None, None]
    @classmethod
    def bstack111lll1l1l1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᵅ")] = jwt
        os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᵆ")] = build_hashed_id
    @classmethod
    def bstack111lll1l11l_opy_(cls, response=None, product=bstack11_opy_ (u"ࠧࠨᵇ")):
        if response == None:
            logger.error(product + bstack11_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᵈ"))
        for error in response[bstack11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᵉ")]:
            bstack11lllll11ll_opy_ = error[bstack11_opy_ (u"ࠨ࡭ࡨࡽࠬᵊ")]
            error_message = error[bstack11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᵋ")]
            if error_message:
                if bstack11lllll11ll_opy_ == bstack11_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤᵌ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧᵍ") + product + bstack11_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᵎ"))
    @classmethod
    def bstack111lll1l1ll_opy_(cls):
        if cls.bstack11l1111llll_opy_ is not None:
            return
        cls.bstack11l1111llll_opy_ = bstack11l1111ll11_opy_(cls.bstack111lll111ll_opy_)
        cls.bstack11l1111llll_opy_.start()
    @classmethod
    def bstack111ll11l1l_opy_(cls):
        if cls.bstack11l1111llll_opy_ is None:
            return
        cls.bstack11l1111llll_opy_.shutdown()
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    def bstack111lll111ll_opy_(cls, bstack111lll1l1l_opy_, event_url=bstack11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᵏ")):
        config = {
            bstack11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᵐ"): cls.default_headers()
        }
        logger.debug(bstack11_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣᵑ").format(bstack11_opy_ (u"ࠩ࠯ࠤࠬᵒ").join([event[bstack11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᵓ")] for event in bstack111lll1l1l_opy_])))
        response = bstack111111ll_opy_(bstack11_opy_ (u"ࠫࡕࡕࡓࡕࠩᵔ"), cls.request_url(event_url), bstack111lll1l1l_opy_, config)
        bstack1l11l111l11_opy_ = response.json()
    @classmethod
    def bstack111111111_opy_(cls, bstack111lll1l1l_opy_, event_url=bstack11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᵕ")):
        logger.debug(bstack11_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨᵖ").format(bstack111lll1l1l_opy_[bstack11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᵗ")]))
        if not bstack1ll11l111l_opy_.bstack111ll1ll11l_opy_(bstack111lll1l1l_opy_[bstack11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᵘ")]):
            logger.debug(bstack11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢᵙ").format(bstack111lll1l1l_opy_[bstack11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᵚ")]))
            return
        bstack11llll1l_opy_ = bstack1ll11l111l_opy_.bstack111ll1lll1l_opy_(bstack111lll1l1l_opy_[bstack11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᵛ")], bstack111lll1l1l_opy_.get(bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᵜ")))
        if bstack11llll1l_opy_ != None:
            if bstack111lll1l1l_opy_.get(bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᵝ")) != None:
                bstack111lll1l1l_opy_[bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᵞ")][bstack11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᵟ")] = bstack11llll1l_opy_
            else:
                bstack111lll1l1l_opy_[bstack11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᵠ")] = bstack11llll1l_opy_
        if event_url == bstack11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᵡ"):
            cls.bstack111lll1l1ll_opy_()
            logger.debug(bstack11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢᵢ").format(bstack111lll1l1l_opy_[bstack11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᵣ")]))
            cls.bstack11l1111llll_opy_.add(bstack111lll1l1l_opy_)
        elif event_url == bstack11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᵤ"):
            cls.bstack111lll111ll_opy_([bstack111lll1l1l_opy_], event_url)
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    def bstack1l1l11ll11_opy_(cls, logs):
        bstack111ll1lllll_opy_ = []
        for log in logs:
            bstack111ll1l1ll1_opy_ = {
                bstack11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᵥ"): bstack11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪᵦ"),
                bstack11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᵧ"): log[bstack11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᵨ")],
                bstack11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᵩ"): log[bstack11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᵪ")],
                bstack11_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ᵫ"): {},
                bstack11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᵬ"): log[bstack11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᵭ")],
            }
            if bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᵮ") in log:
                bstack111ll1l1ll1_opy_[bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᵯ")] = log[bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵰ")]
            elif bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᵱ") in log:
                bstack111ll1l1ll1_opy_[bstack11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᵲ")] = log[bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᵳ")]
            bstack111ll1lllll_opy_.append(bstack111ll1l1ll1_opy_)
        cls.bstack111111111_opy_({
            bstack11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᵴ"): bstack11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᵵ"),
            bstack11_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᵶ"): bstack111ll1lllll_opy_
        })
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    def bstack111lll11l11_opy_(cls, steps):
        bstack111lll11ll1_opy_ = []
        for step in steps:
            bstack111ll1l1lll_opy_ = {
                bstack11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᵷ"): bstack11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨᵸ"),
                bstack11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᵹ"): step[bstack11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᵺ")],
                bstack11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᵻ"): step[bstack11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᵼ")],
                bstack11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᵽ"): step[bstack11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᵾ")],
                bstack11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᵿ"): step[bstack11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᶀ")]
            }
            if bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶁ") in step:
                bstack111ll1l1lll_opy_[bstack11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᶂ")] = step[bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶃ")]
            elif bstack11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶄ") in step:
                bstack111ll1l1lll_opy_[bstack11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᶅ")] = step[bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᶆ")]
            bstack111lll11ll1_opy_.append(bstack111ll1l1lll_opy_)
        cls.bstack111111111_opy_({
            bstack11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᶇ"): bstack11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᶈ"),
            bstack11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᶉ"): bstack111lll11ll1_opy_
        })
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack1lll11111l_opy_)
    def bstack1l11ll11l1_opy_(cls, screenshot):
        cls.bstack111111111_opy_({
            bstack11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᶊ"): bstack11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᶋ"),
            bstack11_opy_ (u"ࠫࡱࡵࡧࡴࠩᶌ"): [{
                bstack11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᶍ"): bstack11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨᶎ"),
                bstack11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᶏ"): datetime.datetime.utcnow().isoformat() + bstack11_opy_ (u"ࠨ࡜ࠪᶐ"),
                bstack11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᶑ"): screenshot[bstack11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᶒ")],
                bstack11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᶓ"): screenshot[bstack11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᶔ")]
            }]
        }, event_url=bstack11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᶕ"))
    @classmethod
    @bstack111lll1lll_opy_(class_method=True)
    def bstack11ll1ll1ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111111111_opy_({
            bstack11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᶖ"): bstack11_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᶗ"),
            bstack11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᶘ"): {
                bstack11_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᶙ"): cls.current_test_uuid(),
                bstack11_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᶚ"): cls.bstack11l1l11lll_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1l1111l_opy_(cls, event: str, bstack111lll1l1l_opy_: bstack11l111l11l_opy_):
        bstack111llll111_opy_ = {
            bstack11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᶛ"): event,
            bstack111lll1l1l_opy_.bstack111llll11l_opy_(): bstack111lll1l1l_opy_.bstack111ll1l1l1_opy_(event)
        }
        cls.bstack111111111_opy_(bstack111llll111_opy_)
        result = getattr(bstack111lll1l1l_opy_, bstack11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᶜ"), None)
        if event == bstack11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᶝ"):
            threading.current_thread().bstackTestMeta = {bstack11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᶞ"): bstack11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᶟ")}
        elif event == bstack11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᶠ"):
            threading.current_thread().bstackTestMeta = {bstack11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᶡ"): getattr(result, bstack11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᶢ"), bstack11_opy_ (u"࠭ࠧᶣ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᶤ"), None) is None or os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᶥ")] == bstack11_opy_ (u"ࠤࡱࡹࡱࡲࠢᶦ")) and (os.environ.get(bstack11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᶧ"), None) is None or os.environ[bstack11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᶨ")] == bstack11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᶩ")):
            return False
        return True
    @staticmethod
    def bstack111lll11lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111lllll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᶪ"): bstack11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᶫ"),
            bstack11_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫᶬ"): bstack11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᶭ")
        }
        if os.environ.get(bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᶮ"), None):
            headers[bstack11_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᶯ")] = bstack11_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᶰ").format(os.environ[bstack11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥᶱ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᶲ").format(bstack111lll11111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᶳ"), None)
    @staticmethod
    def bstack11l1l11lll_opy_(driver):
        return {
            bstack11lll111111_opy_(): bstack11ll1l1l1l1_opy_(driver)
        }
    @staticmethod
    def bstack111lll1111l_opy_(exception_info, report):
        return [{bstack11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᶴ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111l11ll1l_opy_(typename):
        if bstack11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᶵ") in typename:
            return bstack11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᶶ")
        return bstack11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᶷ")