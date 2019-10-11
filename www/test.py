'''
测试数据库存储数据demo

>> mysql -u root -p < schema.sql
'''


import orm
from model import User, Blog, Comment
import asyncio

async def test (loop):
    await orm.create_pool(loop, user='www-data', password='www-data', db='awesome')
    u = User(id='1', name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    await u.save()
    print('sql save success!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    print('Test finished')
    loop.close()