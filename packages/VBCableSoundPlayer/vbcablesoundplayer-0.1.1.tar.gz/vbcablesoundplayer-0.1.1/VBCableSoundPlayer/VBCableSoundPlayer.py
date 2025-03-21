# VBCableSoundPlayer/VBCableSoundPlayer.py

import sounddevice as sd

class VBCableSoundPlayer:
    _instance = None

    def __init__(self, output_device_name="CABLE Input") -> None:
        if VBCableSoundPlayer._instance is not None:
            raise Exception("This class is a singleton!")
        self.output_device_name = output_device_name
        output_device_id = self._search_output_device_id(output_device_name)
        input_device_id = 0
        sd.default.device = [input_device_id, output_device_id]

    @classmethod
    def init_player(cls):
        """Initialize the singleton instance of the player."""
        if cls._instance is None:
            cls._instance = cls(output_device_name="CABLE Input")

    @classmethod
    def play(cls, data, rate) -> bool:
        """Play sound using the singleton instance."""
        if cls._instance is None:
            cls.init_player()
        sd.play(data, rate)
        sd.wait()
        return True

    def _search_output_device_id(self, output_device_name, output_device_host_api=0) -> int:
        devices = sd.query_devices()
        output_device_id = None
        for device in devices:
            is_output_device_name = output_device_name in device["name"]
            is_output_device_host_api = device["hostapi"] == output_device_host_api
            if is_output_device_name and is_output_device_host_api:
                output_device_id = device["index"]
                break

        if output_device_id is None:
            print("VBCable not found")
            exit()
        return output_device_id
