---
name: optimization
description: "Xuan-Master 认知模型家族的仿生脑自优化流程 — 按自检-自举-自进化-反思四维维护和升级技能家族。含 v2/v3/v4 交叉审计方法(质量分层A/B/C→实战EXCELLENT 27/27)、Unix设计哲学×认知模型映射、使能层感知、P0修复工作流。"
version: 3.1.0
author: Arthur
---

# 🔄 Xuan-Master 优化流程（仿生脑自迭代版 v3.1.0）

> **版本**: 3.1.0 | **基于模型**: 仿生脑(026) | **审计脚本**: `scripts/full_audit.py`

## 核心流程

每次优化/重组按仿生脑的**四维自迭代**执行：

### 🩺 自检（Self-Diagnosis）

#### 标准检查项

```sh
cd ~/.hermes/skills/cognition
```

1. **命名一致性**: 所有 skill 目录名是否 `00-entry-NNN-name` 格式？
2. **Frontmatter 完整性** (9/9): `name`, `icon`, `color`, `version`, `author`, `description`, `tags`, `category`, `related_skills`
3. **Category 分配**: 思辨/方法/系统 三类均衡？
4. **Section 完整性** (7/7): 核心定义/多元领域映射/核心原则/实践要点/典型案例/跨模型关联/实战练习
5. **入口路由**: 版本号、模型数量、场景组合、关联网络是否同步？
6. **跨模型网络**: 每个模型是否有同分类和跨分类引用？
7. **飞书文档**: 是否同步最新版本？

#### 自动化审计（v2.0 新增）

```sh
# 快速摘要模式
python3 scripts/full_audit.py --summary-only

# 完整报告模式
python3 scripts/full_audit.py

# 详细数据模式
python3 scripts/full_audit.py --verbose
```

输出示例：
```
#    KB   Sec Ins Rec  Ref  Cross Ver    Cat
001  6.6   7   13  Y    Y    Y    2.1.0  系统
002  2.7   5    1  N    Y    N    1.0.0  系统
...
```

#### Pi 系列版本完整性检查（v2.0 新增）

**问题**: 每次 P 系列改进后，如果从 Git 恢复旧版本，改进会丢失。
**规则**: 每完成一个 P 改进，立即在 Git 中打 tag。
**检查命令**：
```sh
cd ~/.hermes/skills
git tag -l 'v4.*'
git log --oneline -10
```

对每个 Pi 改进，验证 tag 是否存在：
- v4.2.0-P0: P0 阶段完成
- v4.2.0-P1: P1 阶段完成
- v4.3.0: P2 阶段完成
...

如果 tag 不存在 → 未打 tag 的改进在下一次 git restore 中会丢失。

#### Git restore 后完整性校验步骤（v2.0 新增）

执行 `git restore --source=COMMIT -- ...` 后**必须**执行：

```sh
cd ~/.hermes/skills/cognition

# 1. 确认所有文件有换行符（不是单行文件）
for d in 00-entry-*/; do
  lines=$(wc -l < "${d}SKILL.md")
  [ "$lines" -lt 5 ] && echo "⚠️ ${d}: only $lines lines — likely corrupted!"
done

# 2. 确认所有文件有 frontmatter（以 --- 开头）
for d in 00-entry-*/; do
  f="${d}SKILL.md"
  head -1 "$f" | grep -q "^---" || echo "⚠️ ${d}: no frontmatter!"
done

# 3. 自动化审计
python3 scripts/full_audit.py --summary-only
```

### 🚀 自举（Bootstrapping）

**⚡ 第一步：备份（每批量操作前必做）**
```sh
cd ~/.hermes/skills
cp -r cognition/ cognition-backup-$(date +%Y%m%d_%H%M)/
# 或快速 git snapshot
git add -A && git commit -m "snapshot before [action]"
```

批量编辑 3+ 个文件前必须备份。现场恢复（session DB）是最后手段，不是常规流程。

#### 1. 统一目录命名
```sh
cd ~/.hermes/skills/cognition
mv 00-entry-layered-architecture 00-entry-001-layered-architecture
# ... 以此类推
```

