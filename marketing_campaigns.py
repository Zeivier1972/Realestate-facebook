"""
Real Estate Marketing Campaign Templates for Catherine Gomez Realtor
Run this script to create, schedule, and manage Facebook marketing campaigns.
"""

from facebook_client import (
    post_to_page, create_photo_post, get_page_posts,
    create_campaign, get_campaigns, pause_campaign, enable_campaign
)
import json

# ── LISTING POST TEMPLATES ──────────────────────────────────────────────────

def post_new_listing(address, price, beds, baths, sqft, description, image_url=None, link=None):
    message = (
        f"🏡 NEW LISTING — {address}\n\n"
        f"💰 ${price:,}\n"
        f"🛏 {beds} bed | 🛁 {baths} bath | 📐 {sqft:,} sqft\n\n"
        f"{description}\n\n"
        f"📞 Contact Catherine Gomez today for a showing!\n"
        f"#CatherineGomezRealtor #FloridaRealEstate #NewListing #HomesForSale"
    )
    if image_url:
        return create_photo_post(image_url, message)
    return post_to_page(message, link=link)


def post_open_house(address, date, start_time, end_time, price, image_url=None):
    message = (
        f"🚪 OPEN HOUSE — {address}\n\n"
        f"📅 {date}  |  🕐 {start_time} – {end_time}\n"
        f"💰 Listed at ${price:,}\n\n"
        f"Come tour this beautiful home! No appointment needed.\n"
        f"Catherine Gomez will be on site to answer all your questions.\n\n"
        f"#OpenHouse #FloridaRealEstate #CatherineGomezRealtor"
    )
    if image_url:
        return create_photo_post(image_url, message)
    return post_to_page(message)


def post_just_sold(address, price, days_on_market=None):
    days_text = f" in just {days_on_market} days!" if days_on_market else "!"
    message = (
        f"🎉 JUST SOLD — {address}\n\n"
        f"Congratulations to my amazing clients! Closed at ${price:,}{days_text}\n\n"
        f"If you're thinking about buying or selling in Florida, let's talk.\n"
        f"I get results! 💪\n\n"
        f"#JustSold #CatherineGomezRealtor #FloridaRealEstate #ClosingDay"
    )
    return post_to_page(message)


def post_market_update(area, avg_price, homes_sold, avg_days, month_year):
    message = (
        f"📊 {area} Real Estate Market Update — {month_year}\n\n"
        f"📈 Average Sale Price: ${avg_price:,}\n"
        f"🏠 Homes Sold: {homes_sold}\n"
        f"⏱ Average Days on Market: {avg_days}\n\n"
        f"Thinking about buying or selling? The market is moving — let's get you ahead of it!\n"
        f"DM me or call for a free market analysis of YOUR home.\n\n"
        f"#RealEstateMarket #FloridaRealEstate #CatherineGomezRealtor #MarketUpdate"
    )
    return post_to_page(message)


# ── CAMPAIGN CREATION ────────────────────────────────────────────────────────

def create_lead_gen_campaign(name="Realestate Lead Gen", daily_budget=50):
    """Create a Housing-compliant lead generation campaign (PAUSED by default)."""
    result = create_campaign(
        name=name,
        objective="OUTCOME_LEADS",
        daily_budget_cents=daily_budget * 100,
        status="PAUSED"
    )
    print(f"Campaign created: {json.dumps(result, indent=2)}")
    return result


def create_listing_awareness_campaign(name="Listing Awareness", daily_budget=30):
    """Create a reach/awareness campaign for a new listing."""
    result = create_campaign(
        name=name,
        objective="OUTCOME_AWARENESS",
        daily_budget_cents=daily_budget * 100,
        status="PAUSED"
    )
    print(f"Campaign created: {json.dumps(result, indent=2)}")
    return result


# ── QUICK DEMO ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Recent Page Posts ===")
    posts = get_page_posts(5)
    for p in posts.get("data", []):
        print(f"  [{p['created_time']}] {p.get('message','(no text)')[:80]}")

    print("\n=== Active Campaigns ===")
    campaigns = get_campaigns()
    for c in campaigns.get("data", []):
        print(f"  {c['name']} — {c['status']} — {c.get('objective','')}")
