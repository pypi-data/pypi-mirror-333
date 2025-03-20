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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1111ll11l1_opy_ import bstack1111ll1l11_opy_, bstack1111l1lll1_opy_
import os
import threading
class bstack11111l1lll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11_opy_ (u"ࠢࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨ࿎").format(self.name)
class bstack11111ll11l_opy_(Enum):
    NONE = 0
    bstack1111ll1ll1_opy_ = 1
    bstack111l111111_opy_ = 3
    bstack1111ll1l1l_opy_ = 4
    bstack1111l111ll_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣ࿏").format(self.name)
class bstack1111lll11l_opy_(bstack1111ll1l11_opy_):
    framework_name: str
    framework_version: str
    state: bstack11111ll11l_opy_
    previous_state: bstack11111ll11l_opy_
    bstack1111l1111l_opy_: datetime
    bstack1111lll1ll_opy_: datetime
    def __init__(
        self,
        context: bstack1111l1lll1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack11111ll11l_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack11111ll11l_opy_.NONE
        self.bstack1111l1111l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1111lll1ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111lll1l1_opy_(self, bstack1111l1l1ll_opy_: bstack11111ll11l_opy_):
        bstack111l1111ll_opy_ = bstack11111ll11l_opy_(bstack1111l1l1ll_opy_).name
        if not bstack111l1111ll_opy_:
            return False
        if bstack1111l1l1ll_opy_ == self.state:
            return False
        if self.state == bstack11111ll11l_opy_.bstack111l111111_opy_: # bstack1111l1llll_opy_ bstack1111l1l11l_opy_ for bstack111l111l11_opy_ in bstack1111lllll1_opy_, it bstack1111ll1lll_opy_ bstack11111lllll_opy_ bstack1111ll1111_opy_ times bstack1111llllll_opy_ a new state
            return True
        if (
            bstack1111l1l1ll_opy_ == bstack11111ll11l_opy_.NONE
            or (self.state != bstack11111ll11l_opy_.NONE and bstack1111l1l1ll_opy_ == bstack11111ll11l_opy_.bstack1111ll1ll1_opy_)
            or (self.state < bstack11111ll11l_opy_.bstack1111ll1ll1_opy_ and bstack1111l1l1ll_opy_ == bstack11111ll11l_opy_.bstack1111ll1l1l_opy_)
            or (self.state < bstack11111ll11l_opy_.bstack1111ll1ll1_opy_ and bstack1111l1l1ll_opy_ == bstack11111ll11l_opy_.QUIT)
        ):
            raise ValueError(bstack11_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡹࡧࡴࡦࠢࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࠣ࿐") + str(self.state) + bstack11_opy_ (u"ࠥࠤࡂࡄࠠࠣ࿑") + str(bstack1111l1l1ll_opy_))
        self.previous_state = self.state
        self.state = bstack1111l1l1ll_opy_
        self.bstack1111lll1ll_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack11111lll11_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack111l11111l_opy_: Dict[str, bstack1111lll11l_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack1111l1ll11_opy_(self, instance: bstack1111lll11l_opy_, method_name: str, bstack1111l1l1l1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1111lll111_opy_(
        self, method_name, previous_state: bstack11111ll11l_opy_, *args, **kwargs
    ) -> bstack11111ll11l_opy_:
        return
    @abc.abstractmethod
    def bstack1111l1ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1111l11ll1_opy_(self, bstack1111l11l1l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1111l11l1l_opy_:
                bstack111l1111l1_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack111l1111l1_opy_):
                    self.logger.warning(bstack11_opy_ (u"ࠦࡺࡴࡰࡢࡶࡦ࡬ࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࠤ࿒") + str(method_name) + bstack11_opy_ (u"ࠧࠨ࿓"))
                    continue
                bstack1111l11111_opy_ = self.bstack1111lll111_opy_(
                    method_name, previous_state=bstack11111ll11l_opy_.NONE
                )
                bstack11111ll1l1_opy_ = self.bstack11111llll1_opy_(
                    method_name,
                    (bstack1111l11111_opy_ if bstack1111l11111_opy_ else bstack11111ll11l_opy_.NONE),
                    bstack111l1111l1_opy_,
                )
                if not callable(bstack11111ll1l1_opy_):
                    self.logger.warning(bstack11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠦ࡮ࡰࡶࠣࡴࡦࡺࡣࡩࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࠮ࡻࡴࡧ࡯ࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃ࠺ࠡࠤ࿔") + str(self.framework_version) + bstack11_opy_ (u"ࠢࠪࠤ࿕"))
                    continue
                setattr(clazz, method_name, bstack11111ll1l1_opy_)
    def bstack11111llll1_opy_(
        self,
        method_name: str,
        bstack1111l11111_opy_: bstack11111ll11l_opy_,
        bstack111l1111l1_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11lllll1l_opy_ = datetime.now()
            (bstack1111l11111_opy_,) = wrapped.__vars__
            bstack1111l11111_opy_ = (
                bstack1111l11111_opy_
                if bstack1111l11111_opy_ and bstack1111l11111_opy_ != bstack11111ll11l_opy_.NONE
                else self.bstack1111lll111_opy_(method_name, previous_state=bstack1111l11111_opy_, *args, **kwargs)
            )
            if bstack1111l11111_opy_ == bstack11111ll11l_opy_.bstack1111ll1ll1_opy_:
                ctx = bstack1111ll1l11_opy_.create_context(self.bstack1111l111l1_opy_(target))
                if not self.bstack1111l1l111_opy_() or ctx.id not in bstack11111lll11_opy_.bstack111l11111l_opy_:
                    bstack11111lll11_opy_.bstack111l11111l_opy_[ctx.id] = bstack1111lll11l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1111l11111_opy_
                    )
                self.logger.debug(bstack11_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤ࿖") + str(bstack11111lll11_opy_.bstack111l11111l_opy_.keys()) + bstack11_opy_ (u"ࠤࠥ࿗"))
            else:
                self.logger.debug(bstack11_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤ࡮ࡴࡶࡰ࡭ࡨࡨ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧ࿘") + str(bstack11111lll11_opy_.bstack111l11111l_opy_.keys()) + bstack11_opy_ (u"ࠦࠧ࿙"))
            instance = bstack11111lll11_opy_.bstack11111ll1ll_opy_(self.bstack1111l111l1_opy_(target))
            if bstack1111l11111_opy_ == bstack11111ll11l_opy_.NONE or not instance:
                ctx = bstack1111ll1l11_opy_.create_context(self.bstack1111l111l1_opy_(target))
                self.logger.warning(bstack11_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡵ࡯ࡶࡵࡥࡨࡱࡥࡥ࠼ࠣࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤ࿚") + str(bstack11111lll11_opy_.bstack111l11111l_opy_.keys()) + bstack11_opy_ (u"ࠨࠢ࿛"))
                return bstack111l1111l1_opy_(target, *args, **kwargs)
            bstack1111ll11ll_opy_ = self.bstack1111l1ll1l_opy_(
                target,
                (instance, method_name),
                (bstack1111l11111_opy_, bstack11111l1lll_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1111lll1l1_opy_(bstack1111l11111_opy_):
                self.logger.debug(bstack11_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠡࡵࡷࡥࡹ࡫࠭ࡵࡴࡤࡲࡸ࡯ࡴࡪࡱࡱ࠾ࠥࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡲࡵࡩࡻ࡯࡯ࡶࡵࡢࡷࡹࡧࡴࡦࡿࠣࡁࡃࠦࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡶࡸࡦࡺࡥࡾࠢࠫࡿࡹࡿࡰࡦࠪࡷࡥࡷ࡭ࡥࡵࠫࢀ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࢀࡧࡲࡨࡵࢀ࠭ࠥࡡࠢ࿜") + str(instance.ref()) + bstack11_opy_ (u"ࠣ࡟ࠥ࿝"))
            result = (
                bstack1111ll11ll_opy_(target, bstack111l1111l1_opy_, *args, **kwargs)
                if callable(bstack1111ll11ll_opy_)
                else bstack111l1111l1_opy_(target, *args, **kwargs)
            )
            bstack1111llll11_opy_ = self.bstack1111l1ll1l_opy_(
                target,
                (instance, method_name),
                (bstack1111l11111_opy_, bstack11111l1lll_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1111l1ll11_opy_(instance, method_name, datetime.now() - bstack11lllll1l_opy_, *args, **kwargs)
            return bstack1111llll11_opy_ if bstack1111llll11_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1111l11111_opy_,)
        return wrapped
    @staticmethod
    def bstack11111ll1ll_opy_(target: object, strict=True):
        ctx = bstack1111ll1l11_opy_.create_context(target)
        instance = bstack11111lll11_opy_.bstack111l11111l_opy_.get(ctx.id, None)
        if instance and instance.bstack111l111l1l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11111ll111_opy_(
        ctx: bstack1111l1lll1_opy_, state: bstack11111ll11l_opy_, reverse=True
    ) -> List[bstack1111lll11l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack11111lll11_opy_.bstack111l11111l_opy_.values(),
            ),
            key=lambda t: t.bstack1111l1111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111l11lll_opy_(instance: bstack1111lll11l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111lll1l_opy_(instance: bstack1111lll11l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111lll1l1_opy_(instance: bstack1111lll11l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack11111lll11_opy_.logger.debug(bstack11_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡰ࡫ࡹ࠾ࡽ࡮ࡩࡾࢃࠠࡷࡣ࡯ࡹࡪࡃࠢ࿞") + str(value) + bstack11_opy_ (u"ࠥࠦ࿟"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack11111lll11_opy_.bstack11111ll1ll_opy_(target, strict)
        return bstack11111lll11_opy_.bstack11111lll1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack11111lll11_opy_.bstack11111ll1ll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1111l1l111_opy_(self):
        return self.framework_name == bstack11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ࿠")
    def bstack1111l111l1_opy_(self, target):
        return target if not self.bstack1111l1l111_opy_() else self.bstack1111ll111l_opy_()
    @staticmethod
    def bstack1111ll111l_opy_():
        return str(os.getpid()) + str(threading.get_ident())