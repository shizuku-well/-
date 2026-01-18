# HYBBS 论坛系统 API 完整文档

## 一、API 路由规则

### 1.1 路由格式
- **基本格式**: `/?s=Action/Method` 或 `Action/Method.html`
- **URL分隔符**: `/` (url_explode)
- **URL后缀**: `.html` (url_suffix，可配置)
- **伪静态开关**: `REWRITE` (config.php中配置)

### 1.2 URL重写配置
```php
'HY_URL'=>array(
    'action'=>array(
        'thread'=>'t',      // thread -> t
        'forum'=>'f',       // forum -> f
        'my'=>'u',          // my -> u
    ),
    'method'=>array(
        'thread'=>array(
            'del'=>'d'      // thread/del -> t/d
        )
    )
)
```

---

## 二、核心API接口定义

### 2.1 **Api控制器** (Action/Api.php)

主要提供JSON格式的API接口，适合移动端和第三方调用。

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/api/index` | GET/POST | 获取首页帖子列表 | `pageid` - 页码<br>`type` - New(最新)/Btime(最新回复) |
| `/api/article` | GET | 获取帖子详情 | `tid` - 帖子ID<br>`pageid` - 评论页码<br>`order` - 排序(desc/asc) |
| `/api/forum` | GET | 获取论坛分类列表 | `fgid` - 论坛分组ID(可选) |
| `/api/forumlist` | GET | 获取板块帖子列表 | `fid` - 板块ID<br>`pageid` - 页码<br>`type` - 类型(new/daihui/remen/jing)<br>`size` - 每页数量 |
| `/api/searchforum` | GET | 搜索论坛板块 | `name` - 搜索关键词<br>`pageid` - 页码 |
| `/api/user` | GET | 获取用户信息 | `user` - 用户名<br>`type` - 类型(index/thread/post/op/file/log/message)<br>`pageid` - 页码 |
| `/api/login` | POST | 用户登录 | `user` - 用户名<br>`pass` - 密码 |
| `/api/thread_add` | POST | 发布主题 | `forum` - 板块ID<br>`title` - 标题<br>`content` - 内容<br>`tgold` - 付费金币<br>`thide` - 是否隐藏(1/0)<br>`fileid` - 附件ID |
| `/api/thread_edit` | POST | 编辑主题/帖子 | `id` - 帖子/主题ID<br>`content` - 内容<br>`title` - 标题(主题时)<br>`fid` - 板块ID(主题时)<br>`fileid` - 附件ID |
| `/api/thread_editpull` | GET | 获取编辑数据 | `id` - 帖子/主题ID |
| `/api/Post` | POST | 发表评论 | `id` - 主题ID<br>`content` - 评论内容<br>`pid` - 回复的评论ID(可选) |
| `/api/post_post` | POST | 发表子评论 | `pid` - 父评论ID<br>`content` - 内容 |
| `/api/vote` | POST | 投票 | `id` - 主题/评论ID<br>`type` - thread1(thread2)/post1(post2) |
| `/api/del` | POST | 删除评论 | `id` - 评论ID |
| `/api/phb` | GET | 排行榜 | `type` - gold(金币排行)/thread(发帖排行) |
| `/api/ajax_user_switch` | POST | 禁言用户查询/切换 | `type` - login/post/cxzt<br>`uid` - 用户ID |

### 2.2 **Ajax控制器** (Action/Ajax.php)

提供Ajax异步接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/ajax/userjson` | GET | 获取用户JSON信息 | `uid` - 用户ID |
| `/ajax/useravatar` | GET | 获取用户头像 | `user` - 用户名 |
| `/ajax/Downfile` | GET | 下载附件 | `id` - 附件fileid |
| `/ajax/buyfile` | POST | 购买附件 | `id` - 附件fileid |
| `/ajax/buythread` | POST | 购买付费主题 | `id` - 主题tid |
| `/ajax/clear_mess` | POST | 清空消息提醒 | - |

### 2.3 **Thread控制器** (Action/Thread.php)

