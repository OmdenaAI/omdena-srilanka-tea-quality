import 'dart:developer';
import 'dart:io';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:expandable/expandable.dart';
import 'package:omdena_srilanka_tea_quality_client/util/api.dart';
import 'package:omdena_srilanka_tea_quality_client/util/notify.dart';
import 'package:omdena_srilanka_tea_quality_client/util/tflite.dart';

class ResultCard extends StatefulWidget {
  final XFile image;

  const ResultCard({Key? key, required this.image}) : super(key: key);

  @override
  ResultCardState createState() => ResultCardState();
}

class ResultCardState extends State<ResultCard> {
  late Size size;
  ApiImageRes? _res;
  bool _isProcessing = true;
  bool _isSuccess = true;
  String _msg = "Loading";

  @override
  void initState() {
    super.initState();
    runPrediction();
  }

  void runPrediction() async {
    ConnectivityResult _connection = await Connectivity().checkConnectivity();

    if (_connection == ConnectivityResult.none) {
      runOfflinePrediction();
    } else {
      try {
        _res = await Api.checkImageQuality(widget.image.path);

        if (_res != null && !_res!.isSuccess) {
          throw "Online prediction is not success";
        }

        Notify.success("Image results received");

        setState(() {
          _isProcessing = false;
          _isSuccess = true;
        });
      } catch (e) {
        Notify.warn("Falling back to offline method");
        log(e.toString());

        runOfflinePrediction();
      }
    }
  }

  void runOfflinePrediction() async {
    try {
      _res = await predictOffline(widget.image.path);

      setState(() {
        _isSuccess = true;
        _isProcessing = false;
      });
    } catch (e) {
      Notify.error("Error occured in offline model");
      log(e.toString());

      setState(() {
        _isSuccess = false;
        _msg = "Error occured in offline model";
        _isProcessing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return ExpandableNotifier(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expandable(
                collapsed: ExpandableButton(
                  child: Card(
                    child: Row(
                      children: [
                        SizedBox(
                          width: 150,
                          height: 100,
                          child: Image.file(
                            File(widget.image.path),
                            fit: BoxFit.cover,
                          ),
                        ),
                        Expanded(
                          child: Container(
                            margin: const EdgeInsets.symmetric(horizontal: 25),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: _isProcessing
                                  ? const [
                                      Text("Please wait"),
                                      LinearProgressIndicator()
                                    ]
                                  : _isSuccess
                                      ? [
                                          Text(_res?.msg ?? "Loading"),
                                          Text(
                                            _res?.result ??
                                                "Results loading...",
                                            style: const TextStyle(
                                              fontSize: 21,
                                              fontWeight: FontWeight.bold,
                                            ),
                                          )
                                        ]
                                      : [Text(_msg)],
                            ),
                          ),
                        )
                      ],
                    ),
                  ),
                ),
                expanded: Card(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(
                        height: 200,
                        width: 150,
                        child: Image.file(
                          File(widget.image.path),
                          fit: BoxFit.cover,
                        ),
                      ),
                      Expanded(
                        child: Container(
                          margin: const EdgeInsets.symmetric(horizontal: 10),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text((_res?.msg ?? "Loading")),
                              Text("Result " + (_res?.result ?? "Loading")),
                              const Text("\n"),
                              Text("Best " +
                                  (_res?.categories['best']
                                          ?.toStringAsFixed(2) ??
                                      "Loading")),
                              Text("Below best: " +
                                  (_res?.categories['below_best']
                                          ?.toStringAsFixed(2) ??
                                      "Loading")),
                              Text("Poor " +
                                  (_res?.categories['poor']
                                          ?.toStringAsFixed(2) ??
                                      "Loading")),
                              const Text("\n"),
                              ExpandableButton(
                                child: const Text("Back"),
                              )
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ))
          ],
        ),
      ),
    );
  }
}
