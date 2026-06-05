"""
Lead Generation Campaign — Cutler Bay to Kendall Buyers
Catherine Gomez Realtor
"""

import os, json, urllib.request, urllib.parse
from dotenv import load_dotenv

load_dotenv()

PAGE_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")
AD_ACCOUNT_ID = os.getenv("FB_AD_ACCOUNT_ID")
BASE = "https://graph.facebook.com/v25.0"


def _post_api(path, data, token=None):
    data["access_token"] = token or PAGE_TOKEN
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=encoded, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}


def _get_api(path, params=None, token=None):
    params = params or {}
    params["access_token"] = token or PAGE_TOKEN
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}


# ── AD COPY VARIANTS (A/B test these) ───────────────────────────────────────

AD_COPY = {
    "variant_a": {
        "headline": "No HOA. No CDD. Your Dream Home Awaits.",
        "body": (
            "🏡 4 & 5 Bedroom Homes — Cutler Bay to Kendall\n\n"
            "✅ NO HOA fees\n"
            "✅ NO CDD fees\n"
            "✅ Seller pays ALL closing costs\n"
            "✅ Low interest rates available\n"
            "✅ Priced from $380K to $1.4M\n\n"
            "Stop paying HOA every month. Own MORE, pay LESS.\n"
            "Click below to see available homes — no obligation!"
        ),
        "cta": "See Available Homes"
    },
    "variant_b": {
        "headline": "Save $400/Month — No HOA, No CDD in South Miami-Dade",
        "body": (
            "💰 Why pay HOA when you don't have to?\n\n"
            "Beautiful 4 & 5 bedroom homes from Cutler Bay to Kendall:\n"
            "🏠 $380,000 – $1,400,000\n"
            "🚫 No HOA • 🚫 No CDD\n"
            "🎁 ALL closing costs covered by seller\n"
            "📉 Low interest rate options available\n\n"
            "These homes go FAST. Get your list today!"
        ),
        "cta": "Get My Home List"
    },
    "variant_c": {
        "headline": "Seller Pays Closing Costs — 4/5 BR Homes Cutler Bay–Kendall",
        "body": (
            "¿Buscas casa en South Miami-Dade? 🏡\n\n"
            "Casas de 4 y 5 habitaciones disponibles:\n"
            "📍 Cutler Bay · Palmetto Bay · Pinecrest · Kendall\n"
            "💵 Desde $380K hasta $1.4M\n"
            "🚫 Sin HOA · Sin CDD\n"
            "✅ Vendedor paga todos los gastos de cierre\n"
            "📉 Tasas de interés bajas disponibles\n\n"
            "¡Contáctame hoy para ver opciones!"
        ),
        "cta": "Ver Casas Disponibles"
    }
}

# ── AUDIENCE TARGETING ───────────────────────────────────────────────────────

AUDIENCE_CONFIG = {
    "name": "South Miami-Dade Home Buyers 380K-1.4M",
    "geo": {
        "cities": [
            "Cutler Bay, FL",
            "Palmetto Bay, FL",
            "Pinecrest, FL",
            "Kendall, FL",
            "Sunset, FL",
            "Richmond Heights, FL",
            "South Miami, FL",
            "Homestead, FL"
        ],
        "radius_miles": 10
    },
    "age_min": 28,
    "age_max": 65,
    "interests": [
        "Real estate",
        "Home buying",
        "Mortgage",
        "First-time home buyer",
        "Zillow",
        "Realtor.com",
        "Home improvement",
        "Single-family home"
    ],
    "behaviors": [
        "Likely to move",
        "First-time homebuyer",
        "Active home shopper"
    ],
    "income_targeting": "Top 25-50% household income",
    "languages": ["English", "Spanish"]
}

# ── CAMPAIGN CREATION ────────────────────────────────────────────────────────

def create_lead_gen_campaign():
    """Create the main lead gen campaign (HOUSING category required for real estate)."""
    data = {
        "name": "Cutler Bay–Kendall Home Buyers | No HOA No CDD",
        "objective": "OUTCOME_LEADS",
        "status": "PAUSED",
        "special_ad_categories": json.dumps(["HOUSING"]),
        "daily_budget": "5000",  # $50/day — adjust before activating
    }
    result = _post_api(f"/{AD_ACCOUNT_ID}/campaigns", data, token=os.getenv("FB_USER_ACCESS_TOKEN"))
    print("Campaign:", json.dumps(result, indent=2))
    return result.get("id")