帖子相关页面接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/thread/{tid}` | GET | 查看帖子详情页 | `tid` - 主题ID<br>GET参数: `pageid`, `order` |
| `/thread/{tid}/post` | POST/AJAX | 回复帖子 | POST: `content`, `pid` |
| `/thread/{tid}/del` | POST | 删除帖子 | - |
| `/thread/{tid}/top` | POST | 置顶/取消置顶 | - |
| `/thread/{tid}/set_state` | POST | 设置帖子状态 | - |
| `/thread/{tid}/digest` | POST | 加精/取消加精 | - |
| `/thread/{tid}/star` | POST | 收藏/取消收藏 | - |

### 2.4 **Post控制器** (Action/Post.php)

发帖相关接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/post/index` | GET/POST | 发表主题页面/提交 | POST参数见 api/thread_add |
| `/post/uploadfile` | POST | 上传附件 | 支持文件上传 |
| `/post/upload` | POST | 上传图片 | 支持图片上传 |
| `/post/uploadvideo` | POST | 上传视频 | 支持视频上传 |
| `/post/uploadaudio` | POST | 上传音频 | 支持音频上传 |
| `/post/edit` | GET/POST | 编辑帖子 | GET参数: `id` |
| `/post/vote` | POST | 投票 | 见 api/vote |
| `/post/del` | POST | 删除评论 | 见 api/del |

### 2.5 **User控制器** (Action/User.php)

用户相关接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/user/mess` | GET | 查看消息(跳转) | `id` - 消息ID |
| `/user/Edit` | POST | 编辑用户信息 | `gn` - 操作类型(ps/pass/edit_username) |
| `/user/repass` | POST | 找回密码 | `email`, `code`, `pass1`, `pass2` |
| `/user/recode2` | POST | 发送找回密码验证码 | `email`, `code`, `pass1`, `pass2` |
| `/user/recode` | POST | 生成找回密码验证码 | `email` |
| `/user/Login` | POST | 用户登录 | `user`, `pass`, `auto` |
| `/user/Add` | POST | 用户注册 | `user`, `pass1`, `pass2`, `email` |
| `/user/ava` | POST | 上传头像 | 文件上传 |
| `/user/out` | GET | 用户退出 | - |
| `/user/isuser` | GET | 检查用户是否存在 | `user` |
| `/user/isemail` | GET | 检查邮箱是否存在 | `email` |

### 2.6 **My控制器** (Action/My.php)

用户中心接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/u/{username}` | GET | 用户中心首页 | `username` - 用户名<br>`pageid` - 页码(某些功能) |
| `/u/{username}/thread` | GET | 用户主题列表 | - |
| `/u/{username}/post` | GET | 用户评论列表 | - |
| `/u/{username}/mess` | GET | 用户消息列表 | `message` - 类型<br>`uid` - 聊天用户ID |
| `/u/{username}/op` | GET/POST | 用户配置 | `ation` - 操作类型(pass/ps) |
| `/u/{username}/file` | GET | 用户文件列表 | - |
| `/u/{username}/log` | GET | 用户金币积分日志 | - |
| `/u/{username}/message` | GET | 查看消息 | `id` - 消息ID |
| `/u/{username}/index` | GET | 用户首页 | - |
| `/u/{username}/set_state` | POST | 设置状态 | `state` - 状态内容 |

### 2.7 **Forum控制器** (Action/Forum.php)

论坛板块接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/forum/{fid}` | GET | 板块首页 | `fid` - 板块ID<br>GET参数: `pageid`, `type` |
| `/forum/{fid}/thread` | GET | 板块帖子列表 | `pageid`, `type` |

### 2.8 **Friend控制器** (Action/Friend.php)

好友/私信系统

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/friend/friend_state` | GET/POST | 好友状态 | `uid` - 对方UID |
| `/friend/send_chat` | POST | 发送聊天 | `uid` - 接收者<br>`content` - 内容 |
| `/friend/friend_list` | GET | 好友列表 | `type` - 类型(index/follow/fans) |
| `/friend/get_old_chat` | POST | 获取历史聊天 | `uid` - 对方UID<br>`pid` - 最后消息ID |
| `/friend/pm` | POST | 发送私信 | `user`, `content` |
| `/friend/user_info` | GET | 用户信息 | `uid` |

### 2.9 **Search控制器** (Action/Search.php)

搜索功能

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/search` | GET | 搜索页面 | `key` - 关键词<br>`pageid` - 页码<br>`type` - 类型(thread/post/user) |

### 2.10 **Index控制器** (Action/Index.php)

首页接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/` 或 `/index` | GET | 首页 | `pageid` - 页码<br>`type` - New/Btime |

### 2.11 **Admin控制器** (Action/Admin.php)

后台管理接口(需要管理员权限)

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/admin` | GET/POST | 后台首页 | - |
| `/admin/login` | POST | 后台登录 | `user`, `pass` |
| `/admin/out` | GET | 后台退出 | - |
| `/admin/forum_group` | GET/POST | 论坛分组管理 | - |
| `/admin/forum` | GET/POST | 板块管理 | - |
| `/admin/user` | GET/POST | 用户管理 | - |
| `/admin/thread` | GET/POST | 主题管理 | - |
| `/admin/post` | GET/POST | 评论管理 | - |
| `/admin/post_post` | GET/POST | 子评论管理 | - |
| `/admin/view` | GET/POST | 视图管理 | - |
| `/admin/op` | GET/POST | 操作管理 | - |
| `/admin/code` | GET/POST | 代码管理 | - |

---

## 三、特殊API接口

### 3.1 数据清理接口

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/api/cache_data` | POST | 清理数据缓存 | - |
| `/api/lqbc` | POST | 领取补偿奖励 | - |
| `/api/ds` | POST | 打赏接口 | `id` - 目标ID<br>`gold` - 打赏金币 |
| `/api/dhyh` | POST | 兑换用户组 | `goId` - 商品ID |
| `/api/zmlyh` | POST | 招募老用户发送邮箱 | - |
| `/api/zhyhm` | POST | 邮箱获取用户名 | `email` - 邮箱 |
| `/api/phb` | GET | 排行榜 | `type` - gold/thread |

### 3.2 外部数据接口

这些是项目中的外部数据配置文件（JSON格式）：

| 文件 | 功能 |
|------|------|
| `dh.php` | 兑换商品配置 - 商品列表、兑换接口URL |
| `gg.php` | 广告配置 - 广告图片、跳转链接 |
| `zanz.php` | 打赏榜配置 - 打赏排行榜数据 |
| `Updatesv5.php` | APP更新配置 - 版本更新信息、公告内容 |

### 3.2 密码找回流程
1. `/user/recode` - 生成验证码并发送邮件
   - 参数: `email` (POST)
   - 返回: 发送状态

2. `/user/repass` - 验证并重置密码
   - 参数: `email`, `code`, `pass1`, `pass2` (POST)
   - 返回: 修改状态

---

## 四、Model层数据接口

### 4.1 Thread Model
- `read($tid)` - 读取主题
- `get_thread_list($pageid, $size, $order)` - 获取主题列表
- `get_top_thread()` - 获取置顶主题
- `get_user_thread_list($uid, $pageid, $size)` - 获取用户主题
- `format(&$thread_list)` - 格式化主题数据

### 4.2 Post Model
- `read($pid)` - 读取评论
- `insert($data)` - 插入评论
- `update($data, $where)` - 更新评论
- `del($pid)` - 删除评论

### 4.3 User Model
- `read($uid)` - 读取用户
- `user_to_uid($username)` - 用户名转UID
- `email_read($email)` - 邮箱读取用户
- `is_user($username)` - 检查用户是否存在
- `is_email($email)` - 检查邮箱是否存在
- `add_user($user, $pass, $email)` - 添加用户
- `update_int($uid, $field, $op, $value=1)` - 字段增减
- `get_gold($uid)` - 获取用户金币

### 4.4 Forum Model
- `read($fid)` - 读取板块
- `read_all()` - 读取所有板块
- `update_int($fid, $field)` - 更新板块统计

### 4.5 File Model
- `read($fileid)` - 读取文件
- `is_comp($fileid, $uid)` - 检查文件归属
- `get_name($fileid)` - 获取文件名

---

## 五、插件API钩子

### 5.1 常用Hook位置

