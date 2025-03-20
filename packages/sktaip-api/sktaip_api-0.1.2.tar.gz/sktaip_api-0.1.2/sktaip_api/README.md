# sktaip-api
SKT AIX Platform용 Agent API Server. LangGraph 기반의 코드를 Agent Application으로 Deploy 할 수 있도록 돕는 툴

## 사용 시나리오 
### 1. cli에서 sktaip_api를 사용


### 2. agents_backend package에서 사용
- graph json 파일 -> langgraph compiled graph로 변환
- 변환된 compiled graph의 경로를 import
- sktaip_api docker file로 run