def create_ad_set(campaign_id):
    """Create ad set with South Miami-Dade targeting."""
    targeting = {
        "geo_locations": {
            "cities": [
                {"key": "2421836", "name": "Cutler Bay", "region": "Florida", "country": "US"},
                {"key": "2421835", "name": "Palmetto Bay", "region": "Florida", "country": "US"},
                {"key": "2421810", "name": "Pinecrest", "region": "Florida", "country": "US"},
                {"key": "2421798", "name": "Kendall", "region": "Florida", "country": "US"},
                {"key": "2421808", "name": "South Miami", "region": "Florida", "country": "US"},
            ],
            "location_types": ["home", "recent"]
        },
        "age_min": 28,
        "age_max": 65,
        "locales": [6, 23],  # English, Spanish
        "interests": [
            {"id": "6003263680692", "name": "Real estate"},
            {"id": "6003206382714", "name": "Mortgage loan"},
            {"id": "6002925741482", "name": "Home"},
        ]
    }
    data = {
        "name": "South Miami-Dade Buyers 28-65 EN/ES",
        "campaign_id": campaign_id,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LEAD_GENERATION",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "daily_budget": "5000",
        "targeting": json.dumps(targeting),
        "status": "PAUSED",
    }
    result = _post_api(f"/{AD_ACCOUNT_ID}/adsets", data, token=os.getenv("FB_USER_ACCESS_TOKEN"))
    print("Ad Set:", json.dumps(result, indent=2))
    return result.get("id")


def create_lead_form():
    """Create a lead gen form to capture buyer info."""
    questions = [
        {"type": "FULL_NAME"},
        {"type": "EMAIL"},
        {"type": "PHONE"},
        {"type": "CUSTOM", "label": "What is your home buying timeline?",
         "options": [
             {"value": "asap", "key": "ASAP — Ready now"},
             {"value": "3months", "key": "1–3 months"},
             {"value": "6months", "key": "3–6 months"},
             {"value": "exploring", "key": "Just exploring"},
         ]},
        {"type": "CUSTOM", "label": "What price range are you considering?",
         "options": [
             {"value": "380_600", "key": "$380K – $600K"},
             {"value": "600_900", "key": "$600K – $900K"},
             {"value": "900_1400", "key": "$900K – $1.4M"},
         ]},
    ]
    data = {
        "name": "Home Buyer Lead Form — No HOA No CDD",
        "locale": "en_US",
        "questions": json.dumps(questions),
        "privacy_policy": json.dumps({"url": "https://yourfloridahomeforyou.com/privacy"}),
        "thank_you_page": json.dumps({
            "title": "Thanks! I'll be in touch shortly.",
            "body": "Catherine Gomez will contact you within 24 hours with your personalized home list.",
            "cta_type": "VIEW_WEBSITE",
            "cta_link": "https://yourfloridahomeforyou.com"
        }),
        "context_card": json.dumps({
            "title": "Find Your Perfect Home — No HOA, No CDD",
            "content": [
                "4 & 5 bedroom homes from $380K–$1.4M",
                "No HOA fees • No CDD fees",
                "Seller pays ALL closing costs",
                "South Miami-Dade: Cutler Bay to Kendall"
            ],
            "button_text": "Get My Free Home List"
        })
    }
    result = _post_api(f"/{PAGE_ID}/leadgen_forms", data)
    print("Lead Form:", json.dumps(result, indent=2))
    return result.get("id")


def post_organic_teaser():
    """Post an organic teaser to the page to warm up the audience."""
    message = (
        "🚨 Are you still paying HOA every month? You don't have to!\n\n"
        "I have 4 & 5 bedroom homes from Cutler Bay to Kendall with:\n\n"
        "🚫 NO HOA\n"
        "🚫 NO CDD\n"
        "✅ Seller pays ALL closing costs\n"
        "✅ Low interest rates available\n"
        "🏡 Priced from $380,000 to $1,400,000\n\n"
        "These homes are going fast in today's market. DM me or comment "
        "\"INFO\" below and I'll send you the full list! 👇\n\n"
        "#NoCatherineGomezRealtor #NoHOA #NoCDD #SouthMiamiDade "
        "#CutlerBay #Kendall #HomesForSale #FloridaRealEstate "
        "#CasasEnVenta #MiamiCasas"
    )
    result = _post_api(f"/{PAGE_ID}/feed", {"message": message})
    print("Organic post:", json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    print("Creating campaign...")
    campaign_id = create_lead_gen_campaign()

    if campaign_id and "error" not in str(campaign_id):
        print(f"\nCampaign ID: {campaign_id}")
        print("\nCreating ad set...")
        adset_id = create_ad_set(campaign_id)
        print(f"\nAd Set ID: {adset_id}")
        print("\nCreating lead form...")
        form_id = create_lead_form()
        print(f"\nLead Form ID: {form_id}")
        print("\n✅ Campaign structure ready! Set status to ACTIVE when ready to launch.")
    else:
        print("Error creating campaign:", campaign_id)
