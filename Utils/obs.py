import obsws_python as obs
import json
import time


class Obs:
    def __init__(self) -> bool:
        try:
            with open("./Config/obs_config.json", "r") as openfile:
                # Reading from json file
                self.connect = json.load(openfile)
            self.client = obs.ReqClient(
                host=self.connect["IP"],
                port=self.connect["PORT"],
                password=self.connect["PASS"],
            )
        except:
            pass
        try:
            with open("./Config/elem_config.json", "r") as openfile:
                # Reading from json file
                self.scene_data = json.load(openfile)
        except:
            pass

    def test_connection(self) -> str:
        try:
            self.client = obs.ReqClient(
                host=self.connect["IP"],
                port=self.connect["PORT"],
                password=self.connect["PASS"],
            )
            return self.client.get_version().obs_version
        except Exception as e:
            print(e)
            return "ERROR"

    def test_connection_params(self, ip, port, passw) -> str:
        try:
            client = obs.ReqClient(host=ip, port=port, password=passw)
            return client.get_version().obs_version
        except Exception as e:
            print(e)
            return "ERROR"

    def get_scenes(self):
        try:
            resp = self.client.get_scene_list()
            scenes = []
            for scene in [di.get("sceneName") for di in reversed(resp.scenes)]:
                scenes.append(scene)
            return scenes
        except:
            return "ERROR"

    def get_scene_items(self, scene):
        try:
            items_d = {}
            resp = self.client.get_scene_item_list(scene).scene_items
            groups = self.client.get_group_list().groups
            for group in groups:
                resp_g = self.client.get_group_scene_item_list(group).scene_items
                for item in resp_g:
                    items_d[item["sourceName"]] = {
                        "id": item["sceneItemId"],
                        "name": item["sourceName"],
                    }
            for item in resp:
                items_d[item["sourceName"]] = {
                    "id": item["sceneItemId"],
                    "name": item["sourceName"],
                }
            items_d = dict(sorted(items_d.items()))
            return items_d
        except Exception as e:
            return "ERROR" + str(e)

    def serve(self, team):
        try:
            elements = self.scene_data

            if team == "*":
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["H_SERVE"], True
                )
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["A_SERVE"], False
                )
            elif team == "a":
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["H_SERVE"], False
                )
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["A_SERVE"], True
                )
            print("serve " + team)
            return "OK"
        except:
            return "ERROR"

    def time_out(self):
        try:
            elements = self.scene_data

            self.client.set_scene_item_enabled(
                elements["SCENE"], elements["TIME_OUT"], True
            )
            time.sleep(60)
            self.client.set_scene_item_enabled(
                elements["SCENE"], elements["TIME_OUT"], False
            )
            print("time_out")
            return "OK"
        except:
            return "ERROR"

    def substitution(self, team):
        try:
            elements = self.scene_data

            if team == "*":
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["H_SUBSTITUTION"], True
                )
                time.sleep(10)
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["H_SUBSTITUTION"], False
                )
            elif team == "a":
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["A_SUBSTITUTION"], True
                )
                time.sleep(10)
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["A_SUBSTITUTION"], False
                )
            print("substitution")
            return "OK"
        except:
            return "ERROR"

    def match_point(self, show: bool):
        try:
            elements = self.scene_data

            if show == True:
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["MATCH_POINT"], True
                )
            else:
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["MATCH_POINT"], False
                )
            print("match_point " + show)
            return "OK"
        except:
            return "ERROR"

    def set_point(self, show: bool):
        try:
            elements = self.scene_data

            if show == True:
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["SET_POINT"], True
                )
            else:
                self.client.set_scene_item_enabled(
                    elements["SCENE"], elements["SET_POINT"], False
                )
            print("set_point " + show)
            return "OK"
        except:
            return "ERROR"

    def _set_input_settings(self, input, value):
        try:
            return self.client.set_input_settings(input, value, True)
        except:
            return "ERROR"

    def _get_input_settings(self, input):
        try:
            return self.client.get_input_settings(input)
        except:
            return "ERROR"
