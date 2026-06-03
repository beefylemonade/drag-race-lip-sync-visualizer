EXTRACTION_PROMPT_TEMPLATE = """
You are a data extraction assistant for RuPaul's Drag Race wiki pages.
Extract structured data from the wiki text provided below.

Return ONLY a valid JSON object. No explanation, no markdown, no code fences.

The JSON must follow this exact structure:
{{
    "franchise_short_code": "<one of: US, UK, CA, AU, ES, PH, NL, FR, DU, IT, SE, BE, GE>",
    "season_type":          "<one of: regular, all_stars, vs_the_world, global, other>",
    "season_number":        <integer>,
    "episode_count":        <integer or null>,
    "premiere_date":        "<YYYY-MM-DD or null>",
    "contestants": [
        {{
            "drag_name": "<canonical drag name used this season>",
            "aliases":   ["<other names this queen has competed under in other seasons>"]
        }}
    ],
    "episodes": [
        {{
            "episode_number": <integer>,
            "title":          "<episode title or null>",
            "air_date":       "<YYYY-MM-DD or null>",
            "lip_syncs": [
                {{
                    "order_in_episode": <integer, starting at 1>,
                    "lipsync_type":     "<one of: lipsync_for_your_life, lipsync_for_the_win>",
                    "song": {{
                        "title":   "<song title>",
                        "artists": [
                            {{
                                "name":        "<artist name>",
                                "artist_type": "<one of: primary, featuring>"
                            }}
                        ]
                    }},
                    "participants": [
                        {{
                            "contestant_name": "<drag name as listed in contestants above>",
                            "outcome":         "<one of: win, loss>",
                            "role":            "<one of: contestant, assassin>"
                        }}
                    ]
                }}
            ]
        }}
    ]
}}

Rules:
- Only include episodes that contain at least one lip sync.
- Each lip sync may have any number of participants.
- A lip sync may be between two or more bottom contestants to determine who will be eliminated. In that case, the eliminated queen lost the lip sync.
- If both participants lost the lipsync, the outcome is "loss" for both of them.
- If there is a lipsync, but eliminated None. The outcome is "win" for both of them. 
- A lip sync may be between two ore more top contestants to determine who wins the episode. In that case, the winner of the episode is the winner of the lipsync.
- 
- For a double shantay or double win: both participants have outcome "win".
- For a double sashay: both participants have outcome "loss".
- lipsync_for_your_life: the loser is typically eliminated.
- lipsync_for_the_win: winner win the episode and a prize.
- Assassins are returning queens who lip sync against a current contestant. Mark their role as "assassin".
- contestant_name in participants must exactly match a drag_name in the contestants list.
- song can be null if the wiki page does not mention the song.
- Use ISO 8601 date format (YYYY-MM-DD) for all dates, or null if unknown.
- Do not guess or infer missing data. Mark "NULL - REQUIRE MANUAL CHECK" for missing fields.
- aliases should only list names used in OTHER seasons, not the current season.

Wiki page text:
{wiki_text}
"""

def build_extraction_prompt(wiki_text: str) -> str:
    return EXTRACTION_PROMPT_TEMPLATE.format(wiki_text=wiki_text)