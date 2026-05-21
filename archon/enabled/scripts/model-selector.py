#!/usr/bin/env python3
"""
Xuan Master Enabled Layer — Model Selector Script
Maps a problem description to the best matching model stack from the 52-scene table.

Usage: python3 model-selector.py "team is demotivated and project is delayed"
Output: JSON with recommended model stack, confidence score, and rationale.
"""

import json, re, sys

# Scene-to-model mapping (from xuan-master-enabled SKILL.md + xuan-master entry route)
SCENES = {
    # System & DevOps
    "系统架构设计": {"models": [1, 2, 3, 8, 25], "type": "系统设计", "strategy": "complementary"},
    "故障排查/事故响应": {"models": [3, 5, 17, 24], "type": "故障排查", "strategy": "progressive"},
    "Bug诊断": {"models": [3, 5, 9], "type": "故障排查", "strategy": "progressive"},
    "基础设施/系统韧性": {"models": [25, 1, 2, 8], "type": "系统设计", "strategy": "complementary"},
    "AI系统/AI Agent设计": {"models": [26, 1, 3, 25], "type": "AI设计", "strategy": "complementary"},
    
    # Strategic & Decision
    "商业/产品决策": {"models": [6, 4, 5, 12], "type": "决策", "strategy": "tension"},
    "战略定位/竞争分析": {"models": [18, 14, 5], "type": "战略", "strategy": "progressive"},
    "商业难题分析": {"models": [22, 6, 18, 4], "type": "决策", "strategy": "progressive"},
    "年度/季度战略规划": {"models": [23, 22, 18, 4], "type": "战略", "strategy": "progressive"},
    "投资/并购尽调": {"models": [22, 18, 12, 5], "type": "决策", "strategy": "complementary"},
    "产品价值评估": {"models": [20, 15, 4, 14], "type": "决策", "strategy": "complementary"},
    
    # Learning & Growth
    "深度学习/高效自修": {"models": [19, 11, 7, 16], "type": "个人成长", "strategy": "recursive"},
    "个人知识管理": {"models": [21, 19, 7, 11], "type": "个人成长", "strategy": "complementary"},
    "构建知识体系": {"models": [21, 10, 1, 2], "type": "个人成长", "strategy": "progressive"},
    "个人成长/自我进化": {"models": [26, 19, 11, 21], "type": "个人成长", "strategy": "recursive"},
    "个人韧性/抗风险": {"models": [25, 19, 8, 7], "type": "个人成长", "strategy": "tension"},
    "批判性思维/论证评审": {"models": [19, 5, 14, 6], "type": "个人成长", "strategy": "recursive"},
    
    # AI-Native
    "AI高效协作工作流": {"models": [27, 7, 5, 19], "type": "AI设计", "strategy": "recursive"},
    "AI元认知/反思": {"models": [27, 19, 16, 11], "type": "AI设计", "strategy": "recursive"},
    "AI加速知识学习": {"models": [27, 21, 19, 11], "type": "AI设计", "strategy": "recursive"},
    "人机任务分工设计": {"models": [27, 26, 17, 1], "type": "AI设计", "strategy": "recursive"},
    
    # Team & Communication
    "高效会议/群体讨论": {"models": [20, 19, 12, 14], "type": "团队", "strategy": "complementary"},
    "团队决策/投资评估": {"models": [20, 18, 5, 16], "type": "决策", "strategy": "tension"},
    "团队合作决策": {"models": [12, 11, 9], "type": "团队", "strategy": "complementary"},
    "团队知识传承": {"models": [21, 1, 8, 9], "type": "团队", "strategy": "complementary"},
    "结构化表达与提案": {"models": [22, 20, 14, 5], "type": "团队", "strategy": "complementary"},
    
    # High-frequency
    "重要决策/避免认知偏差": {"models": [16, 5, 6, 19], "type": "决策", "strategy": "recursive"},
    "技术/产品风险评估": {"models": [24, 18, 10, 20], "type": "决策", "strategy": "tension"},
    "业务连续性/灾备规划": {"models": [25, 24, 4, 23], "type": "系统设计", "strategy": "complementary"},
    "OKR体系优化": {"models": [23, 4, 11, 7], "type": "战略", "strategy": "progressive"},
    "项目延期分析": {"models": [5, 4, 17, 9], "type": "项目管理", "strategy": "progressive"},
    "技术债务管理": {"models": [8, 1, 7, 4], "type": "系统设计", "strategy": "tension"},
    "代码质量改进": {"models": [11, 7, 5, 10], "type": "系统设计", "strategy": "complementary"},
    "团队士气提升": {"models": [21, 16, 20, 19], "type": "团队", "strategy": "complementary"},
    "团队冲突化解": {"models": [12, 20, 5, 16], "type": "团队", "strategy": "tension"},
    "个人焦虑/决策困难": {"models": [19, 16, 24, 5], "type": "个人成长", "strategy": "recursive"},
}

