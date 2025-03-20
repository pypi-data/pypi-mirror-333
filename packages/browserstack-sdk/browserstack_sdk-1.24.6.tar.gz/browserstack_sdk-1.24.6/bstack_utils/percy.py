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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11l1l1ll1l_opy_, bstack111111ll_opy_
from bstack_utils.measure import measure
class bstack111ll1l1l_opy_:
  working_dir = os.getcwd()
  bstack1llllll1l_opy_ = False
  config = {}
  binary_path = bstack11_opy_ (u"࠭ࠧ᭞")
  bstack11l1ll11l1l_opy_ = bstack11_opy_ (u"ࠧࠨ᭟")
  bstack1111111ll_opy_ = False
  bstack11l1l1l1lll_opy_ = None
  bstack11l1l11ll1l_opy_ = {}
  bstack11l1l1l11l1_opy_ = 300
  bstack11l1lll11l1_opy_ = False
  logger = None
  bstack11l1ll1l1l1_opy_ = False
  bstack1ll11lll11_opy_ = False
  percy_build_id = None
  bstack11l1l1lll11_opy_ = bstack11_opy_ (u"ࠨࠩ᭠")
  bstack11l1lll1l11_opy_ = {
    bstack11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᭡") : 1,
    bstack11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ᭢") : 2,
    bstack11_opy_ (u"ࠫࡪࡪࡧࡦࠩ᭣") : 3,
    bstack11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ᭤") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l1l11lll1_opy_(self):
    bstack11l1l1l1111_opy_ = bstack11_opy_ (u"࠭ࠧ᭥")
    bstack11l1l1111l1_opy_ = sys.platform
    bstack11l1ll11ll1_opy_ = bstack11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭᭦")
    if re.match(bstack11_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣ᭧"), bstack11l1l1111l1_opy_) != None:
      bstack11l1l1l1111_opy_ = bstack1l11111ll1l_opy_ + bstack11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥ᭨")
      self.bstack11l1l1lll11_opy_ = bstack11_opy_ (u"ࠪࡱࡦࡩࠧ᭩")
    elif re.match(bstack11_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤ᭪"), bstack11l1l1111l1_opy_) != None:
      bstack11l1l1l1111_opy_ = bstack1l11111ll1l_opy_ + bstack11_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨ᭫")
      bstack11l1ll11ll1_opy_ = bstack11_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤ᭬")
      self.bstack11l1l1lll11_opy_ = bstack11_opy_ (u"ࠧࡸ࡫ࡱࠫ᭭")
    else:
      bstack11l1l1l1111_opy_ = bstack1l11111ll1l_opy_ + bstack11_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦ᭮")
      self.bstack11l1l1lll11_opy_ = bstack11_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨ᭯")
    return bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_
  def bstack11l1ll111ll_opy_(self):
    try:
      bstack11l1ll1ll11_opy_ = [os.path.join(expanduser(bstack11_opy_ (u"ࠥࢂࠧ᭰")), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᭱")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l1ll1ll11_opy_:
        if(self.bstack11l1ll1llll_opy_(path)):
          return path
      raise bstack11_opy_ (u"࡛ࠧ࡮ࡢ࡮ࡥࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤ᭲")
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣ᭳").format(e))
  def bstack11l1ll1llll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  @measure(event_name=EVENTS.bstack1l111l1l111_opy_, stage=STAGE.bstack1lll11111l_opy_)
  def bstack11l1ll1l11l_opy_(self, bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_):
    try:
      bstack11l1l111ll1_opy_ = self.bstack11l1ll111ll_opy_()
      bstack11l1ll11l11_opy_ = os.path.join(bstack11l1l111ll1_opy_, bstack11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪ᭴"))
      bstack11l1l11l111_opy_ = os.path.join(bstack11l1l111ll1_opy_, bstack11l1ll11ll1_opy_)
      if os.path.exists(bstack11l1l11l111_opy_):
        self.logger.info(bstack11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ᭵").format(bstack11l1l11l111_opy_))
        return bstack11l1l11l111_opy_
      if os.path.exists(bstack11l1ll11l11_opy_):
        self.logger.info(bstack11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢ᭶").format(bstack11l1ll11l11_opy_))
        return self.bstack11l1l1lll1l_opy_(bstack11l1ll11l11_opy_, bstack11l1ll11ll1_opy_)
      self.logger.info(bstack11_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣ᭷").format(bstack11l1l1l1111_opy_))
      response = bstack111111ll_opy_(bstack11_opy_ (u"ࠫࡌࡋࡔࠨ᭸"), bstack11l1l1l1111_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11l1ll11l11_opy_, bstack11_opy_ (u"ࠬࡽࡢࠨ᭹")) as file:
          file.write(response.content)
        self.logger.info(bstack11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦ᭺").format(bstack11l1ll11l11_opy_))
        return self.bstack11l1l1lll1l_opy_(bstack11l1ll11l11_opy_, bstack11l1ll11ll1_opy_)
      else:
        raise(bstack11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥ᭻").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ᭼").format(e))
  def bstack11l1ll1lll1_opy_(self, bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_):
    try:
      retry = 2
      bstack11l1l11l111_opy_ = None
      bstack11l1lll1111_opy_ = False
      while retry > 0:
        bstack11l1l11l111_opy_ = self.bstack11l1ll1l11l_opy_(bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_)
        bstack11l1lll1111_opy_ = self.bstack11l1l1lllll_opy_(bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_, bstack11l1l11l111_opy_)
        if bstack11l1lll1111_opy_:
          break
        retry -= 1
      return bstack11l1l11l111_opy_, bstack11l1lll1111_opy_
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨ᭽").format(e))
    return bstack11l1l11l111_opy_, False
  def bstack11l1l1lllll_opy_(self, bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_, bstack11l1l11l111_opy_, bstack11l1l1ll1ll_opy_ = 0):
    if bstack11l1l1ll1ll_opy_ > 1:
      return False
    if bstack11l1l11l111_opy_ == None or os.path.exists(bstack11l1l11l111_opy_) == False:
      self.logger.warn(bstack11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣ᭾"))
      return False
    bstack11l1l11llll_opy_ = bstack11_opy_ (u"ࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࡜࠰ࡥ࡯࡭ࠥࡢࡤ࠯࡞ࡧ࠯࠳ࡢࡤࠬࠤ᭿")
    command = bstack11_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫᮀ").format(bstack11l1l11l111_opy_)
    bstack11l1l11l1l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l1l11llll_opy_, bstack11l1l11l1l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧᮁ"))
      return False
  def bstack11l1l1lll1l_opy_(self, bstack11l1ll11l11_opy_, bstack11l1ll11ll1_opy_):
    try:
      working_dir = os.path.dirname(bstack11l1ll11l11_opy_)
      shutil.unpack_archive(bstack11l1ll11l11_opy_, working_dir)
      bstack11l1l11l111_opy_ = os.path.join(working_dir, bstack11l1ll11ll1_opy_)
      os.chmod(bstack11l1l11l111_opy_, 0o755)
      return bstack11l1l11l111_opy_
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᮂ"))
  def bstack11l1ll1l111_opy_(self):
    try:
      bstack11l1ll1ll1l_opy_ = self.config.get(bstack11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᮃ"))
      bstack11l1ll1l111_opy_ = bstack11l1ll1ll1l_opy_ or (bstack11l1ll1ll1l_opy_ is None and self.bstack1llllll1l_opy_)
      if not bstack11l1ll1l111_opy_ or self.config.get(bstack11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᮄ"), None) not in bstack1l111l11l11_opy_:
        return False
      self.bstack1111111ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᮅ").format(e))
  def bstack11l1lll1l1l_opy_(self):
    try:
      bstack11l1lll1l1l_opy_ = self.percy_capture_mode
      return bstack11l1lll1l1l_opy_
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᮆ").format(e))
  def init(self, bstack1llllll1l_opy_, config, logger):
    self.bstack1llllll1l_opy_ = bstack1llllll1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1ll1l111_opy_():
      return
    self.bstack11l1l11ll1l_opy_ = config.get(bstack11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᮇ"), {})
    self.percy_capture_mode = config.get(bstack11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᮈ"))
    try:
      bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_ = self.bstack11l1l11lll1_opy_()
      bstack11l1l11l111_opy_, bstack11l1lll1111_opy_ = self.bstack11l1ll1lll1_opy_(bstack11l1l1l1111_opy_, bstack11l1ll11ll1_opy_)
      if bstack11l1lll1111_opy_:
        self.binary_path = bstack11l1l11l111_opy_
        thread = Thread(target=self.bstack11l1ll1l1ll_opy_)
        thread.start()
      else:
        self.bstack11l1ll1l1l1_opy_ = True
        self.logger.error(bstack11_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᮉ").format(bstack11l1l11l111_opy_))
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᮊ").format(e))
  def bstack11l1l11ll11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11_opy_ (u"ࠩ࡯ࡳ࡬࠭ᮋ"), bstack11_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭ᮌ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣᮍ").format(logfile))
      self.bstack11l1ll11l1l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᮎ").format(e))
  @measure(event_name=EVENTS.bstack1l11111l111_opy_, stage=STAGE.bstack1lll11111l_opy_)
  def bstack11l1ll1l1ll_opy_(self):
    bstack11l1ll11111_opy_ = self.bstack11l1lll11ll_opy_()
    if bstack11l1ll11111_opy_ == None:
      self.bstack11l1ll1l1l1_opy_ = True
      self.logger.error(bstack11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤᮏ"))
      return False
    command_args = [bstack11_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣᮐ") if self.bstack1llllll1l_opy_ else bstack11_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬᮑ")]
    bstack11ll111llll_opy_ = self.bstack11l1l1111ll_opy_()
    if bstack11ll111llll_opy_ != None:
      command_args.append(bstack11_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣᮒ").format(bstack11ll111llll_opy_))
    env = os.environ.copy()
    env[bstack11_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣᮓ")] = bstack11l1ll11111_opy_
    env[bstack11_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦᮔ")] = os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᮕ"), bstack11_opy_ (u"࠭ࠧᮖ"))
    bstack11l1l11l1ll_opy_ = [self.binary_path]
    self.bstack11l1l11ll11_opy_()
    self.bstack11l1l1l1lll_opy_ = self.bstack11l1l1l1ll1_opy_(bstack11l1l11l1ll_opy_ + command_args, env)
    self.logger.debug(bstack11_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣᮗ"))
    bstack11l1l1ll1ll_opy_ = 0
    while self.bstack11l1l1l1lll_opy_.poll() == None:
      bstack11l1l111l1l_opy_ = self.bstack11l1l11111l_opy_()
      if bstack11l1l111l1l_opy_:
        self.logger.debug(bstack11_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦᮘ"))
        self.bstack11l1lll11l1_opy_ = True
        return True
      bstack11l1l1ll1ll_opy_ += 1
      self.logger.debug(bstack11_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧᮙ").format(bstack11l1l1ll1ll_opy_))
      time.sleep(2)
    self.logger.error(bstack11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣᮚ").format(bstack11l1l1ll1ll_opy_))
    self.bstack11l1ll1l1l1_opy_ = True
    return False
  def bstack11l1l11111l_opy_(self, bstack11l1l1ll1ll_opy_ = 0):
    if bstack11l1l1ll1ll_opy_ > 10:
      return False
    try:
      bstack11l1ll11lll_opy_ = os.environ.get(bstack11_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫᮛ"), bstack11_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭ᮜ"))
      bstack11l1l1ll11l_opy_ = bstack11l1ll11lll_opy_ + bstack1l1111l1l1l_opy_
      response = requests.get(bstack11l1l1ll11l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬᮝ"), {}).get(bstack11_opy_ (u"ࠧࡪࡦࠪᮞ"), None)
      return True
    except:
      self.logger.debug(bstack11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᮟ"))
      return False
  def bstack11l1lll11ll_opy_(self):
    bstack11l1l1llll1_opy_ = bstack11_opy_ (u"ࠩࡤࡴࡵ࠭ᮠ") if self.bstack1llllll1l_opy_ else bstack11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᮡ")
    bstack11l1l1l1l1l_opy_ = bstack11_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢᮢ") if self.config.get(bstack11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᮣ")) is None else True
    bstack1l1111111ll_opy_ = bstack11_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢᮤ").format(self.config[bstack11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᮥ")], bstack11l1l1llll1_opy_, bstack11l1l1l1l1l_opy_)
    if self.percy_capture_mode:
      bstack1l1111111ll_opy_ += bstack11_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥᮦ").format(self.percy_capture_mode)
    uri = bstack11l1l1ll1l_opy_(bstack1l1111111ll_opy_)
    try:
      response = bstack111111ll_opy_(bstack11_opy_ (u"ࠩࡊࡉ࡙࠭ᮧ"), uri, {}, {bstack11_opy_ (u"ࠪࡥࡺࡺࡨࠨᮨ"): (self.config[bstack11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᮩ")], self.config[bstack11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᮪")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1111111ll_opy_ = data.get(bstack11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹ᮫ࠧ"))
        self.percy_capture_mode = data.get(bstack11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬᮬ"))
        os.environ[bstack11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ᮭ")] = str(self.bstack1111111ll_opy_)
        os.environ[bstack11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᮮ")] = str(self.percy_capture_mode)
        if bstack11l1l1l1l1l_opy_ == bstack11_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᮯ") and str(self.bstack1111111ll_opy_).lower() == bstack11_opy_ (u"ࠦࡹࡸࡵࡦࠤ᮰"):
          self.bstack1ll11lll11_opy_ = True
        if bstack11_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ᮱") in data:
          return data[bstack11_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧ᮲")]
        else:
          raise bstack11_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧ᮳").format(data)
      else:
        raise bstack11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣ᮴").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥ᮵").format(e))
  def bstack11l1l1111ll_opy_(self):
    bstack11l1l111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨ᮶"))
    try:
      if bstack11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᮷") not in self.bstack11l1l11ll1l_opy_:
        self.bstack11l1l11ll1l_opy_[bstack11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᮸")] = 2
      with open(bstack11l1l111l11_opy_, bstack11_opy_ (u"࠭ࡷࠨ᮹")) as fp:
        json.dump(self.bstack11l1l11ll1l_opy_, fp)
      return bstack11l1l111l11_opy_
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᮺ").format(e))
  def bstack11l1l1l1ll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11l1l1lll11_opy_ == bstack11_opy_ (u"ࠨࡹ࡬ࡲࠬᮻ"):
        bstack11l1l1l111l_opy_ = [bstack11_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪᮼ"), bstack11_opy_ (u"ࠪ࠳ࡨ࠭ᮽ")]
        cmd = bstack11l1l1l111l_opy_ + cmd
      cmd = bstack11_opy_ (u"ࠫࠥ࠭ᮾ").join(cmd)
      self.logger.debug(bstack11_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤᮿ").format(cmd))
      with open(self.bstack11l1ll11l1l_opy_, bstack11_opy_ (u"ࠨࡡࠣᯀ")) as bstack11l1l1l1l11_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l1l1l1l11_opy_, text=True, stderr=bstack11l1l1l1l11_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l1ll1l1l1_opy_ = True
      self.logger.error(bstack11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᯁ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l1lll11l1_opy_:
        self.logger.info(bstack11_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤᯂ"))
        cmd = [self.binary_path, bstack11_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧᯃ")]
        self.bstack11l1l1l1ll1_opy_(cmd)
        self.bstack11l1lll11l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᯄ").format(cmd, e))
  def bstack1111ll11_opy_(self):
    if not self.bstack1111111ll_opy_:
      return
    try:
      bstack11l1l111lll_opy_ = 0
      while not self.bstack11l1lll11l1_opy_ and bstack11l1l111lll_opy_ < self.bstack11l1l1l11l1_opy_:
        if self.bstack11l1ll1l1l1_opy_:
          self.logger.info(bstack11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤᯅ"))
          return
        time.sleep(1)
        bstack11l1l111lll_opy_ += 1
      os.environ[bstack11_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫᯆ")] = str(self.bstack11l1lll111l_opy_())
      self.logger.info(bstack11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢᯇ"))
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᯈ").format(e))
  def bstack11l1lll111l_opy_(self):
    if self.bstack1llllll1l_opy_:
      return
    try:
      bstack11l1l1ll111_opy_ = [platform[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᯉ")].lower() for platform in self.config.get(bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᯊ"), [])]
      bstack11l1ll1111l_opy_ = sys.maxsize
      bstack11l1l1l11ll_opy_ = bstack11_opy_ (u"ࠪࠫᯋ")
      for browser in bstack11l1l1ll111_opy_:
        if browser in self.bstack11l1lll1l11_opy_:
          bstack11l1l1ll1l1_opy_ = self.bstack11l1lll1l11_opy_[browser]
        if bstack11l1l1ll1l1_opy_ < bstack11l1ll1111l_opy_:
          bstack11l1ll1111l_opy_ = bstack11l1l1ll1l1_opy_
          bstack11l1l1l11ll_opy_ = browser
      return bstack11l1l1l11ll_opy_
    except Exception as e:
      self.logger.error(bstack11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᯌ").format(e))
  @classmethod
  def bstack111ll11l_opy_(self):
    return os.getenv(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪᯍ"), bstack11_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬᯎ")).lower()
  @classmethod
  def bstack1l1lll11l_opy_(self):
    return os.getenv(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫᯏ"), bstack11_opy_ (u"ࠨࠩᯐ"))
  @classmethod
  def bstack1ll11111lll_opy_(cls, value):
    cls.bstack1ll11lll11_opy_ = value
  @classmethod
  def bstack11l1l11l11l_opy_(cls):
    return cls.bstack1ll11lll11_opy_
  @classmethod
  def bstack1ll111111ll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11l1ll111l1_opy_(cls):
    return cls.percy_build_id