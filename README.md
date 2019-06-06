# azure_get_cost

- [azure_get_cost](#azure_get_cost)
- [準備](#準備)
  - [備考](#備考)
- [実行](#実行)
- [出力例](#出力例)
- [TODO](#todo)
- [その他](#その他)

AzureのREST APIで、
Azureの使用料金(税抜)を取得するサンプルコード。

[Azureポータル](https://portal.azure.com/)の、
[サブスクリプション] - [(サブスクリプション選択)] - [コスト分析]
で表示されるコストを取得する。

検索したら
[Azureでコマンドラインから利用料金を取得する | Ryuzee.com](https://www.ryuzee.com/contents/blog/7098)
のような
古めのAPIを使い、CSPでは動かない
例しか見つからなかったので
作ってみた。

Python2でも3でも動く(このJSONに漢字がないから)。


# 準備

azure-cliで
``` bash
az ad sp create-for-rbac --role Reader -n http://test6 > test6.json
```
(`test6`は例。ログインやアカウント選択手順は省いた)


今回は読取だけなので、組込ロールのReaderを使った(それでも範囲広すぎ)。

ロールについて詳しくは以下参照:
- [Azure リソースの組み込みロール | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/role-based-access-control/built-in-roles)
- [Azure リソースのカスタム ロール | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/role-based-access-control/custom-roles)

## 備考

[Azureポータル](https://portal.azure.com/)の
[Azure Active Directorty] - [App registrations] - [すべてのアプリケーション]
で、いま登録したアプリケーションが編集できる。

いらなくなったら消すこと。



# 実行

``` bash
./get_token.py test6.json > b1.json
```
で1時間使えるtokenを得る。(`b1`は例)

``` bash
./get_cost.py b1.json
```
でcostを得る


# 出力例

``` json
(略)
    "rows": [
      [
        35.849924992,
        20190601,
        "JPY"
      ],
      [
        35.847352576,
        20190602,
        "JPY"
      ],
      [
        73.128169744,
        20190603,
        "JPY"
      ]
    ]
  },
  "sku": null,
  "type": "Microsoft.CostManagement/query"
}
```
rowsの上から
「2019/6/1のコストは35.849924992円(税抜)」
のようなJSONがとれる。


# TODO

- tokenをmemcacheに入れるなど、かっこよく工夫すること。
- RESTの呼び出してtimeoutが入ってないので、なんとかすること。
- subscription毎にRBACが要るのが面倒なので、なんとかすること。


# その他

使用しているAzureのAPIは
- [Subscriptions - List (Azure Resource Management) | Microsoft Docs](https://docs.microsoft.com/en-us/rest/api/resources/subscriptions/list)
- [Query - Usage By Scope (Azure Cost Management) | Microsoft Docs](https://docs.microsoft.com/en-us/rest/api/cost-management/query/usagebyscope)

Query の Request Body がちょっと面白い。
[上記ページ](https://docs.microsoft.com/en-us/rest/api/cost-management/query/usagebyscope)
にある例が参考になる。

CSPでは動きません。

> Subscription xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx offer MS-AZR-0146P is not associated with a supported EA, WebDirect or GTM offer type (Request ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

おそらく対応しないサブスクリプションのオファーは
[Azure Consumption | Microsoft Docs](https://docs.microsoft.com/en-us/rest/api/consumption/#list-of-unsupported-subscription-types)
にあるリストと同じものではないかと。
