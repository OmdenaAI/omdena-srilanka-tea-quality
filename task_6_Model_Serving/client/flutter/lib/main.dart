import 'package:flutter/material.dart';
import 'package:omdena_srilanka_tea_quality_client/providers/result_provider.dart';
import 'package:provider/provider.dart';

import 'pages/splash.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => ResultProvider()),
      ],
      child: const MaterialApp(
        title: "Classy Tea",
        debugShowCheckedModeBanner: false,
        home: Splash(),
      ),
    );
  }
}
