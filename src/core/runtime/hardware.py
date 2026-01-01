class HardwareProbe:
    def capabilities(self):
        caps = {"cpu"}
        try:
            import torch
            if torch.cuda.is_available():
                caps.add("gpu")
        except Exception:
            pass
        return caps

    def vram_mb(self):
        try:
            import torch
            if torch.cuda.is_available():
                return torch.cuda.get_device_properties(0).total_memory // (1024 * 1024)
        except Exception:
            return None
