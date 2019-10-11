# Python Blob Demo Project
---
A python3 webapp tutorial.
---

## 目录结构

```shell
awesome-python3-webapp/  <-- 根目录
|
+- backup/               <-- 备份目录
|
+- conf/                 <-- 配置文件
|
+- dist/                 <-- 打包目录
|
+- www/                  <-- Web目录，存放.py文件
|  |
|  +- static/            <-- 存放静态文件
|  |
|  +- templates/         <-- 存放模板文件
|
+- ios/                  <-- 存放iOS App工程
|
+- LICENSE               <-- 代码LICENSE
```

### 面向对象基础知识
```text
__init__: 构造函数, 在生成对象时调用
__del__: 析构函数, 释放对象时使用
__repr__: 打印, 转换
__setitem__: 按照索引赋值
__getitem__: 按照索引取值
__len__: 获取长度
__cmp__: 比较运算
__call__: 函数调用
__add__: 加运算
__sub__: 减运算
__mul__: 乘运算
__truediv__: 除运算
__mod__: 求余运算
__pow__: 乘方运算
__str__: 返回一个对象描述信息, print打印实例化对象时调用
__new__: 被实例化时调用, 先于`init`调用, 并且第一个参数为当前类


__class__: 类名
__private_attrs: 类的私有属性(写法)
__private_methods: 类的私有方法(写法)


```
