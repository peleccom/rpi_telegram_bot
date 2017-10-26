class Settings:
    class __Settings:
        def __init__(self):
            self.settings = {}

        def set_value(self, name, value):
            self.settings[name] = value

        def get_value(self, name):
            return self.settings.get(name)

    instance = None

    def __init__(self):
        if not Settings.instance:
            Settings.instance = Settings.__Settings()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def set_value(self, name, value):
        self.instance.set_value(name, value)

    def get_value(self, name):
        return self.instance.get_value(name)
