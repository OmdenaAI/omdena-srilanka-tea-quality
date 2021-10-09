import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:omdena_srilanka_tea_quality_client/util/api.dart';
import 'package:omdena_srilanka_tea_quality_client/util/notify.dart';

class ResultPage extends StatefulWidget {
  final XFile? image;
  const ResultPage(this.image, {Key? key}) : super(key: key);

  @override
  _ResultPageState createState() => _ResultPageState();
}

class _ResultPageState extends State<ResultPage> {
  late Size size;
  String _result = "Please wait ...";

  @override
  void initState() {
    super.initState();

    final Connectivity _connectivity = Connectivity();
    _connectivity.checkConnectivity().then((ConnectivityResult result) => {
          if (result == ConnectivityResult.none)
            {
              // warn user if offline ML model is being used
              Notify.warn("You are offline, results maybe less accurate"),

              // TODO: Implement offline ML model
              setState(() {
                _result = "Calculated using offline ML model";
              })
            }
          else
            {
              // send image to server
              Api.checkImageQuality(widget.image!.path).then((value) => {
                    Notify.success("Image results received"),
                    setState(() {
                      _result = value;
                    })
                  })
            }
        });
  }

  @override
  Widget build(BuildContext context) {
    size = MediaQuery.of(context).size;
    return SafeArea(
      child: Scaffold(
        body: Stack(
          children: [
            Column(
              children: [
                buildImage("result_top.png"),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(10),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: size.width * 0.8,
                          height: size.height * 0.35,
                          margin: const EdgeInsets.only(bottom: 10),
                          child: Image.file(
                            File(widget.image?.path ?? ""),
                          ),
                        ),
                        Text(
                          _result,
                          style: TextStyle(
                            fontSize: size.width * 0.04,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                buildImage("result_bottom.png"),
              ],
            ),
            IconButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              icon: const Icon(
                Icons.arrow_back,
                size: 30,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildImage(String image) {
    return Container(
      width: size.width,
      height: size.height * 0.25,
      child: FittedBox(
        fit: BoxFit.fill,
        child: Image.asset("assets/images/$image"),
      ),
    );
  }
}