| Hook名称 | 位置 | 说明 |
|---------|------|------|
| `a_index_index_1` | Index/Index | 首页加载前 |
| `a_thread_empty_1` | Thread/_no | 帖子加载前 |
| `a_post_index_1` | Post/Index | 发帖加载前 |
| `a_user_login_1` | User/Login | 登录前 |
| `a_my_empty_1` | My/_no | 用户中心前 |
| `a_admin_init` | Admin/__construct | 后台初始化 |

### 5.2 插件API示例

#### 系统核心插件
- **backtop** - 返回顶部功能
  - Hook: `right_box_bottom.hook`, `t_header.hook`

#### 功能增强插件
- **fg_tzjj** - 帖子推荐功能
  - Hook: `a_thread_fun.hook`, `right_box_bottom.hook`, `t_m_thread_header_15.hook`
  - 功能: 智能推荐帖子

- **fg_yhmxg** - 用户名修改功能

#### 图片处理插件
- **a_upload_img_min** - 图片压缩上传
- **a_upload_img_water** - 图片水印处理

#### 验证与审核插件
- **nd_jiyan** - 极验验证码
- **nd_shenhe** - 内容审核功能
- **nd_user_img** - 用户头像增强

#### 移动端主题
- **nd_mobile** - 移动端主题
- **nd_website_plus** - 网站增强功能

#### 代码高亮
- **prismjs** - 代码语法高亮显示

#### VIP系统
- **ryvip2.0.1** - VIP会员系统
- **svip** - 超级VIP系统

#### 社交分享
- **webshare** - 网页分享功能
- **Website_Title_Change_Moleft** - 网站标题动态修改

#### 排名与称号
- **tl-ranktitle** - 排行榜称号
- **tlms_topqz** - 前置群组

#### 积分与商城
- **xr_jifenduihuan** - 积分兑换系统
- **xr_3card_new_index** - 三卡新首页
- **zg_card** - 卡密系统

#### 用户功能
- **zg_collectPost** - 收藏帖子
- **zg_giveyoumoney** - 打赏功能
- **zg_invite** - 邀请注册
- **zg_spread** - 推广系统
- **zg_sign** - 签到系统
- **zg_music** - 音乐播放
- **zg_replyTime** - 回复时间限制
- **zg_video** - 视频功能

#### 其他功能
- **tl_diySlide** - 自定义轮播图
- **tl_wall** - 留言墙
- **tl_yxbk** - 优秀板块
- **XR_Aliyun_oss** - 阿里云OSS存储
- **xr_caiji** - 采集功能
- **smtpmail** - SMTP邮件发送

---

## 六、配置相关API

### 6.1 系统配置文件

**config.php** (系统核心配置)
```php
// 数据库配置
'SQL_TYPE' => 'mysql'
'SQL_NAME' => 'hj_zhang123_cn'
'SQL_IP' => 'localhost'
'SQL_USER' => 'hj_zhang123_cn'
'SQL_PASS' => '******'
'SQL_PREFIX' => 'hy_'

// URL配置
'REWRITE' => false
'url_suffix' => '.html'
'url_explode' => '/'
'DOMAIN_NAME' => 'http://hj.zhang123.cn'

// URL重写映射
'HY_URL'=>array(
    'action'=>array('thread'=>'t', 'forum'=>'f', 'my'=>'u'),
    'method'=>array('thread'=>array('del'=>'d'))
)
```

**conf.php** (业务配置 - JSON格式)
```json
{
    "title": "HYBBS",
    "theme": "nd_mobile",
    "homelist": 10,
    "postlist": 10,
    "gold_thread": 2,
    "gold_post": 2,
    "uploadimageext": "jpg,gif,png,jpeg,bmp",
    "uploadfileext": "zip,rar",
    "cache_type": "File"
}
```

### 6.2 缓存配置

支持多种缓存类型:
- File - 文件缓存
- Redis - Redis缓存
- Memcache - Memcache缓存
- Memcached - Memcached缓存

---

## 七、API响应格式

### 7.1 JSON响应格式
```json
{
    "error": true/false,
    "msg": "消息内容",
    "data": {}
}
```

### 7.2 成功响应示例
```json
{
    "error": true,
    "msg": "操作成功",
    "data": {
        "tid": 123,
        "thread_data": {...}
    }
}
```

