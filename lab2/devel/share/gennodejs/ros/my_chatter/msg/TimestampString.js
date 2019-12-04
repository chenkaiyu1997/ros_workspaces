// Auto-generated. Do not edit!

// (in-package my_chatter.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class TimestampString {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.user_enter_message = null;
      this.time_send = null;
    }
    else {
      if (initObj.hasOwnProperty('user_enter_message')) {
        this.user_enter_message = initObj.user_enter_message
      }
      else {
        this.user_enter_message = '';
      }
      if (initObj.hasOwnProperty('time_send')) {
        this.time_send = initObj.time_send
      }
      else {
        this.time_send = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type TimestampString
    // Serialize message field [user_enter_message]
    bufferOffset = _serializer.string(obj.user_enter_message, buffer, bufferOffset);
    // Serialize message field [time_send]
    bufferOffset = _serializer.float64(obj.time_send, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type TimestampString
    let len;
    let data = new TimestampString(null);
    // Deserialize message field [user_enter_message]
    data.user_enter_message = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [time_send]
    data.time_send = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.user_enter_message.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'my_chatter/TimestampString';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0ae91027bb227fc0373ed1998cce1935';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string user_enter_message
    float64 time_send
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new TimestampString(null);
    if (msg.user_enter_message !== undefined) {
      resolved.user_enter_message = msg.user_enter_message;
    }
    else {
      resolved.user_enter_message = ''
    }

    if (msg.time_send !== undefined) {
      resolved.time_send = msg.time_send;
    }
    else {
      resolved.time_send = 0.0
    }

    return resolved;
    }
};

module.exports = TimestampString;
