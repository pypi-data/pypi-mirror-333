from typing import Any, Optional, Type

class Singleton:
    # Class variable to store the single instance of the class
    __INSTANCE__:Optional['Singleton'] = None

    def __new__(cls: Type['Singleton'], *args : Any, **kwargs : Any) -> 'Singleton':
        # Checks to see if an instance already exists
        if cls.__INSTANCE__ == None:
            # Creates a new instance if none currently exist
            cls.__INSTANCE__ = super(Singleton, cls).__new__(cls)

        assert cls.__INSTANCE__ is not None
        return cls.__INSTANCE__