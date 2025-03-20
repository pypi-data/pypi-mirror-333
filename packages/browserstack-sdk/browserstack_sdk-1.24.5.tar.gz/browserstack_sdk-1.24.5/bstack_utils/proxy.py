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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1llll111_opy_
bstack1ll11111ll_opy_ = Config.bstack111lll11_opy_()
def bstack11l11l11l11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11l11l11ll1_opy_(bstack11l11l1l111_opy_, bstack11l11l11l1l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11l11l1l111_opy_):
        with open(bstack11l11l1l111_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11l11l11l11_opy_(bstack11l11l1l111_opy_):
        pac = get_pac(url=bstack11l11l1l111_opy_)
    else:
        raise Exception(bstack1l11l_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ᯪ").format(bstack11l11l1l111_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11l_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣᯫ"), 80))
        bstack11l11l11lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11l11l11lll_opy_ = bstack1l11l_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩᯬ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11l11l11l1l_opy_, bstack11l11l11lll_opy_)
    return proxy_url
def bstack1ll11l1ll_opy_(config):
    return bstack1l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᯭ") in config or bstack1l11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᯮ") in config
def bstack11lll11lll_opy_(config):
    if not bstack1ll11l1ll_opy_(config):
        return
    if config.get(bstack1l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᯯ")):
        return config.get(bstack1l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᯰ"))
    if config.get(bstack1l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᯱ")):
        return config.get(bstack1l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼ᯲ࠫ"))
def bstack1l11ll11l_opy_(config, bstack11l11l11l1l_opy_):
    proxy = bstack11lll11lll_opy_(config)
    proxies = {}
    if config.get(bstack1l11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼ᯳ࠫ")) or config.get(bstack1l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᯴")):
        if proxy.endswith(bstack1l11l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ᯵")):
            proxies = bstack1lll1111l_opy_(proxy, bstack11l11l11l1l_opy_)
        else:
            proxies = {
                bstack1l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ᯶"): proxy
            }
    bstack1ll11111ll_opy_.bstack1ll1l11l11_opy_(bstack1l11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ᯷"), proxies)
    return proxies
def bstack1lll1111l_opy_(bstack11l11l1l111_opy_, bstack11l11l11l1l_opy_):
    proxies = {}
    global bstack11l11l111ll_opy_
    if bstack1l11l_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩ᯸") in globals():
        return bstack11l11l111ll_opy_
    try:
        proxy = bstack11l11l11ll1_opy_(bstack11l11l1l111_opy_, bstack11l11l11l1l_opy_)
        if bstack1l11l_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢ᯹") in proxy:
            proxies = {}
        elif bstack1l11l_opy_ (u"ࠣࡊࡗࡘࡕࠨ᯺") in proxy or bstack1l11l_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣ᯻") in proxy or bstack1l11l_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤ᯼") in proxy:
            bstack11l11l1l11l_opy_ = proxy.split(bstack1l11l_opy_ (u"ࠦࠥࠨ᯽"))
            if bstack1l11l_opy_ (u"ࠧࡀ࠯࠰ࠤ᯾") in bstack1l11l_opy_ (u"ࠨࠢ᯿").join(bstack11l11l1l11l_opy_[1:]):
                proxies = {
                    bstack1l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᰀ"): bstack1l11l_opy_ (u"ࠣࠤᰁ").join(bstack11l11l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᰂ"): str(bstack11l11l1l11l_opy_[0]).lower() + bstack1l11l_opy_ (u"ࠥ࠾࠴࠵ࠢᰃ") + bstack1l11l_opy_ (u"ࠦࠧᰄ").join(bstack11l11l1l11l_opy_[1:])
                }
        elif bstack1l11l_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᰅ") in proxy:
            bstack11l11l1l11l_opy_ = proxy.split(bstack1l11l_opy_ (u"ࠨࠠࠣᰆ"))
            if bstack1l11l_opy_ (u"ࠢ࠻࠱࠲ࠦᰇ") in bstack1l11l_opy_ (u"ࠣࠤᰈ").join(bstack11l11l1l11l_opy_[1:]):
                proxies = {
                    bstack1l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᰉ"): bstack1l11l_opy_ (u"ࠥࠦᰊ").join(bstack11l11l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᰋ"): bstack1l11l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᰌ") + bstack1l11l_opy_ (u"ࠨࠢᰍ").join(bstack11l11l1l11l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᰎ"): proxy
            }
    except Exception as e:
        print(bstack1l11l_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᰏ"), bstack11l1llll111_opy_.format(bstack11l11l1l111_opy_, str(e)))
    bstack11l11l111ll_opy_ = proxies
    return proxies