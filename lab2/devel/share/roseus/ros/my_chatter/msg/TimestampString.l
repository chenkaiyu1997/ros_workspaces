;; Auto-generated. Do not edit!


(when (boundp 'my_chatter::TimestampString)
  (if (not (find-package "MY_CHATTER"))
    (make-package "MY_CHATTER"))
  (shadow 'TimestampString (find-package "MY_CHATTER")))
(unless (find-package "MY_CHATTER::TIMESTAMPSTRING")
  (make-package "MY_CHATTER::TIMESTAMPSTRING"))

(in-package "ROS")
;;//! \htmlinclude TimestampString.msg.html


(defclass my_chatter::TimestampString
  :super ros::object
  :slots (_user_enter_message _time_send ))

(defmethod my_chatter::TimestampString
  (:init
   (&key
    ((:user_enter_message __user_enter_message) "")
    ((:time_send __time_send) 0.0)
    )
   (send-super :init)
   (setq _user_enter_message (string __user_enter_message))
   (setq _time_send (float __time_send))
   self)
  (:user_enter_message
   (&optional __user_enter_message)
   (if __user_enter_message (setq _user_enter_message __user_enter_message)) _user_enter_message)
  (:time_send
   (&optional __time_send)
   (if __time_send (setq _time_send __time_send)) _time_send)
  (:serialization-length
   ()
   (+
    ;; string _user_enter_message
    4 (length _user_enter_message)
    ;; float64 _time_send
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _user_enter_message
       (write-long (length _user_enter_message) s) (princ _user_enter_message s)
     ;; float64 _time_send
       (sys::poke _time_send (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _user_enter_message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _user_enter_message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float64 _time_send
     (setq _time_send (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get my_chatter::TimestampString :md5sum-) "0ae91027bb227fc0373ed1998cce1935")
(setf (get my_chatter::TimestampString :datatype-) "my_chatter/TimestampString")
(setf (get my_chatter::TimestampString :definition-)
      "string user_enter_message
float64 time_send
")



(provide :my_chatter/TimestampString "0ae91027bb227fc0373ed1998cce1935")


