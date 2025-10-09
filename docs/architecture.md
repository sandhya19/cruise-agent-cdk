# Cruise & Stay Quote Agent – Architecture

Below is the high-level system flow showing how different AWS services interact.

```mermaid
graph TD
  A[User in Browser] -->|POST /quote| B[API Gateway]
  B --> C[Lambda: Planner Function]
  C -->|Invoke Model| D[Amazon Bedrock - Claude 3 Sonnet]
  C -->|Read/Write| E[DynamoDB: AgentLogs Table]
  C -->|Send Email| F[Amazon SES]
  C -->|Generate Price| G[Quote Tool (local Python module)]
  H[S3 Static Website] -->|Frontend UI| A
  subgraph AWS Cloud
    B
    C
    D
    E
    F
    G
  end
```