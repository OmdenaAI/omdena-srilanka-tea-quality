import 'package:flutter/material.dart';
import 'package:overlay_support/overlay_support.dart';

class Notify {
  static void success(String msg) {
    showSimpleNotification(Text(msg), background: Colors.green);
  }

  static void warn(String msg) {
    showSimpleNotification(Text(msg), background: Colors.orange);
  }

  static void error(String msg) {
    showSimpleNotification(Text(msg), background: Colors.red);
  }
}
