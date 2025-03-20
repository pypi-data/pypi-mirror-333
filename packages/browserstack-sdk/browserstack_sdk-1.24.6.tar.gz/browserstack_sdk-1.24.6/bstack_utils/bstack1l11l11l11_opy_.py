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
import json
class bstack1l111ll11ll_opy_(object):
  bstack11llllll1l_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠪࢂࠬᔻ")), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᔼ"))
  bstack1l111ll1ll1_opy_ = os.path.join(bstack11llllll1l_opy_, bstack11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬᔽ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1lll1l111l_opy_ = None
  bstack1l1l11l1l1_opy_ = None
  bstack1l111llll11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨᔾ")):
      cls.instance = super(bstack1l111ll11ll_opy_, cls).__new__(cls)
      cls.instance.bstack1l111ll1l11_opy_()
    return cls.instance
  def bstack1l111ll1l11_opy_(self):
    try:
      with open(self.bstack1l111ll1ll1_opy_, bstack11_opy_ (u"ࠧࡳࠩᔿ")) as bstack11lll1ll11_opy_:
        bstack1l111ll1l1l_opy_ = bstack11lll1ll11_opy_.read()
        data = json.loads(bstack1l111ll1l1l_opy_)
        if bstack11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᕀ") in data:
          self.bstack1l111lll11l_opy_(data[bstack11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᕁ")])
        if bstack11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᕂ") in data:
          self.bstack1l111lll1l1_opy_(data[bstack11_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᕃ")])
    except:
      pass
  def bstack1l111lll1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11_opy_ (u"ࠬࡹࡣࡢࡰࠪᕄ")]
      self.bstack1lll1l111l_opy_ = scripts[bstack11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᕅ")]
      self.bstack1l1l11l1l1_opy_ = scripts[bstack11_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᕆ")]
      self.bstack1l111llll11_opy_ = scripts[bstack11_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᕇ")]
  def bstack1l111lll11l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack1l111ll1ll1_opy_, bstack11_opy_ (u"ࠩࡺࠫᕈ")) as file:
        json.dump({
          bstack11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᕉ"): self.commands_to_wrap,
          bstack11_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᕊ"): {
            bstack11_opy_ (u"ࠧࡹࡣࡢࡰࠥᕋ"): self.perform_scan,
            bstack11_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᕌ"): self.bstack1lll1l111l_opy_,
            bstack11_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᕍ"): self.bstack1l1l11l1l1_opy_,
            bstack11_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᕎ"): self.bstack1l111llll11_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll11111l1_opy_(self, bstack1ll1l1lllll_opy_):
    try:
      return any(command.get(bstack11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᕏ")) == bstack1ll1l1lllll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l11l11l11_opy_ = bstack1l111ll11ll_opy_()