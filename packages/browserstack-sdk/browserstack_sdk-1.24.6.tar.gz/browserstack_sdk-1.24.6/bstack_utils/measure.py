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
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11l11l1l_opy_ import get_logger
from bstack_utils.bstack1l1ll1111_opy_ import bstack11111111l1_opy_
bstack1l1ll1111_opy_ = bstack11111111l1_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1ll111llll_opy_: Optional[str] = None):
    bstack11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡄࡦࡥࡲࡶࡦࡺ࡯ࡳࠢࡷࡳࠥࡲ࡯ࡨࠢࡷ࡬ࡪࠦࡳࡵࡣࡵࡸࠥࡺࡩ࡮ࡧࠣࡳ࡫ࠦࡡࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࡥࡱࡵ࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᬑ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l1llll1_opy_: str = bstack1l1ll1111_opy_.bstack1l11l111111_opy_(label)
            start_mark: str = label + bstack11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᬒ")
            end_mark: str = label + bstack11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᬓ")
            result = None
            try:
                if stage.value == STAGE.bstack1l11l1lll1_opy_.value:
                    bstack1l1ll1111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1ll1111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1ll111llll_opy_)
                elif stage.value == STAGE.bstack1lll11111l_opy_.value:
                    start_mark: str = bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᬔ")
                    end_mark: str = bstack1ll1l1llll1_opy_ + bstack11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᬕ")
                    bstack1l1ll1111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1ll1111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1ll111llll_opy_)
            except Exception as e:
                bstack1l1ll1111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1ll111llll_opy_)
            return result
        return wrapper
    return decorator