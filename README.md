# Network State + Closeout Cards Plugin

> 版本：`0.1.0-pre.4` · 组合预备发布版

`network-state-closeout` 把三个职责独立、又能串联工作的 Codex skill 放进同一个插件：

- `initialize-network-state`：首次初始化或接管私人网络资料，并可独立引导 GitHub 私人仓库同步。
- `network-state`：维护独立私人目录中的设备、服务、访问路径、拓扑和可复用排错事实。
- `action-closeout-cards`：在动作完成后分别生成状态卡与技术路线过程卡。

组合工作流会先确认并校验网络事实，再从最终事实中提取最少必要内容生成收尾文档。完整私人网络资料不会被复制到项目卡片。

## 组合工作流

```text
首次使用
  -> 初始化或接管唯一私人资料目录
  -> 可选：通过独立引导模块连接 GitHub 私人仓库
  -> 校验并交给 network-state

日常网络工作
  -> 已启用同步时：强制检查 GitHub 私人仓库最新状态
  -> 完成网络动作
  -> 可选：更新已确认的私人网络状态
  -> 校验私人资料
  -> 生成状态卡：现在是什么状态
  -> 生成过程卡：按什么技术路线实现
  -> 可选：登记到项目现有状态入口
```

三个 skill 可以按职责单独使用。初始化结束后，日常查询和更新不会重复触发引导；普通动作收尾也不要求存在网络状态目录。

## 目录结构

```text
plugin/network-state-closeout/
├── .codex-plugin/plugin.json
└── skills/
    ├── network-state/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── assets/profile-template/
    │   ├── references/writing-rules.md
    │   ├── references/private-sync.md
    │   └── scripts/
    ├── initialize-network-state/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/github-private-sync.md
    └── action-closeout-cards/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/card-templates.md
```

README 位于插件源目录之外，不会作为 skill 上下文加载。

## 环境要求

- 支持插件与 skill 的 Codex 环境。
- Python 3.9 或更高版本，用于初始化和校验私人网络资料。
- `rg` 可选，用于对新建卡片进行敏感信息启发式扫描。
- Git 可选，用于通过已确认的 GitHub 私人仓库同步私人网络状态。

初始化、校验和写卡功能没有网络依赖。只有启用私人 GitHub 同步时，工作流才会执行用户确认范围内的 Git 命令。插件不包含 MCP、App、Hook 或自动自更新功能。

## 当前交付形式

这是可验证的插件源目录，不会自动修改个人插件市场或 Codex 配置。正式安装时，应把：

```text
plugin/network-state-closeout
```

作为完整插件目录交给现有的本地插件市场或安装流程，不要只复制其中一个 skill。

## 初始化私人网络资料

推荐首次使用时直接调用引导 skill：

```text
$initialize-network-state 帮我初始化私人网络状态；先不要扫描网络，再询问我是否启用 GitHub 私人仓库同步。
```

引导 skill 会区分新建、本地已有资料、首台同步设备和新增同步设备，不会覆盖非空目录。只需要手动执行初始化脚本时，可使用：

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py
```

默认创建 `~/.codex/network-state`。也可以指定其他私人位置：

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py \
  --path "$HOME/path/to/private/network-state"
```

初始化脚本不会覆盖非空目录，也会拒绝把私人资料创建在 `network-state` skill 内部。已有资料应交给引导 skill 接管和校验，不要重新套用模板。

如果选择默认目录以外的位置，后续任务必须继续提供同一路径，或者为 Codex 持久设置 `NETWORK_STATE_HOME`；引导 skill 不会擅自修改 shell 启动文件或 Codex 配置。

## 使用示例

首次初始化：

```text
$initialize-network-state 为我建立本地私人网络状态目录，先不启用 GitHub 同步。
```

引导私人同步：

```text
$initialize-network-state 把已有网络状态接入我确认的 GitHub 私人仓库，并把同步设为查询和更新前的强制门禁。
```

只维护网络资料：

```text
$network-state 记录我刚确认的设备和服务。未知字段保留为 unknown，不要扫描网络。
```

只生成收尾卡：

