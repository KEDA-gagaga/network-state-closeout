# Network State + Closeout Cards Plugin

> 版本：`0.1.0-pre.9` · 轻量预备发布版

> 把不断变化的私人网络环境，整理成 Agent 可以跨项目使用、按需读取，并在多台设备之间共享的网络资料。

## 让 Agent 知道“现在的网络是什么样”

还在每次打开新任务、切换项目或更换设备时，重新解释你的主机、服务、代理和访问路径？

还在不同笔记与聊天记录之间翻找设备地址、反向代理、容器端口、域名、TLS 和连接关系？

真正的问题通常不是记录得不够多，而是不断变化的网络资料没有一份统一、可信、容易维护的来源。把所有细节直接写进一个庞大的 skill 也不理想：网络状态会变化，真实端点属于私人信息，无关内容还会占用 Agent 的上下文。

Codex 内置的 OpenAI Docs skill 给出了一个很好的参考：它不把持续变化的官方手册固化在 skill 中，而是把来源选择、时效校验、失败边界和检索路线保留为稳定工作流；真正回答问题前，再从可信来源刷新当前版本，生成可定位的目录，并读取与问题有关的章节。它追求的不是“预先保存所有知识”，而是始终保留一条通往最新知识的可靠路径。

`network-state-closeout` 把稳定能力和动态资料分开：插件保存分类规则、快速校验、安全边界和同步门禁；设备、服务、地址、访问路径与排错经验则保存在用户自己的全局私人 skill 中。Agent 只读取当前问题需要的分类卡片，确认了简单稳定事实后可以直接更新，不要求用户逐次选择。

从设备与服务，到反向代理、域名、TLS、容器端口、SSH、VPN 和访问路径，这些零散信息会被整理成可持续维护的网络卡片。完成重要部署、迁移或排障时，状态卡记录最终状态，过程卡记录技术路线，其中值得复用的结论继续沉淀到对应网络卡片。

最终得到的不是一份很快过期的静态清单，而是一套轻量的私人网络知识层：同一份资料可以跨项目使用，并可通过 GitHub 私人仓库，让多台设备上的 Agent 共享同一份网络资料；每次只加载真正需要的部分。

具体来说：

- **插件保存稳定能力**：分类方式、写入原则、初始化引导、安全校验和同步门禁随插件分发。
- **私人 skill 保存动态资料**：真实设备、服务、地址、端口、上游、访问路径和排错结论不会进入公开插件。
- **Agent 按需读取分类卡片**：查询一个服务不必加载完整设备清单，排查一条路径也不必读取全部拓扑。
- **简单事实直接写入**：允许 Agent 自主维护已经确认的稳定事实，保持日常写入轻量。
- **重要动作再生成收尾卡片**：状态卡说明现在是什么状态，过程卡保留技术路线和未来排查入口。
- **GitHub 私人仓库连接不同设备**：需要跨设备一致时，先经过快速隐私与同步门禁，再提交和推送。

## 核心模型

初始化后，私人网络状态本身就是一个 Codex skill：

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

## 跨项目与跨设备

两者含义不同：

- **跨项目**：私人 skill 安装在 Codex 的全局 `~/.codex/skills/` 中，所以切换到其他项目时，Codex 仍可按需加载同一份网络状态。
- **跨设备**：其他设备先安装本插件，再把同一个 GitHub 私人仓库直接克隆到该设备的 `.codex/skills/private-network-state`。不同设备上的 Agent 因而读取和维护同一份网络资料历史。

当前版本只通过 GitHub 私人仓库进行跨设备同步。GitHub 是同步通道；每台设备真正读取和修改的仍是自己的 `.codex/skills` 活跃缓存。

## 渐进式卡片

网络资料按类型分文件，每个文件内部由多张小卡片组成：

| 问题类型 | 只读取 |
|---|---|
| 设备、地址、路由、在线状态 | `references/devices.md` |
| 服务、端口、域名、TLS、容器、上游 | `references/services.md` |
| SSH、代理、VPN、中继和应用访问方向 | `references/access-paths.md` |
| 稳定拓扑和边界 | `references/topology.md` |
| 已确认、可复用的排错经验 | `references/troubleshooting.md` |
| 用户自定义简称 | `references/glossary.md` |

查询一个服务不需要读取全部设备和拓扑；排查一条路径也不需要加载所有服务。这样可以减少进入 Codex 上下文的内容。

## 轻量写入

- 简单地址、端口、状态或验证时间变化，直接更新对应卡片。
- 任务确认了稳定事实后可以自主写入，不要求用户逐次选择更新；用户可以明确要求本次不记录。
- 只有用户明确要求收尾，或完成了值得长期审计的部署、迁移、排障和配置变更，才调用 `action-closeout-cards`。
- 状态卡与过程卡只保存最终状态和技术路线；其中值得复用的网络事实直接写回对应网络卡片。
- 删除记录和修改真实网络配置仍需明确授权。

## 两条保存路线

### 跨设备同步

需要多台设备保持一致时，先比较 GitHub 私人仓库远端提交与本地提交。相同时立即继续；不同时才获取并仅快进。更新后校验、普通提交并推送。

仓库身份不确定、工作区不干净、校验失败、远端拒绝或历史分叉时停止。

### 仅本地保存

用户明确要求暂不进行网络同步时：

- 直接更新 `.codex/skills/private-network-state`；
- 运行快速校验；
- 已启用 Git 时只创建本地提交，不获取或推送远端；
- 明确说明这次改动尚未跨设备同步。

以后需要同步时，重新执行完整 GitHub 门禁。不会沿用先前的远端检查结果。

## 三个 skill

- `initialize-network-state`：初始化全局私人 skill，或引导另一台设备从 GitHub 私人仓库安装。
- `network-state`：按需读取卡片、直接维护简单事实，并选择仅本地保存或跨设备同步。
- `action-closeout-cards`：只为值得长期记录的完成动作生成状态卡和过程卡。

## 初始化

推荐调用：

```text
$initialize-network-state 帮我初始化全局私人网络状态 skill，先不要扫描网络，再询问是否启用 GitHub 私人仓库同步。
```

手动初始化默认位置：

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py
```

默认创建：

```text
~/.codex/skills/private-network-state
```

初始化器不会覆盖非空目录。

## 另一台设备

先安装本插件，再确认私人仓库身份和可见性，然后执行：

```bash
git clone <private-repository-url> ~/.codex/skills/private-network-state
python3 <network-state-skill-directory>/scripts/validate_profile.py \
  --path ~/.codex/skills/private-network-state
```

Codex 随后会把克隆下来的目录作为全局私人 skill 使用。不要再建立用于日常编辑的项目副本。

## 安全边界

私人卡片可以保存操作所需的主机名、地址、端口、域名、路径、拓扑和验证信号。

不得保存密码、token、API key、私钥、认证密钥、cookie、恢复码、一次性验证码、订阅地址、登录凭据或含凭据 URL。连接需要认证时，只保留钥匙串、密码管理器或 secret manager 中的引用名称。

GitHub 仓库必须是 private。首次推送和远端身份不确定时需要确认可见性；不能强制推送或自动解决分叉。

## 插件目录

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
