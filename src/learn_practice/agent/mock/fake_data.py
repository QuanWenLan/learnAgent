WEATHER_DATA = {
    "北京": {
        "weather": "晴",
        "temperature": 30,
        "advice": "紫外线较强，出门注意防晒。"
    },
    "上海": {
        "weather": "多云",
        "temperature": 27,
        "advice": "早晚温差不大，适合轻便出行。"
    },
    "深圳": {
        "weather": "阵雨",
        "temperature": 29,
        "advice": "建议随身带伞，注意短时降雨。"
    }
}

ORDER_DATA = {
    "A1001": {
        "status": "已发货",
        "logistics": "顺丰快递",
        "eta": "明天 18:00 前送达"
    },
    "A1002": {
        "status": "退款中",
        "logistics": "暂无",
        "eta": "预计 2 个工作日到账"
    },
    "A1003": {
        "status": "已签收",
        "logistics": "京东物流",
        "eta": "已于昨天 15:20 签收"
    }
}

DOC_DATA = [
    {
        "title": "Agent 分层设计概览",
        "summary": "介绍意图识别、skill 路由、function call 和 MCP 接入的分层思路。"
    },
    {
        "title": "Function Call 入门",
        "summary": "说明如何定义工具 schema、参数结构与执行器。"
    },
    {
        "title": "MCP 工具接入指南",
        "summary": "说明如何把外部工具统一封装为标准接口供 Agent 使用。"
    }
]

KNOWLEDGE_BASE = {
    "agent": "Agent 通常由路由、记忆、工具、模型和执行循环组成。",
    "skill": "Skill 是面向某类任务的能力封装，通常内部会编排多个步骤。",
    "function call": "Function call 是模型触发工具调用的一种机制，强调函数定义和参数结构。",
    "mcp": "MCP 是统一外部工具接入方式的协议思路，方便模型和工具解耦。"
}
