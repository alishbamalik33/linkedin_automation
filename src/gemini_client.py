"""Gemini client for Aipply.

Uses Gemini to analyze job descriptions and generate:
- Tailored professional summary
- Relevant competencies
- Cover letter
"""

import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

load_dotenv()


class GeminiClient:
    """Client for generating job application materials with Gemini."""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}

        gemini_config = self.config.get("gemini", {})

        self.model = gemini_config.get(
            "model",
            "gemini-3.8-flash",
        )

        self.temperature = gemini_config.get(
            "temperature",
            0.7,
        )

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Add it to your .env file."
            )

        self.client = genai.Client(api_key=api_key)

        logger.info("Gemini client initialized with model: %s", self.model)

    def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self.temperature,
            ),
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        return response.text.strip()

    def generate_job_materials(
        self,
        job_description: str,
        candidate_profile: dict[str, Any],
        company: str,
        role: str,
    ) -> dict[str, Any]:
        """Generate tailored resume content and cover letter."""

        prompt = f"""
You are an AI assistant helping prepare a job application.

IMPORTANT RULES:
- Use ONLY information present in the candidate profile.
- Do NOT invent experience, education, certifications, projects,
  technologies, achievements, years of experience, or job responsibilities.
- Tailor the application to the job description.
- Keep the writing professional and realistic.
- Do not claim that the candidate has experience they do not have.
- Do not mention that AI was used to generate the materials.

CANDIDATE PROFILE:
{json.dumps(candidate_profile, indent=2)}

COMPANY:
{company}

JOB ROLE:
{role}

JOB DESCRIPTION:
{job_description}

Generate the following:

1. A professional summary suitable for the target role.
2. A list of 8 relevant competencies/skills selected from the candidate's
   actual profile.
3. A professional cover letter of approximately 250-350 words.

Return ONLY valid JSON in exactly this structure:

{{
    "summary": "professional summary here",
    "competencies": [
        "skill 1",
        "skill 2",
        "skill 3",
        "skill 4",
        "skill 5",
        "skill 6",
        "skill 7",
        "skill 8"
    ],
    "cover_letter": "cover letter here"
}}
"""

        response_text = self.generate_text(prompt)

        # Remove possible markdown code fences.
        cleaned = response_text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        if cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.error("Gemini returned invalid JSON: %s", response_text)
            raise ValueError(
                "Gemini returned invalid JSON."
            ) from exc

        required_fields = [
            "summary",
            "competencies",
            "cover_letter",
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(
                    f"Gemini response is missing required field: {field}"
                )

        return result