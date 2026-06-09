"""
Silver Parc - Facebook Lead Gen Campaign
"""
import os, json, requests, time
from dotenv import load_dotenv

load_dotenv()

USER_TOKEN = os.getenv("FB_USER_ACCESS_TOKEN")
PAGE_TOKEN  = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID     = os.getenv("FB_PAGE_ID")
AD_ACCOUNT  = os.getenv("FB_AD_ACCOUNT_ID")
BASE        = "https://graph.facebook.com/v25.0"

IMAGES = {
    "antigua_3bd":  "images/ad_ready/antigua_3bd_1080x1080.jpg",
    "eluthera_4bd": "images/ad_ready/eluthera_4bd_1080x1080.jpg",
}

AD_COPIES = [
    {
        "name": "No HOA No CDD - English",
        "body": "4 & 5 Bedroom Homes - Cutler Bay to Kendall\n\nNO HOA fees\nNO CDD fees\nSeller pays ALL closing costs\nLow interest rates available\nPriced from $380K to $1.4M\n\nStop paying HOA every month. Own MORE, pay LESS.\nClick below to see available homes - no obligation!",
        "title": "No HOA. No CDD. Your Dream Home Awaits.",
        "image_key": "antigua_3bd",
    },
    {
        "name": "Sin HOA Sin CDD - Spanish",
        "body": "Casas de 4 y 5 habitaciones:\nCutler Bay - Palmetto Bay - Pinecrest - Kendall\nDesde $380K hasta $1.4M\nSin HOA - Sin CDD\nVendedor paga todos los gastos de cierre\n\nContactame hoy para ver opciones!",
        "title": "Sin HOA. Sin CDD. Tu hogar ideal te espera.",
        "image_key": "eluthera_4bd",
    },
]


def upload_images():
    print("\n=== Uploading Images ===")
    hashes = {}
    for name, path in IMAGES.items():
        if not os.path.exists(path):
            print("  WARNING: " + path + " not found - skipping")
            continue
        with open(path, "rb") as f:
            res = requests.post(
                BASE + "/" + AD_ACCOUNT + "/adimages",
                data={"access_token": USER_TOKEN},
                files={"filename": (name + ".jpg", f, "image/jpeg")}
            ).json()
        if "images" in res:
            h = list(res["images"].values())[0]["hash"]
            hashes[name] = h
            print("  OK " + name + " -> " + h)
        else:
            print("  FAILED " + name + ": " + str(res))
    return hashes


def create_campaign():
    print("\n=== Creating Campaign ===")
    res = requests.post(BASE + "/" + AD_ACCOUNT + "/campaigns", data={
        "access_token": USER_TOKEN,
        "name": "Silver Parc - No HOA No CDD | Cutler Bay-Kendall",
        "objective": "OUTCOME_LEADS",
        "status": "PAUSED",
        "special_ad_categories": json.dumps(["HOUSING"]),
        "is_adset_budget_sharing_enabled": "false",
    }).json()
    cid = res.get("id")
    print("  Campaign: " + str(cid or res))
    return cid


def create_ad_set(campaign_id):
    print("\n=== Creating Ad Set ===")
    targeting = {
        "geo_locations": {
            "custom_locations": [
                {"latitude": 25.5766, "longitude": -80.3453, "radius": 15, "distance_unit": "mile"},
            ],
            "location_types": ["home", "recent"]
        },
        "age_min": 18,
        "locales": [6, 23],
    }
    res = requests.post(BASE + "/" + AD_ACCOUNT + "/adsets", data={
        "access_token": USER_TOKEN,
        "name": "South Miami-Dade Buyers EN/ES",
        "campaign_id": campaign_id,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LEAD_GENERATION",
        "destination_type": "ON_AD",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "promoted_object": json.dumps({"page_id": PAGE_ID}),
        "daily_budget": "5000",
        "targeting": json.dumps(targeting),
        "status": "PAUSED",
    }).json()
    aid = res.get("id")
    if aid:
        print("  OK Ad Set: " + aid)
    else:
        print("  FAILED Ad Set: " + str(res))
    return aid


