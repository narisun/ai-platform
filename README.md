# Enterprise AI Platform (`ai-platform`)

This repository manages the foundational infrastructure, shared SDKs, and observability sidecars required to run our Agentic AI workloads securely on AWS. 

## 🛠 Prerequisites & CLI Tools

Before you begin, ensure you have the following installed on your local machine:
* **[AWS CLI v2](https://aws.amazon.com/cli/):** For authenticating and interacting with AWS.
* **[Terraform](https://developer.hashicorp.com/terraform/downloads) (v1.5+):** For provisioning infrastructure as code.
* **[Docker Desktop](https://www.docker.com/products/docker-desktop/) or Colima:** For running the local development stack.
* **[Ollama](https://ollama.com/):** For running local models (e.g., Llama 3) to test agent routing without incurring cloud costs.
* **Python 3.10+**: For testing the Shared SDK locally.

---

## 📊 Observability Setup (Dynatrace & OpenTelemetry)

We use OpenTelemetry (OTel) to trace agent decisions, tool calls, and LLM latency, exporting directly to Dynatrace. To run the local stack, you need to configure your Dynatrace credentials.

### Dynatrace API token
1. Go to Dynatrace → Access tokens (Settings → Access tokens, or search "Access tokens").
2. Find the token used in your OTel collector config (or generate a new one).
3. Click Edit and add the scope: `openTelemetryTrace.ingest` (Ingest OpenTelemetry traces) and `metrics.ingest` (Ingest metrics).
4. Save, then copy the updated token.

Set your environment variables in your terminal:
```bash
# Windows (CMD)
set DYNATRACE_ENDPOINT=https://<your-tenant-id>.live.dynatrace.com
set DYNATRACE_API_TOKEN=<your_updated_token>

# Mac/Linux
export DYNATRACE_ENDPOINT="https://<your-tenant-id>.live.dynatrace.com"
export DYNATRACE_API_TOKEN="<your_updated_token>"

```

---

## 💻 Local Development Environment Setup

To maximize development velocity and environment parity, our local stack runs the exact same LiteLLM gateway and OTel collector as production, but routes LLM traffic to a local Ollama instance instead of AWS.

1. **Start your local model:** Open a separate terminal and run:
```bash
ollama run llama3

```


2. **Start the local platform stack:** Navigate to the `local-dev` folder and spin up the database, Redis cache, LiteLLM proxy, and OTel collector:
```bash
cd local-dev
docker-compose up -d

```


3. **Verify the services:** * **LiteLLM Proxy:** `http://localhost:4000`
* **OTel Collector:** `http://localhost:4318`
* **pgvector Database:** `localhost:5432`



---

## 🧪 Testing the Local Setup

You can test that the `shared_sdk` successfully routes traffic through the local LiteLLM proxy, hits your local Ollama model, and exports the trace to Dynatrace.

1. Install the required Python dependencies:
```bash
pip install openai opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-openai

```


2. Run the test script:
```bash
python test_local.py

```


3. **Verify in Dynatrace:** Go to **Applications & Microservices** → **Distributed Traces** in your Dynatrace console. You should see a trace for the `ai-platform-local-agent` service containing the exact prompt and latency.

---

## ☁️ AWS Bedrock Setup (For Cloud/Prod Deployment)

When migrating from local Ollama to AWS Bedrock, ensure your AWS account has model access enabled.

1. Navigate to **Amazon Bedrock** in the AWS Console.
2. Go to the **Model catalog** (left menu).
3. Select the required model (e.g., **Claude 3 Haiku** or **Titan Text G1 - Express**) and click **Open in playground**.
4. *(Anthropic Only)* AWS will prompt you to submit use-case details. Fill out the form and submit. Access is granted instantly across the account.

Ensure your IAM Role has the following permission:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        }
    ]
}

```

---

## 🚀 Provisioning AWS Infrastructure (Terraform)

When you are ready to provision the cloud infrastructure (RDS PostgreSQL with pgvector):

1. Navigate to the RDS terraform directory:
```bash
cd infra/terraform/rds

```


2. Initialize and Apply:
```bash
terraform init
terraform apply -var="db_password=YourSecurePassword123!"

```


## Folder Structure

```
ai-platform/
├── infra/
│   ├── terraform/
│   │   ├── eks/                 # EKS cluster & Karpenter definitions
│   │   ├── rds/                 # PostgreSQL + pgvector provisioning
│   │   └── iam/                 # IRSA roles and least-privilege policies
│   └── kubernetes/
│       ├── litellm/             # LiteLLM proxy deployment manifests
│       └── observability/       # OTel collector and Dynatrace sidecars
├── shared-sdk/
│   ├── python/
│   │   ├── auth/                # JWT and AWS IAM authentication helpers
│   │   └── tracing/             # OpenTelemetry auto-instrumentation wrappers
└── README.md
```