(ns status-im.data-store.realm.schemas.account.v2.core
<<<<<<< HEAD
  (:require [status-im.data-store.realm.schemas.account.v1.chat :as chat]
=======
  (:require [status-im.data-store.realm.schemas.account.v2.chat :as chat]
>>>>>>> Dont open chat on contact request
            [status-im.data-store.realm.schemas.account.v1.transport :as transport]
            [status-im.data-store.realm.schemas.account.v1.contact :as contact]
            [status-im.data-store.realm.schemas.account.v1.message :as message]
            [status-im.data-store.realm.schemas.account.v1.request :as request]
            [status-im.data-store.realm.schemas.account.v1.user-status :as user-status]
<<<<<<< HEAD
            [status-im.data-store.realm.schemas.account.v1.local-storage :as local-storage]
            [status-im.data-store.realm.schemas.account.v2.mailserver :as mailserver]
            [status-im.data-store.realm.schemas.account.v1.browser :as browser]
            [taoensso.timbre :as log]))
=======
            [status-im.data-store.realm.schemas.account.v1.contact-group :as contact-group]
            [status-im.data-store.realm.schemas.account.v1.local-storage :as local-storage]
            [status-im.data-store.realm.schemas.account.v1.browser :as browser]
            [goog.object :as object]
            [taoensso.timbre :as log]
            [cljs.reader :as reader]
            [clojure.string :as string]))
>>>>>>> Dont open chat on contact request

(def schema [chat/schema
             transport/schema
             contact/schema
             message/schema
             request/schema
<<<<<<< HEAD
             mailserver/schema
             user-status/schema
=======
             user-status/schema
             contact-group/schema
>>>>>>> Dont open chat on contact request
             local-storage/schema
             browser/schema])

(defn migration [old-realm new-realm]
<<<<<<< HEAD
  (log/debug "migrating v2 account database: " old-realm new-realm))
=======
  (log/debug "migrating v2 account database: " old-realm new-realm)
  (chat/migration old-realm new-realm))
>>>>>>> Dont open chat on contact request
