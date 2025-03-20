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
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1111ll1111_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1111l1l1l1_opy_:
    bstack1l11l1l11l1_opy_ = bstack1l11l_opy_ (u"ࠢࡣࡧࡱࡧ࡭ࡳࡡࡳ࡭ࠥᒂ")
    context: bstack1111ll1111_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1111ll1111_opy_):
        self.context = context
        self.data = dict({bstack1111l1l1l1_opy_.bstack1l11l1l11l1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᒃ"), bstack1l11l_opy_ (u"ࠩ࠳ࠫᒄ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1111ll11l1_opy_(self, target: object):
        return bstack1111l1l1l1_opy_.create_context(target) == self.context
    def bstack1ll1l11l1ll_opy_(self, context: bstack1111ll1111_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1l1lll11ll_opy_(self, key: str, value: timedelta):
        self.data[bstack1111l1l1l1_opy_.bstack1l11l1l11l1_opy_][key] += value
    def bstack1lll1l111ll_opy_(self) -> dict:
        return self.data[bstack1111l1l1l1_opy_.bstack1l11l1l11l1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1111ll1111_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )