# The-chat-room

使用Python3编写的聊天室

功能简介:

- 群聊功能: 确保端口打开即可多台电脑聊天
- 私聊功能: 给指定用户发消息
- 查看在线用户功能: 可以查看当前在线用户
- 上传下载功能: 用户可以从文件服务器上传下载文件
- 发送表情和图片

更新:

- 优化了代码，封装了三个server
- 界面全部英文化
- 解决了无数个bug：
  - pictureServer和fileServer不能同时运行的问题
  - 截屏按钮不能正常工作的问题
  - 同用户名登录，仍显示不能自己与自己聊天的问题
  - 等等
- 新增功能：
  - 类似QQ小冰的AI聊天机器人
    - 群聊 @Robot
    - 私聊
  - 私聊点对点视频、音频聊天
    - 支持分辨率调节
    - 支持IPv4、IPv6
    - 可以选择是否在桌面上显示自己
- 待完善：
  - 视频聊天需要双方确认
  - 暂时通过重命名后加_2解决问题，不可靠
  - UI美化

部署:

- python3.7
- pip install -r pip-package.txt
- pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl [参考](https://blog.csdn.net/a506681571/article/details/85201279)

演示:

![image](https://raw.githubusercontent.com/11ze/The-chat-room/master/images/user1.png)
![image](https://raw.githubusercontent.com/11ze/The-chat-room/master/images/user2.png)
