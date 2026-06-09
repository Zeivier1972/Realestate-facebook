import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FB_APP_ID")
APP_SECRET = os.getenv("FB_APP_SECRET")
USER_TOKEN = os.getenv("FB_USER_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")
PAGE_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("FB_AD_ACCOUNT_ID")

BASE = "https://graph.facebook.com/v25.0"


def _get(path, params=None, token=None):
    params = params or {}
    params["access_token"] = token or USER_TOKEN
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


def _post(path, data, token=None):
    data["access_token"] = token or PAGE_TOKEN
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=encoded, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def get_page_info():
    return _get(f"/{PAGE_ID}", {"fields": "id,name,fan_count,link"}, PAGE_TOKEN)


def get_page_access_token():
    """Exchange user token for a page access token."""
    result = _get("/me/accounts", token=USER_TOKEN)
    for page in result.get("data", []):
        if page["id"] == PAGE_ID:
            return page["access_token"]
    raise ValueError(f"Page {PAGE_ID} not found in your accounts.")


def post_to_page(message, link=None, scheduled_time=None):
    """Post a message (and optional link) to the Facebook Page."""
    data = {"message": message}
    if link:
        data["link"] = link
    if scheduled_time:
        data["scheduled_publish_time"] = scheduled_time
        data["published"] = "false"
    return _post(f"/{PAGE_ID}/feed", data)


def create_photo_post(image_url, caption):
    """Post a photo with a caption to the page."""
    data = {"url": image_url, "caption": caption}
    return _post(f"/{PAGE_ID}/photos", data)


def get_page_posts(limit=10):
    """Get recent posts from the page."""
    return _get(f"/{PAGE_ID}/feed", {"limit": limit, "fields": "id,message,created_time,permalink_url"}, PAGE_TOKEN)


def get_ad_accounts():
    return _get("/me/adaccounts", {"fields": "id,name,account_status,currency"})


def get_campaigns():
    return _get(f"/{AD_ACCOUNT_ID}/campaigns", {
        "fields": "id,name,status,objective,daily_budget,lifetime_budget",
        "limit": 25
    })


def create_campaign(name, objective="OUTCOME_LEADS", daily_budget_cents=5000, status="PAUSED"):
    """
    Create a campaign. daily_budget_cents is in cents (5000 = $50.00).
    Objectives: OUTCOME_LEADS, OUTCOME_TRAFFIC, OUTCOME_AWARENESS, OUTCOME_SALES
    """
    data = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": json.dumps(["HOUSING"]),  # required for real estate
        "daily_budget": str(daily_budget_cents),
    }
    return _post(f"/{AD_ACCOUNT_ID}/campaigns", data)


def pause_campaign(campaign_id):
    return _post(f"/{campaign_id}", {"status": "PAUSED"})


def enable_campaign(campaign_id):
    return _post(f"/{campaign_id}", {"status": "ACTIVE"})
