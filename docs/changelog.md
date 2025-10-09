# Change Log – Cruise & Stay Quote Agent

## 2025-10-05
**Project Setup**
- Initialized AWS CDK project in Python.
- Created `core_stack.py` with S3, DynamoDB, and IAM roles.
- Verified local environment and region setup.

## 2025-10-06
**Lambda + API Gateway Integration**
- Built `planner.py` Lambda to connect with Amazon Bedrock (Claude 3 Sonnet).
- Created `/quote` endpoint using API Gateway.
- Deployed first working API returning raw model responses.

## 2025-10-07
**Structured Response + Reasoning**
- Updated prompt for structured JSON output (destination, duration, hotel, price).
- Fixed Bedrock schema errors (`anthropic_version` and role validation).
- Added DynamoDB logging for each request.

## 2025-10-08
**Quote Calculation + Email Integration**
- Added `quote_tool.py` for price generation.
- Added `email_tool.py` using Amazon SES.
- Lambda now generates quote, sends email, and logs results.

## 2025-10-09
**Frontend + Stability**
- Created HTML/JS frontend hosted on S3 bucket.
- Connected frontend to `/quote` API.
- Added `/health` endpoint for status checks.

## 2025-10-10
**Documentation + Optimization**
- Added architecture diagram (`docs/architecture.md`).
- Added cost optimization steps and changelog.
- Reduced token usage in system prompt for cost control.

---

**Current Status:**  
- Working end-to-end AI Agent using AWS Bedrock, Lambda, API Gateway, DynamoDB, and SES.  
- Deployed and live-tested successfully with real structured responses.  
- Total monthly cost estimated under $10.  

---

**Next Improvements (Future Work):**
- Integrate Bedrock AgentCore Browser for supplier verification.
- Add FAISS retrieval for local cruise data.
