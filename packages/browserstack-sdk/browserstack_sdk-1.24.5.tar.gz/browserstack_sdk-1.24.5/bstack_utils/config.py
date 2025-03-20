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
conf = {
    bstack1l11l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᕡ"): False,
    bstack1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᕢ"): True,
    bstack1l11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧᕣ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._1l111l1l1ll_opy_ = conf
    @classmethod
    def bstack111lll11_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack1l111l1ll11_opy_=None):
        return self._1l111l1l1ll_opy_.get(property_name, bstack1l111l1ll11_opy_)
    def bstack1ll1l11l11_opy_(self, property_name, bstack1l111l1l1l1_opy_):
        self._1l111l1l1ll_opy_[property_name] = bstack1l111l1l1l1_opy_
    def bstack11llll1111_opy_(self, val):
        self._1l111l1l1ll_opy_[bstack1l11l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᕤ")] = bool(val)
    def bstack111l1l1l1l_opy_(self):
        return self._1l111l1l1ll_opy_.get(bstack1l11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩᕥ"), False)