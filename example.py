from classyapi import ClassyAPIClient
from localsettings import ORGANIZATION_ID, CLIENT_ID, CLIENT_SECRET


def get_transactions():
    """
    This calls the API to return a list of organization transactions.
    :return: None
    """
    data = []
    params = {
        "per_page": 100,
        "page": 1
    }
    client = ClassyAPIClient(ORGANIZATION_ID, CLIENT_ID, CLIENT_SECRET)
    endpoint = f"/2.0/organizations/{ORGANIZATION_ID}/transactions"
    response = client.get(endpoint, params=params)
    data.extend(response.json()["data"])
    print(f"returned {len(data)} transactions")


def get_last_thousand_transactiosn():
    """
    An example of how you could get the last thousand transactions by paging.
    :return:
    """
    data = []
    params = {
        "per_page": 100,
    }
    client = ClassyAPIClient(ORGANIZATION_ID, CLIENT_ID, CLIENT_SECRET)
    endpoint = f"/2.0/organizations/{ORGANIZATION_ID}/transactions"
    for page in range(1, 11):
        params["page"] = page
        response = client.get(endpoint, params=params)
        json = response.json()
        data.extend(json["data"])
        if not json["next_page_url"]:
            break

    print(f"returned {len(data)} transactions")


if __name__ == '__main__':
    get_last_thousand_transactiosn()
