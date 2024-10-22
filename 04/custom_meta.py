from typing import Any


class CustomMeta(type):

    @staticmethod
    def add_prefix(name_creat_cls: str):
        if name_creat_cls.startswith("__") and name_creat_cls.endswith("__"):
            return name_creat_cls
        return f"custom_{name_creat_cls}"

    @staticmethod
    def override_setattr(instance):
        old_setattr = instance.__setattr__

        def new_setattr(obj, name, value):
            custom_name = CustomMeta.add_prefix(name)
            return old_setattr(obj, custom_name, value)

        instance.__setattr__ = new_setattr

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: Any,
    ):
        new_namespace = {}
        for atr_mthd_cls, value in namespace.items():
            new_attr_name = mcs.add_prefix(atr_mthd_cls)
            new_namespace[new_attr_name] = value

        self = super().__new__(mcs, name, bases, new_namespace, **kwds)
        mcs.override_setattr(self)
        return self
