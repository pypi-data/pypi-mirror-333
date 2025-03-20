import OpenSimula as osm
import pytest

case600FF_dict = {
    "name": "Case 600FF",
    "time_step": 3600,
    "n_time_steps": 8760,
    "initial_time": "01/01/2001 00:00:00",
    "components": [
        {
            "type": "File_met",
            "name": "Denver",
            "file_type": "TMY3",
            "file_name": "mets/WD100.tmy3"
        },
        {
            "type": "Material",
            "name": "Plasterboard",
            "conductivity": 0.16,
            "density": 950,
            "specific_heat": 840
        },
        {
            "type": "Material",
            "name": "Fiberglass_quilt",
            "conductivity": 0.04,
            "density": 12,
            "specific_heat": 840
        },
        {
            "type": "Material",
            "name": "Wood_siding",
            "conductivity": 0.14,
            "density": 530,
            "specific_heat": 900
        },
        {
            "type": "Material",
            "name": "Insulation",
            "conductivity": 0.04,
            "density": 0.1,
            "specific_heat": 0.1
        },
        {
            "type": "Material",
            "name": "Timber_flooring",
            "conductivity": 0.14,
            "density": 650,
            "specific_heat": 1200
        },
        {
            "type": "Material",
            "name": "Roofdeck",
            "conductivity": 0.14,
            "density": 530,
            "specific_heat": 900
        },
        {
            "type": "Construction",
            "name": "Wall",
            "solar_alpha": [
                0.6,
                0.6
            ],
            "materials": [
                "Wood_siding",
                "Fiberglass_quilt",
                "Plasterboard"
            ],
            "thicknesses": [
                0.009,
                0.066,
                0.012
            ]
        },
        {
            "type": "Construction",
            "name": "Floor",
            "solar_alpha": [
                0,
                0.6
            ],
            "materials": [
                "Insulation",
                "Timber_flooring"
            ],
            "thicknesses": [
                1.003,
                0.025
            ]
        },
        {
            "type": "Construction",
            "name": "Roof",
            "solar_alpha": [
                0.6,
                0.6
            ],
            "materials": [
                "Roofdeck",
                "Fiberglass_quilt",
                "Plasterboard"
            ],
            "thicknesses": [
                0.019,
                0.1118,
                0.010
            ]
        },
        {
            "type": "Glazing",
            "name": "double_glazing",
            "solar_tau": 0.703,
            "solar_rho": [
                0.128,
                0.128
            ],
            "g": [
                0.769,
                0.769
            ],
            "lw_epsilon": [
                0.84,
                0.84
            ],
            "U": 2.722,
            "f_tau_nor": "-0.1175 * cos_theta**3 - 1.0295 * cos_theta**2 + 2.1354 * cos_theta",
            "f_1_minus_rho_nor": [
                "1.114 * cos_theta**3 - 3.209 * cos_theta**2 + 3.095 * cos_theta",
                "1.114 * cos_theta**3 - 3.209 * cos_theta**2 + 3.095 * cos_theta"
            ]
        },
        {
            "type": "Opening_type",
            "name": "Window",
            "glazing": "double_glazing",
            "frame_fraction": 0,
            "glazing_fraction": 1
        },
        {
            "type": "Space_type",
            "name": "constant_gain_space",
            "people_density": "0",
            "light_density": "0",
            "other_gains_density": "4.1667",
            "other_gains_radiant_fraction": 0.6,
            "infiltration": "0.5",
            "heating_setpoint": "20",
            "cooling_setpoint": "27",
            "heating_on_off": "0",
            "cooling_on_off": "0"
        },
        {
            "type": "Building",
            "name": "Building",
            "file_met": "Denver",
            "albedo": 0.2,
            "azimuth": 0,
            "shadow_calculation": "INSTANT"
        },
        {
            "type": "Space",
            "name": "space_1",
            "building": "Building",
            "space_type": "constant_gain_space",
            "floor_area": 48,
            "volume": 129.6,
            "furniture_weight": 0,
            "perfect_conditioning": False
        },
        {
            "type": "Exterior_surface",
            "name": "north_wall",
            "construction": "Wall",
            "space": "space_1",
            "ref_point": [
                8,
                6,
                0
            ],
            "width": 8,
            "height": 2.7,
            "azimuth": 180,
            "altitude": 0,
            "h_cv": [
                11.9,
                2.2
            ]
        },
        {
            "type": "Exterior_surface",
            "name": "east_wall",
            "construction": "Wall",
            "space": "space_1",
            "ref_point": [
                8,
                0,
                0
            ],
            "width": 6,
            "height": 2.7,
            "azimuth": 90,
            "altitude": 0,
            "h_cv": [
                11.9,
                2.2
            ]
        },
        {
            "type": "Exterior_surface",
            "name": "south_wall",
            "construction": "Wall",
            "space": "space_1",
            "ref_point": [
                0,
                0,
                0
            ],
            "width": 8,
            "height": 2.7,
            "azimuth": 0,
            "altitude": 0,
            "h_cv": [
                11.9,
                2.2
            ]
        },
        {
            "type": "Opening",
            "name": "south_window_1",
            "surface": "south_wall",
            "opening_type": "Window",
            "ref_point": [
                0.5,
                0.2
            ],
            "width": 3,
            "height": 2,
            "h_cv": [
                8.0,
                2.4
            ]
        },
        {
            "type": "Opening",
            "name": "south_window_2",
            "surface": "south_wall",
            "opening_type": "Window",
            "ref_point": [
                4.5,
                0.2
            ],
            "width": 3,
            "height": 2,
            "h_cv": [
                8.0,
                2.4
            ]
        },
        {
            "type": "Exterior_surface",
            "name": "west_wall",
            "construction": "Wall",
            "space": "space_1",
            "ref_point": [
                0,
                6,
                0
            ],
            "width": 6,
            "height": 2.7,
            "azimuth": -90,
            "altitude": 0,
            "h_cv": [
                11.9,
                2.2
            ]
        },
        {
            "type": "Exterior_surface",
            "name": "roof_wall",
            "construction": "Roof",
            "space": "space_1",
            "ref_point": [
                0,
                0,
                2.7
            ],
            "width": 8,
            "height": 6,
            "azimuth": 0,
            "altitude": 90,
            "h_cv": [
                14.4,
                1.8
            ]
        },
        {
            "type": "Exterior_surface",
            "name": "floor_wall",
            "construction": "Floor",
            "space": "space_1",
            "ref_point": [
                0,
                6,
                0
            ],
            "width": 8,
            "height": 6,
            "azimuth": 0,
            "altitude": -90,
            "h_cv": [
                0.8,
                2.2
            ]
        }
    ]
}

def test_ff_temperature():
    sim = osm.Simulation()
    pro = sim.new_project("pro")
    pro.read_dict(case600FF_dict)
    pro.simulate()

    T = pro.component("space_1").variable("temperature").values

    assert T.mean() == pytest.approx(25.167184227)
    assert T.max() == pytest.approx(65.70555480)
    assert T.min() == pytest.approx(-13.368846)
