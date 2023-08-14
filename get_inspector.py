import requests
import os
import jmespath
import pandas as pd

pd.set_option('display.max_colwidth', None)

url = "https://api0.prismacloud.io/search/config"

token = os.getenv("prisma_token")

headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': 'application/json; charset=UTF-8',
  'x-redlock-auth': token
}

payload = "{\r\n  \"query\":\"config from cloud.resource where cloud.type = 'aws' AND api.name = 'aws-region'\",\r\n  \"timeRange\":{\"type\":\"to_now\",\"value\":\"epoch\"},\r\n    \"heuristicSearch\":true\r\n}"

response = requests.request("POST", url, headers=headers, data=payload)
json_data = response.json()
active_regions = set(jmespath.search("data.items[*].name", json_data))

payload = "{\r\n  \"query\":\"config from cloud.resource where finding.source = 'AWS Inspector'\",\r\n  \"timeRange\":{\"type\":\"to_now\",\"value\":\"epoch\"},\r\n    \"heuristicSearch\":true\r\n}"

response = requests.request("POST", url, headers=headers, data=payload)
json_data = response.json()
inspector_regions = set(jmespath.search("data.items[*].regionId", json_data))

with open (f"inspector_regions.txt", 'w') as f:
  f.write("TOTAL ACTIVE REGIONS:\n{0} \
          \nREGIONS WITH INSPECTOR:\n{1} \
          \nREGIONS W/O INSPECTOR:\n{2}" \
          .format('\n'.join(active_regions), \
                  '\n'.join(inspector_regions), \
                  '\n'.join(active_regions.difference(inspector_regions))))
