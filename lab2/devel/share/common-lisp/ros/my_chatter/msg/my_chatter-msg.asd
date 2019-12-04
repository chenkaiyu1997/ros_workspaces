
(cl:in-package :asdf)

(defsystem "my_chatter-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "TimestampString" :depends-on ("_package_TimestampString"))
    (:file "_package_TimestampString" :depends-on ("_package"))
  ))