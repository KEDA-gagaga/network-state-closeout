# Network State + Closeout Cards Plugin

> 版本：`0.1.0-pre.13` · 轻量预备发布版

> 把不断变化的私人网络环境，整理成 Agent 可以跨项目使用、按需读取，并在多台设备之间共享的网络资料。

## 让 Agent 知道“现在的网络是什么样”

还在每次打开新任务、切换项目或更换设备时，重新解释你的主机、服务、代理和访问路径？

还在不同笔记与聊天记录之间翻找设备地址、反向代理、容器端口、域名、TLS 和连接关系？

真正的问题通常不是记录得不够多，而是不断变化的网络资料没有一份统一、可信、容易维护的来源。把所有细节直接写进一个庞大的 skill 也不理想：网络状态会变化，真实端点属于私人信息，无关内容还会占用 Agent 的上下文。

Codex 内置的 OpenAI Docs skill 给出了一个很好的参考：它不把持续变化的官方手册固化在 skill 中，而是把来源选择、时效校验、失败边界和检索路线保留为稳定工作流；真正回答问题前，再从可信来源刷新当前版本，生成可定位的目录，并读取与问题有关的章节。它追求的不是“预先保存所有知识”，而是始终保留一条通往最新知识的可靠路径。

`network-state-closeout` 把同样的思路应用到私人网络状态：插件保存分类规则、写入原则、快速校验、安全边界和同步门禁；设备、服务、地址、访问路径与排错经验则保存在用户自己的全局私人 skill 中。Agent 只读取当前问题需要的分类卡片，并直接维护任务中已经确认的稳定事实。

最终得到的不是一份很快过期的静态清单，而是一套轻量的私人网络知识层：同一份资料可以跨项目使用，并可通过 GitHub 私人仓库，让多台设备上的 Agent 共享同一份网络资料；每次只加载真正需要的部分。

## 直接把链接交给 Codex

把下面这段直接发送给 Codex：

```text
请安装并使用这个插件：
https://github.com/KEDA-gagaga/network-state-closeout

请先阅读仓库中的 INSTALL_WITH_CODEX.md，按照其中的 Agent 流程完成安装；安装后开启新任务，再引导我初始化私人网络状态。
```

仓库已经提供 Codex 可识别的插件目录。完整设计理由、安装命令、初始化顺序和安全边界见 [INSTALL_WITH_CODEX.md](INSTALL_WITH_CODEX.md)。

## 三个 skill 如何协作

插件由三个职责清晰的 skill 组成：

- `initialize-network-state`：初始化全局私人网络状态，经同意从本机只读来源补全网络结构，或引导另一台设备接入已有的 GitHub 私人仓库。
- `network-state`：按需读取和维护分类卡片，并选择仅本地保存或跨设备同步。
- `action-closeout-cards`：分别判断是否需要状态卡或过程卡，只记录有长期价值且有证据支持的内容。

典型流程如下：

```text
首次使用
  -> initialize-network-state 创建或接管全局私人 skill
  -> 说明保存边界并承诺认证秘密绝不进入文件或 Git
  -> 经用户同意，从本机只读来源补全网络结构
  -> 可选：连接 GitHub 私人仓库
  -> 校验后交给 network-state

日常查询或简单更新
  -> network-state 只读取相关分类卡片
  -> 回答问题或直接更新已确认事实
  -> 仅本地保存，或通过门禁后跨设备同步

完成重要部署、迁移或排障
  -> action-closeout-cards 分别判断是否需要状态卡或过程卡
  -> 只有真实过程有可靠记录时才生成过程卡
  -> network-state 把其中值得复用的稳定结论写入对应网络卡片
```

简单的地址、端口、在线状态或验证时间变化不会触发收尾卡片，直接更新网络状态即可。盘点或导入既有网络结构也不生成过程卡，因为当前配置只能证明现在的状态，不能证明它是如何形成的。

## 私人网络状态怎样组织

初始化后，私人网络状态本身就是一个 Codex 全局 skill：

```text
~/.codex/skills/private-network-state/
├── SKILL.md
├── profile.md
└── references/
    ├── devices.md
    ├── services.md
    ├── access-paths.md
    ├── topology.md
    ├── troubleshooting.md
    └── glossary.md
```

这个 `.codex/skills` 活跃缓存是唯一允许修改、提交和同步的位置。项目目录、Documents 和其他 clone 不参与日常写入。

每个分类文件内部由多张小卡片组成。Agent 根据问题渐进式读取：

| 问题类型 | 只读取 |
|---|---|
| 设备、地址、路由、在线状态 | `references/devices.md` |
| 服务、端口、域名、TLS、容器、上游 | `references/services.md` |
| SSH、代理、VPN、中继和应用访问方向 | `references/access-paths.md` |
| 稳定拓扑和网络边界 | `references/topology.md` |
| 已确认、可复用的排错经验 | `references/troubleshooting.md` |
| 用户自定义简称 | `references/glossary.md` |

查询一个服务不需要读取全部设备和拓扑；排查一条路径也不需要加载所有服务。这样可以减少进入 Agent 上下文的内容。

## 跨项目与跨设备

这两个概念解决的是不同问题：

- **跨项目**：私人 skill 位于 Codex 的全局 `~/.codex/skills/` 中。切换到其他项目时，Agent 仍可按需读取同一份网络资料。
- **跨设备**：另一台设备先安装本插件，再把同一个 GitHub 私人仓库直接克隆到自己的 `.codex/skills/private-network-state`。不同设备上的 Agent 因而读取和维护同一份网络资料历史。

