content = open('upload_and_create_campaign.py', encoding='utf-8').read()
old = '"daily_budget": "5000",\n        "targeting": json.dumps(targeting),'
new = '"bid_strategy": "LOWEST_COST_WITHOUT_CAP",\n        "daily_budget": "5000",\n        "targeting": json.dumps(targeting),'
if old in content:
    open('upload_and_create_campaign.py', 'w', encoding='utf-8').write(content.replace(old, new, 1))
    print('Patched OK')
else:
    print('String not found - showing relevant section:')
    idx = content.find('daily_budget')
    print(repr(content[idx-50:idx+200]))
