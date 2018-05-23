(ns status-im.ui.screens.bootnodes-settings.views
  (:require-macros [status-im.utils.views :as views])
  (:require [re-frame.core :as re-frame]
            [status-im.i18n :as i18n]
            [status-im.utils.config :as config]
            [status-im.ui.components.icons.vector-icons :as vector-icons]
            [status-im.ui.components.list.views :as list]
            [status-im.ui.components.react :as react]
            [status-im.ui.components.status-bar.view :as status-bar]
            [status-im.ui.components.toolbar.view :as toolbar]
            [status-im.ui.components.toolbar.actions :as toolbar.actions]
            [status-im.ui.screens.bootnodes-settings.styles :as styles]))

(defn- wnode-icon [connected?]
  [react/view (styles/wnode-icon connected?)
   [vector-icons/icon :icons/wnode {:color (if connected? :white :gray)}]])

(defn navigate-to-add-bootnode []
  (re-frame/dispatch [:edit-bootnode]))

(defn- render-row [current-wnode]
  (fn [{:keys [name id]}]
    (let [connected? (= id current-wnode)]
      [react/touchable-highlight
       {:on-press            #(re-frame/dispatch [:connect-wnode id])
        :accessibility-label :bootnode-item}
       [react/view styles/wnode-item
        [wnode-icon connected?]
        [react/view styles/wnode-item-inner
         [react/text {:style styles/wnode-item-name-text}
          name]]]])))

(views/defview bootnodes-settings []
  (views/letsubs [current-wnode  [:settings/current-wnode]
                  wnodes         [:settings/network-wnodes]]
    [react/view {:flex 1}
     [status-bar/status-bar]
     [toolbar/toolbar {}
      toolbar/default-nav-back
      [toolbar/content-title (i18n/label :t/bootnodes-settings)]
      (when config/add-custom-bootnodes-enabled?
        [toolbar/actions
         [(toolbar.actions/add false navigate-to-add-bootnode)]])]
     [react/view styles/wrapper
      [list/flat-list {:data               (vals wnodes)
                       :default-separator? false
                       :key-fn             :id
                       :render-fn          (render-row current-wnode)}]]]))
