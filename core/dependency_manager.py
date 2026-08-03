"""
Speedway Game Engine

Dependency Manager Module

Version: 1.0

Controls module loading,
dependencies and startup validation.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Callable



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class ModuleDependency:


    name: str

    version: str

    loader: Callable

    dependencies: List[str] = field(
        default_factory=list
    )

    loaded: bool = False



# ==========================================================
# DEPENDENCY MANAGER
# ==========================================================


class DependencyManager:


    def __init__(self):

        self.modules: Dict[
            str,
            ModuleDependency
        ] = {}


        self.load_order: List[str] = []



    # ======================================================
    # REGISTER MODULE
    # ======================================================


    def register_module(
            self,
            name,
            version,
            loader,
            dependencies=None
    ):


        if dependencies is None:

            dependencies = []



        module = ModuleDependency(

            name=name,

            version=version,

            loader=loader,

            dependencies=dependencies

        )


        self.modules[name] = module



    # ======================================================
    # CHECK DEPENDENCIES
    # ======================================================


    def check_dependencies(
            self,
            module_name
    ):


        module = self.modules.get(

            module_name

        )


        if not module:

            return False



        for dependency in module.dependencies:


            if dependency not in self.modules:


                return False



        return True



    # ======================================================
    # LOAD MODULE
    # ======================================================


    def load_module(
            self,
            module_name
    ):


        module = self.modules.get(

            module_name

        )


        if not module:

            raise Exception(

                f"Module not registered: {module_name}"

            )



        if module.loaded:

            return True



        for dependency in module.dependencies:


            self.load_module(

                dependency

            )



        module.loader()


        module.loaded = True


        self.load_order.append(

            module_name

        )


        return True



    # ======================================================
    # LOAD ALL MODULES
    # ======================================================


    def load_all(self):


        for module_name in self.modules:


            self.load_module(

                module_name

            )



        return self.load_order



    # ======================================================
    # HEALTH CHECK
    # ======================================================


    def health_check(self):


        return {


            name:

            {

                "version":

                module.version,


                "loaded":

                module.loaded

            }


            for name, module

            in self.modules.items()

        }



    # ======================================================
    # RESET
    # ======================================================


    def reset(self):


        for module in self.modules.values():


            module.loaded = False



        self.load_order.clear()



# ==========================================================
# GLOBAL MANAGER
# ==========================================================


dependency_manager = DependencyManager()



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    def config_loader():

        print(

            "Configuration Loaded"

        )



    def database_loader():

        print(

            "Database Loaded"

        )



    dependency_manager.register_module(

        "config",

        "1.0",

        config_loader

    )


    dependency_manager.register_module(

        "database",

        "1.0",

        database_loader,

        [

            "config"

        ]

    )


    dependency_manager.load_all()


    print(

        dependency_manager.health_check()

    )
