"""
Tests for the DoseEngine model.
"""

from pinnacle_io.models import DoseEngine, Beam


def test_dose_engine_repr():
    """Test the __repr__ method of the DoseEngine class."""
    # Test without beam
    dose_engine = DoseEngine(
        id=42,
        type_name="TestEngine",
        convolve_homogeneous=1,
        fluence_homogeneous=1
    )

    # Verify the __repr__ output matches the expected format for no beam
    expected_repr = "<DoseEngine(id=42, beam='None', type_name='TestEngine')>"
    assert repr(dose_engine) == expected_repr

    # Test with beam
    beam = Beam(name="TestBeam")
    dose_engine.beam = beam

    # Verify the __repr__ output matches the expected format with beam
    expected_repr = "<DoseEngine(id=42, beam='TestBeam', type_name='TestEngine')>"
    assert repr(dose_engine) == expected_repr


def test_dose_engine_initialization():
    """Test creating a DoseEngine with all fields."""
    dose_engine = DoseEngine(
        type_name="TestEngine",
        convolve_homogeneous=1,
        fluence_homogeneous=1,
        flat_water_phantom=1,
        flat_homogeneous=1,
        electron_homogeneous=1,
        fluence_type="Photon",
        long_step_tuning_factor=1.5,
        short_step_length=0.5,
        number_of_short_steps=10,
        split_fluence_field_size_cutoff=20,
        azimuthal_bin_count=36,
        zenith_bin_count=18,
        cum_kernel_radial_bin_width=0.25,
        siddon_corner_cutoff=0.1,
        nrd_bin_width=0.5,
        allowable_dose_diff=0.02,
        high_fluence_cutoff=100.0,
        low_first_deriv_cutoff=0.1,
        low_second_deriv_cutoff=0.1,
        high_first_deriv_cutoff=10.0,
        high_second_deriv_cutoff=10.0,
        adaptive_levels=3,
        energy_flatness_cutoff=0.05,
        energy_flatness_minimum_distance=5.0,
        energy_flatness_scaling_distance=10.0
    )

    # Verify all fields are set correctly
    assert dose_engine.type_name == "TestEngine"
    assert dose_engine.convolve_homogeneous == 1
    assert dose_engine.fluence_homogeneous == 1
    assert dose_engine.flat_water_phantom == 1
    assert dose_engine.flat_homogeneous == 1
    assert dose_engine.electron_homogeneous == 1
    assert dose_engine.fluence_type == "Photon"
    assert dose_engine.long_step_tuning_factor == 1.5
    assert dose_engine.short_step_length == 0.5
    assert dose_engine.number_of_short_steps == 10
    assert dose_engine.split_fluence_field_size_cutoff == 20
    assert dose_engine.azimuthal_bin_count == 36
    assert dose_engine.zenith_bin_count == 18
    assert dose_engine.cum_kernel_radial_bin_width == 0.25
    assert dose_engine.siddon_corner_cutoff == 0.1
    assert dose_engine.nrd_bin_width == 0.5
    assert dose_engine.allowable_dose_diff == 0.02
    assert dose_engine.high_fluence_cutoff == 100.0
    assert dose_engine.low_first_deriv_cutoff == 0.1
    assert dose_engine.low_second_deriv_cutoff == 0.1
    assert dose_engine.high_first_deriv_cutoff == 10.0
    assert dose_engine.high_second_deriv_cutoff == 10.0
    assert dose_engine.adaptive_levels == 3
    assert dose_engine.energy_flatness_cutoff == 0.05
    assert dose_engine.energy_flatness_minimum_distance == 5.0
    assert dose_engine.energy_flatness_scaling_distance == 10.0


def test_dose_engine_nullable_fields():
    """Test that all fields in DoseEngine are nullable."""
    # Create a dose engine with minimal fields
    dose_engine = DoseEngine()

    # Verify all fields default to None
    assert dose_engine.type_name is None
    assert dose_engine.convolve_homogeneous is None
    assert dose_engine.fluence_homogeneous is None
    assert dose_engine.flat_water_phantom is None
    assert dose_engine.flat_homogeneous is None
    assert dose_engine.electron_homogeneous is None
    assert dose_engine.fluence_type is None
    assert dose_engine.long_step_tuning_factor is None
    assert dose_engine.short_step_length is None
    assert dose_engine.number_of_short_steps is None
    assert dose_engine.split_fluence_field_size_cutoff is None
    assert dose_engine.azimuthal_bin_count is None
    assert dose_engine.zenith_bin_count is None
    assert dose_engine.cum_kernel_radial_bin_width is None
    assert dose_engine.siddon_corner_cutoff is None
    assert dose_engine.nrd_bin_width is None
    assert dose_engine.allowable_dose_diff is None
    assert dose_engine.high_fluence_cutoff is None
    assert dose_engine.low_first_deriv_cutoff is None
    assert dose_engine.low_second_deriv_cutoff is None
    assert dose_engine.high_first_deriv_cutoff is None
    assert dose_engine.high_second_deriv_cutoff is None
    assert dose_engine.adaptive_levels is None
    assert dose_engine.energy_flatness_cutoff is None
    assert dose_engine.energy_flatness_minimum_distance is None
    assert dose_engine.energy_flatness_scaling_distance is None