#### 2. 补齐 Frontmatter
使用 `patch` 工具：
```python
from hermes_tools import patch
patch(path="SKILL.md", old_string="author: Arthur\ntags:",
      new_string='author: Arthur\nicon: 🏗️\ncolor: "#6366F1"\nrelated_skills: [...]\ntags:')
```

#### 3. Pi 改进保护策略（v2.0 新增）
每完成一个 Px 阶段后，立即执行：
```sh
cd ~/.hermes/skills
git add -A && git commit -m "Px complete: [简述做了什么]"
git tag v4.x.y-Px
python3 ~/.hermes/scripts/git-snapshot.py --message "Px complete snapshot"
```

这样即使后续操作从旧 commit restore，也能通过 cherry-pick 或 tag 差异找回。

### 🌱 自进化（Evolution）

#### 交叉审计方法论演进（v2 → v3）

| 审计 | 版本 | 发现问题层次 | 修复层次 | 参与模型 |
|------|------|------------|---------|:---:|
| v1 | v4.2.0 | "有谁没有frontmatter？有谁没有跨模型关联？" | 补缺失section | 8 |
| v2 | v4.3.x | "有谁实战练习是占位符？有谁场景推荐缺失？" | 扩容+补场景+批量补关联 | 8 |
| **v3** | **v4.5.0** | **"有谁的实战练习是真正可用的？跨模型关联是结构化的还是扁平的？"** | **质量升级：实战练习从MINIMAL/NONE→EXCELLENT (27/27)** | **全27** |
| **v4** | **v4.5.0-enabled-unix** | **"Unix 设计哲学如何映射到认知模型？如何注入使能层？"** | **使能层v1.1.0: Unix原则驱动(设计哲学+Policy/Mechanism+管道+降级+数据驱动)** | **全27 + Unix** |

#### v3 质量层级分类（A/B/C 三级）

审计进化到 v3 后，不再只检查"有没有section"，而是评估内容的质量层级：

| 层级 | 实战练习质量 | 特征 | 审计标准 |
|:---:|------|------|------|
| **A级** | EXCELLENT | 含4级结构化实战（初级→中级→高级→反思），每级有具体操作步骤 | 可直接使用——读完就能练 |
| **B级** | MINIMAL | 有实战练习但只有2-3行泛泛文本（"用这个模型分析问题""反思""下周试用"） | 有但无法落地 |
| **C级** | NONE | 完全没有实战练习section | 读完就结束了 |

#### v3 P0 修复工作流（TOP6→B-batch→C-batch 三层递进）

审计发现 A/B/C 三层质量断层后，按以下顺序修复：

**第1层 — TOP6 个体精修** (帕累托优先: 引用频率最高的薄弱模型):
1. 019 元认知（入门推荐 + 11个场景引用）
2. 007 迭代（入门推荐 + 9个场景引用）
3. 016 双系统（6个场景引用）
4. 021 SECI（6个场景引用 + 知识管理高频）
5. 026 仿生脑（总控模型 + 5个场景引用）
6. 008 熵增（6个场景引用）

每个个体精修产出：4级结构化实战练习，内容针对该模型的核心概念量身定制，非模板填充。

**第2层 — B级批量升级** (MINIMAL→GOOD):
004/005/006/010/012/013/014/015/017/018/027 — 11个模型，用精准但高效的4级实战框架替换原有2-3行占位文本。内容需要适配模型但有统一结构要求。

**第3层 — C级补基础** (NONE→GOOD):
020/022/023/024/025 — 5个模型，在无实战练习的位置注入4级结构化框架。

#### 实战练习质量标尺

| 等级 | 标准 | 判定条件 |
|------|------|---------|
| **EXCELLENT** | 初级+中级+高级+反思 四个层级，每层≥3行具体指导 | `"初级" in content and "中级" in content and "高级" in content and "反思" in content` |
| **GOOD** | 至少3个层级有实质内容 | 3/4层存在且非占位 |
| **BASIC** | 至少1个层级有实质内容 | 1-2层存在 |
| **NONE** | 无实战练习section | 无"实战练习"关键词 |

**目标**: 全部27模型达到 EXCELLENT（v4.5.0 已达成）。

**每个模型视角的典型问题**：

