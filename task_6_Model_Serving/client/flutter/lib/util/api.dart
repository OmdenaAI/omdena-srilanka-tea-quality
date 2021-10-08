import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;

class ApiStatusRes {
  late String status;
  late String msg;

  ApiStatusRes(Map<String, dynamic> data) {
    status = data['status'] ?? "n/a";
    msg = data['msg'] ?? "n/a";
  }
}

class ApiImageRes {
  late String status;
  late String msg;

  ApiImageRes(Map<String, dynamic> data) {
    status = data['status'] ?? "n/a";
    msg = data['msg'] ?? "n/a";
  }
}

class Api {
  static String baseUrl =
      "http://omdenatealeafqualitypredapi-env-manual.ap-south-1.elasticbeanstalk.com/api/";

  static Future<bool> checkServerStatus() async {
    try {
      var url = Uri.parse(baseUrl);
      var res = await http.get(url);

      if (res.statusCode != 200) {
        return false;
      }

      final response = ApiStatusRes(json.decode(res.body));
      return response.status.compareTo("success") == 0;
    } catch (e) {
      log(e.toString());
      return false;
    }
  }

  static Future<String> checkImageQuality(String path) async {
    try {
      var req =
          http.MultipartRequest("POST", Uri.parse(baseUrl + "inferences"));

      req.files.add(await http.MultipartFile.fromPath('file', path));

      var res = await req.send();

      if (res.statusCode != 200) {
        return "Response is not okay";
      }

      final response = await http.Response.fromStream(res);
      final data = ApiStatusRes(json.decode(response.body));
      return data.msg;
    } catch (e) {
      log(e.toString());
      return "Error occured";
    }
  }
}
