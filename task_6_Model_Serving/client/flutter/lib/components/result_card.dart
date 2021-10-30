import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:expandable/expandable.dart';
import 'package:omdena_srilanka_tea_quality_client/util/api.dart';
import 'package:omdena_srilanka_tea_quality_client/util/notify.dart';

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

    Api.dummyResponse().then((value) => {
          if (value.isSuccess)
            {
              Notify.success("Image results received"),
              setState(() {
                _res = value;
                _isProcessing = false;
                _isSuccess = true;
              })
            }
          else
            {
              Notify.error("Error occured while fetching results"),
              setState(() {
                _msg = value.error;
                _isProcessing = false;
                _isSuccess = false;
              })
            }
        });
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
                        const SizedBox(
                          width: 25,
                        ),
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: _isProcessing
                                ? const [
                                    Text("Calculating"),
                                    Text("Please wait")
                                  ]
                                : _isSuccess
                                    ? [
                                        const Text("Success"),
                                        Text(_res?.result ??
                                            "Results loading...")
                                      ]
                                    : [Text(_msg)],
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
                        child: Image.file(
                          File(widget.image.path),
                          fit: BoxFit.cover,
                        ),
                      ),
                      Column(
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Message " + (_res?.msg ?? "Loading")),
                          Text("Result " + (_res?.result ?? "Loading")),
                          Text("Below best: " +
                              (_res?.categories['below_best'].toString() ??
                                  "Loading")),
                          Text("Best " +
                              (_res?.categories['best'].toString() ??
                                  "Loading")),
                          Text("Poor " +
                              (_res?.categories['poor'].toString() ??
                                  "Loading")),
                          const Text("\n"),
                          ExpandableButton(
                            child: const Text("Back"),
                          )
                        ],
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
