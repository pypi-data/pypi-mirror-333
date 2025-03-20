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
import json
class bstack1l111ll1ll1_opy_(object):
  bstack11lll1l1_opy_ = os.path.join(os.path.expanduser(bstack1l11l_opy_ (u"ࠩࢁࠫᔺ")), bstack1l11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᔻ"))
  bstack1l111ll11ll_opy_ = os.path.join(bstack11lll1l1_opy_, bstack1l11l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᔼ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l1l111_opy_ = None
  bstack1llllll111_opy_ = None
  bstack1l111llllll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11l_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᔽ")):
      cls.instance = super(bstack1l111ll1ll1_opy_, cls).__new__(cls)
      cls.instance.bstack1l111ll1l1l_opy_()
    return cls.instance
  def bstack1l111ll1l1l_opy_(self):
    try:
      with open(self.bstack1l111ll11ll_opy_, bstack1l11l_opy_ (u"࠭ࡲࠨᔾ")) as bstack1l11l1111l_opy_:
        bstack1l111ll1l11_opy_ = bstack1l11l1111l_opy_.read()
        data = json.loads(bstack1l111ll1l11_opy_)
        if bstack1l11l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᔿ") in data:
          self.bstack1l11l111111_opy_(data[bstack1l11l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᕀ")])
        if bstack1l11l_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᕁ") in data:
          self.bstack1l11l11111l_opy_(data[bstack1l11l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᕂ")])
    except:
      pass
  def bstack1l11l11111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1l11l_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᕃ")]
      self.bstack11l1l111_opy_ = scripts[bstack1l11l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᕄ")]
      self.bstack1llllll111_opy_ = scripts[bstack1l11l_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᕅ")]
      self.bstack1l111llllll_opy_ = scripts[bstack1l11l_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᕆ")]
  def bstack1l11l111111_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack1l111ll11ll_opy_, bstack1l11l_opy_ (u"ࠨࡹࠪᕇ")) as file:
        json.dump({
          bstack1l11l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦᕈ"): self.commands_to_wrap,
          bstack1l11l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦᕉ"): {
            bstack1l11l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᕊ"): self.perform_scan,
            bstack1l11l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᕋ"): self.bstack11l1l111_opy_,
            bstack1l11l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᕌ"): self.bstack1llllll111_opy_,
            bstack1l11l_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᕍ"): self.bstack1l111llllll_opy_
          }
        }, file)
    except:
      pass
  def bstack1lll1ll11_opy_(self, bstack1ll1llll11l_opy_):
    try:
      return any(command.get(bstack1l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᕎ")) == bstack1ll1llll11l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll111111_opy_ = bstack1l111ll1ll1_opy_()