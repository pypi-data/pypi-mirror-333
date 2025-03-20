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
from uuid import uuid4
from bstack_utils.helper import bstack1lllll11ll_opy_, bstack11llll111ll_opy_
from bstack_utils.bstack1ll11ll11l_opy_ import bstack11l111ll11l_opy_
class bstack11l111l11l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111llll11ll_opy_=None, bstack111lllll1ll_opy_=True, bstack1l11ll11111_opy_=None, bstack11llll111_opy_=None, result=None, duration=None, bstack111ll111ll_opy_=None, meta={}):
        self.bstack111ll111ll_opy_ = bstack111ll111ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111lllll1ll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111llll11ll_opy_ = bstack111llll11ll_opy_
        self.bstack1l11ll11111_opy_ = bstack1l11ll11111_opy_
        self.bstack11llll111_opy_ = bstack11llll111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll11lll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1l1l111_opy_(self, meta):
        self.meta = meta
    def bstack11l1l11ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack111llll1111_opy_(self):
        bstack111llll1lll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ᱿"): bstack111llll1lll_opy_,
            bstack11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᲀ"): bstack111llll1lll_opy_,
            bstack11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᲁ"): bstack111llll1lll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧᲂ") + key)
            setattr(self, key, val)
    def bstack111llll1l11_opy_(self):
        return {
            bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᲃ"): self.name,
            bstack11_opy_ (u"࠭ࡢࡰࡦࡼࠫᲄ"): {
                bstack11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᲅ"): bstack11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᲆ"),
                bstack11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᲇ"): self.code
            },
            bstack11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᲈ"): self.scope,
            bstack11_opy_ (u"ࠫࡹࡧࡧࡴࠩᲉ"): self.tags,
            bstack11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᲊ"): self.framework,
            bstack11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᲋"): self.started_at
        }
    def bstack111lllll1l1_opy_(self):
        return {
         bstack11_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ᲌"): self.meta
        }
    def bstack111llll1l1l_opy_(self):
        return {
            bstack11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ᲍"): {
                bstack11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭᲎"): self.bstack111llll11ll_opy_
            }
        }
    def bstack111lllllll1_opy_(self, bstack111llllllll_opy_, details):
        step = next(filter(lambda st: st[bstack11_opy_ (u"ࠪ࡭ࡩ࠭᲏")] == bstack111llllllll_opy_, self.meta[bstack11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᲐ")]), None)
        step.update(details)
    def bstack1lllll11l_opy_(self, bstack111llllllll_opy_):
        step = next(filter(lambda st: st[bstack11_opy_ (u"ࠬ࡯ࡤࠨᲑ")] == bstack111llllllll_opy_, self.meta[bstack11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᲒ")]), None)
        step.update({
            bstack11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᲓ"): bstack1lllll11ll_opy_()
        })
    def bstack11l11ll111_opy_(self, bstack111llllllll_opy_, result, duration=None):
        bstack1l11ll11111_opy_ = bstack1lllll11ll_opy_()
        if bstack111llllllll_opy_ is not None and self.meta.get(bstack11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᲔ")):
            step = next(filter(lambda st: st[bstack11_opy_ (u"ࠩ࡬ࡨࠬᲕ")] == bstack111llllllll_opy_, self.meta[bstack11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᲖ")]), None)
            step.update({
                bstack11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᲗ"): bstack1l11ll11111_opy_,
                bstack11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᲘ"): duration if duration else bstack11llll111ll_opy_(step[bstack11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᲙ")], bstack1l11ll11111_opy_),
                bstack11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᲚ"): result.result,
                bstack11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᲛ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111llllll11_opy_):
        if self.meta.get(bstack11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᲜ")):
            self.meta[bstack11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᲝ")].append(bstack111llllll11_opy_)
        else:
            self.meta[bstack11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᲞ")] = [ bstack111llllll11_opy_ ]
    def bstack11l1111111l_opy_(self):
        return {
            bstack11_opy_ (u"ࠬࡻࡵࡪࡦࠪᲟ"): self.bstack111ll11lll_opy_(),
            **self.bstack111llll1l11_opy_(),
            **self.bstack111llll1111_opy_(),
            **self.bstack111lllll1l1_opy_()
        }
    def bstack111llll111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᲠ"): self.bstack1l11ll11111_opy_,
            bstack11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᲡ"): self.duration,
            bstack11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᲢ"): self.result.result
        }
        if data[bstack11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᲣ")] == bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᲤ"):
            data[bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᲥ")] = self.result.bstack111l11ll1l_opy_()
            data[bstack11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭Ღ")] = [{bstack11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᲧ"): self.result.bstack11lllllll11_opy_()}]
        return data
    def bstack111lllll111_opy_(self):
        return {
            bstack11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᲨ"): self.bstack111ll11lll_opy_(),
            **self.bstack111llll1l11_opy_(),
            **self.bstack111llll1111_opy_(),
            **self.bstack111llll111l_opy_(),
            **self.bstack111lllll1l1_opy_()
        }
    def bstack111ll1l1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᲩ") in event:
            return self.bstack11l1111111l_opy_()
        elif bstack11_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᲪ") in event:
            return self.bstack111lllll111_opy_()
    def bstack111llll11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11ll11111_opy_ = time if time else bstack1lllll11ll_opy_()
        self.duration = duration if duration else bstack11llll111ll_opy_(self.started_at, self.bstack1l11ll11111_opy_)
        if result:
            self.result = result
class bstack11l11lll11_opy_(bstack11l111l11l_opy_):
    def __init__(self, hooks=[], bstack11l1l11111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
        super().__init__(*args, **kwargs, bstack11llll111_opy_=bstack11_opy_ (u"ࠪࡸࡪࡹࡴࠨᲫ"))
    @classmethod
    def bstack111llll1ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11_opy_ (u"ࠫ࡮ࡪࠧᲬ"): id(step),
                bstack11_opy_ (u"ࠬࡺࡥࡹࡶࠪᲭ"): step.name,
                bstack11_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᲮ"): step.keyword,
            })
        return bstack11l11lll11_opy_(
            **kwargs,
            meta={
                bstack11_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᲯ"): {
                    bstack11_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ჰ"): feature.name,
                    bstack11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᲱ"): feature.filename,
                    bstack11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᲲ"): feature.description
                },
                bstack11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭Ჳ"): {
                    bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᲴ"): scenario.name
                },
                bstack11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᲵ"): steps,
                bstack11_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᲶ"): bstack11l111ll11l_opy_(test)
            }
        )
    def bstack111llllll1l_opy_(self):
        return {
            bstack11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᲷ"): self.hooks
        }
    def bstack111lllll11l_opy_(self):
        if self.bstack11l1l11111_opy_:
            return {
                bstack11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᲸ"): self.bstack11l1l11111_opy_
            }
        return {}
    def bstack111lllll111_opy_(self):
        return {
            **super().bstack111lllll111_opy_(),
            **self.bstack111llllll1l_opy_()
        }
    def bstack11l1111111l_opy_(self):
        return {
            **super().bstack11l1111111l_opy_(),
            **self.bstack111lllll11l_opy_()
        }
    def bstack111llll11l_opy_(self):
        return bstack11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᲹ")
class bstack11l1l1l1l1_opy_(bstack11l111l11l_opy_):
    def __init__(self, hook_type, *args,bstack11l1l11111_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack111llll11l1_opy_ = None
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
        super().__init__(*args, **kwargs, bstack11llll111_opy_=bstack11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᲺ"))
    def bstack111ll1lll1_opy_(self):
        return self.hook_type
    def bstack11l11111111_opy_(self):
        return {
            bstack11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᲻"): self.hook_type
        }
    def bstack111lllll111_opy_(self):
        return {
            **super().bstack111lllll111_opy_(),
            **self.bstack11l11111111_opy_()
        }
    def bstack11l1111111l_opy_(self):
        return {
            **super().bstack11l1111111l_opy_(),
            bstack11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ᲼"): self.bstack111llll11l1_opy_,
            **self.bstack11l11111111_opy_()
        }
    def bstack111llll11l_opy_(self):
        return bstack11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᲽ")
    def bstack11l11ll11l_opy_(self, bstack111llll11l1_opy_):
        self.bstack111llll11l1_opy_ = bstack111llll11l1_opy_