;; Auto-generated. Do not edit!


(when (boundp 'planning::ChouChou)
  (if (not (find-package "PLANNING"))
    (make-package "PLANNING"))
  (shadow 'ChouChou (find-package "PLANNING")))
(unless (find-package "PLANNING::CHOUCHOU")
  (make-package "PLANNING::CHOUCHOU"))

(in-package "ROS")
;;//! \htmlinclude ChouChou.msg.html


(defclass planning::ChouChou
  :super ros::object
  :slots (_position_x _position_y _position_z _edge_grad _status_type ))

(defmethod planning::ChouChou
  (:init
   (&key
    ((:position_x __position_x) 0.0)
    ((:position_y __position_y) 0.0)
    ((:position_z __position_z) 0.0)
    ((:edge_grad __edge_grad) 0.0)
    ((:status_type __status_type) "")
    )
   (send-super :init)
   (setq _position_x (float __position_x))
   (setq _position_y (float __position_y))
   (setq _position_z (float __position_z))
   (setq _edge_grad (float __edge_grad))
   (setq _status_type (string __status_type))
   self)
  (:position_x
   (&optional __position_x)
   (if __position_x (setq _position_x __position_x)) _position_x)
  (:position_y
   (&optional __position_y)
   (if __position_y (setq _position_y __position_y)) _position_y)
  (:position_z
   (&optional __position_z)
   (if __position_z (setq _position_z __position_z)) _position_z)
  (:edge_grad
   (&optional __edge_grad)
   (if __edge_grad (setq _edge_grad __edge_grad)) _edge_grad)
  (:status_type
   (&optional __status_type)
   (if __status_type (setq _status_type __status_type)) _status_type)
  (:serialization-length
   ()
   (+
    ;; float64 _position_x
    8
    ;; float64 _position_y
    8
    ;; float64 _position_z
    8
    ;; float64 _edge_grad
    8
    ;; string _status_type
    4 (length _status_type)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _position_x
       (sys::poke _position_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _position_y
       (sys::poke _position_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _position_z
       (sys::poke _position_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _edge_grad
       (sys::poke _edge_grad (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; string _status_type
       (write-long (length _status_type) s) (princ _status_type s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _position_x
     (setq _position_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _position_y
     (setq _position_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _position_z
     (setq _position_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _edge_grad
     (setq _edge_grad (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; string _status_type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _status_type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get planning::ChouChou :md5sum-) "6671b4e310025559f107ccde9e7e7adf")
(setf (get planning::ChouChou :datatype-) "planning/ChouChou")
(setf (get planning::ChouChou :definition-)
      "float64 position_x
float64 position_y
float64 position_z
float64 edge_grad
string status_type
")



(provide :planning/ChouChou "6671b4e310025559f107ccde9e7e7adf")


