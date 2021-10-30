import 'package:flutter/material.dart';
import 'package:overlay_support/overlay_support.dart';
import 'package:provider/provider.dart';

import 'package:omdena_srilanka_tea_quality_client/providers/result_provider.dart';
import 'package:omdena_srilanka_tea_quality_client/util/connectivity.dart';

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
  final _connectivity = ConnectionStateListner();

  @override
  void initState() {
    super.initState();
    _connectivity.listen();
  }

  @override
  void dispose() {
    super.dispose();
    _connectivity.close();
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
