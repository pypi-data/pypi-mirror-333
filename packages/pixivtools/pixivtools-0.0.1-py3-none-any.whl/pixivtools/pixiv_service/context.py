import pixiv_utils.log
import pixiv_api
from pixiv_cfg import PixivConfig
from .model import new_session


class PixivContext:
    def __init__(self, cfg: PixivConfig):
        self.api = pixiv_api.new_pixiv_api(cfg.api)
        self.sql = new_session(cfg.crawler.sql_url)
        self.img_dir = cfg.crawler.img_dir
        self.log = pixiv_utils.log.PixivLog(cfg.log_file)


def new_context(cfg: PixivConfig) -> PixivContext:
    return PixivContext(cfg)
