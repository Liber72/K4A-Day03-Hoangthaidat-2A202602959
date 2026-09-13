# Kịch bản Thuyết trình Demo Day 3: Trợ lý Tài chính AI (ReAct Agent + MCP)

Chào mọi người, sau đây là phần trình bày về project thực hành Day 3: Chuyển đổi từ Chatbot thông thường sang ReAct Agent. 


## 1. Đề tài lựa chọn và Lý do
- **Đề tài:** Xây dựng **Trợ lý Tài chính Chứng khoán thông minh**.
- **Lý do lựa chọn:** 
  Lĩnh vực tài chính chứng khoán là môi trường đặc thù đòi hỏi:
  - **Khả năng thực thi (Action):** Nhà đầu tư không chỉ muốn tra cứu mà còn muốn ra lệnh (ví dụ: "Đặt lệnh mua"). Chỉ có Agent mới có thể kết nối với hệ thống Core Banking / Sàn giao dịch để làm việc này.
## 2. Tại sao ReAct Agent Pattern lại phù hợp? (4 Tiêu chí Agent Fit)
Dự án này hoàn toàn khớp với 4 tiêu chí để áp dụng mô hình Agent (Agent Fit):
1. **Tính phức tạp của tác vụ (Task Complexity):** Yêu cầu của người dùng là chuỗi đa bước (Multi-step). Ví dụ: *"Tra cứu giá cổ phiếu VIC, nếu P/E dưới 15 thì đặt lệnh mua"*.
2. **Tương tác với hệ thống ngoài (External System Interaction):** Agent buộc phải gọi API ra ngoài để lấy giá chứng khoán (External Data) và kết nối với sàn giao dịch để đặt lệnh (External Action).
3. **Tính không thể đoán trước (Unpredictability):** Không thể code cứng logic (if-else) vì người dùng có thể hỏi hàng ngàn mã chứng khoán khác nhau, hoặc hỏi phối hợp nhiều thông tin khác nhau. Agent tự linh hoạt quyết định gọi Tool nào.
4. **Dung sai lỗi (Robustness / Error Tolerance):** Trong tài chính, nếu người dùng nhập sai mã cổ phiếu (vd: XYZ999), Agent sẽ nhận được lỗi từ Tool và tự suy luận, hướng dẫn người dùng nhập lại thay vì bịa ra số liệu.

## 4. Các Tools được xây dựng
Agent được trang bị 2 công cụ chính thông qua MCP Server:
1. **`fetch_stock_info(ticker)`**: 
   - **Công dụng:** Tra cứu dữ liệu tài chính realtime của một mã chứng khoán (Giá hiện tại, chỉ số P/E, P/B, ROE, Vốn hóa).
2. **`place_order(ticker, order_type, quantity, price)`**: 
   - **Công dụng:** Đặt lệnh giao dịch mua/bán (Buy/Sell) cổ phiếu xuống hệ thống sàn giao dịch, tính toán tổng giá trị và trả về mã biên lai (Order ID).

## 5. Demo Trực tiếp & Trace Log

**Kịch bản Demo (Test Case 04 - High Complexity):**
🗣️ **Người dùng:** *"Hãy tra cứu giá hiện tại của cổ phiếu VIC, nếu P/E dưới 15 thì đặt lệnh mua 50 cổ phiếu ở mức giá hiện tại."*

**🔍 Trace Log từng bước (Nhìn thấy trên Web UI):**

- **[Step 1] 🧠 Thought:** Agent nhận thấy cần biết giá và P/E của VIC trước khi quyết định. 
  - **🛠️ Action:** Gọi `fetch_stock_info(ticker="VIC")`
  - **👁️ Observation:** Hệ thống trả về `{"current_price": 42500, "pe_ratio": 12.3 ...}`
- **[Step 2] 🧠 Thought:** Agent phân tích: P/E là 12.3 (thỏa mãn điều kiện < 15). Tiến hành đặt lệnh.
  - **🛠️ Action:** Gọi `place_order(ticker="VIC", order_type="buy", quantity=50, price=42500)`
  - **👁️ Observation:** Đặt lệnh thành công, mã `ORD-VIC-50-99`.
- **[Step 3] 🧠 Thought:** Đã hoàn thành mọi yêu cầu của User.
  - **🏁 Final Answer:** *"Giá hiện tại của cổ phiếu VIC là 42,500 VNĐ và chỉ số P/E của nó là 12.3, dưới mức 15. Do đó, tôi đã đặt lệnh mua 50 cổ phiếu VIC..."*

*(Demo kết thúc bằng việc show ra màn hình Web UI hiển thị chính xác chuỗi suy luận này!)*
