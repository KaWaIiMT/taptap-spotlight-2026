# Unity + Agent 工作流

> 本机 Unity CLI 与 MCP 工作流的配置记录,供 Claude Code(及团队)参考。最后更新:2026-09-18。

## 一、Unity CLI(已配置 ✅)

Unity 没有独立的 CLI 安装包,**编辑器可执行文件本身就是 CLI**。已通过包装脚本 `D:\Unity\bin\unity.cmd` 加入用户 PATH,可直接用 `unity` 命令。

- 默认版本:**6000.3.5f2**(Unity 6.3),路径 `E:\Unity editor\Editor\Unity.exe`
- 切换版本:`unity -v <版本>` 或环境变量 `UNITY_VERSION`
- 本机已装版本:
  - 6000.3.5f2 → `E:\Unity editor\Editor\Unity.exe`(默认,无版本子目录)
  - 2022.3.62f2c1 / 2022.3.21f1c1 / 2022.3.3f1c1 / 2023.2.5f1 → `E:\Unity editor\<版本>\Editor\Unity.exe`

常用命令:

```bash
unity -version
unity -batchmode -quit -projectPath "工程路径" -executeMethod MyBuild.Build -logFile -
unity -batchmode -runTests -testPlatform editmode -projectPath "工程路径" -testResults out.xml
```

- `-executeMethod 类名.静态方法` 依赖工程内 `Assets/Editor/` 下的编辑器脚本。
- 批处理(构建/测试/批量资源)无需额外安装,适合 CI 和 agent 自动化。
- 注意:PATH 改动需**新开终端**才生效。

## 二、MCP 实时编辑器控制(待游戏工程创建后启用)

选定方案:**MCP for Unity(CoplayDev/unity-mcp,v10.0.0,免费 MIT)**。
备选:Unity 官方 MCP(需 Unity 6 + AI Assistant 包 + Unity Cloud + AI 工具 beta 订阅,门槛更高)。

前置依赖(本机已满足):
- Python 3.10+ ✅(3.10.14)
- uv ✅(0.11.25)

启用步骤(待游戏工程创建后):
1. 打开 Unity 工程(游戏工程目录,**不是**本管理目录)。
2. 安装包:`openupm add com.coplaydev.unity-mcp`,或 Package Manager → Add package from git URL 填 `https://github.com/CoplayDev/unity-mcp.git`(建议 pin `#v10.0.0`)。
3. `Window → MCP for Unity → Configure All Detected Clients`,自动写入 Claude Code 的 MCP 配置。
4. 首次连接时在 Unity 里批准「待处理连接」。
5. 验证:让 agent 执行「读取 Unity 控制台消息」之类的指令。

MCP 生效后,agent 可直接读写场景/GameObject/Prefab/脚本/Console。

## 三、GitHub 仓库

- 仓库:https://github.com/KaWaIiMT/taptap-spotlight-2026(公开)
- 本地分支 `main`。
- 日常:`git add -A && git commit -m "..." && git push`。

## 四、待办 / 下一步

- [ ] 创建游戏 Unity 工程(比赛 2026-10-01 开始前)
- [ ] 在新工程里装 MCP for Unity 并连通 Claude Code
- [ ] 定游戏概念/主题 → 排期 → 招募