| 模型 | 视角 | 典型发现 |
|------|------|---------|
| 005 逆向 | 新人视角 | "入口路由画大饼，点进去发现内容不足" |
| 002 流动 | 瓶颈分析 | "哪个模型被引用最多但内容最薄" |
| 003 状态机 | 非法转移 | "reading→bored：没有实战练习就没有出路" |
| 008 熵增 | 退化分析 | "从上次commit至今的退化过程" |
| 016 双系统 | 系统1/2偏差 | "Halo Effect：入口路由好看但内部模型空洞" |
| 019 元认知 | 审计自身的反思 | "被审计的模型也是审计工具" |
| 012 博弈论 | 策略选择 | "合作博弈 vs 逐个精修" |
| 020 六顶帽 | 多维度评估 | 白帽(事实)/红帽(直觉)/黑帽(风险)/黄帽(机会)/绿帽(创意)/蓝帽(过程) |
| 021 SECI | 知识转化 | "审计过程本身就是SECI循环" |
| 024 RICE | 治疗优先级 | RICE分数排序 |

#### 2. 分类体系设计
```
思辨类（Philosophy & Cognition）：抽象推理、世界观
方法类（Method & Execution）：结构化操作、流程
系统类（System & Engineering）：动态交互、工程韧性
```

#### 3. 场景组合分级
```
基础场景（5-6 类）：系统设计 / 战略决策 / 学习成长 / 团队沟通 / 高频场景
每类 5-7 个具体场景，每个场景 3-5 个模型组合
```

#### 4. 关联网络强化
```
同分类关联（强）：思辨↔思辨、方法↔方法、系统↔系统
跨分类关联（桥）：思辨→方法、方法→系统
```

### 🧬 Unix 设计哲学集成 (v4 新增)

#### 10 原则 × Xuan Master 映射

Unix 设计哲学与 Xuan Master 认知模型存在深层同构——两者本质上都是关于 **如何应对复杂性** 的方法论。完整映射参考 `enabled/references/unix-design-philosophy-mapping.md`。

在设计和优化使能层时，以下映射是决策依据：

| Unix 原则 | 对应认知模型 | 使能层应用 |
|----------|------------|-----------|
| 模块原则 | 001分层 · 010奥卡姆 | 每个模型独立加载、独立产出 |
| 组合原则 | 002流动 · 021SECI | 管道模式: 模型A→B→C串行精炼 |
| 一切皆文件 | 003状态机 · 001分层 | 统一接口: context+depth→finding+principle_map |
| 清晰原则 | 006第一性原理 · 016双系统 | 可见推理: 每个结论标注模型+原则 |
| 分离原则 | 001分层 | Phase 1 Policy/Mechanism分离 |
| 简洁原则 | 010奥卡姆 · 009最小阻力 | 轻量外壳: 不增加新内容,只编排 |
| 透明原则 | 011反馈循环 · 003状态机 | 中间状态对外可见 |
| 健壮原则 | 025高可用 · 008熵增 | L1→L2→L3三级降级 |
| 表示原则 | (数据驱动进化) | 学习记录→反向优化模型选择 |
| 最小意外 | 009最小阻力 | 模板标准化,同类问题格式一致 |

#### 使能层设计检查项

优化使能层时，用 Unix 原则逐条自检：
- [ ] 是否每个能力只做一件事（模块）？
- [ ] 是否支持管道组合（组合）？
- [ ] 模型间是否有统一调用接口（一切皆文件）？
- [ ] Phase 1 是否显式分离了 Policy 和 Mechanism（分离）？
- [ ] 是否有降级策略（健壮）？
- [ ] 是否有学习记录支持数据驱动优化（表示）？

### ⚡ 使能层感知 (v4 新增)

`enabled/` 是认知内核之上的执行力外壳，现归属于 `Archon`。技能家族现在包括三层：

```
应用层    → 具体问题→具体产出
Prism专家层 → 领域路由与专门化映射
Archon使能层 → 5-phase协议 (诊断→执行→合成→产出→反馈)
Xuan Master内核层 → 27个认知模型
```

优化内核层模型时需更新使能层：
- 新增模型 → 更新 `enabled/SKILL.md` 的映射表
- 场景→模型映射变化 → 更新 `references/problem-diagnosis-guide.md`
- 模型质量提升 → 不需要改使能层（内核变好=使能层自动受益）

