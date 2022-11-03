from aptc import new_client, APTOS_NODE_URL_LIST, APTClient, HttpxProvider

APT_NODE_URL = APTOS_NODE_URL_LIST[0]

# mainnet
client = new_client(node_url=APT_NODE_URL)
