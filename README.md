
运行启动脚本 ipproxytool.py 也可以分别运行抓取，验证，服务器接口脚本，运行方法参考项目说明

```
$ python ipproxytool.py
```

<br>

#### 爬虫存放于rental文件夹
1，在spiders文件夹追加爬虫,在run_rental.py引入即可<br>
2,setting.py 里面配置爬虫<br>

单独运行 爬虫 run_rental.py

```
$ python run_rental.py
```



## 参考
* [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)


## 项目更新
-----------------------------2017-7-21----------------------------<br>
原项目 已经不支持2.7 由于机器的原因暂时没法支持3 所以改写了不兼容部分<br>
加入了爬去目标网站模块<br>
加入自动切换代理ip 自动切换头信息 （采用ip连续出错10次即推出）<br>
<br>






