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
import threading
import logging
logger = logging.getLogger(__name__)
bstack11l111l11l1_opy_ = 1000
bstack11l1111ll1l_opy_ = 2
class bstack11l1111ll11_opy_:
    def __init__(self, handler, bstack11l111l111l_opy_=bstack11l111l11l1_opy_, bstack11l111l1l11_opy_=bstack11l1111ll1l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11l111l111l_opy_ = bstack11l111l111l_opy_
        self.bstack11l111l1l11_opy_ = bstack11l111l1l11_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111l111lll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack11l1111l1ll_opy_()
    def bstack11l1111l1ll_opy_(self):
        self.bstack111l111lll_opy_ = threading.Event()
        def bstack11l1111l1l1_opy_():
            self.bstack111l111lll_opy_.wait(self.bstack11l111l1l11_opy_)
            if not self.bstack111l111lll_opy_.is_set():
                self.bstack11l111l11ll_opy_()
        self.timer = threading.Thread(target=bstack11l1111l1l1_opy_, daemon=True)
        self.timer.start()
    def bstack11l1111lll1_opy_(self):
        try:
            if self.bstack111l111lll_opy_ and not self.bstack111l111lll_opy_.is_set():
                self.bstack111l111lll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩ᱄") + (str(e) or bstack11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢ᱅")))
        finally:
            self.timer = None
    def bstack11l111l1111_opy_(self):
        if self.timer:
            self.bstack11l1111lll1_opy_()
        self.bstack11l1111l1ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11l111l111l_opy_:
                threading.Thread(target=self.bstack11l111l11ll_opy_).start()
    def bstack11l111l11ll_opy_(self, source = bstack11_opy_ (u"ࠧࠨ᱆")):
        with self.lock:
            if not self.queue:
                self.bstack11l111l1111_opy_()
                return
            data = self.queue[:self.bstack11l111l111l_opy_]
            del self.queue[:self.bstack11l111l111l_opy_]
        self.handler(data)
        if source != bstack11_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ᱇"):
            self.bstack11l111l1111_opy_()
    def shutdown(self):
        self.bstack11l1111lll1_opy_()
        while self.queue:
            self.bstack11l111l11ll_opy_(source=bstack11_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ᱈"))