### 7.3 错误响应示例
```json
{
    "error": false,
    "msg": "请登录后再操作",
    "data": {}
}
```

---

## 八、权限控制

### 8.1 用户组权限
通过 `NOW_GID` 常量获取当前用户组ID
- `1` - 管理员组
- `5` - VIP用户组
- 其他 - 普通用户组

### 8.2 常用权限检查
```php
IS_LOGIN          // 是否登录
NOW_GID           // 当前用户组
NOW_UID           // 当前用户ID
NOW_USER          // 当前用户名
```

### 8.3 板块权限
```php
is_forumg($forum_arr, $uid, $fid)  // 是否为版主
L("Forum")->is_comp($fid, NOW_GID, 'thread', $json)  // 检查板块权限
```

---

## 九、文件路径说明

| 路径 | 说明 |
|------|------|
| `/Action/` | 控制器目录 |
| `/Model/` | 模型目录 |
| `/View/` | 视图模板目录 |
| `/Lib/` | 自定义库目录 |
| `/Plugin/` | 插件目录 |
| `/Conf/` | 配置文件目录 |
| `/Tmp/` | 临时缓存目录 |
| `/upload/` | 上传文件目录 |

---

## 十、常用工具函数

| 函数 | 位置 | 说明 |
|------|------|------|
| `X($key)` | HY/common/function.php | 获取GET/POST参数 |
| `M($name)` | - | 实例化模型 |
| `L($name)` | - | 实例化库类 |
| `S($name)` | - | 实例化Service类 |
| `C($key, $value)` | - | 获取/设置配置 |
| `cookie($name, $value)` | - | Cookie操作 |
| `cache($key, $value, $options)` | - | 缓存操作 |
| `humandate($time)` | - | 时间格式化 |
| `filter_html($html)` | - | HTML过滤 |
| `HYBBS_URLA($action, $arg1, $arg2...)` | - | URL生成 |

---

## 十一、API调用示例

### 11.1 获取首页帖子列表
```bash
GET /api/index?pageid=1&type=New
```

### 11.2 获取帖子详情
```bash
GET /api/article?tid=123&pageid=1&order=asc
```

### 11.3 用户登录
```bash
POST /api/login
Content-Type: application/x-www-form-urlencoded

user=用户名&pass=密码
```

### 11.4 发布主题
```bash
POST /api/thread_add
Content-Type: application/x-www-form-urlencoded

forum=1&title=标题&content=内容&tgold=0&thide=0
```

### 11.5 发表评论
```bash
POST /api/Post
Content-Type: application/x-www-form-urlencoded

id=123&content=评论内容
```

---

## 十二、No控制器 (Action/No.php)

404页面处理控制器

| API路径 | 方法 | 功能描述 |
|---------|------|---------|
| `/*` | GET | 404页面显示 |

---

## 十三、Inst控制器 (Action/Inst.php)

安装向导控制器

| API路径 | 方法 | 功能描述 | 参数说明 |
|---------|------|---------|---------|
| `/install` | GET | 安装首页 | - |
| `/install/install` | POST | 执行安装 | 数据库配置等 |
| `/install/rex` | POST | 重写规则检测 | - |

---

## 十四、外部JSON配置文件说明

### 14.1 兑换商品配置 (dh.php)
```json
{
  "userlist": [
    {
      "id": 商品ID,
      "name1": 商品名称,
      "name2": 商品说明,
      "url": 兑换接口URL,
      "key": "true/false",
      "goId": 商品标识,
      "img": 商品图片,
      "bjk1": 备注字段1,
      "bjk2": 备注字段2,
      "bjk3": 备注字段3
    }
  ]
}
```

### 14.2 广告配置 (gg.php)
```json
{
  "广告图片链接": "跳转链接"
}
```

### 14.3 打赏榜配置 (zanz.php)
```json
{
  "列表": [
    {
      "qq": QQ号,
      "user": 用户名,
      "content": 打赏留言,
      "gold": 打赏金币
    }
  ]
}
```

