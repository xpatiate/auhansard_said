import unittest
import redis
import datetime

class RedisTest(unittest.TestCase):
    def test_redis_is_running(self):
        r = redis.StrictRedis()
        self.assertTrue(r)
        datestr = r.get('__date').decode()
        lastentry = datetime.datetime.strptime(datestr,'%Y-%m-%d').date()
        self.assertTrue(lastentry <= datetime.date.today())

        rkeys = r.keys('r*')
        self.assertTrue(len(rkeys) > 7000)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
