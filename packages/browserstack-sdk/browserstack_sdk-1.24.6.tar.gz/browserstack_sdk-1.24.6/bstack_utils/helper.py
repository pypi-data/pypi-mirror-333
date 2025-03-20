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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l1111lll11_opy_, bstack1llll1l1ll_opy_, bstack1l1ll111l_opy_, bstack11l1ll1ll_opy_,
                                    bstack1l1111l111l_opy_, bstack1l111l11ll1_opy_, bstack1l1111llll1_opy_, bstack1l1111l1l11_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1lll111ll1_opy_, bstack11l1ll1l1_opy_
from bstack_utils.proxy import bstack11l1ll11_opy_, bstack111111l11_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11l11l1l_opy_
from browserstack_sdk._version import __version__
bstack1l1l1lll1_opy_ = Config.bstack11l111l11_opy_()
logger = bstack11l11l1l_opy_.get_logger(__name__, bstack11l11l1l_opy_.bstack1lll1l1lll1_opy_())
def bstack1l11l1l1111_opy_(config):
    return config[bstack11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᢗ")]
def bstack1l11l11l1l1_opy_(config):
    return config[bstack11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᢘ")]
def bstack111l1l111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11ll1lll11l_opy_(obj):
    values = []
    bstack11lll111ll1_opy_ = re.compile(bstack11_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᢙ"), re.I)
    for key in obj.keys():
        if bstack11lll111ll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11lllll1l11_opy_(config):
    tags = []
    tags.extend(bstack11ll1lll11l_opy_(os.environ))
    tags.extend(bstack11ll1lll11l_opy_(config))
    return tags
def bstack11llllllll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11lll1lll11_opy_(bstack11lll11ll1l_opy_):
    if not bstack11lll11ll1l_opy_:
        return bstack11_opy_ (u"ࠬ࠭ᢚ")
    return bstack11_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢᢛ").format(bstack11lll11ll1l_opy_.name, bstack11lll11ll1l_opy_.email)
def bstack1l11l11llll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll1llllll_opy_ = repo.common_dir
        info = {
            bstack11_opy_ (u"ࠢࡴࡪࡤࠦᢜ"): repo.head.commit.hexsha,
            bstack11_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᢝ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᢞ"): repo.active_branch.name,
            bstack11_opy_ (u"ࠥࡸࡦ࡭ࠢᢟ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢᢠ"): bstack11lll1lll11_opy_(repo.head.commit.committer),
            bstack11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨᢡ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨᢢ"): bstack11lll1lll11_opy_(repo.head.commit.author),
            bstack11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᢣ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᢤ"): repo.head.commit.message,
            bstack11_opy_ (u"ࠤࡵࡳࡴࡺࠢᢥ"): repo.git.rev_parse(bstack11_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧᢦ")),
            bstack11_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᢧ"): bstack11ll1llllll_opy_,
            bstack11_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᢨ"): subprocess.check_output([bstack11_opy_ (u"ࠨࡧࡪࡶᢩࠥ"), bstack11_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᢪ"), bstack11_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦ᢫")]).strip().decode(
                bstack11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᢬")),
            bstack11_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ᢭"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ᢮"): repo.git.rev_list(
                bstack11_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧ᢯").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11lll1lllll_opy_ = []
        for remote in remotes:
            bstack11lll11lll1_opy_ = {
                bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᢰ"): remote.name,
                bstack11_opy_ (u"ࠢࡶࡴ࡯ࠦᢱ"): remote.url,
            }
            bstack11lll1lllll_opy_.append(bstack11lll11lll1_opy_)
        bstack11ll1ll1l1l_opy_ = {
            bstack11_opy_ (u"ࠣࡰࡤࡱࡪࠨᢲ"): bstack11_opy_ (u"ࠤࡪ࡭ࡹࠨᢳ"),
            **info,
            bstack11_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᢴ"): bstack11lll1lllll_opy_
        }
        bstack11ll1ll1l1l_opy_ = bstack11lll1111ll_opy_(bstack11ll1ll1l1l_opy_)
        return bstack11ll1ll1l1l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᢵ").format(err))
        return {}
def bstack11lll1111ll_opy_(bstack11ll1ll1l1l_opy_):
    bstack1l111111l1l_opy_ = bstack11ll1lllll1_opy_(bstack11ll1ll1l1l_opy_)
    if bstack1l111111l1l_opy_ and bstack1l111111l1l_opy_ > bstack1l1111l111l_opy_:
        bstack11ll1l111ll_opy_ = bstack1l111111l1l_opy_ - bstack1l1111l111l_opy_
        bstack11lll111lll_opy_ = bstack11ll1l1ll1l_opy_(bstack11ll1ll1l1l_opy_[bstack11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᢶ")], bstack11ll1l111ll_opy_)
        bstack11ll1ll1l1l_opy_[bstack11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᢷ")] = bstack11lll111lll_opy_
        logger.info(bstack11_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤᢸ")
                    .format(bstack11ll1lllll1_opy_(bstack11ll1ll1l1l_opy_) / 1024))
    return bstack11ll1ll1l1l_opy_
def bstack11ll1lllll1_opy_(bstack1l11ll1lll_opy_):
    try:
        if bstack1l11ll1lll_opy_:
            bstack11lll11l111_opy_ = json.dumps(bstack1l11ll1lll_opy_)
            bstack11lllll1ll1_opy_ = sys.getsizeof(bstack11lll11l111_opy_)
            return bstack11lllll1ll1_opy_
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣᢹ").format(e))
    return -1
def bstack11ll1l1ll1l_opy_(field, bstack11llll1l1l1_opy_):
    try:
        bstack11ll1l1lll1_opy_ = len(bytes(bstack1l111l11ll1_opy_, bstack11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᢺ")))
        bstack11lllllll1l_opy_ = bytes(field, bstack11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᢻ"))
        bstack11llll1111l_opy_ = len(bstack11lllllll1l_opy_)
        bstack1l1111111l1_opy_ = ceil(bstack11llll1111l_opy_ - bstack11llll1l1l1_opy_ - bstack11ll1l1lll1_opy_)
        if bstack1l1111111l1_opy_ > 0:
            bstack11llll11l1l_opy_ = bstack11lllllll1l_opy_[:bstack1l1111111l1_opy_].decode(bstack11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᢼ"), errors=bstack11_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬᢽ")) + bstack1l111l11ll1_opy_
            return bstack11llll11l1l_opy_
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦᢾ").format(e))
    return field
def bstack1ll1ll111_opy_():
    env = os.environ
    if (bstack11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᢿ") in env and len(env[bstack11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᣀ")]) > 0) or (
            bstack11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᣁ") in env and len(env[bstack11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᣂ")]) > 0):
        return {
            bstack11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᣃ"): bstack11_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᣄ"),
            bstack11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᣅ"): env.get(bstack11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᣆ")),
            bstack11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᣇ"): env.get(bstack11_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᣈ")),
            bstack11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᣉ"): env.get(bstack11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᣊ"))
        }
    if env.get(bstack11_opy_ (u"ࠧࡉࡉࠣᣋ")) == bstack11_opy_ (u"ࠨࡴࡳࡷࡨࠦᣌ") and bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᣍ"))):
        return {
            bstack11_opy_ (u"ࠣࡰࡤࡱࡪࠨᣎ"): bstack11_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᣏ"),
            bstack11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᣐ"): env.get(bstack11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᣑ")),
            bstack11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᣒ"): env.get(bstack11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᣓ")),
            bstack11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᣔ"): env.get(bstack11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᣕ"))
        }
    if env.get(bstack11_opy_ (u"ࠤࡆࡍࠧᣖ")) == bstack11_opy_ (u"ࠥࡸࡷࡻࡥࠣᣗ") and bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᣘ"))):
        return {
            bstack11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᣙ"): bstack11_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᣚ"),
            bstack11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᣛ"): env.get(bstack11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᣜ")),
            bstack11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᣝ"): env.get(bstack11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᣞ")),
            bstack11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᣟ"): env.get(bstack11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᣠ"))
        }
    if env.get(bstack11_opy_ (u"ࠨࡃࡊࠤᣡ")) == bstack11_opy_ (u"ࠢࡵࡴࡸࡩࠧᣢ") and env.get(bstack11_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᣣ")) == bstack11_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᣤ"):
        return {
            bstack11_opy_ (u"ࠥࡲࡦࡳࡥࠣᣥ"): bstack11_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᣦ"),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᣧ"): None,
            bstack11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᣨ"): None,
            bstack11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᣩ"): None
        }
    if env.get(bstack11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᣪ")) and env.get(bstack11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᣫ")):
        return {
            bstack11_opy_ (u"ࠥࡲࡦࡳࡥࠣᣬ"): bstack11_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᣭ"),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᣮ"): env.get(bstack11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᣯ")),
            bstack11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᣰ"): None,
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᣱ"): env.get(bstack11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᣲ"))
        }
    if env.get(bstack11_opy_ (u"ࠥࡇࡎࠨᣳ")) == bstack11_opy_ (u"ࠦࡹࡸࡵࡦࠤᣴ") and bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᣵ"))):
        return {
            bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᣶"): bstack11_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ᣷"),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᣸"): env.get(bstack11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧ᣹")),
            bstack11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᣺"): None,
            bstack11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᣻"): env.get(bstack11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᣼"))
        }
    if env.get(bstack11_opy_ (u"ࠨࡃࡊࠤ᣽")) == bstack11_opy_ (u"ࠢࡵࡴࡸࡩࠧ᣾") and bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦ᣿"))):
        return {
            bstack11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤀ"): bstack11_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᤁ"),
            bstack11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᤂ"): env.get(bstack11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᤃ")),
            bstack11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᤄ"): env.get(bstack11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᤅ")),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᤆ"): env.get(bstack11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᤇ"))
        }
    if env.get(bstack11_opy_ (u"ࠥࡇࡎࠨᤈ")) == bstack11_opy_ (u"ࠦࡹࡸࡵࡦࠤᤉ") and bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᤊ"))):
        return {
            bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᤋ"): bstack11_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᤌ"),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᤍ"): env.get(bstack11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᤎ")),
            bstack11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᤏ"): env.get(bstack11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᤐ")),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᤑ"): env.get(bstack11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᤒ"))
        }
    if env.get(bstack11_opy_ (u"ࠢࡄࡋࠥᤓ")) == bstack11_opy_ (u"ࠣࡶࡵࡹࡪࠨᤔ") and bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᤕ"))):
        return {
            bstack11_opy_ (u"ࠥࡲࡦࡳࡥࠣᤖ"): bstack11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᤗ"),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᤘ"): env.get(bstack11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᤙ")),
            bstack11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᤚ"): env.get(bstack11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᤛ")) or env.get(bstack11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᤜ")),
            bstack11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᤝ"): env.get(bstack11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᤞ"))
        }
    if bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢ᤟"))):
        return {
            bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᤠ"): bstack11_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᤡ"),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᤢ"): bstack11_opy_ (u"ࠤࡾࢁࢀࢃࠢᤣ").format(env.get(bstack11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᤤ")), env.get(bstack11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᤥ"))),
            bstack11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᤦ"): env.get(bstack11_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᤧ")),
            bstack11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᤨ"): env.get(bstack11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᤩ"))
        }
    if bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᤪ"))):
        return {
            bstack11_opy_ (u"ࠥࡲࡦࡳࡥࠣᤫ"): bstack11_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨ᤬"),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᤭"): bstack11_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧ᤮").format(env.get(bstack11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭᤯")), env.get(bstack11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᤰ")), env.get(bstack11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᤱ")), env.get(bstack11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᤲ"))),
            bstack11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᤳ"): env.get(bstack11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᤴ")),
            bstack11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᤵ"): env.get(bstack11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᤶ"))
        }
    if env.get(bstack11_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᤷ")) and env.get(bstack11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᤸ")):
        return {
            bstack11_opy_ (u"ࠥࡲࡦࡳࡥ᤹ࠣ"): bstack11_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨ᤺"),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᤻ࠣ"): bstack11_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤ᤼").format(env.get(bstack11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ᤽")), env.get(bstack11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭᤾")), env.get(bstack11_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩ᤿"))),
            bstack11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᥀"): env.get(bstack11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ᥁")),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᥂"): env.get(bstack11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ᥃"))
        }
    if any([env.get(bstack11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᥄")), env.get(bstack11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ᥅")), env.get(bstack11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᥆"))]):
        return {
            bstack11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᥇"): bstack11_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦ᥈"),
            bstack11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᥉"): env.get(bstack11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᥊")),
            bstack11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᥋"): env.get(bstack11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᥌")),
            bstack11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᥍"): env.get(bstack11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᥎"))
        }
    if env.get(bstack11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ᥏")):
        return {
            bstack11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᥐ"): bstack11_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᥑ"),
            bstack11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᥒ"): env.get(bstack11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᥓ")),
            bstack11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᥔ"): env.get(bstack11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᥕ")),
            bstack11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᥖ"): env.get(bstack11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᥗ"))
        }
    if env.get(bstack11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᥘ")) or env.get(bstack11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᥙ")):
        return {
            bstack11_opy_ (u"ࠣࡰࡤࡱࡪࠨᥚ"): bstack11_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᥛ"),
            bstack11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᥜ"): env.get(bstack11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᥝ")),
            bstack11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᥞ"): bstack11_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᥟ") if env.get(bstack11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᥠ")) else None,
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᥡ"): env.get(bstack11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᥢ"))
        }
    if any([env.get(bstack11_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᥣ")), env.get(bstack11_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᥤ")), env.get(bstack11_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᥥ"))]):
        return {
            bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᥦ"): bstack11_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᥧ"),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᥨ"): None,
            bstack11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᥩ"): env.get(bstack11_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᥪ")),
            bstack11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᥫ"): env.get(bstack11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᥬ"))
        }
    if env.get(bstack11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᥭ")):
        return {
            bstack11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᥮"): bstack11_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦ᥯"),
            bstack11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᥰ"): env.get(bstack11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᥱ")),
            bstack11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᥲ"): bstack11_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᥳ").format(env.get(bstack11_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᥴ"))) if env.get(bstack11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ᥵")) else None,
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᥶"): env.get(bstack11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᥷"))
        }
    if bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦ᥸"))):
        return {
            bstack11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᥹"): bstack11_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ᥺"),
            bstack11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᥻"): env.get(bstack11_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦ᥼")),
            bstack11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᥽"): env.get(bstack11_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧ᥾")),
            bstack11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᥿"): env.get(bstack11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᦀ"))
        }
    if bstack11l1l1l11_opy_(env.get(bstack11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᦁ"))):
        return {
            bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᦂ"): bstack11_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᦃ"),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᦄ"): bstack11_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᦅ").format(env.get(bstack11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᦆ")), env.get(bstack11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᦇ")), env.get(bstack11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᦈ"))),
            bstack11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᦉ"): env.get(bstack11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᦊ")),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᦋ"): env.get(bstack11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᦌ"))
        }
    if env.get(bstack11_opy_ (u"ࠥࡇࡎࠨᦍ")) == bstack11_opy_ (u"ࠦࡹࡸࡵࡦࠤᦎ") and env.get(bstack11_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᦏ")) == bstack11_opy_ (u"ࠨ࠱ࠣᦐ"):
        return {
            bstack11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦑ"): bstack11_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᦒ"),
            bstack11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᦓ"): bstack11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᦔ").format(env.get(bstack11_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᦕ"))),
            bstack11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᦖ"): None,
            bstack11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦗ"): None,
        }
    if env.get(bstack11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᦘ")):
        return {
            bstack11_opy_ (u"ࠣࡰࡤࡱࡪࠨᦙ"): bstack11_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᦚ"),
            bstack11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᦛ"): None,
            bstack11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᦜ"): env.get(bstack11_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᦝ")),
            bstack11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦞ"): env.get(bstack11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᦟ"))
        }
    if any([env.get(bstack11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᦠ")), env.get(bstack11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᦡ")), env.get(bstack11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᦢ")), env.get(bstack11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᦣ"))]):
        return {
            bstack11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᦤ"): bstack11_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᦥ"),
            bstack11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᦦ"): None,
            bstack11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᦧ"): env.get(bstack11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᦨ")) or None,
            bstack11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᦩ"): env.get(bstack11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᦪ"), 0)
        }
    if env.get(bstack11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᦫ")):
        return {
            bstack11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᦬"): bstack11_opy_ (u"ࠢࡈࡱࡆࡈࠧ᦭"),
            bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᦮"): None,
            bstack11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᦯"): env.get(bstack11_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᦰ")),
            bstack11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᦱ"): env.get(bstack11_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᦲ"))
        }
    if env.get(bstack11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᦳ")):
        return {
            bstack11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦴ"): bstack11_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᦵ"),
            bstack11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᦶ"): env.get(bstack11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᦷ")),
            bstack11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᦸ"): env.get(bstack11_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᦹ")),
            bstack11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦺ"): env.get(bstack11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᦻ"))
        }
    return {bstack11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᦼ"): None}
def get_host_info():
    return {
        bstack11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᦽ"): platform.node(),
        bstack11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᦾ"): platform.system(),
        bstack11_opy_ (u"ࠦࡹࡿࡰࡦࠤᦿ"): platform.machine(),
        bstack11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᧀ"): platform.version(),
        bstack11_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᧁ"): platform.architecture()[0]
    }
def bstack1ll11l11l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11lll111111_opy_():
    if bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᧂ")):
        return bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᧃ")
    return bstack11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᧄ")
def bstack11ll1l1l1l1_opy_(driver):
    info = {
        bstack11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᧅ"): driver.capabilities,
        bstack11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᧆ"): driver.session_id,
        bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᧇ"): driver.capabilities.get(bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᧈ"), None),
        bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᧉ"): driver.capabilities.get(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᧊"), None),
        bstack11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫ᧋"): driver.capabilities.get(bstack11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ᧌"), None),
    }
    if bstack11lll111111_opy_() == bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᧍"):
        if bstack1llllll1l_opy_():
            info[bstack11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᧎")] = bstack11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᧏")
        elif driver.capabilities.get(bstack11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᧐"), {}).get(bstack11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ᧑"), False):
            info[bstack11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ᧒")] = bstack11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ᧓")
        else:
            info[bstack11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ᧔")] = bstack11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᧕")
    return info
