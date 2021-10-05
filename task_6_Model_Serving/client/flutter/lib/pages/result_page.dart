// ignore_for_file: sized_box_for_whitespace

//another
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class ResultPage extends StatefulWidget {
  final XFile? image;
  const ResultPage(this.image, {Key? key}) : super(key: key);

  @override
  _ResultPageState createState() => _ResultPageState();
}

class _ResultPageState extends State<ResultPage> {
  late Size size;
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
                          "The best quality is ...",
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
