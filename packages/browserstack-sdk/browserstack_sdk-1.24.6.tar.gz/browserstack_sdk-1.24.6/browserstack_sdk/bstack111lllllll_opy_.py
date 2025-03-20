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
class RobotHandler():
    def __init__(self, args, logger, bstack111l1l1l11_opy_, bstack111l1l1lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack111l1l1l11_opy_ = bstack111l1l1l11_opy_
        self.bstack111l1l1lll_opy_ = bstack111l1l1lll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l11111l1_opy_(bstack111l11llll_opy_):
        bstack111l11lll1_opy_ = []
        if bstack111l11llll_opy_:
            tokens = str(os.path.basename(bstack111l11llll_opy_)).split(bstack11_opy_ (u"ࠣࡡࠥ࿈"))
            camelcase_name = bstack11_opy_ (u"ࠤࠣࠦ࿉").join(t.title() for t in tokens)
            suite_name, bstack111l11ll11_opy_ = os.path.splitext(camelcase_name)
            bstack111l11lll1_opy_.append(suite_name)
        return bstack111l11lll1_opy_
    @staticmethod
    def bstack111l11ll1l_opy_(typename):
        if bstack11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ࿊") in typename:
            return bstack11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ࿋")
        return bstack11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ࿌")