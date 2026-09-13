# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Hoàng Thái Đạt  
> **Mã Sinh Viên / Mã Học viên:** 2A202602959
> **Chủ đề Lựa chọn:** Trợ lý phân tích tài chính 

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** |5 / 5 | Bài toán có yêu cầu chia nhỏ nhiều bước suy luận nối tiếp nhau không? |
| **2. Tool Interaction** |5 / 5 | Hệ thống có cần kết nối với MCP Server / Cơ sở dữ liệu bên ngoài không? |
| **3. Dynamic Decision** |5 / 5 | Bước tiếp theo có phụ thuộc vào kết quả quan sát bước trước không? |
| **4. Long Horizon Goal** |5 / 5 | Hệ thống có phải giữ mục tiêu xuyên suốt qua nhiều lượt xử lý không? |
| **TỔNG ĐIỂM AGENTIC FIT** | **20 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu giá hiện tại của cổ phiếu VIC, nếu P/E dưới 15 thì đặt lệnh mua 50 cổ phiếu ở mức giá hiện tại.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "fetch_stock_info",
    "arguments": {
      "ticker": "VIC"
    },
    "observation": {
      "status": "SUCCESS",
      "ticker": "VIC",
      "data": {
        "company_name": "Tập đoàn Vingroup",
        "sector": "Bất động sản",
        "current_price": 42500,
        "pe_ratio": 12.3,
        "pb_ratio": 1.9,
        "roe": 8.5,
        "market_cap": "145.200 tỷ VNĐ",
        "status": "Đang giao dịch"
      }
    },
    "latency_ms": 984.14
  },
  {
    "step": 2,
    "query": "Hãy tra cứu giá hiện tại của cổ phiếu VIC, nếu P/E dưới 15 thì đặt lệnh mua 50 cổ phiếu ở mức giá hiện tại.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "place_order",
    "arguments": {
      "ticker": "VIC",
      "order_type": "buy",
      "quantity": 50,
      "price": 42500
    },
    "observation": {
      "status": "SUCCESS",
      "order_id": "ORD-VIC-50-99",
      "ticker": "VIC",
      "order_type": "buy",
      "quantity": 50,
      "price": 42500,
      "total_value": 2125000,
      "message": "Đặt lệnh Mua thành công: 50 cổ phiếu VIC với giá 42,500 VNĐ/cp. Tổng giá trị: 2,125,000 VNĐ."
    },
    "latency_ms": 933.72
  },
  {
    "step": 3,
    "query": "Hãy tra cứu giá hiện tại của cổ phiếu VIC, nếu P/E dưới 15 thì đặt lệnh mua 50 cổ phiếu ở mức giá hiện tại.",
    "action_type": "FINAL_ANSWER",
    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Giá hiện tại của cổ phiếu VIC là 42,500 VNĐ và chỉ số P/E của nó là 12.3, dưới mức 15. Do đó, tôi đã đặt lệnh mua 50 cổ phiếu VIC với giá 42,500 VNĐ/cp.\n\nThông tin giao dịch:\n- Lệnh mua: 50 cổ phiếu VIC\n- Giá mỗi cổ phiếu: 42,500 VNĐ\n- Tổng giá trị: 2,125,000 VNĐ\n\nLệnh mua đã được thực hiện thành công.",
    "latency_ms": 1439.42
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
