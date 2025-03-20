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
from uuid import uuid4
from bstack_utils.helper import bstack111ll1l1l_opy_, bstack11llll11ll1_opy_
from bstack_utils.bstack1111l1l1l_opy_ import bstack11l111l1l1l_opy_
class bstack111lll111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111llllll11_opy_=None, bstack111llll11l1_opy_=True, bstack1l1l1l11111_opy_=None, bstack11ll111lll_opy_=None, result=None, duration=None, bstack111ll1l111_opy_=None, meta={}):
        self.bstack111ll1l111_opy_ = bstack111ll1l111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111llll11l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111llllll11_opy_ = bstack111llllll11_opy_
        self.bstack1l1l1l11111_opy_ = bstack1l1l1l11111_opy_
        self.bstack11ll111lll_opy_ = bstack11ll111lll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11l11l1111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l11ll1l1_opy_(self, meta):
        self.meta = meta
    def bstack11l11l1l1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack111llll1l11_opy_(self):
        bstack111llll11ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ᱾"): bstack111llll11ll_opy_,
            bstack1l11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ᱿"): bstack111llll11ll_opy_,
            bstack1l11l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᲀ"): bstack111llll11ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l11l_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦᲁ") + key)
            setattr(self, key, val)
    def bstack111lllllll1_opy_(self):
        return {
            bstack1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᲂ"): self.name,
            bstack1l11l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᲃ"): {
                bstack1l11l_opy_ (u"࠭࡬ࡢࡰࡪࠫᲄ"): bstack1l11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᲅ"),
                bstack1l11l_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᲆ"): self.code
            },
            bstack1l11l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᲇ"): self.scope,
            bstack1l11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᲈ"): self.tags,
            bstack1l11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᲉ"): self.framework,
            bstack1l11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᲊ"): self.started_at
        }
    def bstack111llllll1l_opy_(self):
        return {
         bstack1l11l_opy_ (u"࠭࡭ࡦࡶࡤࠫ᲋"): self.meta
        }
    def bstack11l1111111l_opy_(self):
        return {
            bstack1l11l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ᲌"): {
                bstack1l11l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ᲍"): self.bstack111llllll11_opy_
            }
        }
    def bstack111lllll111_opy_(self, bstack111llll1111_opy_, details):
        step = next(filter(lambda st: st[bstack1l11l_opy_ (u"ࠩ࡬ࡨࠬ᲎")] == bstack111llll1111_opy_, self.meta[bstack1l11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᲏")]), None)
        step.update(details)
    def bstack11ll11l1_opy_(self, bstack111llll1111_opy_):
        step = next(filter(lambda st: st[bstack1l11l_opy_ (u"ࠫ࡮ࡪࠧᲐ")] == bstack111llll1111_opy_, self.meta[bstack1l11l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᲑ")]), None)
        step.update({
            bstack1l11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᲒ"): bstack111ll1l1l_opy_()
        })
    def bstack11l11ll1ll_opy_(self, bstack111llll1111_opy_, result, duration=None):
        bstack1l1l1l11111_opy_ = bstack111ll1l1l_opy_()
        if bstack111llll1111_opy_ is not None and self.meta.get(bstack1l11l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Დ")):
            step = next(filter(lambda st: st[bstack1l11l_opy_ (u"ࠨ࡫ࡧࠫᲔ")] == bstack111llll1111_opy_, self.meta[bstack1l11l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᲕ")]), None)
            step.update({
                bstack1l11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᲖ"): bstack1l1l1l11111_opy_,
                bstack1l11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭Თ"): duration if duration else bstack11llll11ll1_opy_(step[bstack1l11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᲘ")], bstack1l1l1l11111_opy_),
                bstack1l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭Კ"): result.result,
                bstack1l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᲚ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111llll1l1l_opy_):
        if self.meta.get(bstack1l11l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᲛ")):
            self.meta[bstack1l11l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᲜ")].append(bstack111llll1l1l_opy_)
        else:
            self.meta[bstack1l11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᲝ")] = [ bstack111llll1l1l_opy_ ]
    def bstack111llll1ll1_opy_(self):
        return {
            bstack1l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᲞ"): self.bstack11l11l1111_opy_(),
            **self.bstack111lllllll1_opy_(),
            **self.bstack111llll1l11_opy_(),
            **self.bstack111llllll1l_opy_()
        }
    def bstack111llll111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᲟ"): self.bstack1l1l1l11111_opy_,
            bstack1l11l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᲠ"): self.duration,
            bstack1l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᲡ"): self.result.result
        }
        if data[bstack1l11l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᲢ")] == bstack1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᲣ"):
            data[bstack1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᲤ")] = self.result.bstack111l11ll11_opy_()
            data[bstack1l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᲥ")] = [{bstack1l11l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᲦ"): self.result.bstack11ll1lllll1_opy_()}]
        return data
    def bstack111llllllll_opy_(self):
        return {
            bstack1l11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᲧ"): self.bstack11l11l1111_opy_(),
            **self.bstack111lllllll1_opy_(),
            **self.bstack111llll1l11_opy_(),
            **self.bstack111llll111l_opy_(),
            **self.bstack111llllll1l_opy_()
        }
    def bstack111ll11lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l11l_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨᲨ") in event:
            return self.bstack111llll1ll1_opy_()
        elif bstack1l11l_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᲩ") in event:
            return self.bstack111llllllll_opy_()
    def bstack111ll1ll1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1l1l11111_opy_ = time if time else bstack111ll1l1l_opy_()
        self.duration = duration if duration else bstack11llll11ll1_opy_(self.started_at, self.bstack1l1l1l11111_opy_)
        if result:
            self.result = result
class bstack11l11lll11_opy_(bstack111lll111l_opy_):
    def __init__(self, hooks=[], bstack11l1l11111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
        super().__init__(*args, **kwargs, bstack11ll111lll_opy_=bstack1l11l_opy_ (u"ࠩࡷࡩࡸࡺࠧᲪ"))
    @classmethod
    def bstack111lllll1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11l_opy_ (u"ࠪ࡭ࡩ࠭Ძ"): id(step),
                bstack1l11l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᲬ"): step.name,
                bstack1l11l_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭Ჭ"): step.keyword,
            })
        return bstack11l11lll11_opy_(
            **kwargs,
            meta={
                bstack1l11l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᲮ"): {
                    bstack1l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᲯ"): feature.name,
                    bstack1l11l_opy_ (u"ࠨࡲࡤࡸ࡭࠭Ჰ"): feature.filename,
                    bstack1l11l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᲱ"): feature.description
                },
                bstack1l11l_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᲲ"): {
                    bstack1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᲳ"): scenario.name
                },
                bstack1l11l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᲴ"): steps,
                bstack1l11l_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᲵ"): bstack11l111l1l1l_opy_(test)
            }
        )
    def bstack111lllll1l1_opy_(self):
        return {
            bstack1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭Ჶ"): self.hooks
        }
    def bstack111llll1lll_opy_(self):
        if self.bstack11l1l11111_opy_:
            return {
                bstack1l11l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᲷ"): self.bstack11l1l11111_opy_
            }
        return {}
    def bstack111llllllll_opy_(self):
        return {
            **super().bstack111llllllll_opy_(),
            **self.bstack111lllll1l1_opy_()
        }
    def bstack111llll1ll1_opy_(self):
        return {
            **super().bstack111llll1ll1_opy_(),
            **self.bstack111llll1lll_opy_()
        }
    def bstack111ll1ll1l_opy_(self):
        return bstack1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᲸ")
class bstack11l1l11lll_opy_(bstack111lll111l_opy_):
    def __init__(self, hook_type, *args,bstack11l1l11111_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack111lllll11l_opy_ = None
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
        super().__init__(*args, **kwargs, bstack11ll111lll_opy_=bstack1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᲹ"))
    def bstack111ll111ll_opy_(self):
        return self.hook_type
    def bstack11l11111111_opy_(self):
        return {
            bstack1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᲺ"): self.hook_type
        }
    def bstack111llllllll_opy_(self):
        return {
            **super().bstack111llllllll_opy_(),
            **self.bstack11l11111111_opy_()
        }
    def bstack111llll1ll1_opy_(self):
        return {
            **super().bstack111llll1ll1_opy_(),
            bstack1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ᲻"): self.bstack111lllll11l_opy_,
            **self.bstack11l11111111_opy_()
        }
    def bstack111ll1ll1l_opy_(self):
        return bstack1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ᲼")
    def bstack11l1l11l1l_opy_(self, bstack111lllll11l_opy_):
        self.bstack111lllll11l_opy_ = bstack111lllll11l_opy_