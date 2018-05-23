(ns status-im.ui.screens.bootnodes-settings.subs
  (:require [re-frame.core :as re-frame]
            status-im.ui.screens.bootnodes-settings.edit-bootnode.subs
            [status-im.utils.ethereum.core :as ethereum]))

(re-frame/reg-sub :settings/network-bootnodes
                  :<- [:network]
                  :<- [:get :bootnodes/bootnodes]
                  (fn [[network wnodes]]
                    (let [chain (ethereum/network->chain-keyword network)]
                      (chain wnodes))))
