import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:omdena_srilanka_tea_quality_client/pages/result_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Size size;

  XFile? image;
  late ImagePicker picker;

  @override
  void initState() {
    super.initState();

    picker = ImagePicker();
  }

  void getImage(ImageSource source) async {
    image = await picker.pickImage(
      source: source,
      maxWidth: 512,
      maxHeight: 512,
      imageQuality: 59,
    );

    if (image != null) {
      goToResultScreen(image);
    }
  }

  void goToResultScreen(XFile? image) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => ResultPage(image),
      ),
    );
  }

  ButtonStyle buttonStyle() {
    return ElevatedButton.styleFrom(
      primary: Colors.white,
      onPrimary: Colors.black,
      padding: const EdgeInsets.all(5),
      minimumSize: Size(size.width * 0.55, size.height * 0.08),
    );
  }

  @override
  Widget build(BuildContext context) {
    size = MediaQuery.of(context).size;
    return SafeArea(
      child: Scaffold(
        body: Container(
          width: size.width,
          height: size.height,
          child: Stack(
            children: [
              Container(
                height: size.height * 0.6,
                width: size.width,
                child: FittedBox(
                  fit: BoxFit.fill,
                  child: Image.asset(
                    'assets/images/home.png',
                  ),
                ),
              ),
              Positioned(
                left: size.width * 0.15,
                top: size.height * 0.5,
                child: Container(
                  transformAlignment: Alignment.center,
                  height: size.height * 0.3,
                  width: size.width * 0.7,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(24),
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
                            //Take a picture
                            getImage(ImageSource.camera);
                          },
                          child: Text(
                            'Take Picture',
                            style: TextStyle(fontSize: size.width * 0.045),
                          ),
                          style: buttonStyle(),
                        ),
                        ElevatedButton(
                          onPressed: () {
                            //Browse from gallery!
                            getImage(ImageSource.gallery);
                          },
                          child: Text(
                            'Browse From Gallery',
                            style: TextStyle(fontSize: size.width * 0.045),
                          ),
                          style: buttonStyle(),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
