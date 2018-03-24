# DX CMDB

## 部署
1.将相关配置选项修改成真实环境的值
vi settings.py

2.构建Docker镜像
cd projectDir
docker build -t dx/cmdb .

3.运行容器
docker run -d --name cmdb -p 8000:8000 dx/cmdb
