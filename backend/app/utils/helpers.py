from fastapi import HTTPException
from typing import List, Union

def get_extra_from_payload(data: dict) -> dict:
    required_fields = ["status", "prompt", "subTitle", "title", "key"]

    for field in required_fields:
        value = data.get(field)
        if not value:
            raise HTTPException(
                status_code=400, detail=f"{field} is required in the payload"
            )

    return {
        "dynamic": True,
        "dynamicFields": data.get("dynamicFields", []),
        "meta_data": data,
        "language": data.get("language"),
        "tone": data.get("tone"),
        "GPTVersion": data.get("GPTVersion"),
        "submitButtonText": data.get("submitButtonText"),
    }


def keywords_to_list(keywords: Union[str, List[str]]) -> List[str]:
    if isinstance(keywords, list):
        return keywords
    if isinstance(keywords, str):
        # Accept comma-separated, space-separated or single string
        return [kw.strip() for kw in keywords.split("\n") if kw.strip()]
    return []


# pore kaj ache, after generating the content
def create_post_task(user, keywords, payload, destination, post_type, PostStatus):
    common_args = {
        "user": user,
        "keywords": keywords,
        "payload": payload,
        "post_type": post_type,
        "_status": PostStatus.QUEUE,
        "total": len(keywords),
    }

    if destination == "wordpress":
        common_args["site_id"] = payload.get("selected_website")
    elif destination == "blogger":
        common_args["blogger_site_id"] = payload.get("blogger_site")
    elif destination == "medium":
        common_args["medium_id"] = payload.get("medium_site")
    elif destination == "webhook":
        common_args["webhook_id"] = payload.get("webhook_id")

    return common_args