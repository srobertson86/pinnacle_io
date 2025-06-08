# Product Requirements Document – pinnacle_io

## Purpose
Provide a reliable, local-use Python library for reading and writing Pinnacle treatment planning system files.

## Key Functional Requirements

### 1. Core Capabilities
- Parse Pinnacle structured text files including:
  - `.header`, `.ImageInfo`, `.PatientInfo`
  - `plan.Trial`, `plan.Points`, `plan.roi`, `plan.PatientSetup`
  - `plan.Pinnacle.Machines` and related machine configuration files
  - Binary dose grid files (*.binary.*)
- Represent file data using SQLAlchemy ORM-style models with comprehensive coverage:
  - Patient data (Patient, PatientLite, PatientSetup)
  - Plan components (Plan, Trial, Point, ROI)
  - Machine configuration (Machine, MachineConfig, MachineEnergy, MachineAngle)
  - Treatment details (Beam, ControlPoint, MLC, Compensator, Wedge)
  - Imaging (ImageSet, ImageInfo)
  - Dosimetry (Dose, DoseGrid, DoseEngine, MonitorUnitInfo)
- Write structured model data back to Pinnacle-compatible text files
- Support for handling binary dose grid data

### 2. Utility Functions
- Extract and process Pinnacle data structures
- Handle specialized data conversions via utility modules
- Support patient enumeration and status tracking
- Manage common Pinnacle file format settings (indentation, encoding)

### 3. GUI Support (planned)
- Render Institution file data in a readable format
- Allow interactive navigation of associated Patients and Plans

### 4. Testing
- Comprehensive test suite using `pytest` covering:
  - All reader modules (institution, patient, plan, trial, etc.)
  - All writer modules (corresponding writers for each reader)
  - All data models and their relationships
  - Edge cases and error handling
  - Binary data processing
- Test data provided in tests/test_data with realistic Pinnacle file structures

## Technical Constraints
- Python 3.9+
- No external database dependencies
- Editable installation with `pip install -e .`

## Out of Scope
- Persistent database integration
- DICOM compatibility
- Remote file handling

## Future Considerations
- Full-blown GUI with drag-and-drop support
- Integration with visualization tools for image slices and ROIs

## Directory Structure

pinnacle_io/
├── pinnacle_io/
│   ├── __init__.py
│   ├── config.py                       # Configuration and constants
│   ├── models/                         # SQLAlchemy models
│   │   ├── beam.py
│   │   ├── compensator.py
│   │   ├── control_point.py
│   │   ├── cp_manager.py
│   │   ├── dose.py
│   │   ├── dose_engine.py
│   │   ├── dose_grid.py
│   │   ├── image_info.py
│   │   ├── image_set.py
│   │   ├── institution.py
│   │   ├── machine.py
│   │   ├── machine_angle.py
│   │   ├── machine_config.py
│   │   ├── machine_energy.py
│   │   ├── mlc.py
│   │   ├── monitor_unit_info.py
│   │   ├── patient.py
│   │   ├── patient_lite.py
│   │   ├── patient_representation.py
│   │   ├── patient_setup.py
│   │   ├── pinnacle_base.py
│   │   ├── plan.py
│   │   ├── point.py
│   │   ├── prescription.py
│   │   ├── roi.py
│   │   ├── trial.py
│   │   └── wedge_context.py
│   ├── readers/                        # File readers
│   │   ├── dose_reader.py
│   │   ├── image_set_reader.py
│   │   ├── institution_reader.py
│   │   ├── machine_reader.py
│   │   ├── patient_reader.py
│   │   ├── patient_setup_reader.py
│   │   ├── pinnacle_file_reader.py
│   │   ├── plan_reader.py
│   │   ├── point_reader.py
│   │   ├── roi_reader.py
│   │   └── trial_reader.py
│   ├── writers/                        # File writers
│   │   ├── beam_writer.py
│   │   ├── control_point_writer.py
│   │   ├── dose_writer.py
│   │   ├── image_set_writer.py
│   │   ├── institution_writer.py
│   │   ├── machine_writer.py
│   │   ├── patient_setup_writer.py
│   │   ├── patient_writer.py
│   │   ├── plan_writer.py
│   │   ├── point_writer.py
│   │   ├── roi_writer.py
│   │   └── trial_writer.py
│   ├── gui/                           # Optional visualization tools (planned)
│   │   └── __init__.py
│   └── utils/                         # Utilities
│       ├── converters.py
│       └── patient_enum.py
├── tests/                            # Comprehensive test suite
│   ├── test_beam.py
│   ├── test_compensator.py
│   ├── test_control_point.py
│   ├── test_cp_manager.py
│   ├── test_dose.py
│   ├── test_dose_edge_cases.py
│   ├── test_dose_engine.py
│   ├── test_dose_grid.py
│   ├── test_image_info.py
│   ├── test_image_set.py
│   ├── test_institution.py
│   ├── test_machine.py
│   ├── test_machine_angle.py
│   ├── test_machine_config.py
│   ├── test_machine_energy.py
│   ├── test_max_dose_point.py
│   ├── test_mlc.py
│   ├── test_monitor_unit_info.py
│   ├── test_patient.py
│   ├── test_patient_lite.py
│   ├── test_patient_representation.py
│   ├── test_patient_setup.py
│   ├── test_pinnacle_file_reader.py
│   ├── test_plan.py
│   ├── test_point.py
│   ├── test_roi.py
│   └── test_trial.py
├── examples/                         # Usage examples (to be added)
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.cfg
└── setup.py
