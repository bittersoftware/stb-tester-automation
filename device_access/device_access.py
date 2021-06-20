class DeviceInformation:
    @staticmethod
    def get_device_info():
        device_info = dict()
        device_info["VERSION"] = "v1.2"
        device_info["CASN"] = "CCAB2C967E98"
        device_info["STB_MODEL_NAME"] = "PTT-1000"
        device_info["STB_MANUFACTURER"] = "HUMAX"

        return device_info


class MemoryMonitor:
    @staticmethod
    def start_memory_monitor():
        import random

        return bool(random.getrandbits(1))

    @staticmethod
    def get_memory_data():

        memory_data = {
            "available": [1000, 2000, 1000, 4000],
            "free": [1200, 2200, 1300, 4300],
        }
        if (
            memory_data.get("available") is not None
            and memory_data.get("free") is not None
            and len(memory_data["available"]) > 0
            and len(memory_data["free"]) > 0
        ):
            return memory_data
        else:
            return None
