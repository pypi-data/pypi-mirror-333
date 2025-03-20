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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1111llll1l_opy_ import (
    bstack11111lll11_opy_,
    bstack1111lll11l_opy_,
    bstack11111ll11l_opy_,
    bstack11111l1lll_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1l1ll1111_opy_ import bstack11111111l1_opy_
from bstack_utils.constants import EVENTS
class bstack1llll11111l_opy_(bstack11111lll11_opy_):
    bstack1l1l1l1ll11_opy_ = bstack11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᐘ")
    NAME = bstack11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᐙ")
    bstack1l1llll1ll1_opy_ = bstack11_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭ࠤᐚ")
    bstack1l1lll1l1ll_opy_ = bstack11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᐛ")
    bstack1l11l1ll11l_opy_ = bstack11_opy_ (u"ࠥ࡭ࡳࡶࡵࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᐜ")
    bstack1l1llll11ll_opy_ = bstack11_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᐝ")
    bstack1l1l1ll1lll_opy_ = bstack11_opy_ (u"ࠧ࡯ࡳࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡩࡷࡥࠦᐞ")
    bstack1l11l1ll1l1_opy_ = bstack11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᐟ")
    bstack1l11l1l1ll1_opy_ = bstack11_opy_ (u"ࠢࡦࡰࡧࡩࡩࡥࡡࡵࠤᐠ")
    bstack1ll1llll111_opy_ = bstack11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᐡ")
    bstack1l1ll11l111_opy_ = bstack11_opy_ (u"ࠤࡱࡩࡼࡹࡥࡴࡵ࡬ࡳࡳࠨᐢ")
    bstack1l11l1ll1ll_opy_ = bstack11_opy_ (u"ࠥ࡫ࡪࡺࠢᐣ")
    bstack1ll111l111l_opy_ = bstack11_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᐤ")
    bstack1l1l1ll1111_opy_ = bstack11_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣᐥ")
    bstack1l1l1l1l1l1_opy_ = bstack11_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢᐦ")
    bstack1l11l1lll11_opy_ = bstack11_opy_ (u"ࠢࡲࡷ࡬ࡸࠧᐧ")
    bstack1l11l1lll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1ll111lll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lllll11lll_opy_: Any
    bstack1l1l1l1lll1_opy_: Dict
    def __init__(
        self,
        bstack1l1ll111lll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lllll11lll_opy_: Dict[str, Any],
        methods=[bstack11_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᐨ"), bstack11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᐩ"), bstack11_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᐪ"), bstack11_opy_ (u"ࠦࡶࡻࡩࡵࠤᐫ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1ll111lll_opy_ = bstack1l1ll111lll_opy_
        self.platform_index = platform_index
        self.bstack1111l11ll1_opy_(methods)
        self.bstack1lllll11lll_opy_ = bstack1lllll11lll_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1llll11111l_opy_.bstack1l1lll1l1ll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1llll11111l_opy_.bstack1l1llll1ll1_opy_, target, strict)
    @staticmethod
    def bstack1l11l1l1l11_opy_(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1llll11111l_opy_.bstack1l11l1ll11l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111lll11_opy_.get_data(bstack1llll11111l_opy_.bstack1l1llll11ll_opy_, target, strict)
    @staticmethod
    def bstack1ll1ll1l1ll_opy_(instance: bstack1111lll11l_opy_) -> bool:
        return bstack11111lll11_opy_.bstack11111lll1l_opy_(instance, bstack1llll11111l_opy_.bstack1l1l1ll1lll_opy_, False)
    @staticmethod
    def bstack1ll1lllll11_opy_(instance: bstack1111lll11l_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack11111lll1l_opy_(instance, bstack1llll11111l_opy_.bstack1l1llll1ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1llll11l_opy_(instance: bstack1111lll11l_opy_, default_value=None):
        return bstack11111lll11_opy_.bstack11111lll1l_opy_(instance, bstack1llll11111l_opy_.bstack1l1llll11ll_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l1111_opy_(hub_url: str, bstack1l11l1l1lll_opy_=bstack11_opy_ (u"ࠧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤᐬ")):
        try:
            bstack1l11l1ll111_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l11l1ll111_opy_.endswith(bstack1l11l1l1lll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1lll1111lll_opy_(method_name: str):
        return method_name == bstack11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᐭ")
    @staticmethod
    def bstack1lll111ll11_opy_(method_name: str, *args):
        return (
            bstack1llll11111l_opy_.bstack1lll1111lll_opy_(method_name)
            and bstack1llll11111l_opy_.bstack1l1ll11ll1l_opy_(*args) == bstack1llll11111l_opy_.bstack1l1ll11l111_opy_
        )
    @staticmethod
    def bstack1ll1ll111l1_opy_(method_name: str, *args):
        if not bstack1llll11111l_opy_.bstack1lll1111lll_opy_(method_name):
            return False
        if not bstack1llll11111l_opy_.bstack1l1l1ll1111_opy_ in bstack1llll11111l_opy_.bstack1l1ll11ll1l_opy_(*args):
            return False
        bstack1ll1l1ll111_opy_ = bstack1llll11111l_opy_.bstack1ll1l1l1lll_opy_(*args)
        return bstack1ll1l1ll111_opy_ and bstack11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᐮ") in bstack1ll1l1ll111_opy_ and bstack11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᐯ") in bstack1ll1l1ll111_opy_[bstack11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᐰ")]
    @staticmethod
    def bstack1lll111111l_opy_(method_name: str, *args):
        if not bstack1llll11111l_opy_.bstack1lll1111lll_opy_(method_name):
            return False
        if not bstack1llll11111l_opy_.bstack1l1l1ll1111_opy_ in bstack1llll11111l_opy_.bstack1l1ll11ll1l_opy_(*args):
            return False
        bstack1ll1l1ll111_opy_ = bstack1llll11111l_opy_.bstack1ll1l1l1lll_opy_(*args)
        return (
            bstack1ll1l1ll111_opy_
            and bstack11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᐱ") in bstack1ll1l1ll111_opy_
            and bstack11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢᐲ") in bstack1ll1l1ll111_opy_[bstack11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᐳ")]
        )
    @staticmethod
    def bstack1l1ll11ll1l_opy_(*args):
        return str(bstack1llll11111l_opy_.bstack1lll1111l11_opy_(*args)).lower()
    @staticmethod
    def bstack1lll1111l11_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l1l1lll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack111l11ll1_opy_(driver):
        command_executor = getattr(driver, bstack11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᐴ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11_opy_ (u"ࠢࡠࡷࡵࡰࠧᐵ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11_opy_ (u"ࠣࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠤᐶ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡡࡶࡩࡷࡼࡥࡳࡡࡤࡨࡩࡸࠢᐷ"), None)
        return hub_url
    def bstack1l1ll111l11_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᐸ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᐹ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᐺ")):
                setattr(command_executor, bstack11_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᐻ"), hub_url)
                result = True
        if result:
            self.bstack1l1ll111lll_opy_ = hub_url
            bstack1llll11111l_opy_.bstack1111lll1l1_opy_(instance, bstack1llll11111l_opy_.bstack1l1llll1ll1_opy_, hub_url)
            bstack1llll11111l_opy_.bstack1111lll1l1_opy_(
                instance, bstack1llll11111l_opy_.bstack1l1l1ll1lll_opy_, bstack1llll11111l_opy_.bstack1ll1l1l1111_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_]):
        return bstack11_opy_ (u"ࠢ࠻ࠤᐼ").join((bstack11111ll11l_opy_(bstack1111l11l11_opy_[0]).name, bstack11111l1lll_opy_(bstack1111l11l11_opy_[1]).name))
    @staticmethod
    def bstack1ll1llllll1_opy_(bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_], callback: Callable):
        bstack1l1l1l1ll1l_opy_ = bstack1llll11111l_opy_.bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_)
        if not bstack1l1l1l1ll1l_opy_ in bstack1llll11111l_opy_.bstack1l11l1lll1l_opy_:
            bstack1llll11111l_opy_.bstack1l11l1lll1l_opy_[bstack1l1l1l1ll1l_opy_] = []
        bstack1llll11111l_opy_.bstack1l11l1lll1l_opy_[bstack1l1l1l1ll1l_opy_].append(callback)
    def bstack1111l1ll11_opy_(self, instance: bstack1111lll11l_opy_, method_name: str, bstack1111l1l1l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐽ")):
            return
        cmd = args[0] if method_name == bstack11_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᐾ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l11l1l1l1l_opy_ = bstack11_opy_ (u"ࠥ࠾ࠧᐿ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1ll1ll11_opy_(bstack11_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠧᑀ") + bstack1l11l1l1l1l_opy_, bstack1111l1l1l1_opy_)
    def bstack1111l1ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111lll11l_opy_, str],
        bstack1111l11l11_opy_: Tuple[bstack11111ll11l_opy_, bstack11111l1lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1111l11111_opy_, bstack1l1l1l1llll_opy_ = bstack1111l11l11_opy_
        bstack1l1l1l1ll1l_opy_ = bstack1llll11111l_opy_.bstack1l1l1l1l11l_opy_(bstack1111l11l11_opy_)
        self.logger.debug(bstack11_opy_ (u"ࠧࡵ࡮ࡠࡪࡲࡳࡰࡀࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑁ") + str(kwargs) + bstack11_opy_ (u"ࠨࠢᑂ"))
        if bstack1111l11111_opy_ == bstack11111ll11l_opy_.QUIT:
            if bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.PRE:
                bstack1ll1l1llll1_opy_ = bstack11111111l1_opy_.bstack1ll1ll11111_opy_(EVENTS.bstack1ll1lll1l1_opy_.value)
                bstack11111lll11_opy_.bstack1111lll1l1_opy_(instance, EVENTS.bstack1ll1lll1l1_opy_.value, bstack1ll1l1llll1_opy_)
                self.logger.debug(bstack11_opy_ (u"ࠢࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᑃ").format(instance, method_name, bstack1111l11111_opy_, bstack1l1l1l1llll_opy_))
        if bstack1111l11111_opy_ == bstack11111ll11l_opy_.bstack1111ll1ll1_opy_:
            if bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.POST and not bstack1llll11111l_opy_.bstack1l1lll1l1ll_opy_ in instance.data:
                session_id = getattr(target, bstack11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᑄ"), None)
                if session_id:
                    instance.data[bstack1llll11111l_opy_.bstack1l1lll1l1ll_opy_] = session_id
        elif (
            bstack1111l11111_opy_ == bstack11111ll11l_opy_.bstack1111ll1l1l_opy_
            and bstack1llll11111l_opy_.bstack1l1ll11ll1l_opy_(*args) == bstack1llll11111l_opy_.bstack1l1ll11l111_opy_
        ):
            if bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.PRE:
                hub_url = bstack1llll11111l_opy_.bstack111l11ll1_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll11111l_opy_.bstack1l1llll1ll1_opy_: hub_url,
                            bstack1llll11111l_opy_.bstack1l1l1ll1lll_opy_: bstack1llll11111l_opy_.bstack1ll1l1l1111_opy_(hub_url),
                            bstack1llll11111l_opy_.bstack1ll1llll111_opy_: int(
                                os.environ.get(bstack11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤᑅ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll1l1ll111_opy_ = bstack1llll11111l_opy_.bstack1ll1l1l1lll_opy_(*args)
                bstack1l11l1l1l11_opy_ = bstack1ll1l1ll111_opy_.get(bstack11_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᑆ"), None) if bstack1ll1l1ll111_opy_ else None
                if isinstance(bstack1l11l1l1l11_opy_, dict):
                    instance.data[bstack1llll11111l_opy_.bstack1l11l1ll11l_opy_] = copy.deepcopy(bstack1l11l1l1l11_opy_)
                    instance.data[bstack1llll11111l_opy_.bstack1l1llll11ll_opy_] = bstack1l11l1l1l11_opy_
            elif bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᑇ"), dict()).get(bstack11_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣᑈ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll11111l_opy_.bstack1l1lll1l1ll_opy_: framework_session_id,
                                bstack1llll11111l_opy_.bstack1l11l1ll1l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1111l11111_opy_ == bstack11111ll11l_opy_.bstack1111ll1l1l_opy_
            and bstack1llll11111l_opy_.bstack1l1ll11ll1l_opy_(*args) == bstack1llll11111l_opy_.bstack1l11l1lll11_opy_
            and bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.POST
        ):
            instance.data[bstack1llll11111l_opy_.bstack1l11l1l1ll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l1l1l1ll1l_opy_ in bstack1llll11111l_opy_.bstack1l11l1lll1l_opy_:
            bstack1l1l1l1l111_opy_ = None
            for callback in bstack1llll11111l_opy_.bstack1l11l1lll1l_opy_[bstack1l1l1l1ll1l_opy_]:
                try:
                    bstack1l1l1l11lll_opy_ = callback(self, target, exec, bstack1111l11l11_opy_, result, *args, **kwargs)
                    if bstack1l1l1l1l111_opy_ == None:
                        bstack1l1l1l1l111_opy_ = bstack1l1l1l11lll_opy_
                except Exception as e:
                    self.logger.error(bstack11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦᑉ") + str(e) + bstack11_opy_ (u"ࠢࠣᑊ"))
                    traceback.print_exc()
            if bstack1111l11111_opy_ == bstack11111ll11l_opy_.QUIT:
                if bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.POST:
                    bstack1ll1l1llll1_opy_ = bstack11111lll11_opy_.bstack11111lll1l_opy_(instance, EVENTS.bstack1ll1lll1l1_opy_.value)
                    if bstack1ll1l1llll1_opy_!=None:
                        bstack11111111l1_opy_.end(EVENTS.bstack1ll1lll1l1_opy_.value, bstack1ll1l1llll1_opy_+bstack11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᑋ"), bstack1ll1l1llll1_opy_+bstack11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᑌ"), True, None)
            if bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.PRE and callable(bstack1l1l1l1l111_opy_):
                return bstack1l1l1l1l111_opy_
            elif bstack1l1l1l1llll_opy_ == bstack11111l1lll_opy_.POST and bstack1l1l1l1l111_opy_:
                return bstack1l1l1l1l111_opy_
    def bstack1111lll111_opy_(
        self, method_name, previous_state: bstack11111ll11l_opy_, *args, **kwargs
    ) -> bstack11111ll11l_opy_:
        if method_name == bstack11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᑍ") or method_name == bstack11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᑎ"):
            return bstack11111ll11l_opy_.bstack1111ll1ll1_opy_
        if method_name == bstack11_opy_ (u"ࠧࡷࡵࡪࡶࠥᑏ"):
            return bstack11111ll11l_opy_.QUIT
        if method_name == bstack11_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᑐ"):
            if previous_state != bstack11111ll11l_opy_.NONE:
                bstack1ll1l1lllll_opy_ = bstack1llll11111l_opy_.bstack1l1ll11ll1l_opy_(*args)
                if bstack1ll1l1lllll_opy_ == bstack1llll11111l_opy_.bstack1l1ll11l111_opy_:
                    return bstack11111ll11l_opy_.bstack1111ll1ll1_opy_
            return bstack11111ll11l_opy_.bstack1111ll1l1l_opy_
        return bstack11111ll11l_opy_.NONE