当前版本只通过 GitHub 私人仓库进行跨设备同步。GitHub 保存跨设备共享的历史；每台设备真正读取和修改的仍是自己的 `.codex/skills` 活跃缓存。

## 轻量写入与保存

任务确认了稳定事实后，Agent 可以自主更新对应卡片，不要求用户逐次选择。用户仍可明确要求某次任务不记录。

只有完成了值得长期记录的部署、迁移、排障或配置变更，或者用户明确要求收尾时，才进入卡片判断；状态卡和过程卡不是固定配套：

- 状态卡只在最终状态、入口、验证结果或边界值得长期引用时生成。
- 过程卡只在实际过程有可靠记录，而且技术路线、关键决策或排查入口以后仍有价值时生成。
- 既有网络结构、简单事实和只有当前配置但没有过程记录的情况，不生成过程卡。
- 用户要求过程卡但证据不足时，Agent 必须说明未生成，不能猜测或补写一张形式化卡片。
- 其中值得复用的网络事实直接写回对应分类卡片。

删除已有记录或修改真实网络配置仍需用户明确授权。

### 仅本地保存

暂时不进行网络同步时：

- 直接更新 `.codex/skills/private-network-state`；
- 运行快速校验；
- 已启用 Git 时只创建本地提交，不获取或推送远端；
- 明确说明本次改动尚未跨设备同步。

以后需要同步时，必须重新执行完整的隐私与同步门禁，不沿用之前的远端检查结果。

### 跨设备同步

需要多台设备保持一致时，先比较 GitHub 私人仓库的远端提交与本地提交。相同时立即继续；不同时才获取并仅快进。更新后执行校验、创建普通提交并推送。

仓库身份不确定、工作区不干净、校验失败、远端拒绝或历史分叉时停止。不会强制推送或自动处理分叉。

## 开始使用

### 第一台设备

推荐直接调用初始化引导：

```text
$initialize-network-state 帮我初始化全局私人网络状态 skill。先说明可以采集和绝不保存的信息，作出隐私承诺，再征求我同意，通过本机只读检查尽可能补全网络结构。
```

初始化引导会先区分两类信息：

- **可以保存的网络结构**：设备别名与角色、地址、子网、路由、SSH 访问关系、Docker 网络和端口、反向代理、域名、TLS 状态、虚拟局域网、VPS 及服务依赖。
- **绝不保存的认证秘密**：密码、口令、token、API key、私钥内容、VPN 私钥或预共享密钥、cookie、恢复码、一次性验证码、订阅地址和含凭据 URL。

Codex 必须先承诺认证秘密不会进入私人 skill、状态卡、过程卡、Git 暂存区、提交历史或 GitHub 仓库，再询问是否允许读取本机配置并运行只读命令。用户拒绝时保留空白卡片继续初始化；用户同意后只整理授权范围内的结构事实。

本机只读采集不包含主动扫描子网、调用云服务 API 或登录其他主机。这些扩展操作必须说明具体范围并再次征求授权；获准检查其他主机时优先使用 SSH。

也可以手动运行初始化器：

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py
```

默认创建位置：

```text
~/.codex/skills/private-network-state
```

初始化器不会覆盖非空目录。

### 另一台设备

先安装本插件，再确认私人仓库身份和可见性，然后执行：

```bash
git clone <private-repository-url> ~/.codex/skills/private-network-state
python3 <network-state-skill-directory>/scripts/validate_profile.py \
  --path ~/.codex/skills/private-network-state
```

验证通过后，Agent 会把该目录作为全局私人 skill 使用。不要再创建用于日常编辑的项目副本。

## 安全边界

经用户同意，私人卡片可以保存操作所需的主机名、地址、端口、域名、路径、拓扑、服务关系和验证信号。这些结构事实只进入全局私人 skill，以及用户确认的 GitHub 私人仓库。

不得保存密码、口令、token、API key、私钥内容、VPN 私钥或预共享密钥、cookie、会话、恢复码、一次性验证码、订阅地址、登录凭据或含凭据 URL。连接需要认证时，只保留身份文件路径、钥匙串条目名、密码管理器条目名、环境变量名或 secret manager 中的安全引用。

GitHub 仓库必须是 private。首次推送和远端身份不确定时需要确认可见性。

## 安装整个插件

推荐直接让 Codex 按 [INSTALL_WITH_CODEX.md](INSTALL_WITH_CODEX.md) 操作。命令行安装入口为：

```bash
codex plugin marketplace add KEDA-gagaga/network-state-closeout
codex plugin add network-state-closeout@network-state-closeout
```

安装后开启新任务，再调用 `$initialize-network-state`。

```text
plugin/network-state-closeout/
├── .codex-plugin/plugin.json
└── skills/
    ├── initialize-network-state/
    ├── network-state/
    └── action-closeout-cards/
```

正式安装时应安装整个 `plugin/network-state-closeout`，不要只复制其中一个 skill。

## 校验

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py \
  plugin/network-state-closeout

python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugin/network-state-closeout/skills/network-state

python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugin/network-state-closeout/skills/initialize-network-state

python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugin/network-state-closeout/skills/action-closeout-cards
```

初始化测试：

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py \
  --path /tmp/private-network-state-test

python3 plugin/network-state-closeout/skills/network-state/scripts/validate_profile.py \
  --path /tmp/private-network-state-test
```

## 许可证

本项目使用 [MIT License](LICENSE)。
