""" Prompt Client"""

from typing import Optional
from uuid import UUID

from modelhub.models.prompts import (
    CreatePrompt,
    CreatePromptVersion,
    Prompt,
    PromptVersion,
    PromptWithVersion,
    UpdatePrompt,
    UpdatePromptVersion,
)

from ..core import BaseClient
from ..utils import setup_logger

logger = setup_logger(__name__)

NO_PROMPT_FOUND = "No Prompt Found"


class PromptClient(BaseClient):
    """Client for managing prompts."""

    async def create_prompt(self, prompt: CreatePrompt) -> PromptWithVersion:
        """
        Creates a new prompt and stores it in the database.

        Args:
            prompt (PromptCreate): The prompt data to be stored.
        Returns:
            Prompt: The newly created prompt object.
        Raises:
            HTTPException: If the prompt creation fails or an error occurs while interacting with the database.
        """

        endpoint = "prompts"
        return self.post(endpoint=endpoint, json=prompt)

    async def add_prompt_version(
        self, prompt_version: CreatePromptVersion, prompt_name: str
    ) -> PromptVersion:
        """
        Adds a new version to an existing prompt in the database.

        Args:
            prompt_version (CreatePromptVersion): The details of the new prompt version.
            prompt_name (str): The name of the existing prompt.

        Returns:
            PromptVersion: The newly created prompt version.

        Raises:
            HTTPException: If the prompt does not exist or the version creation fails.
        """
        endpoint = f"prompts/{prompt_name}"
        return self.post(endpoint=endpoint, json=prompt_version)

    async def get_prompts(self, prompt_type: Optional[str] = None) -> list[Prompt]:
        """
        Retrieves all prompts from the database.

        Returns:
            list[Prompt]: A list of all stored prompt objects.
        """
        endpoint = "prompts"
        if prompt_type:
            endpoint = f"prompts?prompt_type={prompt_type}"
        return self.get(endpoint=endpoint)

    async def get_prompt_versions(
        self, prompt_name: Optional[str] = None
    ) -> list[PromptVersion]:
        """
        Retrieves all versions of a given prompt.

        Args:
            prompt_name (Optional[str]): The name of the prompt. If None, retrieves all versions.

        Returns:
            list[PromptVersion]: A list of all versions of the specified prompt.

        Raises:
            HTTPException: If the prompt does not exist.
        """
        endpoint = f"prompts/versions?prompt_name={prompt_name}"
        return self.get(endpoint=endpoint)

    async def get_prompt_version(
        self, prompt_name: str, version: Optional[str] = None
    ) -> Optional[PromptVersion]:
        """
        Retrieves a specific version of a given prompt, or the latest version if none is specified.

        Args:
            prompt_name (str): The name of the prompt.
            version (Optional[str]): The specific version to fetch. If None, retrieves the latest version.

        Returns:
            PromptVersion: The requested prompt version.

        Raises:
            HTTPException: If the prompt or version is not found.
        """
        endpoint = f"prompts/{prompt_name}/version"
        if version:
            endpoint = f"{endpoint}?version={version}"
        return self.get(endpoint=endpoint)

    async def get_prompt(self, prompt_id: UUID) -> Optional[Prompt]:
        """
        Retrieves a specific prompt by its ID.

        Args:
            prompt_id (UUID): The unique identifier of the prompt.

        Returns:
            Prompt | None: The found prompt object, or raises an exception if not found.

        Raises:
            HTTPException: If the prompt is not found in the database.
        """
        endpoint = f"prompts/id/{prompt_id}"
        return self.get(endpoint=endpoint)

    async def get_prompt_by_name(self, name: str) -> Optional[Prompt]:
        """
        Retrieves a specific prompt by its name.

        Args:
            name (str): The unique name of the prompt.

        Returns:
            Prompt | None: The found prompt object, or None if not found.
        """

        endpoint = f"prompts/name/{name}"
        return self.get(endpoint=endpoint)

    async def update_prompt(self, prompt_id: str, prompt: UpdatePrompt) -> Prompt:
        """
        Updates an existing prompt in the database.

        Args:
            prompt_id (UUID): The unique identifier of the prompt to update.
            prompt (UpdatePrompt): The updated prompt data.

        Returns:
            Prompt: The updated prompt object.

        Raises:
            HTTPException: If the prompt is not found or the update fails.
        """
        endpoint = f"prompts/{prompt_id}"
        return self.patch(endpoint=endpoint, json=prompt)

    async def update_prompt_version(
        self,
        prompt_name: str,
        update_prompt_version: UpdatePromptVersion,
        version: Optional[str] = None,
    ) -> PromptVersion:
        """
        Updates an existing prompt version in the database.

        Args:
            prompt_name (str): The name of the prompt.
            updatePromptVersion (UpdatePromptVersion): The updated version data.
            version (Optional[str]): The specific version to update (if not provided, the latest version is updated).

        Returns:
            PromptVersion: The updated prompt version object.

        Raises:
            HTTPException: If the prompt or version is not found, or the update fails.
        """
        # Get existing prompt
        endpoint = f"prompts/{prompt_name}/version"
        if version:
            endpoint = f"{endpoint}?version={version}"
        return self.patch(endpoint=endpoint, json=update_prompt_version)

    async def delete_prompt(self, prompt_id: UUID) -> None:
        """
        Deletes a prompt from the database.

        Args:
            prompt_id (UUID): The unique identifier of the prompt to delete.

        Raises:
            HTTPException: If the prompt is not found.
        """
        endpoint = f"prompts/{prompt_id}"
        return self.delete(endpoint=endpoint)

    async def delete_prompt_version(self, prompt_id: UUID, version: str) -> None:
        """
        Deletes a specific version of a prompt from the database.

        Args:
            prompt_id (UUID): The unique identifier of the prompt.
            version (str): The version number to delete.

        Raises:
            HTTPException: If the specified version does not exist.
        """
        endpoint = f"prompts/{prompt_id}/{version}"
        return self.delete(endpoint=endpoint)
