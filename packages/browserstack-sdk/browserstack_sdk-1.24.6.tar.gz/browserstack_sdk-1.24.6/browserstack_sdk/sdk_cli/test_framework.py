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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111ll11l1_opy_ import bstack1111ll1l11_opy_, bstack1111l1lll1_opy_
class bstack111111l1ll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᑑ").format(self.name)
class bstack1lll1l11ll1_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᑒ").format(self.name)
class bstack1lllll1lll1_opy_(bstack1111ll1l11_opy_):
    bstack1lll111l1l1_opy_: List[str]
    bstack1l1l1111l1l_opy_: Dict[str, str]
    state: bstack1lll1l11ll1_opy_
    bstack1111l1111l_opy_: datetime
    bstack1111lll1ll_opy_: datetime
    def __init__(
        self,
        context: bstack1111l1lll1_opy_,
        bstack1lll111l1l1_opy_: List[str],
        bstack1l1l1111l1l_opy_: Dict[str, str],
        state=bstack1lll1l11ll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1lll111l1l1_opy_ = bstack1lll111l1l1_opy_
        self.bstack1l1l1111l1l_opy_ = bstack1l1l1111l1l_opy_
        self.state = state
        self.bstack1111l1111l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1111lll1ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111lll1l1_opy_(self, bstack1111l1l1ll_opy_: bstack1lll1l11ll1_opy_):
        bstack111l1111ll_opy_ = bstack1lll1l11ll1_opy_(bstack1111l1l1ll_opy_).name
        if not bstack111l1111ll_opy_:
            return False
        if bstack1111l1l1ll_opy_ == self.state:
            return False
        self.state = bstack1111l1l1ll_opy_
        self.bstack1111lll1ll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l1l1l11l11_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1llll1l111l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1ll1l111_opy_ = bstack11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᑓ")
    bstack1l1l1l111l1_opy_ = bstack11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᑔ")
    bstack1lll11111ll_opy_ = bstack11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᑕ")
    bstack1l1l11llll1_opy_ = bstack11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᑖ")
    bstack1l1l1l1111l_opy_ = bstack11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᑗ")
    bstack1l1ll1ll1ll_opy_ = bstack11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᑘ")
    bstack1ll1111ll11_opy_ = bstack11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᑙ")
    bstack1ll11l1lll1_opy_ = bstack11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᑚ")
    bstack1ll11llll1l_opy_ = bstack11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᑛ")
    bstack1l11ll111ll_opy_ = bstack11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᑜ")
    bstack1lll11111l1_opy_ = bstack11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᑝ")
    bstack1ll11lllll1_opy_ = bstack11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᑞ")
    bstack1l1l11lllll_opy_ = bstack11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᑟ")
    bstack1l1lllllll1_opy_ = bstack11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥᑠ")
    bstack1ll1llll111_opy_ = bstack11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᑡ")
    bstack1l1ll1ll1l1_opy_ = bstack11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᑢ")
    bstack1l11ll11lll_opy_ = bstack11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᑣ")
    bstack1l1l11l111l_opy_ = bstack11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᑤ")
    bstack1l11ll11l11_opy_ = bstack11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤᑥ")
    bstack1l11l1lllll_opy_ = bstack11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬᑦ")
    bstack1l1l1lll11l_opy_ = bstack11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᑧ")
    bstack1l11ll1ll1l_opy_ = bstack11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᑨ")
    bstack1l1l11ll11l_opy_ = bstack11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᑩ")
    bstack1l1l111l1ll_opy_ = bstack11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧᑪ")
    bstack1l1l11lll1l_opy_ = bstack11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥᑫ")
    bstack1l1l111lll1_opy_ = bstack11_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤᑬ")
    bstack1l11lll1ll1_opy_ = bstack11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥᑭ")
    bstack1l1l111l111_opy_ = bstack11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᑮ")
    bstack1l11lll1lll_opy_ = bstack11_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᑯ")
    bstack1ll1111ll1l_opy_ = bstack11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧᑰ")
    bstack1ll111ll1l1_opy_ = bstack11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨᑱ")
    bstack111l11111l_opy_: Dict[str, bstack1lllll1lll1_opy_] = dict()
    bstack1l11l1lll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1lll111l1l1_opy_: List[str]
    bstack1l1l1111l1l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1lll111l1l1_opy_: List[str],
        bstack1l1l1111l1l_opy_: Dict[str, str],
    ):
        self.bstack1lll111l1l1_opy_ = bstack1lll111l1l1_opy_
        self.bstack1l1l1111l1l_opy_ = bstack1l1l1111l1l_opy_
    def track_event(
        self,
        context: bstack1l1l1l11l11_opy_,
        test_framework_state: bstack1lll1l11ll1_opy_,
        test_hook_state: bstack111111l1ll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᑲ") + str(kwargs) + bstack11_opy_ (u"ࠨࠢᑳ"))
    def bstack1l1l1111l11_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_)
        if not bstack1l1l1l1ll1l_opy_ in TestFramework.bstack1l11l1lll1l_opy_:
            return
        self.logger.debug(bstack11_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࠥᑴ") + str(len(TestFramework.bstack1l11l1lll1l_opy_[bstack1l1l1l1ll1l_opy_])) + bstack11_opy_ (u"ࠣࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠧᑵ"))
        for callback in TestFramework.bstack1l11l1lll1l_opy_[bstack1l1l1l1ll1l_opy_]:
            try:
                callback(self, instance, bstack1111l11l11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࠢᑶ") + str(e) + bstack11_opy_ (u"ࠥࠦᑷ"))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll11lll1ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1ll11ll111l_opy_(self, instance, bstack1111l11l11_opy_):
        return
    @abc.abstractmethod
    def bstack1ll111lllll_opy_(self, instance, bstack1111l11l11_opy_):
        return
    @staticmethod
    def bstack11111ll1ll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1111ll1l11_opy_.create_context(target)
        instance = TestFramework.bstack111l11111l_opy_.get(ctx.id, None)
        if instance and instance.bstack111l111l1l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll11l111ll_opy_(reverse=True) -> List[bstack1lllll1lll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack111l11111l_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111ll111_opy_(ctx: bstack1111l1lll1_opy_, reverse=True) -> List[bstack1lllll1lll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack111l11111l_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111l11lll_opy_(instance: bstack1lllll1lll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111lll1l_opy_(instance: bstack1lllll1lll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111lll1l1_opy_(instance: bstack1lllll1lll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦ࡫ࡦࡻࡀࡿࡰ࡫ࡹࡾࠢࡹࡥࡱࡻࡥ࠾ࠤᑸ") + str(value) + bstack11_opy_ (u"ࠧࠨᑹ"))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll1111l_opy_(instance: bstack1lllll1lll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࠦᑺ") + str(entries) + bstack11_opy_ (u"ࠢࠣᑻ"))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l11l1l11ll_opy_(instance: bstack1lll1l11ll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦ࡫ࡦࡻࡀࡿࡰ࡫ࡹࡾࠢࡹࡥࡱࡻࡥ࠾ࠤᑼ") + str(value) + bstack11_opy_ (u"ࠤࠥᑽ"))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111ll1ll_opy_(target, strict)
        return TestFramework.bstack11111lll1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111ll1ll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1l1l11ll1_opy_(instance: bstack1lllll1lll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11lll111l_opy_(instance: bstack1lllll1lll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_]):
        return bstack11_opy_ (u"ࠥ࠾ࠧᑾ").join((bstack1lll1l11ll1_opy_(bstack1111l11l11_opy_[0]).name, bstack111111l1ll_opy_(bstack1111l11l11_opy_[1]).name))
    @staticmethod
    def bstack1ll1llllll1_opy_(bstack1111l11l11_opy_: Tuple[bstack1lll1l11ll1_opy_, bstack111111l1ll_opy_], callback: Callable):
        bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_)
        TestFramework.logger.debug(bstack11_opy_ (u"ࠦࡸ࡫ࡴࡠࡪࡲࡳࡰࡥࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢ࡫ࡳࡴࡱ࡟ࡳࡧࡪ࡭ࡸࡺࡲࡺࡡ࡮ࡩࡾࡃࠢᑿ") + str(bstack1l1l1l1ll1l_opy_) + bstack11_opy_ (u"ࠧࠨᒀ"))
        if not bstack1l1l1l1ll1l_opy_ in TestFramework.bstack1l11l1lll1l_opy_:
            TestFramework.bstack1l11l1lll1l_opy_[bstack1l1l1l1ll1l_opy_] = []
        TestFramework.bstack1l11l1lll1l_opy_[bstack1l1l1l1ll1l_opy_].append(callback)
    @staticmethod
    def bstack1ll11l1l111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᒁ"):
            return klass.__qualname__
        return module + bstack11_opy_ (u"ࠢ࠯ࠤᒂ") + klass.__qualname__
    @staticmethod
    def bstack1ll11lll11l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}