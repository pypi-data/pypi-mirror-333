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
from bstack_utils.helper import bstack111l11l1l_opy_, bstack11lllll1l_opy_
from bstack_utils.measure import measure
class bstack1lll111lll_opy_:
  working_dir = os.getcwd()
  bstack111l1l11l_opy_ = False
  config = {}
  binary_path = bstack1l11l_opy_ (u"ࠬ࠭᭝")
  bstack11l1l111lll_opy_ = bstack1l11l_opy_ (u"࠭ࠧ᭞")
  bstack11l1lll11_opy_ = False
  bstack11l1l11lll1_opy_ = None
  bstack11l1l11ll1l_opy_ = {}
  bstack11l1lll11l1_opy_ = 300
  bstack11l1lll111l_opy_ = False
  logger = None
  bstack11l1l1l1l1l_opy_ = False
  bstack111ll11l1_opy_ = False
  percy_build_id = None
  bstack11l1ll11l1l_opy_ = bstack1l11l_opy_ (u"ࠧࠨ᭟")
  bstack11l1ll11lll_opy_ = {
    bstack1l11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ᭠") : 1,
    bstack1l11l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ᭡") : 2,
    bstack1l11l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨ᭢") : 3,
    bstack1l11l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫ᭣") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l1l1l11l1_opy_(self):
    bstack11l1l11l11l_opy_ = bstack1l11l_opy_ (u"ࠬ࠭᭤")
    bstack11l1l11l1l1_opy_ = sys.platform
    bstack11l1ll1ll1l_opy_ = bstack1l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ᭥")
    if re.match(bstack1l11l_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢ᭦"), bstack11l1l11l1l1_opy_) != None:
      bstack11l1l11l11l_opy_ = bstack1l1111l1ll1_opy_ + bstack1l11l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤ᭧")
      self.bstack11l1ll11l1l_opy_ = bstack1l11l_opy_ (u"ࠩࡰࡥࡨ࠭᭨")
    elif re.match(bstack1l11l_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣ᭩"), bstack11l1l11l1l1_opy_) != None:
      bstack11l1l11l11l_opy_ = bstack1l1111l1ll1_opy_ + bstack1l11l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧ᭪")
      bstack11l1ll1ll1l_opy_ = bstack1l11l_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣ᭫")
      self.bstack11l1ll11l1l_opy_ = bstack1l11l_opy_ (u"࠭ࡷࡪࡰ᭬ࠪ")
    else:
      bstack11l1l11l11l_opy_ = bstack1l1111l1ll1_opy_ + bstack1l11l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥ᭭")
      self.bstack11l1ll11l1l_opy_ = bstack1l11l_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧ᭮")
    return bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_
  def bstack11l1l111ll1_opy_(self):
    try:
      bstack11l1ll111ll_opy_ = [os.path.join(expanduser(bstack1l11l_opy_ (u"ࠤࢁࠦ᭯")), bstack1l11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᭰")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l1ll111ll_opy_:
        if(self.bstack11l1l1ll11l_opy_(path)):
          return path
      raise bstack1l11l_opy_ (u"࡚ࠦࡴࡡ࡭ࡤࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣ᭱")
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢ᭲").format(e))
  def bstack11l1l1ll11l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  @measure(event_name=EVENTS.bstack1l11111lll1_opy_, stage=STAGE.bstack1111111l_opy_)
  def bstack11l1l1l1lll_opy_(self, bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_):
    try:
      bstack11l1l1lll1l_opy_ = self.bstack11l1l111ll1_opy_()
      bstack11l1l11l1ll_opy_ = os.path.join(bstack11l1l1lll1l_opy_, bstack1l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩ᭳"))
      bstack11l1l1llll1_opy_ = os.path.join(bstack11l1l1lll1l_opy_, bstack11l1ll1ll1l_opy_)
      if os.path.exists(bstack11l1l1llll1_opy_):
        self.logger.info(bstack1l11l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤ᭴").format(bstack11l1l1llll1_opy_))
        return bstack11l1l1llll1_opy_
      if os.path.exists(bstack11l1l11l1ll_opy_):
        self.logger.info(bstack1l11l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨ᭵").format(bstack11l1l11l1ll_opy_))
        return self.bstack11l1l11l111_opy_(bstack11l1l11l1ll_opy_, bstack11l1ll1ll1l_opy_)
      self.logger.info(bstack1l11l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢ᭶").format(bstack11l1l11l11l_opy_))
      response = bstack11lllll1l_opy_(bstack1l11l_opy_ (u"ࠪࡋࡊ࡚ࠧ᭷"), bstack11l1l11l11l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11l1l11l1ll_opy_, bstack1l11l_opy_ (u"ࠫࡼࡨࠧ᭸")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11l_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥ᭹").format(bstack11l1l11l1ll_opy_))
        return self.bstack11l1l11l111_opy_(bstack11l1l11l1ll_opy_, bstack11l1ll1ll1l_opy_)
      else:
        raise(bstack1l11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤ᭺").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣ᭻").format(e))
  def bstack11l1l1l1ll1_opy_(self, bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_):
    try:
      retry = 2
      bstack11l1l1llll1_opy_ = None
      bstack11l1l111l11_opy_ = False
      while retry > 0:
        bstack11l1l1llll1_opy_ = self.bstack11l1l1l1lll_opy_(bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_)
        bstack11l1l111l11_opy_ = self.bstack11l1ll11ll1_opy_(bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_, bstack11l1l1llll1_opy_)
        if bstack11l1l111l11_opy_:
          break
        retry -= 1
      return bstack11l1l1llll1_opy_, bstack11l1l111l11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧ᭼").format(e))
    return bstack11l1l1llll1_opy_, False
  def bstack11l1ll11ll1_opy_(self, bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_, bstack11l1l1llll1_opy_, bstack11l1ll1l1l1_opy_ = 0):
    if bstack11l1ll1l1l1_opy_ > 1:
      return False
    if bstack11l1l1llll1_opy_ == None or os.path.exists(bstack11l1l1llll1_opy_) == False:
      self.logger.warn(bstack1l11l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ᭽"))
      return False
    bstack11l1l1l111l_opy_ = bstack1l11l_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣ᭾")
    command = bstack1l11l_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ᭿").format(bstack11l1l1llll1_opy_)
    bstack11l1l1lllll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l1l1l111l_opy_, bstack11l1l1lllll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᮀ"))
      return False
  def bstack11l1l11l111_opy_(self, bstack11l1l11l1ll_opy_, bstack11l1ll1ll1l_opy_):
    try:
      working_dir = os.path.dirname(bstack11l1l11l1ll_opy_)
      shutil.unpack_archive(bstack11l1l11l1ll_opy_, working_dir)
      bstack11l1l1llll1_opy_ = os.path.join(working_dir, bstack11l1ll1ll1l_opy_)
      os.chmod(bstack11l1l1llll1_opy_, 0o755)
      return bstack11l1l1llll1_opy_
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᮁ"))
  def bstack11l1l1111ll_opy_(self):
    try:
      bstack11l1ll1l11l_opy_ = self.config.get(bstack1l11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᮂ"))
      bstack11l1l1111ll_opy_ = bstack11l1ll1l11l_opy_ or (bstack11l1ll1l11l_opy_ is None and self.bstack111l1l11l_opy_)
      if not bstack11l1l1111ll_opy_ or self.config.get(bstack1l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᮃ"), None) not in bstack1l1111ll1l1_opy_:
        return False
      self.bstack11l1lll11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᮄ").format(e))
  def bstack11l1lll1111_opy_(self):
    try:
      bstack11l1lll1111_opy_ = self.percy_capture_mode
      return bstack11l1lll1111_opy_
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᮅ").format(e))
  def init(self, bstack111l1l11l_opy_, config, logger):
    self.bstack111l1l11l_opy_ = bstack111l1l11l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1l1111ll_opy_():
      return
    self.bstack11l1l11ll1l_opy_ = config.get(bstack1l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᮆ"), {})
    self.percy_capture_mode = config.get(bstack1l11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᮇ"))
    try:
      bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_ = self.bstack11l1l1l11l1_opy_()
      bstack11l1l1llll1_opy_, bstack11l1l111l11_opy_ = self.bstack11l1l1l1ll1_opy_(bstack11l1l11l11l_opy_, bstack11l1ll1ll1l_opy_)
      if bstack11l1l111l11_opy_:
        self.binary_path = bstack11l1l1llll1_opy_
        thread = Thread(target=self.bstack11l1ll11111_opy_)
        thread.start()
      else:
        self.bstack11l1l1l1l1l_opy_ = True
        self.logger.error(bstack1l11l_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᮈ").format(bstack11l1l1llll1_opy_))
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᮉ").format(e))
  def bstack11l1l111l1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11l_opy_ (u"ࠨ࡮ࡲ࡫ࠬᮊ"), bstack1l11l_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᮋ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11l_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢᮌ").format(logfile))
      self.bstack11l1l111lll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᮍ").format(e))
  @measure(event_name=EVENTS.bstack1l111l1111l_opy_, stage=STAGE.bstack1111111l_opy_)
  def bstack11l1ll11111_opy_(self):
    bstack11l1ll1l111_opy_ = self.bstack11l1l1ll1l1_opy_()
    if bstack11l1ll1l111_opy_ == None:
      self.bstack11l1l1l1l1l_opy_ = True
      self.logger.error(bstack1l11l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣᮎ"))
      return False
    command_args = [bstack1l11l_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢᮏ") if self.bstack111l1l11l_opy_ else bstack1l11l_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫᮐ")]
    bstack11l1lllllll_opy_ = self.bstack11l1l1lll11_opy_()
    if bstack11l1lllllll_opy_ != None:
      command_args.append(bstack1l11l_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢᮑ").format(bstack11l1lllllll_opy_))
    env = os.environ.copy()
    env[bstack1l11l_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᮒ")] = bstack11l1ll1l111_opy_
    env[bstack1l11l_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥᮓ")] = os.environ.get(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᮔ"), bstack1l11l_opy_ (u"ࠬ࠭ᮕ"))
    bstack11l1ll1111l_opy_ = [self.binary_path]
    self.bstack11l1l111l1l_opy_()
    self.bstack11l1l11lll1_opy_ = self.bstack11l1l1111l1_opy_(bstack11l1ll1111l_opy_ + command_args, env)
    self.logger.debug(bstack1l11l_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᮖ"))
    bstack11l1ll1l1l1_opy_ = 0
    while self.bstack11l1l11lll1_opy_.poll() == None:
      bstack11l1l1ll1ll_opy_ = self.bstack11l1ll1lll1_opy_()
      if bstack11l1l1ll1ll_opy_:
        self.logger.debug(bstack1l11l_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᮗ"))
        self.bstack11l1lll111l_opy_ = True
        return True
      bstack11l1ll1l1l1_opy_ += 1
      self.logger.debug(bstack1l11l_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᮘ").format(bstack11l1ll1l1l1_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᮙ").format(bstack11l1ll1l1l1_opy_))
    self.bstack11l1l1l1l1l_opy_ = True
    return False
  def bstack11l1ll1lll1_opy_(self, bstack11l1ll1l1l1_opy_ = 0):
    if bstack11l1ll1l1l1_opy_ > 10:
      return False
    try:
      bstack11l1l1ll111_opy_ = os.environ.get(bstack1l11l_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᮚ"), bstack1l11l_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᮛ"))
      bstack11l1ll1l1ll_opy_ = bstack11l1l1ll111_opy_ + bstack1l11111ll11_opy_
      response = requests.get(bstack11l1ll1l1ll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᮜ"), {}).get(bstack1l11l_opy_ (u"࠭ࡩࡥࠩᮝ"), None)
      return True
    except:
      self.logger.debug(bstack1l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᮞ"))
      return False
  def bstack11l1l1ll1l1_opy_(self):
    bstack11l1l11111l_opy_ = bstack1l11l_opy_ (u"ࠨࡣࡳࡴࠬᮟ") if self.bstack111l1l11l_opy_ else bstack1l11l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᮠ")
    bstack11l1l1l1l11_opy_ = bstack1l11l_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᮡ") if self.config.get(bstack1l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᮢ")) is None else True
    bstack1l111111l1l_opy_ = bstack1l11l_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨᮣ").format(self.config[bstack1l11l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᮤ")], bstack11l1l11111l_opy_, bstack11l1l1l1l11_opy_)
    if self.percy_capture_mode:
      bstack1l111111l1l_opy_ += bstack1l11l_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤᮥ").format(self.percy_capture_mode)
    uri = bstack111l11l1l_opy_(bstack1l111111l1l_opy_)
    try:
      response = bstack11lllll1l_opy_(bstack1l11l_opy_ (u"ࠨࡉࡈࡘࠬᮦ"), uri, {}, {bstack1l11l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᮧ"): (self.config[bstack1l11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᮨ")], self.config[bstack1l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᮩ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l1lll11_opy_ = data.get(bstack1l11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ᮪࠭"))
        self.percy_capture_mode = data.get(bstack1l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨ᮫ࠫ"))
        os.environ[bstack1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᮬ")] = str(self.bstack11l1lll11_opy_)
        os.environ[bstack1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᮭ")] = str(self.percy_capture_mode)
        if bstack11l1l1l1l11_opy_ == bstack1l11l_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧᮮ") and str(self.bstack11l1lll11_opy_).lower() == bstack1l11l_opy_ (u"ࠥࡸࡷࡻࡥࠣᮯ"):
          self.bstack111ll11l1_opy_ = True
        if bstack1l11l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ᮰") in data:
          return data[bstack1l11l_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ᮱")]
        else:
          raise bstack1l11l_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭᮲").format(data)
      else:
        raise bstack1l11l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢ᮳").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤ᮴").format(e))
  def bstack11l1l1lll11_opy_(self):
    bstack11l1l11ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧ᮵"))
    try:
      if bstack1l11l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ᮶") not in self.bstack11l1l11ll1l_opy_:
        self.bstack11l1l11ll1l_opy_[bstack1l11l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᮷")] = 2
      with open(bstack11l1l11ll11_opy_, bstack1l11l_opy_ (u"ࠬࡽࠧ᮸")) as fp:
        json.dump(self.bstack11l1l11ll1l_opy_, fp)
      return bstack11l1l11ll11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᮹").format(e))
  def bstack11l1l1111l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11l1ll11l1l_opy_ == bstack1l11l_opy_ (u"ࠧࡸ࡫ࡱࠫᮺ"):
        bstack11l1ll111l1_opy_ = [bstack1l11l_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᮻ"), bstack1l11l_opy_ (u"ࠩ࠲ࡧࠬᮼ")]
        cmd = bstack11l1ll111l1_opy_ + cmd
      cmd = bstack1l11l_opy_ (u"ࠪࠤࠬᮽ").join(cmd)
      self.logger.debug(bstack1l11l_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣᮾ").format(cmd))
      with open(self.bstack11l1l111lll_opy_, bstack1l11l_opy_ (u"ࠧࡧࠢᮿ")) as bstack11l1lll1l1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l1lll1l1l_opy_, text=True, stderr=bstack11l1lll1l1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l1l1l1l1l_opy_ = True
      self.logger.error(bstack1l11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᯀ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l1lll111l_opy_:
        self.logger.info(bstack1l11l_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣᯁ"))
        cmd = [self.binary_path, bstack1l11l_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᯂ")]
        self.bstack11l1l1111l1_opy_(cmd)
        self.bstack11l1lll111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᯃ").format(cmd, e))
  def bstack1ll11111l_opy_(self):
    if not self.bstack11l1lll11_opy_:
      return
    try:
      bstack11l1l1l11ll_opy_ = 0
      while not self.bstack11l1lll111l_opy_ and bstack11l1l1l11ll_opy_ < self.bstack11l1lll11l1_opy_:
        if self.bstack11l1l1l1l1l_opy_:
          self.logger.info(bstack1l11l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣᯄ"))
          return
        time.sleep(1)
        bstack11l1l1l11ll_opy_ += 1
      os.environ[bstack1l11l_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᯅ")] = str(self.bstack11l1ll1llll_opy_())
      self.logger.info(bstack1l11l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨᯆ"))
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᯇ").format(e))
  def bstack11l1ll1llll_opy_(self):
    if self.bstack111l1l11l_opy_:
      return
    try:
      bstack11l1l1l1111_opy_ = [platform[bstack1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᯈ")].lower() for platform in self.config.get(bstack1l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᯉ"), [])]
      bstack11l1lll1l11_opy_ = sys.maxsize
      bstack11l1lll11ll_opy_ = bstack1l11l_opy_ (u"ࠩࠪᯊ")
      for browser in bstack11l1l1l1111_opy_:
        if browser in self.bstack11l1ll11lll_opy_:
          bstack11l1ll1ll11_opy_ = self.bstack11l1ll11lll_opy_[browser]
        if bstack11l1ll1ll11_opy_ < bstack11l1lll1l11_opy_:
          bstack11l1lll1l11_opy_ = bstack11l1ll1ll11_opy_
          bstack11l1lll11ll_opy_ = browser
      return bstack11l1lll11ll_opy_
    except Exception as e:
      self.logger.error(bstack1l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᯋ").format(e))
  @classmethod
  def bstack1ll11lll_opy_(self):
    return os.getenv(bstack1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᯌ"), bstack1l11l_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫᯍ")).lower()
  @classmethod
  def bstack1lllll1111_opy_(self):
    return os.getenv(bstack1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᯎ"), bstack1l11l_opy_ (u"ࠧࠨᯏ"))
  @classmethod
  def bstack1l1llllllll_opy_(cls, value):
    cls.bstack111ll11l1_opy_ = value
  @classmethod
  def bstack11l1ll11l11_opy_(cls):
    return cls.bstack111ll11l1_opy_
  @classmethod
  def bstack1l1lllllll1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11l1l11llll_opy_(cls):
    return cls.percy_build_id