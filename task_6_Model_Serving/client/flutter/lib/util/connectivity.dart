import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/material.dart';
import 'package:overlay_support/overlay_support.dart';

class ConnectionStateListner {
  final Connectivity _connectivity = Connectivity();
  late StreamSubscription<ConnectivityResult> _connectivitySubscription;
  // setting initial state to not none to avoid "went online" notification at startup
  ConnectivityResult _prevConnectivityStatus = ConnectivityResult.wifi;

  void listen() {
    // trigger when connection type changes
    _connectivitySubscription =
        _connectivity.onConnectivityChanged.listen((ConnectivityResult result) {
      if (result == ConnectivityResult.none) {
        if (_prevConnectivityStatus != ConnectivityResult.none) {
          // user has gone offline
          showSimpleNotification(const Text("You are offline"),
              background: Colors.red);
        }
      } else {
        if (_prevConnectivityStatus == ConnectivityResult.none) {
          // user has came online from offline state
          showSimpleNotification(const Text("You are online"),
              background: Colors.green);
        }
      }

      _prevConnectivityStatus = result;
    });
  }

  void close() {
    _connectivitySubscription.cancel();
  }
}
