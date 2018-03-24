# DX CMDB

## 部署
1.将相关配置选项修改成真实环境的值<br/>
vi settings.py<br/>

2.构建Docker镜像<br/>
cd projectDir<br/>
docker build -t dx/cmdb  .<br/>

3.运行容器<br/>
docker run -d --name cmdb -p 8000:8000 dx/cmdb
