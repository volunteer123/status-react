(ns status-im.ui.screens.bootnodes-settings.events
  (:require [re-frame.core :as re-frame]
            [status-im.utils.handlers :as handlers]
            [status-im.utils.handlers-macro :as handlers-macro]
            [status-im.ui.screens.accounts.events :as accounts-events]
            [status-im.i18n :as i18n]
            [status-im.transport.core :as transport]
            [status-im.utils.ethereum.core :as ethereum]))

(handlers/register-handler-fx
 ::save-bootnode
 (fn [{:keys [db now] :as cofx} [_ chain wnode]]
   (let [settings (get-in db [:account/account :settings])]
     (handlers-macro/merge-fx cofx
                              (accounts-events/update-settings
                               (assoc-in settings [:bootnode chain] wnode)
                               [:logout])))))
