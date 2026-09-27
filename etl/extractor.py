import json
from models import SeasonModel
from etl.prompts import build_extraction_prompt
from google import genai
from pydantic import BaseModel, Field
from google.genai import types
import os
from pathlib import Path

import re


file_path='./result_test.txt'
CACHE_LOCATION = Path("data/extracted")

api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found. Did you create a .env file?")


def strip_code_fences(text: str) -> str:
    """
    Remove markdown code fences (```json ... ``` or ``` ... ```) that LLMs
    sometimes wrap around JSON output, despite being instructed not to.

    Args:
        text: Raw text response from the LLM.

    Returns:
        Text with surrounding code fences removed, if present.
    """
    text = text.strip()
    match = re.match(r"^```(?:json)?\s*\n(.*?)\n```$", text, re.DOTALL)
    return match.group(1) if match else text


def _llm_generate_reponse(wiki_text, franchise, season_number):
    
    client = genai.Client(api_key=api_key)
    print("Sending request to Gemini...")
    prompt = build_extraction_prompt(wiki_text,short_code=franchise.name,season_type=franchise.season_type,season_number=season_number,title = franchise.title)
    #prompt = "Generate a 3-digit number for me"
    response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
    
    return strip_code_fences(response.text)
    #print (response.text)
    


#def extract_season_data(wiki_text: str, llm_client, franchise, season_number) -> SeasonModel:

def extract_data(wiki_text, franchise, season_number, use_cache):

    CACHE_LOCATION.mkdir(parents=True, exist_ok=True)
    file_path = CACHE_LOCATION / f"{franchise.name}_S{season_number:02d}_extracted.json"

    if file_path.exists():
        print(f"Read cached extracted data from {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Parse JSON into Python object
                season = SeasonModel(**data)
                return season
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format. {e}")
            raise ValueError(f"LLM returned invalid JSON")
        except PermissionError:
            print(f"Error: Permission denied for file '{file_path}'.")
            raise ValueError(f"permission issuewith JSON")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise ValueError(f"LLM output failed Pydantic validation: {e}")

        return None
        
    
    
    try:
        llm_response = _llm_generate_reponse(wiki_text, franchise, season_number)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(llm_response)
        data = json.loads(llm_response)  # Parse JSON into Python object
        season = SeasonModel(**data)
        return season
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. {e}")
        raise ValueError(f"LLM returned invalid JSON")
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.")
        raise ValueError(f"permission issuewith JSON")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise ValueError(f"LLM output failed Pydantic validation: {e}")