#### 1. 重构入口路由 SKILL.md
- 按三大分类重新组织模型表格
- 场景组合加入图标前缀
- 关联网络分为"同分类"和"跨分类"两栏

#### 2. 重建飞书文档
```python
# 删除旧文档（需 ?type=docx 参数）
curl -X DELETE "https://open.feishu.cn/open-apis/drive/v1/files/{doc_id}?type=docx" \
  -H "Authorization: Bearer {token}"

# 设置公开权限
curl -X PATCH "https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_id}/public?type=docx" \
  -H "Authorization: Bearer {token}" \
  -d '{"external_access_entity":"open","security_entity":"anyone_can_view"}'
```

#### 3. 更新 Memory
- 记录新版本号、模型数量、分类统计
- 记录新飞书文档 ID

#### 4. 最终 Git 保护
```sh
cd ~/.hermes/skills
git add -A && git commit -m "00-entry v{version}: [简要描述改进]"
git tag v{version}
# 运行自动化验证
python3 scripts/full_audit.py --summary-only
```

## 已知陷阱

| 陷阱 | 表现 | 解决 |
|------|------|------|
| 目录重命名后 skill 无法加载 | skill_manage 缓存的路径变成旧的 | 重启 Hermes 或等缓存刷新 |
| 飞书文档 API 特殊字符 400 | →、← 等箭头符号导致 batch 失败 | 用 ->、<- 替代 |
| 飞书不能删除中间 block | 只能追加或重建 | 直接删除旧档重建新文档 |
| **patch 返回 `?` 状态不可靠** | `patch()` 返回 `{'status': '?'}` 但实际修改成功 | 用 `read_file` 或 `grep` 验证 |
| **批处理脚本提前 break/return** | 文件只写入了前半部分 | 写入后 assert 目标内容存在 |
| **行号污染的源文件** | 文件开头是 `     1|---` 而非 `---` | 从 `read_file` 输出的带行号格式被直接写入文件所致。修复：`sed -i 's/\s*[0-9]\+\|//g' SKILL.md`，然后 `cat -A` 验证换行符存在 |
| **无备份的批量编辑风险** | 27 个文件截断后只能从 session DB 恢复 | 每批量操作前 `cp -r cognition/ cognition-backup/` |
| **session DB 有 14 天保留期** | 超过保留期的内容无法恢复 | 重要里程碑后立即 git commit + tag |
| **Git restore 丢失 Pi 改进** | P1/P2 的改进在 restore 后消失 | 每完成 Px 立即打 tag；restore 后用 full_audit.py 校验 |
| **Pi 系列不连续** | v4.2.0 跳回到 v4.2.0-P1 时中间有 gap | 版本号用 v4.x.y 递增，Pi 改进用 git tag 记录 |

## 工具清单

| 脚本/文件 | 用途 | 路径 |
|-----------|------|------|
| `recover_from_session.py` | 从 session JSONL 恢复截断文件 | `scripts/recover_from_session.py` |
| `full_audit.py` | 全家族 27 模型自动化审计扫描 | `scripts/full_audit.py` |
| `v3-audit-summary.md` | v3 交叉审计摘要 — 质量分层/修复工作流/结果 | `references/v3-audit-summary.md` |
| `git-snapshot.py` | 快速 Git snapshot + 日期标记 | `~/.hermes/scripts/git-snapshot.py` |

## Session 灾难恢复流程

详见 `scripts/recover_from_session.py`。当 SKILL.md 被截断且无 git 备份时的最后手段。

## 版本记录

- 2026.05.19: v1.1 — 增加批处理陷阱(session DB恢复流程/备份推荐/文件截断验证)
- 2026.05.19: v1.2 — 恢复脚本增加 patch new_string 提取支持；自举阶段增加"第一步：备份"；增加 patch ? 状态陷阱说明
- 2026.05.19: **v2.0** — 新增: full_audit.py 审计脚本、交叉审计方法论(12 模型视角)、Pi 系列版本标记保护规则、Git restore 后完整性校验步骤、行号污染文件修复方法、工具清单表格