### 14.4 APP更新配置 (Updatesv5.php)
```json
{
  "cid": 更新ID,
  "title": 更新标题,
  "content": 更新内容,
  "version": 版本号,
  "link": 下载链接,
  "ggbt": 公告标题,
  "ggnr": 公告内容,
  "ggkg": 公告开关(开/关),
  "ggurl": 公告链接,
  "ggan2": 公告按钮文字,
  "Appurl": APP地址,
  "wh": 维护开关(开/关),
  "qq": 官方QQ,
  "whnr": 维护内容
}
```

---

## 十五、注意事项

1. **登录状态**: 大部分API需要登录，请检查Cookie `HYBBS_HEX`
2. **CSRF防护**: 后台接口有CSRF验证
3. **权限检查**: 注意用户组权限和板块权限
4. **文件上传**: 注意文件大小和格式限制
5. **缓存机制**: API数据会被缓存，注意更新缓存
6. **调试模式**: 开启DEBUG模式可查看详细错误信息
7. **插件机制**: 插件可以拦截和修改API行为

---

## 十六、完整的控制器列表

| 控制器 | 文件 | 功能说明 |
|--------|------|---------|
| Index | `Action/Index.php` | 首页控制器 |
| Api | `Action/Api.php` | JSON API接口 |
| Ajax | `Action/Ajax.php` | Ajax异步接口 |
| Thread | `Action/Thread.php` | 帖子控制器 |
| Post | `Action/Post.php` | 发帖控制器 |
| User | `Action/User.php` | 用户控制器 |
| My | `Action/My.php` | 用户中心控制器 |
| Forum | `Action/Forum.php` | 论坛板块控制器 |
| Search | `Action/Search.php` | 搜索控制器 |
| Friend | `Action/Friend.php` | 好友/私信控制器 |
| Admin | `Action/Admin.php` | 后台管理控制器 |
| No | `Action/No.php` | 404页面控制器 |
| Inst | `Action/Inst.php` | 安装向导控制器 |
| HYBBS | `Action/HYBBS.php` | 系统基类控制器 |

---

## 十七、Model层完整列表

| Model | 文件 | 功能说明 |
|-------|------|---------|
| Thread | `Model/Thread.php` | 帖子数据模型 |
| Post | `Model/Post.php` | 评论数据模型 |
| Post_post | `Model/Post_post.php` | 子评论数据模型 |
| User | `Model/User.php` | 用户数据模型 |
| Usergroup | `Model/Usergroup.php` | 用户组数据模型 |
| Forum | `Model/Forum.php` | 板块数据模型 |
| Forum_group | `Model/Forum_group.php` | 板块分组数据模型 |
| Friend | `Model/Friend.php` | 好友数据模型 |
| Chat | `Model/Chat.php` | 聊天数据模型 |
| Chat_count | `Model/Chat_count.php` | 聊天统计模型 |
| File | `Model/File.php` | 文件数据模型 |
| Fileinfo | `Model/Fileinfo.php` | 文件信息模型 |
| Count | `Model/Count.php` | 统计数据模型 |
| Data | `Model/Data.php` | 数据模型 |

---

## 十八、Lib库类完整列表

| Lib类 | 文件 | 功能说明 |
|-------|------|---------|
| Upload | `Lib/Upload.php` | 文件上传库 |
| Image | `Lib/Image.php` | 图片处理库 |
| Email | `Lib/Email.php` | 邮件发送库 |
| Encrypt | `Lib/Encrypt.php` | 加密解密库 |
| File | `Lib/File.php` | 文件操作库 |
| User | `Lib/User.php` | 用户操作库 |
| Usergroup | `Lib/Usergroup.php` | 用户组库 |
| Forum | `Lib/Forum.php` | 板块库 |
| Kses | `Lib/Kses.php` | HTML过滤库 |
| Rsa | `Lib/Rsa.php` | RSA加密库 |
| Zip | `Lib/Zip.php` | ZIP压缩库 |

---

以上是整个HYBBS论坛系统的完整API文档。该系统基于HYPHP 2.8框架开发，采用了MVC架构，支持插件扩展，提供了完整的论坛功能API接口，共包含：
- 13个主要控制器
- 100+个API接口
- 14个数据模型
- 11个核心库类
- 40+个功能插件
