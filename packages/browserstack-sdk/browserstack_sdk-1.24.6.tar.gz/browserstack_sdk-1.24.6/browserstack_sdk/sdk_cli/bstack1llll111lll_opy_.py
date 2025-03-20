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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111l11l11l_opy_ import bstack111l11l1l1_opy_
class bstack1lll11l1lll_opy_(abc.ABC):
    bin_session_id: str
    bstack111l11l11l_opy_: bstack111l11l1l1_opy_
    def __init__(self):
        self.bstack11111l11ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111l11l11l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack111111111l_opy_(self):
        return (self.bstack11111l11ll_opy_ != None and self.bin_session_id != None and self.bstack111l11l11l_opy_ != None)
    def configure(self, bstack11111l11ll_opy_, config, bin_session_id: str, bstack111l11l11l_opy_: bstack111l11l1l1_opy_):
        self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111l11l11l_opy_ = bstack111l11l11l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡯ࡲࡨࡺࡲࡥࠡࡽࡶࡩࡱ࡬࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡ࠱ࡣࡤࡴࡡ࡮ࡧࡢࡣࢂࡀࠠࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᅛ") + str(self.bin_session_id) + bstack11_opy_ (u"ࠨࠢᅜ"))
    def bstack1ll1ll11lll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11_opy_ (u"ࠢࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡓࡵ࡮ࡦࠤᅝ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False