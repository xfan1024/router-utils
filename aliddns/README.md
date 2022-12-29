# aliddns

一个基于python3编写的阿里云动态解析域名的工具

## 使用方法

* 编写配置文件

  | 参数                            | 介绍                                                         |
  | ------------------------------- | ------------------------------------------------------------ |
  | `AccessKeyId`,`AccessKeySecret` | 参考[创建AccessKey](https://help.aliyun.com/document_detail/116401.html?spm=5176.21213303.J_6704733920.7.fd0053c9YgctEe)。 |
  | `RecordId`                      | 前往[域名解析](https://dns.console.aliyun.com/#/dns/domainList)创建一条记录，然后前往[DescribeDomainRecords API调试](https://next.api.aliyun.com/api/Alidns/2015-01-09/DescribeDomainRecords)在线调用接口，获取找到匹配的记录，获得对应的`RecordId`。 |
  | `RR`                            | 一般指三级域名。                                             |
  | `Type`                          | `A`: 用于ipv4，`AAAA`: 用于ipv6。                            |
  | `Interface`                     | 要获取ipv4或ipv6的接口名。                                   |
  | `Delay`                         | 每次查询接口IP地址是否改变的间隔时间。默认为10。             |
  | `Region`                        | 阿里云服务地区ID，如`cn-hangzhou`,`cn-beijing`等。建议不填。 |

* 运行`python3 aliddns.py /path/to/aliddns.conf`

## 安装方法

### OpenWRT

```shell
opkg install python3-pip python3-cryptography python3-jmespath
python3 -m pip install aliyun-python-sdk-alidns
```

