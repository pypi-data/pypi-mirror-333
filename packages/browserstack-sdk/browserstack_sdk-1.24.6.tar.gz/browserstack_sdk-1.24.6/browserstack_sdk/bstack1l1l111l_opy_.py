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
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll11l11l_opy_ = {}
        bstack11l1l1ll11_opy_ = os.environ.get(bstack11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ๥"), bstack11_opy_ (u"ࠫࠬ๦"))
        if not bstack11l1l1ll11_opy_:
            return bstack1ll11l11l_opy_
        try:
            bstack11l1l1l1ll_opy_ = json.loads(bstack11l1l1ll11_opy_)
            if bstack11_opy_ (u"ࠧࡵࡳࠣ๧") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠨ࡯ࡴࠤ๨")] = bstack11l1l1l1ll_opy_[bstack11_opy_ (u"ࠢࡰࡵࠥ๩")]
            if bstack11_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ๪") in bstack11l1l1l1ll_opy_ or bstack11_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ๫") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ๬")] = bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ๭"), bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ๮")))
            if bstack11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ๯") in bstack11l1l1l1ll_opy_ or bstack11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ๰") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ๱")] = bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ๲"), bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ๳")))
            if bstack11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ๴") in bstack11l1l1l1ll_opy_ or bstack11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ๵") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ๶")] = bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ๷"), bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ๸")))
            if bstack11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤ๹") in bstack11l1l1l1ll_opy_ or bstack11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ๺") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ๻")] = bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ๼"), bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ๽")))
            if bstack11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ๾") in bstack11l1l1l1ll_opy_ or bstack11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ๿") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ຀")] = bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧກ"), bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥຂ")))
            if bstack11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ຃") in bstack11l1l1l1ll_opy_ or bstack11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣຄ") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ຅")] = bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦຆ"), bstack11l1l1l1ll_opy_.get(bstack11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦງ")))
            if bstack11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧຈ") in bstack11l1l1l1ll_opy_:
                bstack1ll11l11l_opy_[bstack11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨຉ")] = bstack11l1l1l1ll_opy_[bstack11_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢຊ")]
        except Exception as error:
            logger.error(bstack11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧ຋") +  str(error))
        return bstack1ll11l11l_opy_