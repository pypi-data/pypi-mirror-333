<p align="center">
  <a href="https://github.com/JohnRichard4096/nonebot_plugin_suggarchat/"><img src="https://github.com/user-attachments/assets/b5162036-5b17-4cf4-b0cb-8ec842a71bc6" width="200" height="200" alt="nonebot"></a>
</p>
<p align="center"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>

<div align="center">

# SuggarChat 高可扩展性大模型聊天插件/框架

Chat plugin/framework for **Nonebot2** with **Onebot V11 adapter**. 


[![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/) [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) [![PyPi](https://img.shields.io/badge/pypi-%23ececec.svg?style=for-the-badge&logo=pypi&logoColor=1f73b7)](https://pypi.org/project/nonebot-plugin-suggarchat/)






## 描述
适用于**Nonebot2**的**Onebot V11 适配器**的高可扩展性LLM聊天插件

</div align="center">

## 目录
- [温馨提示](#温馨提示)
- [特性](#特性)
- [安装方式](#安装方式)
- [配置文件](#配置文件)
- [提示词设置](#提示词)
- [模型预设](#模型预设)
- [预设使用方法](#预设使用方法)
- [指令](#指令使用方法)
- [API](#api)
- [适配器规范](#适配器规范)
- [实验功能](#实验功能)
- [交流/反馈](#讨论)



## 温馨提示

**可能会与其他插件冲突**，比如导致指令无法触发，我的设计目的只是为了一个纯粹的聊天机器人，问题请提交到[ISSUE](https://github.com/JohnRichard4096/nonebot_plugin_suggarchat/issues)。

### Issue不用模板一律不看！

*本插件更面向于有Nonebot2基础或插件开发者以及有LLM API开发/使用经验的用户！*

不推荐直接调用**resources.py的**方法，而是通过插件API进行调用。

<hr />

传入LLM的信息格式如下，请自行在**提示词**内做好处理，便于LLM理解（这里我提供了use_base_prompt选项，如果启用了可以忽略，这个选项将自动在你的prompt前插入内容，对消息段作出解释）：


~~不会写就来QQ群问群主吧（~~
<details><summary>点击查看详细格式</summary>
可解析的消息段：文字，at，合并转发

<hr />

at+文字：
```plaintext
你好世界@Somebody
```
合并转发（暂不支持解析**嵌套的合并转发消息**）：
```
\（合并转发
[YYYY-MM-DD hh:mm:ss PM/AM][昵称(QQ号)]说：<内容>
[[YYYY-MM-DD hh:mm:ss PM/AM][昵称(QQ号)]说：<内容>]
）\
......以此类推
```

<hr />

私聊普通消息：
```plaintext
[YYYY-MM-DD weekday hh:mm:ss AM/PM]用户昵称（QQ号）：<内容>
```
私聊引用消息：
```plaintext
私聊普通消息格式+ （（（引用的消息）））：引用消息内其他消息段解析后内容
```
私聊合并转发消息：
```plaintext
私聊普通消息格式+合并转发消息格式
```

<hr />

聊群普通消息：
```plaintext
[管理员/群主/自己/群员][YYYY-MM-DD weekday hh:mm:ss AM/PM][昵称（QQ号）]说:<内容>
```

聊群引用消息：
```plaintext
聊群普通消息格式+ （（（引用的消息）））：引用消息内其他消息段解析后内容
```
聊群合并转发消息：
```plaintext
聊群普通消息格式+合并转发消息格式
```

<hr />

戳一戳消息：
```plaintext
\(戳一戳消息\) 昵称(QQ:qq号) 戳了戳你
```
</details>

### 对于源码

警告！本插件源码可能含有以下内容

<details><summary>

~~点我开始赤史~~
</summary>

《三角形具有稳定性》
```python
if:
    if:
        if:
            if:
            else:
        else:
    else:
else:
```
《无意义分支》
```python
if a:do()
else:pass

```
《如判断》
```python
if True:
    todo()
#或者说
while True:
    todo()
    break
```
</details>

## 特性

- OpenAI API 支持
- 高扩展性接口提供
- 允许注册LLM 协议适配器
- QQ群组聊天支持
- QQ私聊支持
- 群组AT触发
- API 开放
- [SuggarMatcher扩展处理器](#suggarmatcher)
- 戳一戳消息触发支持
- 多模型切换选择
- 不同群内自定义聊天开关
- 不同聊群可设置的自定义补充Prompt
- 向超控（特定聊群）推送插件的错误日志
- 自定义Bot消息被撤回时缓解尴尬的推送
- 合并转发/引用消息解析支持（只会解析纯文本/at消息段，如果您不理解这是什么意思，你可以理解为丢给LLM的信息只有"@a 你好"这样的格式，会在下文介绍提及）
- “伪人模式”-聊群自动随机概率回复功能
- 会话控制

## 安装方式
1. **通过NB-CLI安装（推荐）**
```bash
nb plugin install nonebot-plugin-suggarchat
```

如果使用以下方法需要在你机器人项目根目录的`pyproject.toml`中的**plugins**`列表`做如下修改：
```toml
plugins=['nonebot_plugin_suggarchat","nonebot_plugin_xxx']
#添加"nonebot_plugin_suggarchat"
```
此外，如果你创建了**虚拟环境**，并且使用以下的方法安装，请额外在**机器人项目根目录**使用`pipenv shell`**进入虚拟环境**再进行安装，**否则**插件将会安装在你的**系统Python环境**中。

2. **通过pip安装**
确保已安装Python（版本>=3.9）。
打开命令行工具，执行以下命令来安装插件：
```bash
pip install nonebot-plugin-suggarchat
```
​     

3. **通过PDM安装**
```bash
pdm add nonebot-plugin-suggarchat
```


​    



## 配置文件

- **配置文件路径**： 将在插件启动时在控制台输出。
### **配置项说明**
<details><summary>点此展开</summary>

| 配置项                         | 类型                | 默认值        | 解释                                                         |
|------------------------------|-------------------|--------------|------------------------------------------------------------|
| `memory_length_limit`          | int               | 50           | 单会话允许存储的最大消息数（**如果您不知道这是什么意思，请不要修改**）                                       |
| `enable`                       | bool               | **false**         | 是否启用聊天机器人（即该插件）                                          |
| `poke_reply`                   | bool               | true         | 是否启用戳一戳回复功能                                          |
| `enable_group_chat`            | bool               | true         | 是否启用群聊功能                                            |
| `enable_private_chat`          | bool               | true         | 是否启用私聊功能                                            |
| `allow_custom_prompt`          | bool               | true         | 是否允许自定义提示                                          |
| `allow_send_to_admin`          | bool               | true         | 是否允许向管理员发送消息                                    |
| `admin_group`                  | int               | 0            | 管理员群组的ID                                             |
| `admins`                       | list[int]               | []           | 管理员用户的列表                                            |
| `open_ai_base_url`             | string             | ""           | OpenAI协议 API URL                                        |
| `open_ai_api_key`              | string             | ""           | OpenAI协议 API 密钥                                            |
| `say_after_self_msg_be_deleted` | bool               | true         | 自己的消息被删除后是否回复                                  |
| `group_added_msg`              | string             | "你好，我是Suggar，欢迎使用Suggar的AI聊天机器人，你可以向我提问任何问题，我会尽力回答你的问题，如果你需要帮助，你可以向我发送“帮助”" | 加入群组时发送的欢迎消息                                     |
| `send_msg_after_be_invited`    | bool               | true         | 被邀请进群后是否发送消息                                        |
| `after_deleted_say_what`       | list[str]               | [ "Suggar说错什么话了吗～下次我会注意的呢～", "抱歉啦，不小心说错啦～", ... ] | 消息被删除后随机回复的内容                                   |
| `use_base_prompt`       | bool               | true | 是否使用基本提示词（即让LLM理解消息段解析）                                   |
| `preset`       | string               | __main__ | 是否使用预设（在控制台打印的models文件夹下，预设json格式参考下文（你的预设名**不能**设为`__main__`）午）                                   |
| `max_tokens`       | int               | 100 | 在单次对话时，LLM最多可以生成多少个token（并非完全等于字数，如果你的模型提供商支持）                                   |
| `tokens_count_mode`       | str               | bpe | 上下文窗口tokens 计算模式，可选 'word'(词，较大误差), 'bpe'(子词，最精准), 'char'(字符，不推荐)                                  |
| `session_max_tokens`       | int               | 5000 | 上下文最多允许多少的tokens数 ,**此计算可能有10%的误差**                                   |
| `enable_tokens_limit`       | bool               | true | 是否启用上下文长度限制，如果启用，则上下文长度将不会超过`session_max_tokens`                                   |
| `model`       | str               | auto | 使用什么模型（具体看你的API提供商                                   |
| `parse_segments` | bool               | true | 是否解析消息段，此权重覆盖`use_base_prompt`（即at/合并转发等）                                   |
| `fake_people`      |     bool     |     true    |   是否启用自动回复模式    |
| `probability`      |     float     |     1e-2   |   随机回复的概率(1%~100%)    |
|  `keyword`         |     str     |     "at"    |   触发bot对话关键词,at为to_me,其他为以这个词开头必定回复   |
|  `nature_chat_style`         |     bool     |     false    |   启用更加自然的聊天风格   |
|  `matcher_function`         |     bool     |     false    |   启用matcher,当这一项启用,SuggaeMatcher将会运行（这是一个实验性的功能）。   |
| `session_control`       | bool   | false  | 启用会话控制机制（根据设定的会话时间差自动裁切上下文，如果超时则裁切上下文并询问是否继续对话） |
| `session_control_time`  | int    | 60     | 会话控制时间间隔（单位：分钟）                                                           |
| `session_control_history` | int  | 10     | 储存的会话历史最大条数                                                                   |
| `procotol` | str  | __main__     | 协议适配器（__main__为默认值，即使用默认的OpenAI适配器，第三方适配器请参考对应文档）                                   |


</details>

## 提示词
提示词位于将在控制台打印的config文件夹，分别`为prompt_group.txt`与`prompt_private.txt`，分别对应群聊和私聊的提示词。

## 模型预设
预设文件位于将在控制台打印的models文件夹下，预设文件为json格式，具体格式如下：

```json
    {
    "model":"auto",
    "name":"",
    "base_url":"",
    "api_key":"",
    "procotol":"__main__"
    }
```
### 解释：
- `model`: 使用的模型，默认为auto，即自动选择。
- `name`: 预设的名字，用于在插件中选择使用。
- `base_url`: OpenAI协议 API URL，默认为空。
- `api_key`: OpenAI协议 API 密钥，默认为空。
- `procotol`: 预设的协议，默认为__main__，其他协议请阅读对应的文档。
## 预设使用方法
1. 在控制台打印的models文件夹下，创建一个json文件，文件名必须与预设的名字一致。
2. 在json文件中，填写预设的内容。
3. 在插件配置文件中，将`preset`的值设置为预设的名字（我们更推荐你使用**指令**来切换而不是直接修改配置文件）。
## 指令使用方法
| 指令            |                    参数     |           解释     |
|--------------|-----------------|------------------------------|
| **/聊天菜单** 或 **/chat_menu**: | 无 | 显示聊天菜单| 
| **/del_memory**, **/失忆**, **/删除记忆**, **/删除历史消息**, **/删除回忆**| 无 | 删除群/私聊会话聊天上下文 |
| **/enable_chat** 或 **/启用聊天** | 无  | 启用聊天功能 |
 | **/disable_chat** 或 **/禁用聊天**| 无 |禁用聊天功能
 | **/prompt** | `--(show)` 展示当前提示词，`--(clear)` 清空当前prompt，`--(set) <文字>`则设置提示词 | 设置或查看当前自定义提示词（适用于用户自定义补充提示词）
 | **/presets** | 无 | 查看可用的预设列表
 | **/set_preset** 或 **/设置预设** 或 **/设置模型预设** | `<预设名>`  |设置当前使用的预设
| **/sessions**       | 无                     | 查看历史会话列表（显示编号、消息片段和时间戳）                        |
| **/sessions**       | `set <编号>` 用指定编号的历史会话覆盖当前记忆 `del <编号>` 删除指定编号的历史会话 `archive` 将当前会话归档到历史记录中，并清空当前聊天上下文 `clear` 清空所有历史会话记录          | 会话控制管理指令                                      |                                          |

<details><summary>隐藏指令</summary>

## 隐藏指令

为什么会有？因为开发者为了DEBUG，会保留一些在开发过程中测试的指令，如果您只是普通用户，请忽略。

。
| 指令            |                    参数     |           解释     |
|--------------|-----------------|------------------------------|
| **/debug** | 无 | 显示调试信息并推送 |


</details>

## API

<details>

### API 文档

### 概述
该 API 提供了配置管理、适配器注册、菜单管理、管理员操作和聊天消息处理等功能。以下是各个类的详细说明。

---

### 类说明

### `Config`
用于处理配置注册和管理的类。

#### 方法
- **`get_config(value: str | None)`**  
  获取配置信息。  
  - 参数：  
    - `value` (str | None): 配置项的名称。如果为 `None`，返回所有配置。  
  - 返回：  
    - 配置值或整个配置字典。

- **`get_models()`**  
  获取模型配置。  
  - 返回：  
    - 模型配置字典。

- **`reg_config(key: str)`**  
  注册一个新的配置项。  
  - 参数：  
    - `key` (str): 配置项的名称。  
  - 异常：  
    - 如果配置项已存在，抛出 `Exception`。

- **`reg_model_config(key: str)`**  
  注册一个新的模型配置项。  
  - 参数：  
    - `key` (str): 模型配置项的名称。  
  - 异常：  
    - 如果配置项已存在，抛出 `Exception`。

---

### `Adapter`
用于处理适配器注册的类。

#### 方法
- **`register_adapter(func: callable, protocol: str)`**  
  注册一个适配器。  
  - 参数：  
    - `func` (callable): 适配器函数。  
    - `protocol` (str): 协议名称。  
  - 异常：  
    - 如果协议适配器已存在，抛出 `ValueError`。

---

### `Menu`
用于注册菜单项的类。

#### 方法
- **`reg_menu(cmd_name: str, describe: str)`**  
  注册一个新的菜单项。  
  - 参数：  
    - `cmd_name` (str): 菜单项的命令名称。  
    - `describe` (str): 菜单项的描述。  
  - 返回：  
    - `Menu` 实例，支持链式调用。

---

### `Admin`
管理员管理类，用于处理与管理员相关的操作。

#### 方法
- **`send_with(msg: str)`**  
  异步发送消息给管理员。  
  - 参数：  
    - `msg` (str): 要发送的消息内容。  
  - 返回：  
    - `Admin` 实例，支持链式调用。

- **`send_error(msg: str)`**  
  异步发送错误消息给管理员，并记录错误日志。  
  - 参数：  
    - `msg` (str): 要发送的错误消息内容。  
  - 返回：  
    - `Admin` 实例，支持链式调用。

- **`is_admin(user_id: int)`**  
  检查用户是否是管理员。  
  - 参数：  
    - `user_id` (int): 用户 ID。  
  - 返回：  
    - `bool`: 用户是否是管理员。

- **`add_admin(user_id: int)`**  
  添加新的管理员用户 ID。  
  - 参数：  
    - `user_id` (int): 要添加的用户 ID。  
  - 返回：  
    - `Admin` 实例，支持链式调用。

- **`set_admin_group(group_id: int)`**  
  设置管理员组 ID。  
  - 参数：  
    - `group_id` (int): 管理员组 ID。  
  - 返回：  
    - `Admin` 实例，支持链式调用。

---

### `Chat`
用于处理与 LLM（大语言模型）相关的操作。

#### 方法
- **`get_msg(prompt: str, message: list)`**  
  获取聊天消息。  
  - 参数：  
    - `prompt` (str): 提示语。  
    - `message` (list): 消息列表。  
  - 返回：  
    - 聊天消息。

- **`get_msg_on_list(message: list)`**  
  根据消息列表获取聊天消息。  
  - 参数：  
    - `message` (list): 消息列表。  
  - 返回：  
    - 聊天消息。

---

## 示例代码

### 配置管理
```python
config = Config()
config_value = config.get_config("some_key")
```

### 注册适配器
```python
adapter = Adapter()
adapter.register_adapter(my_func, "my_protocol")
```

### 注册菜单项
```python
menu = Menu()
menu.reg_menu("help", "显示帮助信息")
```

### 发送消息给管理群组
```python
admin = Admin()
await admin.send_with("Hello, Admin!")
```

### 说明
- 该文档基于代码中的类和方法编写，涵盖了主要功能和用法。
- 代码中标记为“施工中”的部分未包含在文档中，待功能完善后可补充。

</details>

## 适配器规范
适配器规范定义了适配器应该实现的功能，包括消息处理、事件处理、群组管理、用户管理等。

上文已经提及了API接口如何注册适配器，下面将进行详细介绍。

exapmle:

```python
from nonebot import get_driver
from nonebot.plugin import require

require("nonebot_plugin_suggarchat")
from nonebot_plugin_suggarchat.API import Adapter

#必须实现的形式参数说明：
#base_url: api地址（来自配置文件）
#model: 模型名称
#key: api key（来自配置文件）
#messages: 消息列表
#max_tokens: 最大token数（来自配置文件）
#config 配置文件
async def example_adapter(base_url:str, model:str, key:str, messages:list, max_tokens:int, config:dict)->str:
    # 你的逻辑,必须返回一个字符串
    # todo
    return string
@get_driver().on_startup
async def startup():
    adapter = Adapter()
    adapter.register_adapter(example_adapter, "example")

```

### 上架Nonebot商店：
推荐的命名格式：nonebot_plugin_suggaradapter_yourpluginname

## 实验功能
### SuggarMatcher
- 事件循环套事件循环？实现了一个简单的Matcher功能，可以注册处理器函数，并进行额外处理。
```python
from nonebot import logger
from nonebot.plugin import require
require("nonebot_plugin_suggarchat")
from nonebot_plugin_suggarchat.event import (
    ChatEvent,
    PokeEvent,
    BeforeChatEvent,
    BeforePokeEvent,
)
from nonebot_plugin_suggarchat.on_event import (
    on_chat,
    on_before_chat,
    on_poke,
    on_before_poke,
)

@on_poke().handle(priority_value=10)
async def _(event: PokeEvent):
    logger.info("戳了！")
    logger.info(event)


@on_before_poke().handle(priority_value=10)
async def _(event: BeforePokeEvent):
    logger.info("现在在获取模型的回复之前！")
    logger.info(event)


@on_before_chat().handle(priority_value=10)
async def _(event: BeforeChatEvent):
    logger.info("现在在获取模型的回复之前！")
    logger.info(event)


@on_chat().handle(priority_value=10)
async def _(event: ChatEvent):
    logger.info("收到聊天事件!")
    logger.info(event)

```
更多示例代码请参考插件源码测试用例处。
### 会话控制
- （在配置文件中设置，详情见配置文件部分）


## 讨论

QQ 交流群: [链接](https://qm.qq.com/q/PFcfb4296m)
