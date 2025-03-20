from OpenSimula.components.Test_component import Test_component
from OpenSimula.components.Material import Material
from OpenSimula.components.Glazing import Glazing
from OpenSimula.components.Frame import Frame
from OpenSimula.components.Construction import Construction
from OpenSimula.components.Opening_type import Opening_type
from OpenSimula.components.File_data import File_data
from OpenSimula.components.Day_schedule import Day_schedule
from OpenSimula.components.Week_schedule import Week_schedule
from OpenSimula.components.Year_schedule import Year_schedule
from OpenSimula.components.File_met import File_met
from OpenSimula.components.Space_type import Space_type
from OpenSimula.components.Building import Building
from OpenSimula.components.Space import Space
from OpenSimula.components.Exterior_surface import Exterior_surface
from OpenSimula.components.Interior_surface import Interior_surface
from OpenSimula.components.Virtual_surface import Virtual_surface
from OpenSimula.components.Underground_surface import Underground_surface
from OpenSimula.components.Shadow_surface import Shadow_surface
from OpenSimula.components.Opening import Opening
from OpenSimula.components.Calculator import Calculator
from OpenSimula.components.HVAC_DX_equipment import HVAC_DX_equipment
from OpenSimula.components.HVAC_DX_system import HVAC_DX_system
from OpenSimula.components.HVAC_perfect_system import HVAC_perfect_system

DEFAULT_COMPONENTS_ORDER = [
                    "Space_type",
                    "Exterior_surface",
                    "Underground_surface",
                    "Interior_surface",
                    "Virtual_surface",
                    "Shadow_surface",
                    "Opening",
                    "Space",
                    "Building",
                    "HVAC_perfect_system",
                    "HVAC_DX_system",
                    "Calculator"
                ]

