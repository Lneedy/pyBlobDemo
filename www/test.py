'''
测试数据库存储数据demo

>> mysql -u root -p < schema.sql
'''


import orm
from models import User, Blog, Comment
import asyncio

async def test (loop):
    await orm.create_pool(loop, user='www-data', password='www-data', db='awesome')
    # u = User(id='2', name='Test1', email='test1@example.com', passwd='1234567890', image='about:blank')
    # await u.save()
    u = await User.findAll()
    print('sql save success! %s' % u)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    print('Test finished')
    loop.close()