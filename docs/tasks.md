# Task Breakdown – pinnacle_io

This file tracks the high-level and detailed tasks for building the `pinnacle_io` Python library.

---

## 📁 Project Initialization

- [ ] Set up project directory structure
- [ ] Initialize `git` repository
- [ ] Add `.gitignore` for Python, virtual environments, and common IDEs
- [ ] Add MIT `LICENSE` file
- [ ] Create `README.md`
- [ ] Create packaging files:
  - [ ] `pyproject.toml`
  - [ ] `setup.py`
  - [ ] `setup.cfg`

---

## 🏗️ Core Modules

### Models (SQLAlchemy)
- [x] Implement `models/base.py` (base model for all SQLAlchemy models)
- [x] Implement `models/institution.py` (including PatientLite model)
- [x] Implement `models/patient.py`
- [x] Implement `models/image_set.py` (including ImageInfo model)
- [ ] Implement `models/plan.py`

### Readers
- [x] Implement `readers/institution_reader.py`
- [x] Implement `readers/patient_reader.py`
- [x] Implement `readers/image_set_reader.py`
- [ ] Implement `readers/plan_reader.py`

### Writers
- [x] Implement `writers/institution_writer.py`
- [x] Implement `writers/patient_writer.py`
- [x] Implement `writers/image_set_writer.py`
- [ ] Implement `writers/plan_writer.py`

---

## 🔧 Utilities

- [ ] Implement `utils/tar_handler.py`
  - [ ] Check disk space before extraction
  - [ ] Support compressed and uncompressed `.tar` files
- [ ] Implement `utils/temp_manager.py`
  - [ ] Create and manage temporary working directory
  - [ ] Provide cleanup function

---

## 🧪 Testing

- [ ] Set up `pytest` test environment
- [ ] Write unit tests for:
  - [ ] SQLAlchemy models
  - [ ] File readers
  - [ ] File writers
  - [ ] Utility functions

---

## 🎨 GUI (Optional)

- [ ] Implement basic GUI viewer in `gui/viewer.py`
  - [ ] Display contents of Institution file
  - [ ] Provide links/navigation to Patients and Plans

---

## 🧰 Developer Experience

- [ ] Create `examples/basic_usage.py`
- [ ] Add type hints and docstrings throughout codebase
- [ ] Add basic logging (optional)
- [ ] Document development instructions in README

