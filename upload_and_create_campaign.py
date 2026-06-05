"""
Run this script on your LOCAL computer to upload images and create
the Silver Parc lead gen campaign on Facebook Ads Manager.

Setup:
    pip install requests python-dotenv
    python3 upload_and_create_campaign.py
"""

import os, json, requests
from dotenv import load_dotenv

load_dotenv()

USER_TOKEN = os.getenv("FB_USER_ACCESS_TOKEN")
PAGE_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID    = os.getenv("FB_PAGE_ID")
AD_ACCOUNT = os.getenv("FB_AD_ACCOUNT_ID")
BASE       = "https://graph.facebook.com/v25.0"

IMAGES = {
    "catalina_4bd": "images/ad_ready/catalina_4bd_1080x1080.jpg",
    "eluthera_4bd": "images/ad_ready/eluthera_4bd_1080x1080.jpg",
    "cover_hero":   "images/ad_ready/cover_hero_1080x1080.jpg",
}

AD_COPIES = [
    {
        "name": "No HOA No CDD — English",
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
        "title": "No HOA. No CDD. Your Dream Home Awaits.",
        "image_key": "catalina_4bd",
    },
    {
        "name": "Sin HOA Sin CDD — Spanish",
        "body": (
            "¿Buscas casa en South Miami-Dade? 🏡\n\n"
            "Casas de 4 y 5 habitaciones:\n"
            "📍 Cutler Bay · Palmetto Bay · Pinecrest · Kendall\n"
            "💵 Desde $380K hasta $1.4M\n"
            "🚫 Sin HOA · Sin CDD\n"
            "✅ Vendedor paga todos los gastos de cierre\n"
            "📉 Tasas de interés bajas disponibles\n\n"
            "¡Contáctame hoy para ver opciones!"
        ),
        "title": "Sin HOA. Sin CDD. Tu hogar ideal te espera.",
        "image_key": "eluthera_4bd",
    },
]


def upload_images():
    print("\n=== Uploading Images ===")
    hashes = {}
    for name, path in IMAGES.items():
        if not os.path.exists(path):
            print(f"  ⚠️  {path} not found — skipping")
            continue
        with open(path, "rb") as f:
            res = requests.post(
                f"{BASE}/{AD_ACCOUNT}/adimages",
                data={"access_token": USER_TOKEN},
                files={"filename": (f"{name}.jpg", f, "image/jpeg")}
            ).json()
        if "images" in res:
            h = list(res["images"].values())[0]["hash"]
            hashes[name] = h
            print(f"  ✅ {name} → {h}")
        else:
            print(f"  ❌ {name}: {res}")
    return hashes


def create_campaign():
    print("\n=== Creating Campaign ===")
    res = requests.post(f"{BASE}/{AD_ACCOUNT}/campaigns", data={
        "access_token": USER_TOKEN,
        "name": "Silver Parc — No HOA No CDD | Cutler Bay–Kendall",
        "objective": "OUTCOME_LEADS",
        "status": "PAUSED",
        "special_ad_categories": json.dumps(["HOUSING"]),
        "daily_budget": "5000",
    }).json()
    campaign_id = res.get("id")
    print(f"  Campaign: {campaign_id or res}")
    return campaign_id


def create_ad_set(campaign_id):
    print("\n=== Creating Ad Set ===")
    targeting = {
        "geo_locations": {
            "cities": [
                {"key": "2421836", "name": "Cutler Bay",    "region": "Florida", "country": "US"},
                {"key": "2421835", "name": "Palmetto Bay",  "region": "Florida", "country": "US"},
                {"key": "2421810", "name": "Pinecrest",     "region": "Florida", "country": "US"},
                {"key": "2421798", "name": "Kendall",       "region": "Florida", "country": "US"},
                {"key": "2421808", "name": "South Miami",   "region": "Florida", "country": "US"},
            ],
            "location_types": ["home", "recent"]
        },
        "age_min": 28,
        "age_max": 65,
        "locales": [6, 23],
    }
    res = requests.post(f"{BASE}/{AD_ACCOUNT}/adsets", data={
        "access_token": USER_TOKEN,
        "name": "South Miami-Dade Buyers 28-65 EN/ES",
        "campaign_id": campaign_id,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LEAD_GENERATION",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "bid_amount": "500",
        "daily_budget": "5000",
        "targeting": json.dumps(targeting),
        "status": "PAUSED",
        "destination_type": "ON_AD",
    }).json()
    adset_id = res.get("id")
    print(f"  Ad Set: {adset_id or res}")
    return adset_id


