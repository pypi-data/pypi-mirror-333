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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1l1l1_opy_, bstack1111ll1111_opy_
class bstack1llll11ll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l11l_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᑐ").format(self.name)
class bstack1lll11ll11l_opy_(Enum):
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
        return bstack1l11l_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᑑ").format(self.name)
class bstack1lllll1lll1_opy_(bstack1111l1l1l1_opy_):
    bstack1ll1ll1l1l1_opy_: List[str]
    bstack1l1l11111l1_opy_: Dict[str, str]
    state: bstack1lll11ll11l_opy_
    bstack1111l1lll1_opy_: datetime
    bstack1111l11l11_opy_: datetime
    def __init__(
        self,
        context: bstack1111ll1111_opy_,
        bstack1ll1ll1l1l1_opy_: List[str],
        bstack1l1l11111l1_opy_: Dict[str, str],
        state=bstack1lll11ll11l_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1l1l1_opy_
        self.bstack1l1l11111l1_opy_ = bstack1l1l11111l1_opy_
        self.state = state
        self.bstack1111l1lll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1111l11l11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111l1ll1l_opy_(self, bstack1111llllll_opy_: bstack1lll11ll11l_opy_):
        bstack1111ll1l11_opy_ = bstack1lll11ll11l_opy_(bstack1111llllll_opy_).name
        if not bstack1111ll1l11_opy_:
            return False
        if bstack1111llllll_opy_ == self.state:
            return False
        self.state = bstack1111llllll_opy_
        self.bstack1111l11l11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11lll1ll1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lllll11111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l1lll1l_opy_ = bstack1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦᑒ")
    bstack1l11lll1l11_opy_ = bstack1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᑓ")
    bstack1lll111ll11_opy_ = bstack1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᑔ")
    bstack1l1l111l11l_opy_ = bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᑕ")
    bstack1l1l11111ll_opy_ = bstack1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᑖ")
    bstack1l1lll1111l_opy_ = bstack1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᑗ")
    bstack1ll11l11l11_opy_ = bstack1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᑘ")
    bstack1ll111l111l_opy_ = bstack1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᑙ")
    bstack1ll111l1lll_opy_ = bstack1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᑚ")
    bstack1l11ll1l1l1_opy_ = bstack1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᑛ")
    bstack1ll1llll1l1_opy_ = bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᑜ")
    bstack1ll111lll11_opy_ = bstack1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᑝ")
    bstack1l1l11ll111_opy_ = bstack1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤᑞ")
    bstack1ll1111l111_opy_ = bstack1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᑟ")
    bstack1ll1ll1llll_opy_ = bstack1l11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᑠ")
    bstack1l1ll1lll11_opy_ = bstack1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᑡ")
    bstack1l11llll1l1_opy_ = bstack1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᑢ")
    bstack1l11llll111_opy_ = bstack1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᑣ")
    bstack1l1l1l11l1l_opy_ = bstack1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᑤ")
    bstack1l11l1llll1_opy_ = bstack1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᑥ")
    bstack1l1l1lll11l_opy_ = bstack1l11l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᑦ")
    bstack1l1l111l1l1_opy_ = bstack1l11l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᑧ")
    bstack1l1l1l111ll_opy_ = bstack1l11l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᑨ")
    bstack1l1l11lll11_opy_ = bstack1l11l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᑩ")
    bstack1l1l111lll1_opy_ = bstack1l11l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᑪ")
    bstack1l1l1111lll_opy_ = bstack1l11l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᑫ")
    bstack1l1l111l1ll_opy_ = bstack1l11l_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᑬ")
    bstack1l1l1111ll1_opy_ = bstack1l11l_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᑭ")
    bstack1l11ll1l111_opy_ = bstack1l11l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᑮ")
    bstack1ll11l1llll_opy_ = bstack1l11l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᑯ")
    bstack1ll1l11111l_opy_ = bstack1l11l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᑰ")
    bstack11111ll1l1_opy_: Dict[str, bstack1lllll1lll1_opy_] = dict()
    bstack1l11l1l1l11_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1ll1l1l1_opy_: List[str]
    bstack1l1l11111l1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1ll1l1l1_opy_: List[str],
        bstack1l1l11111l1_opy_: Dict[str, str],
    ):
        self.bstack1ll1ll1l1l1_opy_ = bstack1ll1ll1l1l1_opy_
        self.bstack1l1l11111l1_opy_ = bstack1l1l11111l1_opy_
    def track_event(
        self,
        context: bstack1l11lll1ll1_opy_,
        test_framework_state: bstack1lll11ll11l_opy_,
        test_hook_state: bstack1llll11ll1l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l11l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᑱ") + str(kwargs) + bstack1l11l_opy_ (u"ࠧࠨᑲ"))
    def bstack1l11lll11ll_opy_(
        self,
        instance: bstack1lllll1lll1_opy_,
        bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1l1l1l1_opy_ = TestFramework.bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_)
        if not bstack1l1l1l1l1l1_opy_ in TestFramework.bstack1l11l1l1l11_opy_:
            return
        self.logger.debug(bstack1l11l_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࠤᑳ") + str(len(TestFramework.bstack1l11l1l1l11_opy_[bstack1l1l1l1l1l1_opy_])) + bstack1l11l_opy_ (u"ࠢࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦᑴ"))
        for callback in TestFramework.bstack1l11l1l1l11_opy_[bstack1l1l1l1l1l1_opy_]:
            try:
                callback(self, instance, bstack11111lll1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨᑵ") + str(e) + bstack1l11l_opy_ (u"ࠤࠥᑶ"))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll1111llll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1ll111ll1l1_opy_(self, instance, bstack11111lll1l_opy_):
        return
    @abc.abstractmethod
    def bstack1ll1111lll1_opy_(self, instance, bstack11111lll1l_opy_):
        return
    @staticmethod
    def bstack1111l1llll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1111l1l1l1_opy_.create_context(target)
        instance = TestFramework.bstack11111ll1l1_opy_.get(ctx.id, None)
        if instance and instance.bstack1111ll11l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll111l1ll1_opy_(reverse=True) -> List[bstack1lllll1lll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11111ll1l1_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1lll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111lllll_opy_(ctx: bstack1111ll1111_opy_, reverse=True) -> List[bstack1lllll1lll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11111ll1l1_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1lll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111l111l1l_opy_(instance: bstack1lllll1lll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1111ll111l_opy_(instance: bstack1lllll1lll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111l1ll1l_opy_(instance: bstack1lllll1lll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11l_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥࡱࡥࡺ࠿ࡾ࡯ࡪࡿࡽࠡࡸࡤࡰࡺ࡫࠽ࠣᑷ") + str(value) + bstack1l11l_opy_ (u"ࠦࠧᑸ"))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll11lll_opy_(instance: bstack1lllll1lll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l11l_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࠥᑹ") + str(entries) + bstack1l11l_opy_ (u"ࠨࠢᑺ"))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l11l1l11ll_opy_(instance: bstack1lll11ll11l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥࡱࡥࡺ࠿ࡾ࡯ࡪࡿࡽࠡࡸࡤࡰࡺ࡫࠽ࠣᑻ") + str(value) + bstack1l11l_opy_ (u"ࠣࠤᑼ"))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1111l1llll_opy_(target, strict)
        return TestFramework.bstack1111ll111l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1111l1llll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1l111l111_opy_(instance: bstack1lllll1lll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l1l1l111l1_opy_(instance: bstack1lllll1lll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_]):
        return bstack1l11l_opy_ (u"ࠤ࠽ࠦᑽ").join((bstack1lll11ll11l_opy_(bstack11111lll1l_opy_[0]).name, bstack1llll11ll1l_opy_(bstack11111lll1l_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll1l11l_opy_(bstack11111lll1l_opy_: Tuple[bstack1lll11ll11l_opy_, bstack1llll11ll1l_opy_], callback: Callable):
        bstack1l1l1l1l1l1_opy_ = TestFramework.bstack1l1l1l1ll1l_opy_(bstack11111lll1l_opy_)
        TestFramework.logger.debug(bstack1l11l_opy_ (u"ࠥࡷࡪࡺ࡟ࡩࡱࡲ࡯ࡤࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡪࡲࡳࡰࡥࡲࡦࡩ࡬ࡷࡹࡸࡹࡠ࡭ࡨࡽࡂࠨᑾ") + str(bstack1l1l1l1l1l1_opy_) + bstack1l11l_opy_ (u"ࠦࠧᑿ"))
        if not bstack1l1l1l1l1l1_opy_ in TestFramework.bstack1l11l1l1l11_opy_:
            TestFramework.bstack1l11l1l1l11_opy_[bstack1l1l1l1l1l1_opy_] = []
        TestFramework.bstack1l11l1l1l11_opy_[bstack1l1l1l1l1l1_opy_].append(callback)
    @staticmethod
    def bstack1ll11ll1l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡷ࡭ࡳࡹࠢᒀ"):
            return klass.__qualname__
        return module + bstack1l11l_opy_ (u"ࠨ࠮ࠣᒁ") + klass.__qualname__
    @staticmethod
    def bstack1ll11l1l1ll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}