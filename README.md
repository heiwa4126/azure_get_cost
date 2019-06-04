# azure_get_cost

AzureのREST APIで、
Azureの使用料金(税抜)を取得する例。

Azureポータルの、
[サブスクリプション]-[(サブスクリプション選択)]-[コスト分析]
で表示されるコストを取得する。

# 備考

一応Python2でも3でも動く(JSONに漢字がないから)。


# 準備

```
az ad sp create-for-rbac --role Reader -n http://test6 > test6.json
```
(`test6`は例)


今回は読み取りだけなので、組み込みロールのReaderを使った。

詳しくは以下参照:
- [Azure リソースの組み込みロール | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/role-based-access-control/built-in-roles)
- [Azure リソースのカスタム ロール | Microsoft Docs](https://docs.microsoft.com/ja-jp/azure/role-based-access-control/custom-roles)

## 備考

Azureポータルで
[Azure Active Directorty] - [App registrations] - [すべてのアプリケーション]
で、いま登録したアプリケーションが編集できる。

いらなくなったら消すこと。



# 実行

```
./get_token.py test6.json > b1.json
```
で1時間使えるtokenを得る。(`b1`は例)

```
./get_cost.py b1.json
```
でcostを得る


# 出力例

```
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

- tokenをmemcacheに入れるとか工夫すること。
- RESTの呼び出してtimeoutが入ってないので、なんとかすること。
