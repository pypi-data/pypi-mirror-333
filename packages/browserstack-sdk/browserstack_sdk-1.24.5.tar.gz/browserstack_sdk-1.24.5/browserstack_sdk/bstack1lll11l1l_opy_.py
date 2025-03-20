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
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l111ll111_opy_ = {}
        bstack11l1l1l1ll_opy_ = os.environ.get(bstack1l11l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ๤"), bstack1l11l_opy_ (u"ࠪࠫ๥"))
        if not bstack11l1l1l1ll_opy_:
            return bstack1l111ll111_opy_
        try:
            bstack11l1l1ll11_opy_ = json.loads(bstack11l1l1l1ll_opy_)
            if bstack1l11l_opy_ (u"ࠦࡴࡹࠢ๦") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠧࡵࡳࠣ๧")] = bstack11l1l1ll11_opy_[bstack1l11l_opy_ (u"ࠨ࡯ࡴࠤ๨")]
            if bstack1l11l_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦ๩") in bstack11l1l1ll11_opy_ or bstack1l11l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦ๪") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ๫")] = bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ๬"), bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢ๭")))
            if bstack1l11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨ๮") in bstack11l1l1ll11_opy_ or bstack1l11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ๯") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ๰")] = bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ๱"), bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ๲")))
            if bstack1l11l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ๳") in bstack11l1l1ll11_opy_ or bstack1l11l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ๴") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ๵")] = bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ๶"), bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ๷")))
            if bstack1l11l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣ๸") in bstack11l1l1ll11_opy_ or bstack1l11l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ๹") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ๺")] = bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦ๻"), bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ๼")))
            if bstack1l11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ๽") in bstack11l1l1ll11_opy_ or bstack1l11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ๾") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ๿")] = bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ຀"), bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤກ")))
            if bstack1l11l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢຂ") in bstack11l1l1ll11_opy_ or bstack1l11l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ຃") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣຄ")] = bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥ຅"), bstack11l1l1ll11_opy_.get(bstack1l11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥຆ")))
            if bstack1l11l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦງ") in bstack11l1l1ll11_opy_:
                bstack1l111ll111_opy_[bstack1l11l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧຈ")] = bstack11l1l1ll11_opy_[bstack1l11l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨຉ")]
        except Exception as error:
            logger.error(bstack1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦຊ") +  str(error))
        return bstack1l111ll111_opy_