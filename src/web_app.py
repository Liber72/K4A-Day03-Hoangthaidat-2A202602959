"""
🌐 WEB APPLICATION - Flask Frontend cho ReAct Agent Trợ lý Tài chính
Giao diện web đẹp cho Agent, hiển thị Thought → Action → Observation → Final Answer
"""

import json
import os
import sys
import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_server import MCPFinanceServer
from prompts import (
    CHATBOT_BASELINE_PROMPT,
    REACT_AGENT_SYSTEM_PROMPT,
    MAX_ITERATIONS
)
from providers import get_llm_provider

load_dotenv()

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))

# Khởi tạo Provider và MCP Server
provider = get_llm_provider()
mcp_server = MCPFinanceServer()

# Phương án 2: Lưu trữ lịch sử chat In-Memory (Backend)
SESSION_STORE = {}
MAX_HISTORY_TURNS = 5  # Nhớ tối đa 5 lượt hỏi đáp gần nhất


def run_react_agent_web(user_query: str, session_id: str = "default") -> dict:
    """
    Chạy ReAct Agent và trả về kết quả dạng structured cho frontend
    Hỗ trợ nạp lịch sử hội thoại từ SESSION_STORE
    """
    step = 0
    trace_steps = []
    tools_list = mcp_server.list_tools()
    
    # Lấy lịch sử cũ
    history = SESSION_STORE.get(session_id, [])
    history_context = ""
    if history:
        history_context = "=== LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY ===\n"
        for turn in history:
            history_context += f"User: {turn['user']}\nAgent: {turn['agent']}\n"
        history_context += "===================================\n\n"

    # Augmented prompt ban đầu = Lịch sử (nếu có) + Câu hỏi hiện tại
    augmented_prompt = f"{history_context}Câu hỏi hiện tại: {user_query}"
    final_answer = ""

    while step < MAX_ITERATIONS:
        step += 1
        step_start_time = time.time()

        llm_response = provider.generate_with_tools(
            augmented_prompt, tools_list, system_prompt=REACT_AGENT_SYSTEM_PROMPT
        )
        latency_ms = round((time.time() - step_start_time) * 1000, 2)
        thought = llm_response.get("thought", "Đang suy luận...")

        # Trường hợp 1: Final Answer
        if llm_response.get("type") == "text":
            final_answer = llm_response.get("content", "")
            trace_steps.append({
                "step": step,
                "type": "FINAL_ANSWER",
                "thought": thought,
                "content": final_answer,
                "latency_ms": latency_ms
            })
            break

        # Trường hợp 2: Tool Call
        elif llm_response.get("type") == "tool_call":
            tool_name = llm_response.get("tool_name")
            arguments = llm_response.get("arguments", {})

            mcp_result = mcp_server.call_tool(tool_name, arguments)
            obs_data = mcp_result.get("result", {})
            obs_str = json.dumps(obs_data, ensure_ascii=False)

            trace_steps.append({
                "step": step,
                "type": "TOOL_CALL",
                "thought": thought,
                "tool_name": tool_name,
                "arguments": arguments,
                "observation": obs_data,
                "latency_ms": latency_ms
            })

            if not obs_data:
                final_answer = "MCP Server trả về rỗng."
                break

            # Nạp observation trở lại prompt
            augmented_prompt += (
                f"\n\n--- KẾT QUẢ TỪ HỆ THỐNG TRẢ VỀ Ở BƯỚC {step} ---\n"
                f"Công cụ đã gọi: {tool_name}\n"
                f"Kết quả (Observation): {obs_str}\n"
                f"-----------------------------------------\n"
                f"HƯỚNG DẪN: Dựa trên kết quả trên, hãy tiếp tục thực hiện yêu cầu. "
                f"CHÚ Ý: Bạn PHẢI sử dụng công cụ (Tool) nếu cần thực hiện hành động tiếp theo (ví dụ đặt lệnh). KHÔNG tự ý viết ra text [Action]. Nếu đã hoàn thành toàn bộ yêu cầu, hãy đưa ra câu trả lời cuối cùng."
            )

    # Lưu vào lịch sử sau khi hoàn tất
    if final_answer:
        if session_id not in SESSION_STORE:
            SESSION_STORE[session_id] = []
        SESSION_STORE[session_id].append({"user": user_query, "agent": final_answer})
        # Giữ lại số lượt quy định
        if len(SESSION_STORE[session_id]) > MAX_HISTORY_TURNS:
            SESSION_STORE[session_id].pop(0)

    return {
        "query": user_query,
        "final_answer": final_answer,
        "trace_steps": trace_steps,
        "total_steps": len(trace_steps),
        "provider": provider.__class__.__name__
    }


def run_baseline_chatbot_web(user_query: str, session_id: str = "default") -> dict:
    """Chạy Chatbot Baseline và trả về kết quả (Có tính năng nhớ)"""
    start = time.time()
    
    # Xử lý lịch sử
    history = SESSION_STORE.get(session_id, [])
    history_context = ""
    if history:
        history_context = "=== LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY ===\n"
        for turn in history:
            history_context += f"User: {turn['user']}\nAgent: {turn['agent']}\n"
        history_context += "===================================\n\n"

    full_prompt = f"{history_context}Câu hỏi hiện tại: {user_query}"
    
    response = provider.generate(full_prompt, system_prompt=CHATBOT_BASELINE_PROMPT)
    latency_ms = round((time.time() - start) * 1000, 2)
    
    # Lưu vào lịch sử
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = []
    SESSION_STORE[session_id].append({"user": user_query, "agent": response})
    if len(SESSION_STORE[session_id]) > MAX_HISTORY_TURNS:
        SESSION_STORE[session_id].pop(0)

    return {
        "query": user_query,
        "response": response,
        "latency_ms": latency_ms,
        "provider": provider.__class__.__name__
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    query = data.get("query", "").strip()
    mode = data.get("mode", "agent")  # "agent" or "chatbot"
    session_id = data.get("session_id", "default") # Nhận session_id từ frontend

    if not query:
        return jsonify({"error": "Câu hỏi không được để trống"}), 400

    if mode == "chatbot":
        result = run_baseline_chatbot_web(query, session_id)
    else:
        result = run_react_agent_web(query, session_id)

    return jsonify(result)


@app.route("/api/test-cases", methods=["GET"])
def api_test_cases():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/info", methods=["GET"])
def api_info():
    return jsonify({
        "provider": provider.__class__.__name__,
        "mcp_server": mcp_server.server_name,
        "version": mcp_server.version,
        "tools": [t["name"] for t in mcp_server.list_tools()]
    })


if __name__ == "__main__":
    print("==========================================================")
    print("📈 FINANCE ASSISTANT — WEB UI")
    print("==========================================================")
    print(f"🔌 LLM Provider: {provider.__class__.__name__}")
    print(f"🌐 MCP Server: {mcp_server.server_name}")
    print(f"🌍 Mở trình duyệt: http://127.0.0.1:5000")
    print("==========================================================")
    app.run(debug=True, port=5000)
