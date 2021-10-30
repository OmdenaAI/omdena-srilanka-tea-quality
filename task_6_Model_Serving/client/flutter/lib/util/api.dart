import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:omdena_srilanka_tea_quality_client/constants.dart' as constants;

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
  late String result;
  late String error;
  Map<String, double> categories = {};
  bool isSuccess = true;

  ApiImageRes(Map<String, dynamic> data) {
    status = data['status'] ?? "n/a";

    categories['below_best'] =
        data['predictions']['categories']['below_best'] ?? 0;
    categories['best'] = data['predictions']['categories']['best'] ?? 0;
    categories['poor'] = data['predictions']['categories']['poor'] ?? 0;

    result = data['predictions']['type'] ?? "unknown";
    msg = data['msg'] ?? "n/a";

    log("Image res success" + status + " " + categories.toString());
  }

  ApiImageRes.error(String errorMsg) {
    log("Error occured in ApiImageRes");
    log(errorMsg);

    isSuccess = false;
    error = errorMsg;
  }
}

class Api {
  static Future<bool> checkServerStatus() async {
    try {
      var url = Uri.parse(constants.serverUrl);
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

  static Future<ApiImageRes> checkImageQuality(String path) async {
    try {
      var req = http.MultipartRequest(
          "POST", Uri.parse(constants.serverUrl + "inferences"));

      req.files.add(await http.MultipartFile.fromPath('file', path));

      var res = await req.send();

      if (res.statusCode != 200) {
        return ApiImageRes.error("Response is not okay");
      }

      final response = await http.Response.fromStream(res);
      final data = ApiImageRes(json.decode(response.body));
      return data;
    } catch (e) {
      return ApiImageRes.error(e.toString());
    }
  }

  // FOR LOCAL DEV PURPOSE ONLY!
  static Future<ApiImageRes> dummyResponse() async {
    try {
      var body = {
        "status": "success",
        "msg": "image processed",
        "predictions": {
          "type": "Fresh",
          "categories": {"below_best": 100.0}
        }
      };

      final data = ApiImageRes(body);

      await Future.delayed(const Duration(seconds: 2));

      return data;
    } catch (e) {
      return ApiImageRes.error(e.toString());
    }
  }
}
