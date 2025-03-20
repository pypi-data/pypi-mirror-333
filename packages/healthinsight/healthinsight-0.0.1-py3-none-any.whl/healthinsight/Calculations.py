# -*- coding: utf-8 -*-

from __future__ import division
import math

class HealthCalc:
    """
    A class containing various health indicator calculations, including BMI, BAI, BSI, and mortality rates.
    """

    @staticmethod
    def bmi(mass, height):
        """ 
        Calculate Body Mass Index (BMI).

        Params:
        ------
        mass: float : Mass of the person in kg
        height: float : Height of the person in meters

        Usage:
        -----
        >>> HealthCalc.bmi(mass=65, height=1.70)
        """
        bmi_value = mass / height ** 2
        category = ("Underweight" if bmi_value < 18.5 else "Overweight" if bmi_value > 23 else "Obese" if bmi_value > 30 else "Normal")
        return bmi_value, category

    @staticmethod
    def bai(hip_circumference, height):
        """ 
        Calculate Body Adipose Index (BAI).

        Params:
        ------
        hip_circumference: float : Hip circumference in cm
        height: float : Height in meters

        Usage:
        -----
        >>> HealthCalc.bai(hip_circumference=90, height=1.75)
        """
        return ((100 * hip_circumference) / (height * math.sqrt(height))) - 18

    @staticmethod
    def bsi(wc, mass, height):
        """ 
        Calculate Body Shape Index (BSI).

        Params:
        ------
        wc: float : Waist circumference in cm
        mass: float : Mass of the person in kg
        height: float : Height in meters

        Usage:
        -----
        >>> HealthCalc.bsi(wc=80, mass=65, height=1.75)
        """
        return wc / (math.pow((mass / height ** 2), 2 / 3)) * math.sqrt(height)



    @staticmethod
    def tbw(weight, age):
        """ 
        Calculate Total Body Water (TBW).

        Params:
        ------
        weight: float : Weight of the person in kg
        age: int : Age of the person in years

        Usage:
        -----
        >>> HealthCalc.tbw(weight=70, age=30)
        """
        C = 0.6 if age in range(18, 60) else 0.5 if age in range(61, 100) else 0.45
        return weight * C

    @staticmethod
    def corpulence_index(mass, height):
        """ 
        Calculate Corpulence Index.

        Params:
        ------
        mass: float : Mass of the person in kg
        height: float : Height in meters

        Usage:
        -----
        >>> HealthCalc.corpulence_index(mass=65, height=1.75)
        """
        return mass / height ** 3

    @staticmethod
    def waist_to_hip(waist_size, hip_size):
        """ 
        Calculate Waist to Hip Ratio.

        Params:
        ------
        waist_size: float : Waist circumference in cm
        hip_size: float : Hip circumference in cm

        Usage:
        -----
        >>> HealthCalc.waist_to_hip(waist_size=80, hip_size=90)
        """
        return waist_size / hip_size

    @staticmethod
    def pignetindex(height, weight, chest_circumference):
        """ 
        Calculate Pignet Index (Body Build Index).

        Params:
        ------
        height: float : Height in cm
        weight: float : Weight in kg
        chest_circumference: float : Chest circumference in cm

        Usage:
        -----
        >>> HealthCalc.pignetindex(height=175, weight=70, chest_circumference=90)
        """
        return height - (weight + chest_circumference)

    @staticmethod
    def perinatal_mortality(neonatal_deaths):
        """ 
        Calculate Perinatal Mortality Rate.

        Params:
        ------
        neonatal_deaths: int : Number of neonatal deaths

        Usage:
        -----
        >>> HealthCalc.perinatal_mortality(neonatal_deaths=500)
        """
        return (sum(neonatal_deaths) / 1000) * 100

    @staticmethod
    def maternal_mortality_ratio(num_maternal_deaths):
        """ 
        Calculate Maternal Mortality Ratio.

        Params:
        ------
        num_maternal_deaths: int : Number of maternal deaths

        Usage:
        -----
        >>> HealthCalc.maternal_mortality_ratio(num_maternal_deaths=100)
        """
        return num_maternal_deaths / 100000

    @staticmethod
    def infant_mortality(num_infant_deaths):
        """ 
        Calculate Infant Mortality Rate.

        Params:
        ------
        num_infant_deaths: int : Number of infant deaths

        Usage:
        -----
        >>> HealthCalc.infant_mortality(num_infant_deaths=50)
        """
        return (num_infant_deaths / 100000) * 100

    @staticmethod
    def birthrate(number_of_live_births, population):
        """ 
        Calculate Birth Rate.

        Params:
        ------
        number_of_live_births: int : Number of live births
        population: int : Total population

        Usage:
        -----
        >>> HealthCalc.birthrate(number_of_live_births=2000, population=1000000)
        """
        return (number_of_live_births / population) * 1000
