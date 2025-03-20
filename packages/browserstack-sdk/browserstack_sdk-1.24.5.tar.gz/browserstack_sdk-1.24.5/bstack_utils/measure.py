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
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1lll111ll_opy_ import get_logger
from bstack_utils.bstack1ll1l1lll1_opy_ import bstack1lll1ll1l11_opy_
bstack1ll1l1lll1_opy_ = bstack1lll1ll1l11_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l11l1l1l_opy_: Optional[str] = None):
    bstack1l11l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᬐ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1ll11111_opy_: str = bstack1ll1l1lll1_opy_.bstack1l111lll1l1_opy_(label)
            start_mark: str = label + bstack1l11l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᬑ")
            end_mark: str = label + bstack1l11l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᬒ")
            result = None
            try:
                if stage.value == STAGE.bstack11111ll1_opy_.value:
                    bstack1ll1l1lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1ll1l1lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l11l1l1l_opy_)
                elif stage.value == STAGE.bstack1111111l_opy_.value:
                    start_mark: str = bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᬓ")
                    end_mark: str = bstack1ll1ll11111_opy_ + bstack1l11l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᬔ")
                    bstack1ll1l1lll1_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1ll1l1lll1_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l11l1l1l_opy_)
            except Exception as e:
                bstack1ll1l1lll1_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l11l1l1l_opy_)
            return result
        return wrapper
    return decorator