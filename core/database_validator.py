"""
Speedway Game Engine

Database Validator Module

Version: 1.0

Validates imported JSON databases
before use by the game engine.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any
import json
import os



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class ValidationReport:


    database_name: str

    valid: bool = True

    errors: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )



# ==========================================================
# VALIDATOR
# ==========================================================


class DatabaseValidator:


    def __init__(self):

        self.reports: List[ValidationReport] = []



    # ======================================================
    # LOAD JSON
    # ======================================================


    def load_json(
            self,
            filepath
    ):


        if not os.path.exists(filepath):

            raise FileNotFoundError(

                filepath

            )


        with open(

            filepath,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    # ======================================================
    # REQUIRED FIELDS
    # ======================================================


    def check_required_fields(
            self,
            database_name,
            records,
            required_fields
    ):


        report = ValidationReport(

            database_name

        )


        for index, record in enumerate(records):


            for field in required_fields:


                if field not in record:


                    report.valid = False


                    report.errors.append(

                        f"Record {index} missing {field}"

                    )



        self.reports.append(

            report

        )


        return report



    # ======================================================
    # DUPLICATE CHECK
    # ======================================================


    def check_duplicates(
            self,
            database_name,
            records,
            key="id"
    ):


        report = ValidationReport(

            database_name

        )


        seen = set()



        for record in records:


            value = record.get(

                key

            )


            if value in seen:


                report.valid = False


                report.errors.append(

                    f"Duplicate {key}: {value}"

                )


            seen.add(

                value

            )



        self.reports.append(

            report

        )


        return report



    # ======================================================
    # TYPE CHECK
    ======================================================


    def check_types(
            self,
            database_name,
            records,
            rules
    ):


        report = ValidationReport(

            database_name

        )


        for index, record in enumerate(records):


            for field, expected in rules.items():


                value = record.get(

                    field

                )


                if value is not None:


                    if not isinstance(

                        value,

                        expected

                    ):


                        report.valid = False


                        report.errors.append(

                            f"{field} wrong type in record {index}"

                        )



        self.reports.append(

            report

        )


        return report



    # ======================================================
    # RIDER DATABASE VALIDATION
    ======================================================


    def validate_riders(
            self,
            riders
    ):


        self.check_required_fields(

            "Riders",

            riders,

            [

                "id",

                "name",

                "age",

                "cma"

            ]

        )


        self.check_duplicates(

            "Riders",

            riders

        )


        self.check_types(

            "Riders",

            riders,

            {

                "id": int,

                "age": int,

                "cma": (int,float)

            }

        )



    # ======================================================
    # TEAM DATABASE VALIDATION
    ======================================================


    def validate_teams(
            self,
            teams
    ):


        self.check_required_fields(

            "Teams",

            teams,

            [

                "id",

                "name"

            ]

        )


        self.check_duplicates(

            "Teams",

            teams

        )



    # ======================================================
    # FIXTURE VALIDATION
    ======================================================


    def validate_fixtures(
            self,
            fixtures
    ):


        self.check_required_fields(

            "Fixtures",

            fixtures,

            [

                "home_team",

                "away_team",

                "date"

            ]

        )



    # ======================================================
    # SUMMARY
    ======================================================


    def summary(self):


        return [

            {

                "database":

                    report.database_name,


                "valid":

                    report.valid,


                "errors":

                    len(

                        report.errors

                    ),


                "warnings":

                    len(

                        report.warnings

                    )

            }

            for report

            in self.reports

        ]



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    validator = DatabaseValidator()


    riders = [

        {

            "id":1,

            "name":"Test Rider",

            "age":20,

            "cma":7.5

        }

    ]


    validator.validate_riders(

        riders

    )


    print(

        validator.summary()

    )
