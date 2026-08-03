"""
Speedway Game Engine

Merchandise Manager Module

Version: 1.0

Controls commercial merchandise sales,
product demand and brand value.

"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List



# ==========================================================
# DATA STRUCTURES
# ==========================================================


@dataclass(slots=True)
class Product:


    name: str

    category: str

    price: float

    popularity: int = 50

    sales: int = 0



@dataclass(slots=True)
class MerchandiseProfile:


    entity_id: int

    brand_value: int = 50

    total_sales: int = 0

    revenue: float = 0

    products: List[Product] = field(
        default_factory=list
    )



# ==========================================================
# MANAGER
# ==========================================================


class MerchandiseManager:


    def __init__(self):

        self.club_merchandise: Dict[int, MerchandiseProfile] = {}

        self.rider_merchandise: Dict[int, MerchandiseProfile] = {}

        self.sales_history = []



    # ======================================================
    # PROFILE MANAGEMENT
    # ======================================================


    def get_club_profile(
            self,
            club_id
    ):


        if club_id not in self.club_merchandise:


            self.club_merchandise[club_id] = MerchandiseProfile(

                entity_id=club_id

            )


        return self.club_merchandise[club_id]



    def get_rider_profile(
            self,
            rider_id
    ):


        if rider_id not in self.rider_merchandise:


            self.rider_merchandise[rider_id] = MerchandiseProfile(

                entity_id=rider_id

            )


        return self.rider_merchandise[rider_id]



    # ======================================================
    # PRODUCT CREATION
    # ======================================================


    def create_product(
            self,
            profile,
            name,
            category,
            price
    ):


        product = Product(

            name=name,

            category=category,

            price=price

        )


        profile.products.append(

            product

        )


        return product



    # ======================================================
    # SALES CALCULATION
    # ======================================================


    def calculate_sales(
            self,
            profile,
            fan_loyalty,
            popularity,
            championship_bonus=0
    ):


        demand = (

            profile.brand_value

            +

            fan_loyalty

            +

            popularity

            +

            championship_bonus

        )


        units = int(

            demand *

            5

        )


        return max(

            units,

            0

        )



    # ======================================================
    # PROCESS SALE
    # ======================================================


    def sell_product(
            self,
            profile,
            product,
            quantity
    ):


        revenue = (

            product.price *

            quantity

        )


        product.sales += quantity

        profile.total_sales += quantity

        profile.revenue += revenue


        self.sales_history.append({

            "product":

                product.name,

            "quantity":

                quantity,

            "revenue":

                revenue

        })


        return revenue



    # ======================================================
    # CHAMPIONSHIP EFFECT
    # ======================================================


    def championship_boost(
            self,
            profile
    ):


        profile.brand_value += 10


        profile.brand_value = min(

            profile.brand_value,

            100

        )



    # ======================================================
    # BRAND DEVELOPMENT
    # ======================================================


    def update_brand_value(
            self,
            profile,
            media_attention,
            attendance
    ):


        growth = (

            media_attention *

            0.1

            +

            attendance *

            0.001

        )


        profile.brand_value += int(

            growth

        )


        profile.brand_value = max(

            0,

            min(

                profile.brand_value,

                100

            )

        )



    # ======================================================
    # RETRO COLLECTIONS
    # ======================================================


    def create_retro_collection(
            self,
            club_profile,
            era
    ):


        product = Product(

            name=f"{era} Retro Collection",

            category="Historical",

            price=35,

            popularity=80

        )


        club_profile.products.append(

            product

        )


        return product



    # ======================================================
    # REPORTS
    # ======================================================


    def commercial_report(
            self,
            entity_id,
            entity_type="club"
    ):


        if entity_type == "club":

            profile = self.get_club_profile(

                entity_id

            )

        else:

            profile = self.get_rider_profile(

                entity_id

            )


        return {


            "brand_value":

                profile.brand_value,


            "sales":

                profile.total_sales,


            "revenue":

                round(

                    profile.revenue,

                    2

                )

        }



# ==========================================================
# TEST MODULE
# ==========================================================


if __name__ == "__main__":


    manager = MerchandiseManager()


    profile = manager.get_club_profile(1)


    manager.create_product(

        profile,

        "1976 Championship Jacket",

        "Retro",

        25

    )


    print(

        manager.commercial_report(1)

    )
