"""
@Author: kang.yang
@Date: 2023/11/16 17:47
"""
import kytest
from kytest.ios import TestCase

from pages.ios_page import DemoPage


@kytest.module('测试demo')
class TestIosDemo(TestCase):

    def start(self):
        self.page = DemoPage(self.driver)

    @kytest.title('进入设置页')
    def test_go_setting(self):
        self.page.adBtn.click_exists()
        self.page.myTab.click()
        self.page.setBtn.click()
        self.page.about.assert_exists()

