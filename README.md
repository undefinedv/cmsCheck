# cmsCheck
多线程的cms文件确认工具。
Multi-thread cms file check tools.
主要目的在于安全渗透人员在进行安全测试时手上有目标相似但不完全一样的代码时，核对服务器上文件以方便精确白盒审计的范围所用。
有任何bug欢迎联系。
邮箱mathyouqu@gmail.com

## 关于反爬
当网站有反爬判断的时候，我们可以自定义check函数，通过修改header或者请求方式进行修正。

## 对于应对不存在的文件不返回404的网站
可自定义mycheck函数设计判断文件是否存在的方法。


