import json
from models import SeasonModel
from etl.prompts import build_extraction_prompt
from google import genai
from pydantic import BaseModel, Field
from google.genai import types
import os

file_path='./result_test.txt'
api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found. Did you create a .env file?")



def extract_data(wiki_text, franchise, season_number):

    client = genai.Client(api_key=api_key)
    print("Sending request to Gemini...")
    prompt = build_extraction_prompt(wiki_text,short_code=franchise.name,season_number=season_number,title = franchise.title)
    #prompt = "Generate a 3-digit number for me"
    response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
    #print (response.text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    # extracted_data = json.loads(response.text)
    # with open(file_path, "w", encoding="utf-8") as f:
    #     json.dump(extracted_data, f, indent=4, ensure_ascii=False)  
    
    # try:
    #     # 2. Generate a response from the model
    #     response = client.models.generate_content(
    #         model='gemini-2.5-flash',
    #         contents=f"Extract the show statistics from this text:\n\n{wiki_text}",
    #         config=types.GenerateContentConfig(
    #             response_mime_type="application/json",
    #             response_schema=SeasonModel,
    #             temperature=0.1, # Low temperature ensures strict adherence to facts in the text
    #         ),
    #     )


        
    # except Exception as e:
    #     print("\n--- Something went wrong ---")
    #     print(f"Error details: {e}")
