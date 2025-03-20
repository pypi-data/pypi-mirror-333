from ._p2p_method import P2PMethod


class P2PMethods:
    GET_CURRENT_BALANCE = P2PMethod("/v5/account/wallet-balance", "GET", ["accountType"])
    GET_ACCOUNT_INFORMATION = P2PMethod("/v5/p2p/user/personal/info", "POST", [])
    GET_ADS_LIST = P2PMethod("/v5/p2p/item/personal/list", "POST", [])
    GET_AD_DETAIL = P2PMethod("/v5/p2p/item/info", "POST", ["itemId"])
    UPDATE_AD = P2PMethod("/v5/p2p/item/update", "POST",
                          [
                              "id",
                              "priceType",
                              "premium",
                              "price",
                              "minAmount",
                              "maxAmount",
                              "remark",
                              "tradingPreferenceSet",
                              "paymentIds",
                              "actionType",
                              "quantity",
                              "paymentPeriod"
                          ]
                          )
    OFFLINE_AD = P2PMethod("/v5/p2p/item/cancel", "POST", ["itemId"])
    GET_ORDERS = P2PMethod("/v5/p2p/order/simplifyList", "POST", ["page", "size"])
    GET_PENDING_ORDERS = P2PMethod("/v5/p2p/order/pending/simplifyList", "POST", ["page", "size"])
    GET_USER_ORDER_STATISTIC = P2PMethod("/v5/p2p/user/order/personal/info", "POST", ["originalUid", "orderId"])
    GET_ORDER_DETAILS = P2PMethod("/v5/p2p/order/info", "POST", ["orderId"])
    RELEASE_ASSETS = P2PMethod("/v5/p2p/order/finish", "POST", ["orderId"])
    MARK_AS_PAID = P2PMethod("/v5/p2p/order/pay", "POST", ["orderId", "paymentType", "paymentId"])
    GET_CHAT_MESSAGES = P2PMethod("/v5/p2p/order/message/list", "POST", ["orderId", "size"])
    UPLOAD_CHAT_FILE = P2PMethod("/v5/p2p/oss/upload_file", "FILE", ["upload_file"])
    SEND_CHAT_MESSAGE = P2PMethod("/v5/p2p/order/message/send", "POST", ["message", "contentType", "orderId"])
    POST_NEW_AD = P2PMethod("/v5/p2p/item/create", "POST", [
                              "tokenId",
                              "currencyId",
                              "side",
                              "priceType",
                              "premium",
                              "price",
                              "minAmount",
                              "maxAmount",
                              "remark",
                              "tradingPreferenceSet",
                              "paymentIds",
                              "quantity",
                              "paymentPeriod",
                              "itemType"
                          ]
                        )
    GET_ONLINE_ADS = P2PMethod("/v5/p2p/item/online", "POST", ["tokenId", "currencyId", "side"])
    GET_USER_PAYMENT_TYPES = P2PMethod("/v5/p2p/user/payment/list", "POST", [])
