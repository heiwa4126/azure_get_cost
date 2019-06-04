#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-msg=C0103, C0111

import sys
import requests
import codecs
import json

BASE_URL = "https://api.partnercenter.microsoft.com"


def beautify_json(obj):
    return json.dumps(
        obj,
        sort_keys=True,
        # encoding="utf-8",
        ensure_ascii=False,
        indent=2,
        separators=(",", ": "),
    )


def remove_bom(s):
    if s[:3] == codecs.BOM_UTF8:
        return s[3:]
    else:
        return s


def get_subscriptions_list(cred):

    params = {"api-version": "2019-05-01"}
    headers = {"Authorization": "Bearer {}".format(cred["access_token"])}

    return requests.get(
        "https://management.azure.com/subscriptions", headers=headers, params=params
    )


def query_cost1(cred, subId):
    """
    https://docs.microsoft.com/en-us/rest/api/cost-management/query/usagebyscope
    を使って
    特定サブスクリプションの、今月分のコストを日単位で得る(税抜価格)。
    ちょうどAzure Portalで
    [サブスクリプション]->[(サブスクリプション選択)]->[cost analysis]で
    表示されるグラフのもととなるデータが得られる。
    """

    url = "https://management.azure.com/subscriptions/{}/providers/Microsoft.CostManagement/query".format(
        subId
    )
    headers = {
        "Authorization": "Bearer {}".format(cred["access_token"]),
        "Content-type": "application/json",
    }
    params = {"api-version": "2019-01-01"}
    body = '{"type":"Usage","timeframe":"MonthToDate","dataset":{"granularity":"Daily","aggregation":{"totalCost":{"name":"PreTaxCost","function":"Sum"}}}}'

    return requests.post(url, headers=headers, params=params, data=body)


def decode_json(s):
    # s = s.encode("utf-8")
    s = remove_bom(s)
    return json.loads(s)


def display_result(r):
    sys.stderr.write("URL:{}\nStatus Code:{}\n".format(r.url, r.status_code))

    if r.status_code != 200:
        # sys.stderr.write(r.text.encode("utf-8"))
        sys.stderr.write(r.text)
        return None
    else:
        q = decode_json(r.text)
        # print(beautify_json(q).encode("utf-8"))
        print(beautify_json(q))
        return q


def main():
    """main"""

    with open(sys.argv[1], "r") as f:
        cred = json.load(f)

    r = get_subscriptions_list(cred)
    q = display_result(r)
    if q is None:
        sys.exit(1)

    for i in q["value"]:
        r = query_cost1(cred, i["subscriptionId"])
        q2 = display_result(r)
        if q2 is None:
            sys.exit(1)


if __name__ == "__main__":
    main()