def create_lead_form():
    print("\n=== Creating Lead Form ===")
    questions = [
        {"type": "FULL_NAME"},
        {"type": "EMAIL"},
        {"type": "PHONE"},
        {"type": "CUSTOM", "label": "What is your buying timeline?",
         "options": [
             {"value": "asap",       "key": "ASAP — Ready now"},
             {"value": "3months",    "key": "1–3 months"},
             {"value": "6months",    "key": "3–6 months"},
             {"value": "exploring",  "key": "Just exploring"},
         ]},
        {"type": "CUSTOM", "label": "Price range?",
         "options": [
             {"value": "380_600",  "key": "$380K – $600K"},
             {"value": "600_900",  "key": "$600K – $900K"},
             {"value": "900_1400", "key": "$900K – $1.4M"},
         ]},
    ]
    res = requests.post(f"{BASE}/{PAGE_ID}/leadgen_forms", data={
        "access_token": PAGE_TOKEN,
        "name": "Silver Parc Home Buyer Form",
        "locale": "en_US",
        "questions": json.dumps(questions),
        "privacy_policy": json.dumps({"url": "https://yourfloridahomeforyou.com/privacy"}),
        "thank_you_page": json.dumps({
            "title": "Thanks! I'll be in touch shortly.",
            "body": "Catherine will contact you within 24 hours with your personalized home list.",
            "cta_type": "VIEW_WEBSITE",
            "cta_link": "https://yourfloridahomeforyou.com"
        }),
        "context_card": json.dumps({
            "title": "No HOA · No CDD · Seller Pays Closing Costs",
            "content": [
                "4 & 5 bedroom homes from $380K–$1.4M",
                "No HOA fees • No CDD fees",
                "Seller pays ALL closing costs",
                "Cutler Bay · Palmetto Bay · Pinecrest · Kendall"
            ],
            "button_text": "Get My Free Home List"
        })
    }).json()
    form_id = res.get("id")
    print(f"  Lead Form: {form_id or res}")
    return form_id


def create_ads(adset_id, image_hashes, form_id):
    print("\n=== Creating Ads ===")
    for copy in AD_COPIES:
        img_hash = image_hashes.get(copy["image_key"])
        if not img_hash:
            print(f"  ⚠️  No image hash for {copy['image_key']} — skipping")
            continue

        # Create ad creative
        creative_res = requests.post(f"{BASE}/{AD_ACCOUNT}/adcreatives", data={
            "access_token": USER_TOKEN,
            "name": copy["name"],
            "object_story_spec": json.dumps({
                "page_id": PAGE_ID,
                "link_data": {
                    "image_hash": img_hash,
                    "link": "https://yourfloridahomeforyou.com",
                    "message": copy["body"],
                    "name": copy["title"],
                    "call_to_action": {
                        "type": "LEARN_MORE",
                        "value": {"lead_gen_form_id": form_id}
                    }
                }
            }),
        }).json()
        creative_id = creative_res.get("id")
        if not creative_id:
            print(f"  ❌ Creative for {copy['name']}: {creative_res}")
            continue
        print(f"  ✅ Creative: {creative_id}")

        # Create ad
        ad_res = requests.post(f"{BASE}/{AD_ACCOUNT}/ads", data={
            "access_token": USER_TOKEN,
            "name": copy["name"],
            "adset_id": adset_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": "PAUSED",
        }).json()
        print(f"  ✅ Ad: {ad_res.get('id') or ad_res}")


if __name__ == "__main__":
    print("🚀 Silver Parc — Facebook Lead Gen Campaign Setup")
    print("=" * 50)

    image_hashes = upload_images()

    # Campaign already created — reuse existing ID
    campaign_id = "120247131196090156"
    print(f"\n=== Reusing existing Campaign ID: {campaign_id} ===")

    adset_id = create_ad_set(campaign_id)
    form_id  = create_lead_form()
    create_ads(adset_id, image_hashes, form_id)

    print("\n✅ Done! Go to Facebook Ads Manager to review:")
    print("   https://www.facebook.com/adsmanager")
    print(f"   Campaign ID: {campaign_id}")
