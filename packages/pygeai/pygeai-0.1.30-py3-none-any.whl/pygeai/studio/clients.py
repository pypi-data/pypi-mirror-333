import json
from typing import Any, Union

from pygeai.core.base.clients import BaseClient
from pygeai.studio.endpoints import CREATE_AGENT_V2


class AIStudioClient(BaseClient):

    def create_agent(
            self,
            name: str,
            access_scope: str,
            public_name: str,
            job_description: str,
            avatar_image: str,
            description: str,
            agent_data_prompt: dict,
            agent_data_llm_config: dict,
            agent_data_models: list
    ) -> dict:
        data = {
            "agentDefinition": {
                "name": name,
                "accessScope": access_scope,
                "publicName": public_name,
                "jobDescription": job_description,
                "avatarImage": avatar_image,
                "description": description,
                "agentData": {
                    "prompt": agent_data_prompt,
                    "llmConfig": agent_data_llm_config,
                    "models": agent_data_models
                }
            }
        }
        response = self.api_service.post(
            endpoint=CREATE_AGENT_V2,
            data=data
        )
        print(f"response: {response}")
        result = json.loads(response.content)
        return result

