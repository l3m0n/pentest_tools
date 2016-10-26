# encoding: utf-8

# 结果回调邮箱
callback_mail = ''

# 并行扫描的WVS进程数
queue_num = 2

# web接口监听的端口，一般不需改动
web_port = 8082
expire_url = 'http://127.0.0.1:%s/expire' % str(web_port)

# wvs安装位置
wvs_location = 'C:/"Program Files (x86)"/Acunetix/"Web Vulnerability Scanner 10"/'

# 扫描结果存储位置
wvs_save_dir = 'C:/wvs_result/'

# WVS扫描语句，具体可在http://www.acunetix.com/blog/docs/acunetix-wvs-cli-operation/ 查询
wvs_scan_sentence = '/Scan %s /Profile default /ExportXML /SaveFolder %s  --RestrictToBaseFolder=true'


# WVS结果过滤
filter = {
    "color_white_list": ["orange", "red"],  # green,blue,orange,red四种级别
    "bug_black_list": [						# 漏洞黑名单，过滤掉一些危害等级高，但没什么卵用的洞
    	"User credentials are sent in clear text"
    ]
}


# 邮箱配置：
mail_conf = {
    "username": "test",
    "password": "test",
    "smtp_server": 'smtp.163.com',
    "mail_address": 'test@163.com'
}