```text
$action-closeout-cards 这个部署已经结束，请按项目现有命名生成状态卡和过程卡，不要写命令流水。
```

使用组合流程：

```text
更新这次网络变更的已确认状态并运行校验，然后生成状态卡和技术路线过程卡；卡片只保留项目需要的最少网络信息。
```

组合流程中，只有用户明确要求更新网络状态时才修改私人资料。只要求写卡时，网络状态保持只读。

## GitHub 私人仓库同步

私人网络状态可以通过 GitHub 私人仓库在多台设备间同步；插件安装目录与私人状态仓库保持独立。首次接入由 `initialize-network-state/references/github-private-sync.md` 引导，日常强制同步规则位于 `network-state/references/private-sync.md`。

- 首次推送前确认仓库可见性是 private，并限制访问账户和设备。
- 私人仓库只保存状态 Markdown 和 `.gitignore`，不保存插件代码、脚本、原始日志或配置导出。
- 使用 SSH remote（远端地址）：Git 连接仓库的位置，或系统凭据管理器；不要把 token 或密码写进 URL。
- 一旦启用同步，每次查询或更新已保存状态前都必须完成最新检查；先比较远端与本地提交，仅在不一致时执行 `fetch` 与 fast-forward-only（仅快进合并）：只接受远端在现有历史上直线前进的更新。
- 更新后先校验资料，只暂存已知文件，审查 staged diff（暂存差异）：即将提交的具体内容，再使用普通推送。
- 新设备完成 clone（克隆）后，在 POSIX 平台恢复目录 `0700`、文件 `0600` 权限；其他平台使用等效访问控制。
- 仓库隐私无法确认、远端不匹配、历史分叉、校验失败或推送被拒绝时必须停止，不能强制推送。
- 最新检查失败时停止，不继续使用本地副本回答已保存状态。

私人仓库仍不能保存任何凭据。Git 历史也需要单独审查，不能只检查当前文件。

## 两类资料的边界

| 私人网络状态 | 项目状态卡与过程卡 |
|---|---|
| 结构化、可复用的设备与连接事实 | 面向人阅读的动作收尾摘要 |
| 保存在独立私人目录 | 保存在当前项目文档目录 |
| 可包含操作所必需的私人端点 | 默认只引用设备、服务和配置别名 |
| 不保存聊天过程或完整日志 | 不复制完整清单、拓扑或原始配置 |
| 通过 `validate_profile.py` 校验 | 通过内容分离检查和敏感信息扫描 |

状态卡只回答“现在是什么状态”；过程卡只回答“按什么技术路线实现，以及以后从哪里排查”。

## 校验

在仓库根目录运行插件和三个 skill 的结构校验：

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

测试私人资料初始化与校验：

```bash
python3 plugin/network-state-closeout/skills/network-state/scripts/init_profile.py \
  --path /tmp/network-state-closeout-test

python3 plugin/network-state-closeout/skills/network-state/scripts/validate_profile.py \
  --path /tmp/network-state-closeout-test
```

通过校验不代表私人资料可以直接同步。每次提交、推送或写卡后仍需人工检查。

启用同步时，校验器还会强制检查 `.gitignore`、远端别名、默认分支和 `required-before-query-and-update` 同步策略；同步关闭时，这些字段必须保持未启用状态。

## 隐私边界

不要保存或写入卡片：

- 密码、token、API key、私钥、认证密钥或 cookie；
- 恢复码、一次性验证码、登录二维码、订阅链接或含凭据的 URL；
- 完整配置导出、原始日志、命令流水或个人仓库历史。

主机名、地址、域名、用户名、拓扑、服务版本和验证时间仍属于敏感资料。卡片只提取完成收尾所需的最少内容。

## 版本状态

当前版本已经具备插件清单、初始化引导 skill、日常网络状态 skill、状态卡与过程卡 skill、独立 GitHub 私人同步引导模块、强制最新检查、内容模板和本地校验能力。安装时接入用户选定的插件市场即可。

## 许可证

本项目使用 [MIT License](LICENSE)，允许在保留版权和许可声明的前提下使用、复制、修改和分发。
