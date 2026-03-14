# Enterprise AI Platform (`ai-platform`)

This repository manages the foundational infrastructure, shared SDKs, and observability sidecars required to run our Agentic AI workloads securely on AWS. 

## 🛠 Prerequisites & CLI Tools

Before you begin, ensure you have the following installed on your local machine:
* **[AWS CLI v2](https://aws.amazon.com/cli/):** For authenticating and interacting with AWS.
* **[Terraform](https://developer.hashicorp.com/terraform/downloads) (v1.5+):** For provisioning infrastructure as code.
* **[Docker Desktop](https://www.docker.com/products/docker-desktop/) or Colima:** For running the local development stack.
* **[PostgreSQL Client (`psql`)](https://www.postgresql.org/download/):** To connect to the database and verify schemas.

## 🔐 AWS Authentication & Environment Variables

For enterprise deployments, we strongly recommend using AWS SSO (Identity Center). However, for this sample application, you can use standard IAM access keys.

Configure your AWS CLI by running `aws configure` or explicitly export the following environment variables:

```bash
export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
export AWS_SESSION_TOKEN="your_session_token" # (If using temporary STS credentials)
export AWS_DEFAULT_REGION="us-east-1"

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