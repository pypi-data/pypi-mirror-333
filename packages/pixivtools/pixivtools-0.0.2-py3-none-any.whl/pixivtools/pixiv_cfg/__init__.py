import pathlib
from typing import NamedTuple


class ApiMetaArgument(NamedTuple):
    phpsessid: str
    proxy: str


class CrawlerConfig(NamedTuple):
    img_dir: pathlib.Path
    sql_url: str


class PixivConfig(NamedTuple):
    api: ApiMetaArgument
    crawler: CrawlerConfig
    log_file: pathlib.Path


def _load_api_config(api_obj: dict) -> ApiMetaArgument:
    return ApiMetaArgument(**api_obj)


def _load_crawler_config(crawler_obj: dict) -> CrawlerConfig:
    img_file_dir = pathlib.Path() / crawler_obj["img_dir"]
    if not img_file_dir.exists():
        img_file_dir.mkdir(parents=True)

    crawler_obj["img_dir"] = img_file_dir
    return CrawlerConfig(**crawler_obj)


def _load_config(obj: dict) -> PixivConfig:
    log_file_path = pathlib.Path() / obj["log_file"]
    log_file_dir = log_file_path.parent
    if not log_file_dir.exists():
        log_file_dir.mkdir(parents=True)

    return PixivConfig(
        api=_load_api_config(obj["api"]),
        crawler=_load_crawler_config(obj["crawler"]),
        log_file=log_file_path
    )


g_cfg = None


def get_pixiv_config(filename: str = "config.yaml") -> PixivConfig:
    global g_cfg
    if g_cfg:
        return g_cfg

    import yaml
    cfg_path = pathlib.Path() / filename
    if not cfg_path.exists():
        raise FileNotFoundError(f"文件{cfg_path.absolute}不存在")
    with open(cfg_path, "r") as f:
        obj = yaml.safe_load(f)

    g_cfg = _load_config(obj)
    return g_cfg