def create_lead_form():
    print("\n=== Creating Lead Form ===")
    questions = [
        {"type": "FULL_NAME"},
        {"type": "EMAIL"},
        {"type": "CUSTOM", "label": "Cual es tu plazo para comprar?",
         "options": [
             {"value": "asap",      "key": "Lo antes posible"},
             {"value": "3months",   "key": "1-3 meses"},
             {"value": "6months",   "key": "3-6 meses"},
             {"value": "exploring", "key": "Solo explorando"},
         ]},
        {"type": "CUSTOM", "label": "Cual es tu rango de precio?",
         "options": [
             {"value": "380_600",  "key": "$380K - $600K"},
             {"value": "600_900",  "key": "$600K - $900K"},
             {"value": "900_1400", "key": "$900K - $1.4M"},
         ]},
    ]
    form_name = "Silver Parc Buyer Form " + str(int(time.time()))
    res = requests.post(BASE + "/" + PAGE_ID + "/leadgen_forms", data={
        "access_token": PAGE_TOKEN,
        "name": form_name,
        "locale": "en_US",
        "questions": json.dumps(questions),
        "privacy_policy": json.dumps({"url": "https://yourfloridahomeforyou.com/privacy"}),
        "thank_you_page": json.dumps({
            "title": "Thanks! I will be in touch shortly.",
            "body": "Catherine will contact you within 24 hours with your personalized home list.",
            "button_type": "NONE",
        }),
        "context_card": json.dumps({
            "style": "LIST_STYLE",
            "title": "No HOA - No CDD - Seller Pays Closing Costs",
            "content": [
                "4 & 5 bedroom homes from $380K-$1.4M",
                "No HOA fees - No CDD fees",
                "Seller pays ALL closing costs",
                "Cutler Bay - Palmetto Bay - Pinecrest - Kendall"
            ],
            "button_text": "Get My Free Home List"
        })
    }).json()
    fid = res.get("id")
    if fid:
        print("  OK Lead Form: " + fid)
    else:
        print("  FAILED Lead Form: " + str(res))
    return fid


def create_ads(adset_id, image_hashes, form_id):
    print("\n=== Creating Ads ===")
    if not form_id:
        print("  ERROR: No lead form ID - cannot create ads")
        return
    for copy in AD_COPIES:
        img_hash = image_hashes.get(copy["image_key"])
        if not img_hash:
            print("  WARNING: No image hash for " + copy["image_key"] + " - skipping")
            continue
        creative_res = requests.post(BASE + "/" + AD_ACCOUNT + "/adcreatives", data={
            "access_token": USER_TOKEN,
            "name": copy["name"],
            "object_story_spec": json.dumps({
                "page_id": PAGE_ID,
                "link_data": {
                    "image_hash": img_hash,
                    "link": "https://www.facebook.com/lead_gen_form/" + form_id,
                    "message": copy["body"],
                    "name": copy["title"],
                    "call_to_action": {
                        "type": "SIGN_UP",
                        "value": {
                            "lead_gen_form_id": form_id,
                            "link": "https://www.facebook.com/lead_gen_form/" + form_id
                        }
                    }
                }
            }),
        }).json()
        creative_id = creative_res.get("id")
        if not creative_id:
            print("  FAILED Creative: " + str(creative_res))
            continue
        print("  OK Creative: " + creative_id)
        ad_res = requests.post(BASE + "/" + AD_ACCOUNT + "/ads", data={
            "access_token": USER_TOKEN,
            "name": copy["name"],
            "adset_id": adset_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": "PAUSED",
        }).json()
        ad_id = ad_res.get("id")
        if ad_id:
            print("  OK Ad: " + ad_id)
        else:
            print("  FAILED Ad: " + str(ad_res))


if __name__ == "__main__":
    print("Silver Parc - Facebook Lead Gen Campaign Setup")
    print("=" * 50)
    image_hashes = upload_images()
    campaign_id = create_campaign()
    if not campaign_id:
        print("Campaign creation failed.")
        exit(1)
    adset_id = create_ad_set(campaign_id)
    if not adset_id:
        print("Ad Set creation failed.")
        exit(1)
    form_id = create_lead_form()
    create_ads(adset_id, image_hashes, form_id)
    print("\nDone! Review at: https://www.facebook.com/adsmanager")
    print("Campaign ID: " + campaign_id)
