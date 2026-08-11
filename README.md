# Agent Harness Bootstrap

简体中文 | [English](README.en.md)

为新项目或已有项目建立小而可执行的工程 Harness（工程护栏）。

本项目包含仓库审计工具和一个可安装的 Skill，用分层方式把项目约定转化为工程契约：

1. 简洁的仓库协作说明；
2. 纳入版本控制的事实来源；
3. 确定性的格式、Lint、类型、测试、构建和产物检查；
4. 单一的本地验证入口；
5. 复用同一验证入口的 CI；
6. 可选的本地 Hooks；
7. 明确的人工授权与验收边界。

默认工作流从只读审计开始：先了解目标仓库，给出最小且适用的 Harness 方案，只有在用户授权实施后才修改文件。

## 当前状态

`0.1.0` 版本是一套可用的早期基础，目前提供：

- 零依赖、只读的仓库审计器；
- 默认预览、不会覆盖文件的 `AGENTS.md` 生成器；
- 可移植的 `bootstrap-project-harness` Skill；
- 面向 Codex 与 Claude Code 的分发清单；
- 面向 JavaScript/TypeScript、Python、Rust、Go、JVM、.NET、Ruby 和 PHP 项目的选择指南；
- 覆盖打包工具的测试和跨平台 CI。

它不会自动创建远端仓库、修改分支保护、安装 Hooks、管理密钥、部署、提交或推送。

## 快速开始

只读审计目标仓库：

```shell
python skills/bootstrap-project-harness/scripts/audit_repo.py /path/to/repository
```

输出适合程序处理的 JSON：

```shell
python skills/bootstrap-project-harness/scripts/audit_repo.py /path/to/repository --json
```

只预览最小仓库契约，不修改文件：

```shell
python skills/bootstrap-project-harness/scripts/generate_harness.py /path/to/repository
```

确认方案后创建缺失的 `AGENTS.md`：

```shell
python skills/bootstrap-project-harness/scripts/generate_harness.py /path/to/repository --apply
```

生成器绝不会覆盖已有文件，也不会凭空编造项目尚不具备的格式化、Lint、测试、构建、CI 或 Hooks 配置。

### 安装 Skill

Skill 本身与具体工具无关，可用于 Codex、Claude Code，或任何读取 `SKILL.md` 的编码代理。

**Codex** —— 让内置安装器直接从 GitHub 安装：

```text
使用 $skill-installer 从以下地址安装 bootstrap-project-harness Skill：
https://github.com/Mr-CG-end/agent-harness-bootstrap/tree/main/skills/bootstrap-project-harness
```

如果希望锁定到当前版本，请把 URL 中的 `main` 替换为 `v0.1.0`。安装后输入 `$bootstrap-project-harness` 调用。

**Claude Code** —— 添加插件市场并安装：

```text
/plugin marketplace add Mr-CG-end/agent-harness-bootstrap
/plugin install agent-harness-bootstrap@agent-harness
```

安装后的完整命令为 `/agent-harness-bootstrap:bootstrap-project-harness`；未与其他命令重名时，直接输入 `/bootstrap-project-harness` 也可调用。

**手动安装** —— 把 `skills/bootstrap-project-harness` 整个目录复制到代理的 Skills 目录（Claude Code 为 `~/.claude/skills/`），然后重启或重新加载代理。

调用后可以这样描述需求：

```text
为这个仓库建立最小工程 Harness。
```

仓库同时提供 `.codex-plugin/plugin.json` 与 `.claude-plugin/marketplace.json` 两份分发清单，位于各自目录，互不影响。

## 参与开发

仓库没有第三方运行时依赖，需要 Python 3.10 或更高版本。

```shell
python scripts/verify.py
```

贡献规则见 [CONTRIBUTING.md](CONTRIBUTING.md)，版本记录见 [CHANGELOG.md](CHANGELOG.md)，首版产品边界见 [docs/v0.1-plan.md](docs/v0.1-plan.md)。

## 设计原则

- 修改前先检查。
- 复用项目原生工具链。
- 优先用可执行检查表达约束。
- 维护一份规范的仓库契约。
- 本地验证和 CI 使用同一入口。
- Hooks 用于缩短反馈，不作为强制边界。
- 权限和远端操作由人控制。
- 默认只预览生成结果，不覆盖已有项目契约。

## 许可证

使用 Apache License 2.0，详见 [LICENSE](LICENSE)。
