# Agent Harness Bootstrap

简体中文 | [English](README.md)

为新项目或已有项目建立小而可执行的工程 Harness（工程护栏）。

本项目包含仓库审计工具和一个可安装的 Codex Skill，用分层方式把项目约定转化为工程契约：

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
- 用于按包分发的 Codex Plugin 清单；
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

在 Codex 中让内置安装器直接从 GitHub 安装：

```text
使用 $skill-installer 从以下地址安装 bootstrap-project-harness Skill：
https://github.com/Mr-CG-end/agent-harness-bootstrap/tree/main/skills/bootstrap-project-harness
```

如果希望锁定到当前版本，请把 URL 中的 `main` 替换为 `v0.1.0`。也可以手动把 `skills/bootstrap-project-harness` 复制到 Codex Skills 目录；手动安装后需重启或重新加载 Codex，再输入：

```text
使用 $bootstrap-project-harness 为这个仓库建立最小工程 Harness。
```

仓库同时提供 `.codex-plugin/plugin.json`，可作为 Codex Plugin 分发。在进入公开插件目录前，直接从 GitHub 安装独立 Skill 是最直接的社区安装方式。

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
