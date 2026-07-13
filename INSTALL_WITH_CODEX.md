# 把这个仓库交给 Codex

这份文档写给收到仓库链接的 Agent。目标是把公开组合插件安装到当前 Codex 环境，再引导用户建立自己的全局私人网络状态。

仓库地址：

```text
https://github.com/KEDA-gagaga/network-state-closeout
```

## 为什么采用这种部署方式

网络状态包含两类生命周期完全不同的内容：

- **稳定能力**：分类方式、按需读取、轻量写入、隐私校验、同步门禁和收尾卡片规则。适合放在公开插件中安装和更新。
- **动态私人资料**：真实设备、地址、端口、域名、SSH 路径、Docker 网络、反向代理、虚拟局域网、VPS 和排错结论。只属于用户自己的全局私人 skill。

把两者分开可以让用户放心分享和升级插件，同时避免把真实网络信息带入公开仓库。公开插件负责“怎么读取和维护”；`~/.codex/skills/private-network-state` 负责保存“用户当前的网络是什么样”。

仓库提供 repo marketplace，因此用户只需交给 Codex 一个链接，Agent 就能识别并安装完整插件，不必猜测该复制哪个子目录。插件安装后，私人资料仍在用户设备上的 `.codex/skills` 中生成和维护。

## 收到链接后的 Agent 流程

如果用户只发送了链接但没有表达安装意图，先简要说明这是一个私人网络状态组合插件，并询问是否安装。用户明确要求安装、部署或使用时，继续以下流程。

### 1. 核对公开来源

确认仓库地址、`.agents/plugins/marketplace.json`、`plugin/network-state-closeout/.codex-plugin/plugin.json` 和本文件存在。不要在这个公开仓库中创建或写入用户的私人网络资料。

### 2. 添加仓库插件目录

优先使用当前 Codex 提供的插件命令：

```bash
codex plugin marketplace add KEDA-gagaga/network-state-closeout
codex plugin list --marketplace network-state-closeout
```

如果同名插件目录已经存在，先核对它是否指向本仓库；来源不一致时停止，不要替换。

### 3. 安装完整组合插件

```bash
codex plugin add network-state-closeout@network-state-closeout
```

不要只复制其中一个 skill，也不要把插件仓库当作私人网络资料仓库。

### 4. 开启新任务

安装完成后，提示用户开启一个新的 Codex 任务。新安装的 skill 只保证在新任务中被发现；不要假装当前任务已经加载了它们。

推荐新任务提示词：

```text
$initialize-network-state 帮我初始化全局私人网络状态 skill。先说明可以采集和绝不保存的信息，作出隐私承诺，再征求我同意，通过本机只读检查尽可能补全网络结构。
```

### 5. 执行初始化引导

在新任务中调用 `initialize-network-state`：

1. 默认使用 `~/.codex/skills/private-network-state`，并把它作为唯一修改真源。
2. 先区分可以保存的网络结构与绝不保存的认证秘密。
3. 明确承诺认证秘密不会进入文件、卡片、Git 暂存区、提交历史或远端仓库。
4. 征得用户同意后，才从本机只读来源整理 SSH、Docker、反向代理、虚拟局域网、VPS、路由和 DNS 等结构。
5. 主动扫描、云服务 API、提权读取或登录其他主机必须分别再次授权；获准检查其他主机时优先使用 SSH。
6. 运行私人 skill 校验，并只报告采集类别、剩余缺口和校验结果，不在最终回复中重复私人端点。

### 6. 可选的跨设备共享

只有用户明确需要让多台设备上的 Agent 共享同一份网络资料时，才引导用户准备另一个 GitHub 私人仓库。

- 这个私人仓库保存完整的 `private-network-state` skill。
- 这个公开插件仓库不保存任何用户网络资料。
- 每台设备真正读取和修改的都是自己的 `~/.codex/skills/private-network-state`。
- 其他设备先安装本插件，再把同一个私人仓库克隆到该路径。

## 绝对安全边界

可以在用户同意后保存：主机名、地址、子网、路由、端口、域名、服务角色、访问关系、Docker 网络、反向代理、虚拟局域网、VPS 和验证信号。

绝不能保存：密码、口令、token、API key、私钥内容、VPN 私钥或预共享密钥、cookie、会话、恢复码、一次性验证码、订阅地址、云凭据和含凭据 URL。

需要认证时，只保留身份文件路径、钥匙串条目名、密码管理器条目名、环境变量名或 secret manager 别名。任何认证秘密都不得进入私人 skill、状态卡、过程卡、临时文件、Git 暂存区、提交历史或远端仓库。

## 验收

- `codex plugin list --marketplace network-state-closeout` 能看到插件。
- 插件安装成功，并提示用户开启新任务。
- 新任务可以调用 `$initialize-network-state`。
- 私人 skill 位于 `.codex/skills`，而不是项目目录或 Documents 副本。
- 初始化前已完成隐私说明、承诺和用户授权。
- `validate_profile.py` 校验通过。

## 更新插件

刷新仓库插件目录并重新安装：

```bash
codex plugin marketplace upgrade network-state-closeout
codex plugin add network-state-closeout@network-state-closeout
```

更新完成后开启新任务。

## 官方依据

- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
