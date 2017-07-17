# hackerweb

> 用python 2.7实现的web框架建立的功能平台，基于原作者进行二次开发
> web框架是flask  前端框架是amazeUI

## 安装
`git clone xxx.git`

`pip install flask`

`pip install requests`  

`pip install MySQLdb  `

创建数据库,任意数据库名称，创建表，任意表名
将sql文件导入表中,数据库文件地址 [1]

[usage]: python `main.py `
> 默认使用0.0.0.0,端口5000,如需更改请修改main.py中app.run的host, port

乌云数据库文件安装 链接: http://pan.baidu.com/s/1hrKYy8W 密码: yrrr [1]

## 更新

- 12.7 更新 加入乌云漏洞库忽略漏洞查询
- 11.22 更新 集成了乌云漏洞查询
- 11.7 更新 加入了在线社工库 调用的接口~
- 10.25 更新 加入了社会工程学密码生成和whois查询
- 10.21 更新 加入了CMS在线识别
- 基于作者进行二次开发，修复了查询乌云导致mysql mysql server has gone away问题
- 修复cms识别导致脚本报错问题
- 修复socket setdefaulttimeout导致脚本不能正常运行问题
- 增加googlehacking查询功能(备份查找/目录发现/数据库文件/日志/配置文件/登录页面/数据库报错/phpinfo/文档发现)
- 增加手机号归属地验证及是否为恶意手机号码 //TODO

## 在线演示

http://so.javasec.cn