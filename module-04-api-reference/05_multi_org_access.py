"""
05_multi_org_access.py - Handle multiple organizations and projects
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class MultiOrgManager:
    """Manage API access across multiple organizations"""

    def __init__(self):
        self.organizations = {
            "personal": {
                "api_key": os.getenv("OPENAI_API_KEY_PERSONAL"),
                "org_id": os.getenv("OPENAI_ORG_ID_PERSONAL")
            },
            "work": {
                "api_key": os.getenv("OPENAI_API_KEY_WORK"),
                "org_id": os.getenv("OPENAI_ORG_ID_WORK")
            }
        }

    def get_client(self, org_name):
        """Get client for specific organization"""
        org_config = self.organizations.get(org_name)

        if not org_config:
            raise ValueError(f"Unknown organization: {org_name}")

        return OpenAI(
            api_key=org_config["api_key"],
            organization=org_config.get("org_id")
        )

    def make_request(self, org_name, prompt):
        """Make request using specific organization"""
        client = self.get_client(org_name)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


# Project-specific access
class ProjectManager:
    """Manage API access at project level"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.projects = {
            "chatbot": os.getenv("OPENAI_PROJECT_CHATBOT"),
            "analytics": os.getenv("OPENAI_PROJECT_ANALYTICS"),
            "research": os.getenv("OPENAI_PROJECT_RESEARCH")
        }

    def get_client(self, project_name):
        """Get client for specific project"""
        project_id = self.projects.get(project_name)

        if not project_id:
            raise ValueError(f"Unknown project: {project_name}")

        return OpenAI(
            api_key=self.api_key,
            project=project_id
        )


# Usage example
multi_org_guide = """
MULTI-ORGANIZATION ACCESS:

Setup:
1. Create separate API keys for each org
2. Store in separate environment variables
3. Use organization-specific clients

Environment Variables:
OPENAI_API_KEY_PERSONAL=sk-proj-...
OPENAI_ORG_ID_PERSONAL=org-...
OPENAI_API_KEY_WORK=sk-proj-...
OPENAI_ORG_ID_WORK=org-...

Project-Level Access:
OPENAI_API_KEY=sk-proj-...
OPENAI_PROJECT_CHATBOT=proj-...
OPENAI_PROJECT_ANALYTICS=proj-...

Benefits:
- Separate billing
- Different rate limits
- Access control
- Usage tracking per org/project

Best Practices:
- Use project keys when possible
- Implement least privilege
- Monitor usage per org/project
- Rotate keys regularly
"""

print(multi_org_guide)
