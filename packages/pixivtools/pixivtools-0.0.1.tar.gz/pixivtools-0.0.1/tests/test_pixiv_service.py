import unittest
import pixivtools.pixiv_service as pixiv_service
import pixivtools.pixiv_cfg as pixiv_cfg


TEST_ARTWORK_IDS = [128168801]  # 使用有效的artwork_id进行测试
TEST_USER_IDS = [85966]         # 使用有效的user_id进行测试
TEST_PIXIVISION_AIDS = [10176]  # 使用有效的aid进行测试
TEST_TAGS = ["東方Project"]     # 使用有效的tag进行测试


class TestPixivService(unittest.TestCase):
    def setUp(self):
        self.service = pixiv_service.new_pixiv_service(pixiv_cfg.get_pixiv_config())
        self.crawler = self.service.crawler()

    def test_get_artwork_info(self):
        for artwork_id in TEST_ARTWORK_IDS:
            self.crawler.get_by_artwork_id(artwork_id)


if __name__ == '__main__':
    unittest.main()
