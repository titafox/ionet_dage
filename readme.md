
# 大哥们的 ionet 挂机监控

这是专门给我大哥们安排的一个监控 io.net上机器是否挂了整套前后端。
我的每个大哥都有一个大哥号，把大哥号填写进去后，就能简单判断是谁的机器。


## 前端
前端是一个 chrome 的插件，把所有机器状态都抛到后端，方便批量运维。
插件会检测你是否停留在https://cloud.io.net/worker/devices这个页面，如果是，那么每 30 分钟刷新一次页面。
如果出现 error，直接刷新，越是 error 越往死里刷新直到刷成功为止。
代码放在了src文件夹，修改：content.js中 68 行，为你自己的域名。    
```javascript
fetch('https://www.你的域名.com/ionet')
```


![dage.png](dage.png)

### 前端安装方法
下载src 文件夹中的文件，打开chrome浏览器，输入 chrome://extensions/，打开开发者模式，点击加载已解压的扩展程序，选择src文件夹即可。


## 后端docker 构建与部署
后端我的目的是跟运维系统对接，一旦遇到大哥们的机器挂了，就去删 docker容器和镜像。不断删不断重置，直下一次大哥的灯绿了才罢休。


构建
```bash

docker build -t dageio .
```

运行下面的命令，就可以启动一个容器，监听 8000 端口。
```bash
docker run -d --name dageio -p 8000:8000 dageio
```

## nginx 配置

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

## 最后希望大哥们喜欢。