# Keyword-to-scene mapping
KEYWORD_MAP = {
    # System/Tech
    ("架构", "设计"): "系统架构设计",
    ("故障", "事故", "宕机", "挂了", "异常"): "故障排查/事故响应",
    ("bug", "错误", "出错"): "Bug诊断",
    ("韧性", "容灾", "高可用", "冗余", "备份"): "基础设施/系统韧性",
    ("ai", "agent", "智能体", "自动化"): "AI系统/AI Agent设计",
    ("代码", "质量", "重构", "review"): "代码质量改进",
    ("技术债", "遗留", "屎山"): "技术债务管理",
    ("延期", "进度", "赶不上", "delay"): "项目延期分析",
    
    # Strategic
    ("产品", "决策", "商业"): "商业/产品决策",
    ("战略", "竞争", "定位"): "战略定位/竞争分析",
    ("投资", "收购", "并购"): "投资/并购尽调",
    ("年度", "季度", "规划", "计划"): "年度/季度战略规划",
    ("okr", "kpi", "目标", "指标"): "OKR体系优化",
    
    # Personal growth
    ("学习", "自学", "效率"): "深度学习/高效自修",
    ("知识管理", "笔记", "文档"): "个人知识管理",
    ("成长", "进化", "提升"): "个人成长/自我进化",
    ("焦虑", "压力", "迷茫", "不知所措"): "个人焦虑/决策困难",
    ("批判", "论证", "思辨"): "批判性思维/论证评审",
    
    # Team
    ("会议", "讨论", "brainstorm"): "高效会议/群体讨论",
    ("士气", "氛围", "motivation"): "团队士气提升",
    ("冲突", "矛盾", "吵架"): "团队冲突化解",
    ("知识传承", "老员工", "交接"): "团队知识传承",
    ("提案", "表达", "汇报"): "结构化表达与提案",
}

def diagnose(problem_text: str) -> dict:
    """
    Given a problem description, return the best matching model stack.
    """
    text_lower = problem_text.lower()
    
    # Score each scene by keyword matches
    scores = {}
    for keywords, scene_name in KEYWORD_MAP.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[scene_name] = score
    
    # Sort by score, take top match
    ranked = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    
    if not ranked:
        return {
            "status": "no_match",
            "message": "No clear scene match. Try BFS-DFS: explore all 6 categories broadly, then narrow down.",
            "suggestion": "Provide more context about the problem type (system/strategy/team/personal/AI)."
        }
    
    best_scene, confidence = ranked[0]
    scene_data = SCENES[best_scene]
    
    # Adjust depth based on model count
    model_count = len(scene_data["models"])
    depth = "deep" if model_count >= 4 else "standard" if model_count >= 2 else "quick"
    
    # Map model numbers to skill names
    model_skills = [f"xuan-master-{m:03d}" for m in scene_data["models"]]
    
    return {
        "status": "match",
        "problem_text": problem_text,
        "scene": best_scene,
        "problem_type": scene_data["type"],
        "confidence": confidence,
        "depth": depth,
        "synthesis_strategy": scene_data["strategy"],
        "model_stack": scene_data["models"],
        "model_skills": model_skills,
        "alternatives": [
            {"scene": alt[0], "confidence": alt[1]}
            for alt in ranked[1:4]
        ] if len(ranked) > 1 else []
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        problem = " ".join(sys.argv[1:])
    else:
        problem = input("Problem: ")
    
    result = diagnose(problem)
    print(json.dumps(result, ensure_ascii=False, indent=2))
