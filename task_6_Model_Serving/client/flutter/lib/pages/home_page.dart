import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        alignment: Alignment.topCenter,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Image.asset('assets/images/home.png', height: 500, width: 400),
            Container(
              transformAlignment: Alignment.center,
              height: 250,
              width: 350,
              decoration: const BoxDecoration(
                borderRadius: BorderRadius.all(Radius.circular(24)),
                color: Colors.amber,
              ),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    ElevatedButton(
                        onPressed: () {
                          print('clicked me!');
                        },
                        child: const Text(
                          'Take Picture',
                          style: TextStyle(fontSize: 20),
                        ),
                        style: ElevatedButton.styleFrom(
                            primary: Colors.white,
                            onPrimary: Colors.black,
                            padding: const EdgeInsets.all(20),
                            minimumSize: const Size(200, 60))),
                    ElevatedButton(
                      onPressed: () {
                        print('Browse from gallery!');
                      },
                      child: const Text(
                        'Browse From Gallery',
                        style: TextStyle(fontSize: 20),
                      ),
                      style: ElevatedButton.styleFrom(
                          primary: Colors.white,
                          onPrimary: Colors.black,
                          padding: const EdgeInsets.all(20),
                          minimumSize: const Size(200, 60)),
                    )
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
