(ns status-im.data-store.bootnodes
  (:require [re-frame.core :as re-frame]
            [status-im.data-store.realm.core :as core]))

(re-frame/reg-cofx
 :data-store/get-all-bootnodes
 (fn [cofx _]
   (assoc cofx :data-store/bootnodes (-> @core/account-realm
                                         (core/get-all :bootnodes)
                                         (core/all-clj :bootnodes)))))

(defn save-bootnode-tx
  "Returns tx function for saving a bootnode"
  [{:keys [id] :as bootnode}]
  (fn [realm]
    (core/create realm
                 :bootnode
                 bootnode
                 (core/exists? realm :bootnode :id id))))
