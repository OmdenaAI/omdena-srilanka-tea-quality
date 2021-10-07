import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/material.dart';
import 'package:omdena_srilanka_tea_quality_client/providers/result_provider.dart';
import 'package:overlay_support/overlay_support.dart';
import 'package:provider/provider.dart';

import 'pages/splash.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  // connectivity_plus
  final Connectivity _connectivity = Connectivity();
  late StreamSubscription<ConnectivityResult> _connectivitySubscription;
  // setting initial state to not none to avoid "went online" notification at startup
  ConnectivityResult _prevConnectivityStatus = ConnectivityResult.wifi;

  @override
  void initState() {
    super.initState();

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

  @override
  void dispose() {
    super.dispose();

    _connectivitySubscription.cancel();
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => ResultProvider()),
      ],
      child: const OverlaySupport.global(
        child: MaterialApp(
          title: "Classy Tea",
          debugShowCheckedModeBanner: false,
          home: Splash(),
        ),
      ),
    );
  }
}
