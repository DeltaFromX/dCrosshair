import json
import os


class ConfigManager:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.data = {
            "profiles": {
                "default": {
                    "dot_size": 4,
                    "dot_color": [255, 0, 0],
                    "crosshair_type": "Dot",
                    "opacity": 1.0
                }
            },
            "active_profile": "default"
        }
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.data = json.load(f)
            except Exception:
                self.save()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_active(self):
        active = self.data.get("active_profile", "default")
        return self.data["profiles"].get(active, {})

    def set_active(self, profile_name):
        if profile_name in self.data["profiles"]:
            self.data["active_profile"] = profile_name
            self.save()

    def get(self, key, default=None):
        return self.get_active().get(key, default)

    def set(self, key, value):
        active = self.data.get("active_profile", "default")
        self.data["profiles"].setdefault(active, {})
        self.data["profiles"][active][key] = value
        self.save()

    def get_profiles(self):
        return list(self.data["profiles"].keys())

    def add_profile(self, name, dot_size=4, dot_color=[255, 0, 0], crosshair_type="Dot", opacity=1.0):
        self.data["profiles"][name] = {
            "dot_size": dot_size,
            "dot_color": dot_color,
            "crosshair_type": crosshair_type,
            "opacity": opacity
        }
        self.save()
