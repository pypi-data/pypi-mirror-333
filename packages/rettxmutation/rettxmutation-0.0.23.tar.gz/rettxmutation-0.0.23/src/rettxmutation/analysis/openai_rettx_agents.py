import re
import json
import backoff
import logging
import pkg_resources
from typing import List, Tuple
from openai import AzureOpenAI, RateLimitError
from rettxmutation.analysis.models import GeneMutation


logger = logging.getLogger(__name__)


class InvalidResponse(Exception):
    """Custom exception for invalid OpenAI response."""
    def __init__(self,  message: str = "Invalid OpenAI response."):
        self.message = message
        super().__init__(f"{message}")


class OpenAIRettXAgents:
    """
    Handles creating a prompt and calling AzureOpenAI for advanced summarization,
    variant extraction, or other GPT-based tasks.
    """
    def __init__(self, api_key: str, api_version: str, azure_endpoint: str, model_name: str):
        self._client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        self._model = model_name
        self._latest_transcripts = self._load_latest_transcripts()

    def _load_latest_transcripts(self):
        """
        Loads the latest transcripts configuration from a JSON file.

        Parameters:
        - config_path (str): Path to the JSON configuration file.

        Returns:
        - dict: Mapping of base transcript IDs to latest versions.
        """
        resource_path = pkg_resources.resource_filename(__name__, "data/latest_transcript_version.json")

        with open(resource_path, 'r') as file:
            latest_transcripts = json.load(file)
        return latest_transcripts

    # Mutation extractor powered by OpenAI
    @backoff.on_exception(
        backoff.expo,
        (RateLimitError),
        max_tries=5
    )
    def extract_mutations(
        self,
        document_text: str,
        mecp2_keywords: str,
        variant_list: str
    ) -> List[GeneMutation]:
        """
        Example method that constructs a custom system and user prompt,
        then calls AzureOpenAI to generate a summary or extraction.
        """
        try:
            logger.debug("Running analysis with OpenAI")

            system_prompt = (
                "You are an expert in genetics. "
                "You must only extract MECP2 cDNA mutations explicitly mentioned in the provided text. "
                "These mutations are typically in a format like c.916C>T, c.1035A>G or c.1140_1160del. "
                "If you find more than one mutation, list each on a new line in the format:\n\n"
                "transcript:gene_variation;confidence=score\n\n"
                "Examples:\n"
                "1) NM_004992.4:c.916C>T;confidence=1.0\n"
                "2) NM_001110792.1:c.538C>T;confidence=0.8\n"
                "3) NM_004992.4:c.1035A>G;confidence=0.6\n\n"
                "4) NM_004992.4:c.1152_1195del;confidence=1.0\n"
                "If the text only describes a deletion of exons (or no explicit cDNA nomenclature), "
                "then output 'No mutation found'.\n\n"
                "Guidelines:\n"
                "1) Do NOT fabricate or infer cDNA variants from exon-level deletions. "
                "If cDNA notation is not present, respond with 'No mutation found'.\n"
                "2) Use only the transcripts provided in the keywords. "
                "If no transcript is provided, default to NM_004992.4.\n"
                "3) Confidence score must be between 0 and 1.\n"
                "4) Provide no extra commentary beyond the specified format.\n"
            )

            # 2) Build user prompt
            user_prompt = (
                f"Cleaned Text:\n{document_text}\n\n"
                f"Detected Keywords:\n{mecp2_keywords}\n\n"
                f"Detected Variants:\n{variant_list}\n\n"
                "Identify any cDNA mutations (e.g., c.XXXXC>T, c.XXXX_XXXXdel) "
                "related to MECP2 in the text using only the transcripts found in the keywords. "
                "If no valid cDNA mutation is present, return 'No mutation found'."
            )

            logger.debug(f"System Prompt: {system_prompt}")
            logger.debug(f"User Prompt: {user_prompt}")

            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.1,
                n=1,
                stop=None
            )

        except Exception as e:
            logger.error(f"Error generating analysis: {e}")
            raise

        # Send exception if response is empty
        if (
            not response.choices
            or not response.choices[0].message
            or response.choices[0].message.content is None
        ):
            logger.error("No response provided by OpenAI")
            raise InvalidResponse("No response provided by OpenAI")
        logger.debug(f"OpenAI extractor response: {response.choices[0].message.content}")

        # List to store the valid mutations
        list_valid_mutations = []

        # For each line, we need to confirm it's a valid mutation
        for line in response.choices[0].message.content.split("\n"):
            try:
                # Split the line and validate the mutation
                components = line.split(";")
                mutation_info = components[0].strip()
                confidence = float(components[1].split("=")[1])

                logger.debug(f"mutation_info = {mutation_info}")
                logger.debug(f"confidence = {confidence}")

                # Validate the mutation
                mutation = GeneMutation.from_hgvs_string(mutation_info)
                logger.debug(f"Valid mutation found: {mutation.to_hgvs_string()}")

                # Update confidence score
                mutation.confidence = confidence

                # Append the valid mutation to the list
                list_valid_mutations.append(mutation)

            except Exception as e:
                # Invalid mutation found, but keep trying to validate the remaining mutations, if any
                logger.error(f"Invalid mutation found: {line} with exception: {e}")
                continue

        logger.info(f"OpenAI extractor identified {len(list_valid_mutations)} mutations")
        logger.info(f"Mutation list: {list_valid_mutations}")

        # Return the list of valid mutations
        return list_valid_mutations

    # Summarize genetic report powered by OpenAI
    @backoff.on_exception(
        backoff.expo,
        (RateLimitError),
        max_tries=5
    )
    def summarize_report(
        self,
        document_text: str,
        keywords: str
    ) -> str:
        """
        Summarizes a genetic report using OpenAI.

        Args:
            document_text (str): The cleaned OCR text.

        Returns:
            str: The summarized text.
        """
        logger.debug("Running report summarization with OpenAI")

        system_prompt = (
            "You are an expert at summarizing genetic clinical reports. "
            "Output a concise summary focusing on any mention of the MECP2 gene, transcripts "
            "(e.g., NM_004992, NM_001110792), and variants (e.g., c.538C>T). "
            "Ignore unrelated text. "
            "You will be provided with a list of keywords to guide your summary. "
        )

        user_prompt = (
            f"Text to Summarize:\n{document_text}\n\n"
            f"Keywords:\n{keywords}\n\n"
            "Focus on:\n"
            "- Mentions of MECP2 gene\n"
            "- Mentions of transcripts (NM_...)\n"
            "- Mentions of variants (c.XXX...>XXX...)\n"
            "- Key statements that connect them\n"
            "Return 1-3 paragraphs, no more than 300 words total."
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.1,
                n=1,
                stop=None
            )
        except Exception as e:
            logger.error(f"Error generating summary of report: {e}")
            raise

        # Handle empty response
        if (
            not response.choices
            or not response.choices[0].message
            or response.choices[0].message.content is None
        ):
            logger.error("No response provided by OpenAI")
            raise InvalidResponse("No response provided by OpenAI")

        # Return the summary
        logger.debug(f"OpenAI summary response: {response}")
        return response.choices[0].message.content

    # Correct mistakes from a genetic report summary, powered by OpenAI
    @backoff.on_exception(
        backoff.expo,
        (RateLimitError),
        max_tries=5
    )
    def correct_summary_mistakes(
        self,
        document_text: str,
        keywords: str,
        text_analytics: str
    ) -> str:
        """
        Analyzes the summary of a genetic report to find and correct mistakes using OpenAI.

        Args:
            document_text (str): The cleaned OCR text.
            keywords (str): The list of keywords to guide the summary.
            text_analytics (str): The results of the text analytics.

        Returns:
            str: The corrected summary text.
        """
        logger.debug("Running report summarization correction with OpenAI")

        system_prompt = (
            "You are an expert in finding and correcting mistakes in genetic clinical reports. "
            "Your goal is to correct any errors in the provided summary, not to rewrite it. "
            "You will be provided with a summary of a genetic report, a list of keywords to guide the summary, "
            "and the results of text analytics. "
            "Look for any mistakes in the summary and correct them. "
            "You can use the keywords and text analytics results to guide your corrections. "
            "If you detect a mutation incorrectly spelled, correct it (e.g., c538CT -> c.538C>T, c.808C->T -> c.808C>T). "
            "Some mistakes are related with OCR errors (e.g., c.8080>T -> c.808C>T, "
            "mutations need to have nucleotide changes or deletions). "
            f"For transcripts, use the provided list of transcripts to validate the format: {self._latest_transcripts}."
        )

        user_prompt = (
            f"Summary:\n{document_text}\n\n"
            f"Keywords:\n{keywords}\n\n"
            f"Text Analytics:\n{text_analytics}\n\n"
            "Focus on:\n"
            "- Mentions of transcripts (NM_...)\n"
            "- Mentions of variants (c.XXX...>XXX...)\n"
            "Return the same text, with any corrections made."
        )

        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.1,
                n=1,
                stop=None
            )
        except Exception as e:
            logger.error(f"Error during summary correction: {e}")
            raise

        # Handle empty response
        if (
            not response.choices
            or not response.choices[0].message
            or response.choices[0].message.content is None
        ):
            logger.error("No response provided by OpenAI")
            raise InvalidResponse("No response provided by OpenAI")

        # Return the corrected summary
        logger.debug(f"OpenAI summary correction: {response}")
        return response.choices[0].message.content


    # Validate if the document is a valid mutation report
    def validate_document(self, document_text: str) -> Tuple[bool, float]:
        """
        Validates whether a document is a valid mutation report by combining a regex check
        with a GPT-based evaluation. The regex result is provided as context to the GPT agent.
        
        Args:
            document_text (str): The document text to validate.
        
        Returns:
            Tuple[bool, float]: True with confidence if valid; False with confidence if not.
        """
        import re
        from typing import Tuple

        # Step 1: Rule-based check using regex
        mutation_pattern = re.compile(r'c\.\d+(?:[ACGT]>[ACGT]|_\d+del)', re.IGNORECASE)
        transcript_pattern = re.compile(r'NM_\d+\.\d+')
        regex_has_mutation = bool(mutation_pattern.search(document_text))
        regex_has_transcript = bool(transcript_pattern.search(document_text))
        regex_result = regex_has_mutation and regex_has_transcript

        # Prepare a context message about the regex result
        regex_context = (
            "The initial regex check indicates that the document "
            + ("contains" if regex_result else "does not contain")
            + " obvious mutation patterns and transcript identifiers."
        )

        # Step 2: Use GPT to provide a more nuanced evaluation
        system_prompt = (
            "You are an expert in genetics. Evaluate the following text to decide if "
            "it is a valid mutation report describing explicit MECP2 cDNA mutations. "
            f"Consider the following context: {regex_context} "
            "Output a single line exactly in the following format: "
            "'True, confidence=X' if it is valid, or 'False, confidence=X' if it is not, "
            "where X is a float between 0 and 1 representing your confidence."
        )
        user_prompt = f"Text to evaluate:\n{document_text}"

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=50,
                temperature=0.1,
                n=1,
                stop=None
            )
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            return False, 0.0

        answer = response.choices[0].message.content.strip()
        try:
            decision, conf_part = answer.split(",")
            is_valid = decision.strip() == "True"
            confidence = float(conf_part.split("=")[1].strip())
        except Exception as e:
            logger.error(f"Failed to parse validation response '{answer}': {e}")
            return False, 0.0

        return is_valid, confidence
