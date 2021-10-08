import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:omdena_srilanka_tea_quality_client/util/api.dart';
import 'package:omdena_srilanka_tea_quality_client/util/notify.dart';

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
          Notify.error("You are offline");
        }
      } else {
        if (_prevConnectivityStatus == ConnectivityResult.none) {
          // user has came online from offline state

          // check the server status
          Api.checkServerStatus().then((bool status) {
            if (status) {
              Notify.success("You are online");
            } else {
              Notify.warn("Cannot connect with the server");
            }
          });
        }
      }

      _prevConnectivityStatus = result;
    });
  }

  void close() {
    _connectivitySubscription.cancel();
  }
}
