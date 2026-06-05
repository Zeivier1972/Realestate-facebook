import re

content = open('upload_and_create_campaign.py', encoding='utf-8').read()
changes = 0

# Fix 1: Use antigua and eluthera images only
old = '''IMAGES = {
    "catalina_4bd": "images/ad_ready/catalina_4bd_1080x1080.jpg",
    "eluthera_4bd": "images/ad_ready/eluthera_4bd_1080x1080.jpg",
    "cover_hero":   "images/ad_ready/cover_hero_1080x1080.jpg",
}'''
new = '''IMAGES = {
    "antigua_3bd":  "images/ad_ready/antigua_3bd_1080x1080.jpg",
    "eluthera_4bd": "images/ad_ready/eluthera_4bd_1080x1080.jpg",
}'''
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print('Fix 1: images updated')
else:
    print('Fix 1: images already updated or not found')

# Fix 2: Use antigua image key in English ad copy
old2 = '"image_key": "catalina_4bd",'
new2 = '"image_key": "antigua_3bd",'
if old2 in content:
    content = content.replace(old2, new2, 1)
    changes += 1
    print('Fix 2: ad copy image key updated')
else:
    print('Fix 2: already updated or not found')

# Fix 3: Add LIST_STYLE to context card
old3 = '"context_card": json.dumps({\n            "title":'
new3 = '"context_card": json.dumps({\n            "style": "LIST_STYLE",\n            "title":'
if old3 in content:
    content = content.replace(old3, new3, 1)
    changes += 1
    print('Fix 3: context card style added')
elif '"style": "LIST_STYLE"' in content:
    print('Fix 3: context card style already present')
else:
    print('Fix 3: context card not found')

# Fix 4: destination_type ON_AD and remove bid cap
old4 = '"optimization_goal": "LEAD_GENERATION",\n        "bid_strategy": "LOWEST_COST_WITH_BID_CAP",\n        "bid_amount": "500",'
new4 = '"optimization_goal": "LEAD_GENERATION",\n        "destination_type": "ON_AD",\n        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",'
if old4 in content:
    content = content.replace(old4, new4, 1)
    changes += 1
    print('Fix 4: destination_type and bid strategy updated')
elif '"destination_type": "ON_AD"' in content:
    print('Fix 4: destination_type already present')
else:
    print('Fix 4: not found - checking current state')
    idx = content.find('optimization_goal')
    print(repr(content[idx-20:idx+150]))

open('upload_and_create_campaign.py', 'w', encoding='utf-8').write(content)
print(f'\nDone — {changes} fixes applied')