def bstack1llllll1l_opy_():
    if bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᧖")):
        return True
    if bstack11l1l1l11_opy_(os.environ.get(bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ᧗"), None)):
        return True
    return False
def bstack111111ll_opy_(bstack11llll1lll1_opy_, url, data, config):
    headers = config.get(bstack11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ᧘"), None)
    proxies = bstack11l1ll11_opy_(config, url)
    auth = config.get(bstack11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ᧙"), None)
    response = requests.request(
            bstack11llll1lll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll111l111_opy_(bstack1l1ll11l11_opy_, size):
    bstack1l11l111l_opy_ = []
    while len(bstack1l1ll11l11_opy_) > size:
        bstack1l1lll1lll_opy_ = bstack1l1ll11l11_opy_[:size]
        bstack1l11l111l_opy_.append(bstack1l1lll1lll_opy_)
        bstack1l1ll11l11_opy_ = bstack1l1ll11l11_opy_[size:]
    bstack1l11l111l_opy_.append(bstack1l1ll11l11_opy_)
    return bstack1l11l111l_opy_
def bstack11lll11111l_opy_(message, bstack11lllll1111_opy_=False):
    os.write(1, bytes(message, bstack11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᧚")))
    os.write(1, bytes(bstack11_opy_ (u"ࠫࡡࡴࠧ᧛"), bstack11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᧜")))
    if bstack11lllll1111_opy_:
        with open(bstack11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬ᧝") + os.environ[bstack11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭᧞")] + bstack11_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭᧟"), bstack11_opy_ (u"ࠩࡤࠫ᧠")) as f:
            f.write(message + bstack11_opy_ (u"ࠪࡠࡳ࠭᧡"))
def bstack1ll1111l1l1_opy_():
    return os.environ[bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᧢")].lower() == bstack11_opy_ (u"ࠬࡺࡲࡶࡧࠪ᧣")
def bstack11l1l1ll1l_opy_(bstack1l1111111ll_opy_):
    return bstack11_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ᧤").format(bstack1l1111lll11_opy_, bstack1l1111111ll_opy_)
def bstack1lllll11ll_opy_():
    return bstack11l111l1l1_opy_().replace(tzinfo=None).isoformat() + bstack11_opy_ (u"࡛ࠧࠩ᧥")
def bstack11llll111ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11_opy_ (u"ࠨ࡜ࠪ᧦"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11_opy_ (u"ࠩ࡝ࠫ᧧")))).total_seconds() * 1000
def bstack11llllll1ll_opy_(timestamp):
    return bstack11ll1l11lll_opy_(timestamp).isoformat() + bstack11_opy_ (u"ࠪ࡞ࠬ᧨")
def bstack11ll1lll111_opy_(bstack11ll1l1l1ll_opy_):
    date_format = bstack11_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩ᧩")
    bstack11lllll1l1l_opy_ = datetime.datetime.strptime(bstack11ll1l1l1ll_opy_, date_format)
    return bstack11lllll1l1l_opy_.isoformat() + bstack11_opy_ (u"ࠬࡠࠧ᧪")
def bstack11ll1l11l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᧫")
    else:
        return bstack11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᧬")
def bstack11l1l1l11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11_opy_ (u"ࠨࡶࡵࡹࡪ࠭᧭")
def bstack11lll1111l1_opy_(val):
    return val.__str__().lower() == bstack11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ᧮")
def bstack111lll1lll_opy_(bstack11lllll11ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11lllll11ll_opy_ as e:
                print(bstack11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ᧯").format(func.__name__, bstack11lllll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11lll111l11_opy_(bstack11lll11llll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11lll11llll_opy_(cls, *args, **kwargs)
            except bstack11lllll11ll_opy_ as e:
                print(bstack11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦ᧰").format(bstack11lll11llll_opy_.__name__, bstack11lllll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11lll111l11_opy_
    else:
        return decorator
def bstack1ll11ll1l1_opy_(bstack111l1l1l11_opy_):
    if os.getenv(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᧱")) is not None:
        return bstack11l1l1l11_opy_(os.getenv(bstack11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ᧲")))
    if bstack11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᧳") in bstack111l1l1l11_opy_ and bstack11lll1111l1_opy_(bstack111l1l1l11_opy_[bstack11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᧴")]):
        return False
    if bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᧵") in bstack111l1l1l11_opy_ and bstack11lll1111l1_opy_(bstack111l1l1l11_opy_[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᧶")]):
        return False
    return True
def bstack11l1ll11ll_opy_():
    try:
        from pytest_bdd import reporting
        bstack11llll1l1ll_opy_ = os.environ.get(bstack11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦ᧷"), None)
        return bstack11llll1l1ll_opy_ is None or bstack11llll1l1ll_opy_ == bstack11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ᧸")
    except Exception as e:
        return False
def bstack111l11ll1_opy_(hub_url, CONFIG):
    if bstack111l111l1_opy_() <= version.parse(bstack11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭᧹")):
        if hub_url:
            return bstack11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᧺") + hub_url + bstack11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ᧻")
        return bstack1l1ll111l_opy_
    if hub_url:
        return bstack11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᧼") + hub_url + bstack11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ᧽")
    return bstack11l1ll1ll_opy_
def bstack11lll1ll111_opy_():
    return isinstance(os.getenv(bstack11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ᧾")), str)
def bstack1111111l1_opy_(url):
    return urlparse(url).hostname
def bstack11lll11l1_opy_(hostname):
    for bstack1llll11ll1_opy_ in bstack1llll1l1ll_opy_:
        regex = re.compile(bstack1llll11ll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1l11111111l_opy_(bstack11ll1l11ll1_opy_, file_name, logger):
    bstack11llllll1l_opy_ = os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠬࢄࠧ᧿")), bstack11ll1l11ll1_opy_)
    try:
        if not os.path.exists(bstack11llllll1l_opy_):
            os.makedirs(bstack11llllll1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11_opy_ (u"࠭ࡾࠨᨀ")), bstack11ll1l11ll1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11_opy_ (u"ࠧࡸࠩᨁ")):
                pass
            with open(file_path, bstack11_opy_ (u"ࠣࡹ࠮ࠦᨂ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll111ll1_opy_.format(str(e)))
def bstack11lll1lll1l_opy_(file_name, key, value, logger):
    file_path = bstack1l11111111l_opy_(bstack11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᨃ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11111111l_opy_ = json.load(open(file_path, bstack11_opy_ (u"ࠪࡶࡧ࠭ᨄ")))
        else:
            bstack11111111l_opy_ = {}
        bstack11111111l_opy_[key] = value
        with open(file_path, bstack11_opy_ (u"ࠦࡼ࠱ࠢᨅ")) as outfile:
            json.dump(bstack11111111l_opy_, outfile)
def bstack1lll1l1l1l_opy_(file_name, logger):
    file_path = bstack1l11111111l_opy_(bstack11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᨆ"), file_name, logger)
    bstack11111111l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11_opy_ (u"࠭ࡲࠨᨇ")) as bstack11lll1ll11_opy_:
            bstack11111111l_opy_ = json.load(bstack11lll1ll11_opy_)
    return bstack11111111l_opy_
def bstack1l11l1l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫᨈ") + file_path + bstack11_opy_ (u"ࠨࠢࠪᨉ") + str(e))
def bstack111l111l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦᨊ")
def bstack11111111_opy_(config):
    if bstack11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᨋ") in config:
        del (config[bstack11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᨌ")])
        return False
    if bstack111l111l1_opy_() < version.parse(bstack11_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫᨍ")):
        return False
    if bstack111l111l1_opy_() >= version.parse(bstack11_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬᨎ")):
        return True
    if bstack11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᨏ") in config and config[bstack11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᨐ")] is False:
        return False
    else:
        return True
def bstack1111l1ll1_opy_(args_list, bstack11lllllllll_opy_):
    index = -1
    for value in bstack11lllllllll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l11l1l11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l11l1l11_opy_ = bstack11l11l1l11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᨑ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᨒ"), exception=exception)
    def bstack111l11ll1l_opy_(self):
        if self.result != bstack11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᨓ"):
            return None
        if isinstance(self.exception_type, str) and bstack11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᨔ") in self.exception_type:
            return bstack11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᨕ")
        return bstack11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᨖ")
    def bstack11lllllll11_opy_(self):
        if self.result != bstack11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᨗ"):
            return None
        if self.bstack11l11l1l11_opy_:
            return self.bstack11l11l1l11_opy_
        return bstack11lll11l1l1_opy_(self.exception)
def bstack11lll11l1l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll1ll1l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llllll111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1ll11ll_opy_(config, logger):
    try:
        import playwright
        bstack11lll1l11ll_opy_ = playwright.__file__
        bstack11ll1ll111l_opy_ = os.path.split(bstack11lll1l11ll_opy_)
        bstack11ll1l11l11_opy_ = bstack11ll1ll111l_opy_[0] + bstack11_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷᨘࠬ")
        os.environ[bstack11_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ᨙ")] = bstack111111l11_opy_(config)
        with open(bstack11ll1l11l11_opy_, bstack11_opy_ (u"ࠫࡷ࠭ᨚ")) as f:
            bstack1lll1lll1l_opy_ = f.read()
            bstack11ll1lll1l1_opy_ = bstack11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫᨛ")
            bstack11lll11l1ll_opy_ = bstack1lll1lll1l_opy_.find(bstack11ll1lll1l1_opy_)
            if bstack11lll11l1ll_opy_ == -1:
              process = subprocess.Popen(bstack11_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥ᨜"), shell=True, cwd=bstack11ll1ll111l_opy_[0])
              process.wait()
              bstack11lllll1lll_opy_ = bstack11_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧ᨝")
              bstack11llll1ll11_opy_ = bstack11_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧ᨞")
              bstack1l111111111_opy_ = bstack1lll1lll1l_opy_.replace(bstack11lllll1lll_opy_, bstack11llll1ll11_opy_)
              with open(bstack11ll1l11l11_opy_, bstack11_opy_ (u"ࠩࡺࠫ᨟")) as f:
                f.write(bstack1l111111111_opy_)
    except Exception as e:
        logger.error(bstack11l1ll1l1_opy_.format(str(e)))
def bstack11ll111l1_opy_():
  try:
    bstack11lll1l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᨠ"))
    bstack11llllll1l1_opy_ = []
    if os.path.exists(bstack11lll1l1l1l_opy_):
      with open(bstack11lll1l1l1l_opy_) as f:
        bstack11llllll1l1_opy_ = json.load(f)
      os.remove(bstack11lll1l1l1l_opy_)
    return bstack11llllll1l1_opy_
  except:
    pass
  return []
def bstack1llll1lll_opy_(bstack111lll11l_opy_):
  try:
    bstack11llllll1l1_opy_ = []
    bstack11lll1l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᨡ"))
    if os.path.exists(bstack11lll1l1l1l_opy_):
      with open(bstack11lll1l1l1l_opy_) as f:
        bstack11llllll1l1_opy_ = json.load(f)
    bstack11llllll1l1_opy_.append(bstack111lll11l_opy_)
    with open(bstack11lll1l1l1l_opy_, bstack11_opy_ (u"ࠬࡽࠧᨢ")) as f:
        json.dump(bstack11llllll1l1_opy_, f)
  except:
    pass
def bstack11111ll1l_opy_(logger, bstack11llll1llll_opy_ = False):
  try:
    test_name = os.environ.get(bstack11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᨣ"), bstack11_opy_ (u"ࠧࠨᨤ"))
    if test_name == bstack11_opy_ (u"ࠨࠩᨥ"):
        test_name = threading.current_thread().__dict__.get(bstack11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨᨦ"), bstack11_opy_ (u"ࠪࠫᨧ"))
    bstack11llllll111_opy_ = bstack11_opy_ (u"ࠫ࠱ࠦࠧᨨ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11llll1llll_opy_:
        bstack1l1l1111ll_opy_ = os.environ.get(bstack11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᨩ"), bstack11_opy_ (u"࠭࠰ࠨᨪ"))
        bstack1lllll1111_opy_ = {bstack11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᨫ"): test_name, bstack11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᨬ"): bstack11llllll111_opy_, bstack11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᨭ"): bstack1l1l1111ll_opy_}
        bstack11ll1llll1l_opy_ = []
        bstack11ll1llll11_opy_ = os.path.join(tempfile.gettempdir(), bstack11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᨮ"))
        if os.path.exists(bstack11ll1llll11_opy_):
            with open(bstack11ll1llll11_opy_) as f:
                bstack11ll1llll1l_opy_ = json.load(f)
        bstack11ll1llll1l_opy_.append(bstack1lllll1111_opy_)
        with open(bstack11ll1llll11_opy_, bstack11_opy_ (u"ࠫࡼ࠭ᨯ")) as f:
            json.dump(bstack11ll1llll1l_opy_, f)
    else:
        bstack1lllll1111_opy_ = {bstack11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᨰ"): test_name, bstack11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᨱ"): bstack11llllll111_opy_, bstack11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᨲ"): str(multiprocessing.current_process().name)}
        if bstack11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬᨳ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1lllll1111_opy_)
  except Exception as e:
      logger.warn(bstack11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᨴ").format(e))
def bstack1ll1lll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11lll1l1lll_opy_ = []
    bstack1lllll1111_opy_ = {bstack11_opy_ (u"ࠪࡲࡦࡳࡥࠨᨵ"): test_name, bstack11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᨶ"): error_message, bstack11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᨷ"): index}
    bstack11lllll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᨸ"))
    if os.path.exists(bstack11lllll11l1_opy_):
        with open(bstack11lllll11l1_opy_) as f:
            bstack11lll1l1lll_opy_ = json.load(f)
    bstack11lll1l1lll_opy_.append(bstack1lllll1111_opy_)
    with open(bstack11lllll11l1_opy_, bstack11_opy_ (u"ࠧࡸࠩᨹ")) as f:
        json.dump(bstack11lll1l1lll_opy_, f)
  except Exception as e:
    logger.warn(bstack11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᨺ").format(e))
def bstack1l11lll11_opy_(bstack1l1111ll11_opy_, name, logger):
  try:
    bstack1lllll1111_opy_ = {bstack11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᨻ"): name, bstack11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᨼ"): bstack1l1111ll11_opy_, bstack11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᨽ"): str(threading.current_thread()._name)}
    return bstack1lllll1111_opy_
  except Exception as e:
    logger.warn(bstack11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᨾ").format(e))
  return
def bstack11lll1l111l_opy_():
    return platform.system() == bstack11_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧᨿ")
def bstack11ll1111ll_opy_(bstack11ll1ll1lll_opy_, config, logger):
    bstack11lll11ll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11ll1ll1lll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᩀ").format(e))
    return bstack11lll11ll11_opy_
def bstack11llll111l1_opy_(bstack11ll1l1l11l_opy_, bstack1l111111l11_opy_):
    bstack11lll1ll11l_opy_ = version.parse(bstack11ll1l1l11l_opy_)
    bstack11lll1ll1l1_opy_ = version.parse(bstack1l111111l11_opy_)
    if bstack11lll1ll11l_opy_ > bstack11lll1ll1l1_opy_:
        return 1
    elif bstack11lll1ll11l_opy_ < bstack11lll1ll1l1_opy_:
        return -1
    else:
        return 0
def bstack11l111l1l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll1l11lll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11llll1l111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1ll1l111_opy_(options, framework, bstack11llll1l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11_opy_ (u"ࠨࡩࡨࡸࠬᩁ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1llll11111_opy_ = caps.get(bstack11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᩂ"))
    bstack11lll1l1ll1_opy_ = True
    bstack1l11l1l1l_opy_ = os.environ[bstack11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᩃ")]
    if bstack11lll1111l1_opy_(caps.get(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡗ࠴ࡅࠪᩄ"))) or bstack11lll1111l1_opy_(caps.get(bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᩅ"))):
        bstack11lll1l1ll1_opy_ = False
    if bstack11111111_opy_({bstack11_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨᩆ"): bstack11lll1l1ll1_opy_}):
        bstack1llll11111_opy_ = bstack1llll11111_opy_ or {}
        bstack1llll11111_opy_[bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᩇ")] = bstack11llll1l111_opy_(framework)
        bstack1llll11111_opy_[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩈ")] = bstack1ll1111l1l1_opy_()
        bstack1llll11111_opy_[bstack11_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᩉ")] = bstack1l11l1l1l_opy_
        bstack1llll11111_opy_[bstack11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᩊ")] = bstack11llll1l_opy_
        if getattr(options, bstack11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᩋ"), None):
            options.set_capability(bstack11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᩌ"), bstack1llll11111_opy_)
        else:
            options[bstack11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᩍ")] = bstack1llll11111_opy_
    else:
        if getattr(options, bstack11_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᩎ"), None):
            options.set_capability(bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᩏ"), bstack11llll1l111_opy_(framework))
            options.set_capability(bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩐ"), bstack1ll1111l1l1_opy_())
            options.set_capability(bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᩑ"), bstack1l11l1l1l_opy_)
            options.set_capability(bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᩒ"), bstack11llll1l_opy_)
        else:
            options[bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᩓ")] = bstack11llll1l111_opy_(framework)
            options[bstack11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᩔ")] = bstack1ll1111l1l1_opy_()
            options[bstack11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᩕ")] = bstack1l11l1l1l_opy_
            options[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᩖ")] = bstack11llll1l_opy_
    return options
def bstack11ll1ll11l1_opy_(bstack11lll1l11l1_opy_, framework):
    bstack11llll1l_opy_ = bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᩗ"))
    if bstack11lll1l11l1_opy_ and len(bstack11lll1l11l1_opy_.split(bstack11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᩘ"))) > 1:
        ws_url = bstack11lll1l11l1_opy_.split(bstack11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᩙ"))[0]
        if bstack11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᩚ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11llll11l11_opy_ = json.loads(urllib.parse.unquote(bstack11lll1l11l1_opy_.split(bstack11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᩛ"))[1]))
            bstack11llll11l11_opy_ = bstack11llll11l11_opy_ or {}
            bstack1l11l1l1l_opy_ = os.environ[bstack11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᩜ")]
            bstack11llll11l11_opy_[bstack11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᩝ")] = str(framework) + str(__version__)
            bstack11llll11l11_opy_[bstack11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩞ")] = bstack1ll1111l1l1_opy_()
            bstack11llll11l11_opy_[bstack11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᩟")] = bstack1l11l1l1l_opy_
            bstack11llll11l11_opy_[bstack11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴ᩠ࠬ")] = bstack11llll1l_opy_
            bstack11lll1l11l1_opy_ = bstack11lll1l11l1_opy_.split(bstack11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᩡ"))[0] + bstack11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᩢ") + urllib.parse.quote(json.dumps(bstack11llll11l11_opy_))
    return bstack11lll1l11l1_opy_
def bstack11lll11l11_opy_():
    global bstack1l11ll11ll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l11ll11ll_opy_ = BrowserType.connect
    return bstack1l11ll11ll_opy_
def bstack1llll1lll1_opy_(framework_name):
    global bstack1l1ll111ll_opy_
    bstack1l1ll111ll_opy_ = framework_name
    return framework_name
def bstack1l11111ll1_opy_(self, *args, **kwargs):
    global bstack1l11ll11ll_opy_
    try:
        global bstack1l1ll111ll_opy_
        if bstack11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᩣ") in kwargs:
            kwargs[bstack11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᩤ")] = bstack11ll1ll11l1_opy_(
                kwargs.get(bstack11_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᩥ"), None),
                bstack1l1ll111ll_opy_
            )
    except Exception as e:
        logger.error(bstack11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᩦ").format(str(e)))
    return bstack1l11ll11ll_opy_(self, *args, **kwargs)
def bstack11llll11ll1_opy_(bstack11ll1lll1ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l1ll11_opy_(bstack11ll1lll1ll_opy_, bstack11_opy_ (u"ࠦࠧᩧ"))
        if proxies and proxies.get(bstack11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᩨ")):
            parsed_url = urlparse(proxies.get(bstack11_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᩩ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᩪ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᩫ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᩬ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᩭ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11lll111l_opy_(bstack11ll1lll1ll_opy_):
    bstack11lll1llll1_opy_ = {
        bstack1l1111l1l11_opy_[bstack11lll11l11l_opy_]: bstack11ll1lll1ll_opy_[bstack11lll11l11l_opy_]
        for bstack11lll11l11l_opy_ in bstack11ll1lll1ll_opy_
        if bstack11lll11l11l_opy_ in bstack1l1111l1l11_opy_
    }
    bstack11lll1llll1_opy_[bstack11_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᩮ")] = bstack11llll11ll1_opy_(bstack11ll1lll1ll_opy_, bstack1l1l1lll1_opy_.get_property(bstack11_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᩯ")))
    bstack11ll1l1llll_opy_ = [element.lower() for element in bstack1l1111llll1_opy_]
    bstack11lllll111l_opy_(bstack11lll1llll1_opy_, bstack11ll1l1llll_opy_)
    return bstack11lll1llll1_opy_
def bstack11lllll111l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᩰ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11lllll111l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11lllll111l_opy_(item, keys)
def bstack11llll11lll_opy_():
    bstack11lll1l1l11_opy_ = [os.environ.get(bstack11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᩱ")), os.path.join(os.path.expanduser(bstack11_opy_ (u"ࠣࢀࠥᩲ")), bstack11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᩳ")), os.path.join(bstack11_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᩴ"), bstack11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᩵"))]
    for path in bstack11lll1l1l11_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ᩶") + str(path) + bstack11_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ᩷"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦ᩸") + str(path) + bstack11_opy_ (u"ࠣࠩࠥ᩹"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤ᩺") + str(path) + bstack11_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣ᩻"))
            else:
                logger.debug(bstack11_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨ᩼") + str(path) + bstack11_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤ᩽"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ᩾") + str(path) + bstack11_opy_ (u"ࠢࠨ࠰᩿ࠥ"))
            return path
        except Exception as e:
            logger.debug(bstack11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ᪀") + str(e) + bstack11_opy_ (u"ࠤࠥ᪁"))
    logger.debug(bstack11_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ᪂"))
    return None
@measure(event_name=EVENTS.bstack1l11111llll_opy_, stage=STAGE.bstack1lll11111l_opy_)
def bstack1lll1llllll_opy_(binary_path, bstack1llll11ll1l_opy_, bs_config):
    logger.debug(bstack11_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥ᪃").format(binary_path))
    bstack11ll1ll11ll_opy_ = bstack11_opy_ (u"ࠬ࠭᪄")
    bstack11ll1ll1111_opy_ = {
        bstack11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᪅"): __version__,
        bstack11_opy_ (u"ࠢࡰࡵࠥ᪆"): platform.system(),
        bstack11_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤ᪇"): platform.machine(),
        bstack11_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ᪈"): bstack11_opy_ (u"ࠪ࠴ࠬ᪉"),
        bstack11_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥ᪊"): bstack11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᪋")
    }
    try:
        if binary_path:
            bstack11ll1ll1111_opy_[bstack11_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᪌")] = subprocess.check_output([binary_path, bstack11_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᪍")]).strip().decode(bstack11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᪎"))
        response = requests.request(
            bstack11_opy_ (u"ࠩࡊࡉ࡙࠭᪏"),
            url=bstack11l1l1ll1l_opy_(bstack1l1111lll1l_opy_),
            headers=None,
            auth=(bs_config[bstack11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᪐")], bs_config[bstack11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᪑")]),
            json=None,
            params=bstack11ll1ll1111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11_opy_ (u"ࠬࡻࡲ࡭ࠩ᪒") in data.keys() and bstack11_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᪓") in data.keys():
            logger.debug(bstack11_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣ᪔").format(bstack11ll1ll1111_opy_[bstack11_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᪕")]))
            bstack11ll1l111l1_opy_ = bstack11ll1l1l111_opy_(data[bstack11_opy_ (u"ࠩࡸࡶࡱ࠭᪖")], bstack1llll11ll1l_opy_)
            bstack11ll1ll11ll_opy_ = os.path.join(bstack1llll11ll1l_opy_, bstack11ll1l111l1_opy_)
            os.chmod(bstack11ll1ll11ll_opy_, 0o777) # bstack11ll1ll1ll1_opy_ permission
            return bstack11ll1ll11ll_opy_
    except Exception as e:
        logger.debug(bstack11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡗࡉࡑࠠࡼࡿࠥ᪗").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack1l1111ll11l_opy_, stage=STAGE.bstack1lll11111l_opy_)
def bstack11ll1l1l111_opy_(bstack11llllll11l_opy_, bstack11lll1ll1ll_opy_):
    logger.debug(bstack11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰ࠾ࠥࠨ᪘") + str(bstack11llllll11l_opy_) + bstack11_opy_ (u"ࠧࠨ᪙"))
    zip_path = os.path.join(bstack11lll1ll1ll_opy_, bstack11_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡢࡪ࡮ࡲࡥ࠯ࡼ࡬ࡴࠧ᪚"))
    bstack11ll1l111l1_opy_ = bstack11_opy_ (u"ࠧࠨ᪛")
    with requests.get(bstack11llllll11l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11_opy_ (u"ࠣࡹࡥࠦ᪜")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠦ᪝"))
    with zipfile.ZipFile(zip_path, bstack11_opy_ (u"ࠪࡶࠬ᪞")) as zip_ref:
        bstack11ll1l1ll11_opy_ = zip_ref.namelist()
        if len(bstack11ll1l1ll11_opy_) > 0:
            bstack11ll1l111l1_opy_ = bstack11ll1l1ll11_opy_[0] # bstack11lll1l1111_opy_ bstack1l1111l1111_opy_ will be bstack11llll1ll1l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11lll1ll1ll_opy_)
        logger.debug(bstack11_opy_ (u"ࠦࡋ࡯࡬ࡦࡵࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥࡺ࡯ࠡࠩࠥ᪟") + str(bstack11lll1ll1ll_opy_) + bstack11_opy_ (u"ࠧ࠭ࠢ᪠"))
    os.remove(zip_path)
    return bstack11ll1l111l1_opy_
def get_cli_dir():
    bstack11llll11111_opy_ = bstack11llll11lll_opy_()
    if bstack11llll11111_opy_:
        bstack1llll11ll1l_opy_ = os.path.join(bstack11llll11111_opy_, bstack11_opy_ (u"ࠨࡣ࡭࡫ࠥ᪡"))
        if not os.path.exists(bstack1llll11ll1l_opy_):
            os.makedirs(bstack1llll11ll1l_opy_, mode=0o777, exist_ok=True)
        return bstack1llll11ll1l_opy_
    else:
        raise FileNotFoundError(bstack11_opy_ (u"ࠢࡏࡱࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠥ᪢"))
def bstack11111l1l11_opy_(bstack1llll11ll1l_opy_):
    bstack11_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡩ࡯ࠢࡤࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠥࠦࠧ᪣")
    bstack11llll1l11l_opy_ = [
        os.path.join(bstack1llll11ll1l_opy_, f)
        for f in os.listdir(bstack1llll11ll1l_opy_)
        if os.path.isfile(os.path.join(bstack1llll11ll1l_opy_, f)) and f.startswith(bstack11_opy_ (u"ࠤࡥ࡭ࡳࡧࡲࡺ࠯ࠥ᪤"))
    ]
    if len(bstack11llll1l11l_opy_) > 0:
        return max(bstack11llll1l11l_opy_, key=os.path.getmtime) # get bstack11lll111l1l_opy_ binary
    return bstack11_opy_ (u"ࠥࠦ᪥")