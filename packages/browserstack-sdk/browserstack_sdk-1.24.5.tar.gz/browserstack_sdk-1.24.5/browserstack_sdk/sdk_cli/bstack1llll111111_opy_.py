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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111l11l11l_opy_ import bstack111l11l1l1_opy_
class bstack1lll1ll1l1l_opy_(abc.ABC):
    bin_session_id: str
    bstack111l11l11l_opy_: bstack111l11l1l1_opy_
    def __init__(self):
        self.bstack1llllll1l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111l11l11l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll111l1l_opy_(self):
        return (self.bstack1llllll1l11_opy_ != None and self.bin_session_id != None and self.bstack111l11l11l_opy_ != None)
    def configure(self, bstack1llllll1l11_opy_, config, bin_session_id: str, bstack111l11l11l_opy_: bstack111l11l1l1_opy_):
        self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111l11l11l_opy_ = bstack111l11l11l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l11l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᅚ") + str(self.bin_session_id) + bstack1l11l_opy_ (u"ࠧࠨᅛ"))
    def bstack1ll1l1ll1ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l11l_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣᅜ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False