import unittest
import scraper 

class test_scraper(unittest.TestCase):
    def test_urls_len(self):
        test_cases = [1, 10, 100]
        for tc in test_cases:
            urls = scraper.get_img_urls(tc, 'cats')
            self.assertEqual(len(urls), tc)

if __name__ == '__main__':
    unittest.main()
