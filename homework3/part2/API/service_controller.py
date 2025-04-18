class ServiceController:

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._methods_name = {}

        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith("__") and attr_name != "controller":
                splited_names = attr_name.split("_")

                cls._methods_name.update({
                    f"{splited_names[0]}{"".join([words.capitalize() for words in splited_names[1:]])}": attr_name
                })

    def controller(self, method_name, *args, **kwargs):
        real_name = self.__class__._methods_name.get(method_name)
        if not real_name:
            raise AttributeError(f"Method '{method_name}' not found")

        method = getattr(self, real_name)
        return method(*args, **kwargs)
