import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:image_picker/image_picker.dart';
import 'package:omdena_srilanka_tea_quality_client/components/result_card.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final GlobalKey<AnimatedListState> _listKey = GlobalKey<AnimatedListState>();
  List images = <XFile>[];
  late ImagePicker picker;

  @override
  void initState() {
    super.initState();

    picker = ImagePicker();
  }

  void _getImage(ImageSource source) async {
    XFile? image = await picker.pickImage(
      source: source,
      maxWidth: 512,
      maxHeight: 512,
      imageQuality: 59,
    );

    if (image is XFile) {
      setState(() {
        images.add(image);
        _listKey.currentState?.insertItem(images.length - 1);
      });
    }
  }

  Widget mainButtons() {
    return Column(
      children: [
        const SizedBox(
          height: 15,
        ),
        SizedBox(
          width: 200,
          child: ElevatedButton(
            onPressed: () => {_getImage(ImageSource.camera)},
            child: const Text(
              "Open Camera",
              style: TextStyle(fontSize: 18),
            ),
          ),
        ),
        SizedBox(
          width: 200,
          child: ElevatedButton(
            onPressed: () => {_getImage(ImageSource.gallery)},
            child: const Text(
              "Browse Gallery",
              style: TextStyle(fontSize: 18),
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: Column(
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 500),
              curve: Curves.fastOutSlowIn,
              padding: const EdgeInsets.all(10),
              height: images.isEmpty
                  ? MediaQuery.of(context).size.height - 24
                  : 100,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const Text(
                    "Classy Tea",
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  images.isEmpty ? mainButtons() : const SizedBox.shrink()
                ],
              ),
            ),
            Expanded(
              child: AnimatedList(
                key: _listKey,
                itemBuilder: (_, index, animation) {
                  return Column(
                    children: [
                      SlideTransition(
                        position: Tween<Offset>(
                          begin: const Offset(-1, 0),
                          end: const Offset(0, 0),
                        ).animate(animation),
                        child: ResultCard(
                          image: images[index],
                        ),
                      ),
                      index == (images.length - 1)
                          ? const SizedBox(height: 150)
                          : const SizedBox.shrink()
                    ],
                  );
                },
              ),
            ),
          ],
        ),
        floatingActionButton: Wrap(
          direction: Axis.vertical,
          children: images.isNotEmpty
              ? [
                  Container(
                    width: 150,
                    margin:
                        const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    child: FloatingActionButton.extended(
                      heroTag: "camerabtn",
                      onPressed: () => {_getImage(ImageSource.camera)},
                      label: const Text("Open Camera"),
                    ),
                  ),
                  Container(
                    width: 150,
                    margin:
                        const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    child: FloatingActionButton.extended(
                      heroTag: "gallerybtn",
                      onPressed: () => {_getImage(ImageSource.gallery)},
                      label: const Text("Browse Gallery"),
                    ),
                  )
                ]
              : [],
        ),
      ),
    );
  }
}
