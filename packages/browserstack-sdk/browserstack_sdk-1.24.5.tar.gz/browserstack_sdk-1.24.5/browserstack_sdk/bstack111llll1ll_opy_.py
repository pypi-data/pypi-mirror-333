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
class RobotHandler():
    def __init__(self, args, logger, bstack111ll11111_opy_, bstack111l1llll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack111ll11111_opy_ = bstack111ll11111_opy_
        self.bstack111l1llll1_opy_ = bstack111l1llll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l111l111_opy_(bstack111l11lll1_opy_):
        bstack111l11llll_opy_ = []
        if bstack111l11lll1_opy_:
            tokens = str(os.path.basename(bstack111l11lll1_opy_)).split(bstack1l11l_opy_ (u"ࠢࡠࠤ࿇"))
            camelcase_name = bstack1l11l_opy_ (u"ࠣࠢࠥ࿈").join(t.title() for t in tokens)
            suite_name, bstack111l11ll1l_opy_ = os.path.splitext(camelcase_name)
            bstack111l11llll_opy_.append(suite_name)
        return bstack111l11llll_opy_
    @staticmethod
    def bstack111l11ll11_opy_(typename):
        if bstack1l11l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ࿉") in typename:
            return bstack1l11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ࿊")
        return bstack1l11l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ࿋")