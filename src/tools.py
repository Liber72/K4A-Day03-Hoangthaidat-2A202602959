"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "fetch_stock_info",
        "description": "Tra cứu thông tin tài chính và giá cổ phiếu trên thị trường chứng khoán Việt Nam bằng mã cổ phiếu.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Mã cổ phiếu cần tra cứu (ví dụ: 'FPT', 'VNM', 'VIC')"
                }
            },
            "required": ["ticker"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - ticker (string): Mã cổ phiếu cần giao dịch (ví dụ: 'VNM')
    #    - order_type (string): Loại lệnh: 'buy' (mua) hoặc 'sell' (bán)
    #    - quantity (integer): Số lượng cổ phiếu cần mua/bán
    #    - price (number): Giá đặt lệnh (đơn vị: VNĐ)
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "place_order",
        "description": "Đặt lệnh mua hoặc bán cổ phiếu trên sàn chứng khoán Việt Nam.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Mã cổ phiếu cần giao dịch (ví dụ: 'VNM', 'FPT')"
                },
                "order_type": {
                    "type": "string",
                    "description": "Loại lệnh giao dịch: 'buy' (mua vào) hoặc 'sell' (bán ra)"
                },
                "quantity": {
                    "type": "integer",
                    "description": "Số lượng cổ phiếu cần mua hoặc bán (ví dụ: 100)"
                },
                "price": {
                    "type": "number",
                    "description": "Giá đặt lệnh mỗi cổ phiếu, đơn vị VNĐ (ví dụ: 75000)"
                }
            },
            "required": ["ticker", "order_type", "quantity", "price"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "FPT": {
        "company_name": "Công ty Cổ phần FPT",
        "sector": "Công nghệ thông tin",
        "current_price": 125000,
        "pe_ratio": 18.5,
        "pb_ratio": 4.2,
        "roe": 22.8,
        "market_cap": "168.750 tỷ VNĐ",
        "status": "Đang giao dịch"
    },
    "VNM": {
        "company_name": "Công ty Cổ phần Sữa Việt Nam (Vinamilk)",
        "sector": "Hàng tiêu dùng",
        "current_price": 72000,
        "pe_ratio": 14.2,
        "pb_ratio": 3.8,
        "roe": 28.5,
        "market_cap": "150.480 tỷ VNĐ",
        "status": "Đang giao dịch"
    },
    "VIC": {
        "company_name": "Tập đoàn Vingroup",
        "sector": "Bất động sản",
        "current_price": 42500,
        "pe_ratio": 12.3,
        "pb_ratio": 1.9,
        "roe": 8.5,
        "market_cap": "145.200 tỷ VNĐ",
        "status": "Đang giao dịch"
    }
}


def execute_fetch_stock_info(ticker: str) -> str:
    """Thực thi tra cứu thông tin tài chính theo mã cổ phiếu"""
    stock = MOCK_DATABASE.get(ticker.strip().upper())
    if stock:
        return json.dumps({
            "status": "SUCCESS",
            "ticker": ticker.upper(),
            "data": stock
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu cổ phiếu có mã '{ticker}'"
        }, ensure_ascii=False)


def execute_place_order(ticker: str, order_type: str, quantity: int, price: float) -> str:
    """Thực thi đặt lệnh mua/bán cổ phiếu"""
    order_type_vn = "Mua" if order_type.lower() == "buy" else "Bán"
    total_value = quantity * price
    return json.dumps({
        "status": "SUCCESS",
        "order_id": f"ORD-{ticker.upper()}-{quantity}-99",
        "ticker": ticker.upper(),
        "order_type": order_type.lower(),
        "quantity": quantity,
        "price": price,
        "total_value": total_value,
        "message": f"Đặt lệnh {order_type_vn} thành công: {quantity} cổ phiếu {ticker.upper()} với giá {price:,.0f} VNĐ/cp. Tổng giá trị: {total_value:,.0f} VNĐ."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "fetch_stock_info": execute_fetch_stock_info,
    "place_order": execute_place_order
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
