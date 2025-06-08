"""
Tests for the PinnacleFileReader class.

This module contains tests for the PinnacleFileReader class which parses Pinnacle files into Python dictionaries.
"""

import os
import json
import tempfile

from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader


class TestPinnacleFileReader:
    """Tests for the PinnacleFileReader class."""
    
    def test_parse_key_value_file_valid_file(self):
        """Test parsing a valid Pinnacle file with multiple trials."""
        # Arrange
        file_content = """
          Trial ={
            Name = "Trial_1";
            PrescriptionList ={
              Prescription ={
                Name = "Brain";
              };
            };
            BeamList ={
              Beam ={
                Name = "02  Lao Brain";
                IsocenterName = "iso";
                PrescriptionName = "Brain";
                MonitorUnitInfo ={
                  PrescriptionDose = 126.27;
                  SourceToPrescriptionPointDistance = 100;
                };
                DoseVolume = \\XDR:8\\;
                DoseVarVolume = \\XDR:9\\;
                Weight = 50;
              };
            };
          };
          Trial ={
            Name = "Trial_2";
            PrescriptionList ={
              Prescription ={
                Name = "Lung";
              };
            };
            BeamList ={
              Beam ={
                Name = "03  AP Lung";
                IsocenterName = "iso";
                PrescriptionName = "Lung";
                MonitorUnitInfo ={
                  PrescriptionDose = 212.12;
                  SourceToPrescriptionPointDistance = 100;
                };
                DoseVolume = \\XDR:10\\;
                DoseVarVolume = \\XDR:11\\;
                Weight = 100;
              };
            };
          };"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(file_content)
            file_path = temp_file.name
        
        try:
            # Act
            reader = PinnacleFileReader()
            result = reader.parse_key_value_file(file_path)
            
            # Assert
            assert result is not None
            assert isinstance(result, dict)
            
            trials = result.get("TrialList", [])
            assert len(trials) == 2
            
            trial1 = trials[0]
            trial2 = trials[1]
            
            # Check basic string values
            assert trial1["Name"] == "Trial_1"
            assert trial1["PrescriptionList"][0]["Name"] == "Brain"
            
            assert trial2["Name"] == "Trial_2"
            assert trial2["PrescriptionList"][0]["Name"] == "Lung"
            
            # Check basic number values
            beam1 = trial1["BeamList"][0]
            beam2 = trial2["BeamList"][0]
            
            assert beam1["MonitorUnitInfo"]["PrescriptionDose"] == 126.27
            assert beam1["MonitorUnitInfo"]["SourceToPrescriptionPointDistance"] == 100
            
            assert beam2["MonitorUnitInfo"]["PrescriptionDose"] == 212.12
            assert beam2["MonitorUnitInfo"]["SourceToPrescriptionPointDistance"] == 100
            
            # Check a deeply nested value
            assert trial1["BeamList"][0]["DoseVolume"] == "XDR:8"
            
        finally:
            # Cleanup
            os.unlink(file_path)
    
    def test_parse_content_complex_nested_structure(self):
        """Test parsing complex nested structures with points arrays."""
        # Arrange
        content = """
          BeamModifier ={
            Name = "BeamModifier_1";
            FixToCollimator = 1;
            AutoBlock = 0;
            StructureToBlock = "Manual";
            Margin = 0;
            InsideMode = "Expose";
            OutsideMode = "Block";
            ContourList ={
              CurvePainter ={
                Curve ={
                  RawData ={
                    NumberOfDimensions = 2;
                    NumberOfPoints = 6;
                    Points[] ={
                      -12.0066,-12.6974,
                      -6.67763,-5.83777e-07,
                      0.0986838,5.19737,
                      0.625,6.84211,
                      11.8092,-11.3816,
                      -12.0066,-12.6974
                    };
                  };
                  LabelList ={
                    #0 ={
                      String = "X";
                    };
                    #1 ={
                      String = "Y";
                    };
                  };
                  RowLabelList ={
                  };
                  LabelFormatList ={
                    #0 ={
                      String = "%6.2f";
                    };
                    #1 ={
                      String = "%6.2f";
                    };
                  };
                };
                Color = "Red";
                SliceCoordinate = 0;
                Orientation = "Transverse";
              };
            };
          };"""
        
        # Act
        reader = PinnacleFileReader()
        result = reader.parse_key_value_content(content)
        
        # Assert
        assert result is not None
        
        contour_list = result["BeamModifier"]["ContourList"]
        curve_painter = contour_list[0]["CurvePainter"]
        curve_data = curve_painter["Curve"]["RawData"]
        points = curve_data["Points"]
        
        assert curve_painter["Color"] == "Red"
        assert curve_data["NumberOfDimensions"] == 2
        assert curve_data["NumberOfPoints"] == 6
        assert len(points) == 12
        assert points[0] == -12.0066
    
    def test_parse_content_empty_values(self):
        """Test handling of empty and null values."""
        # Arrange
        content = """
          Trial ={
            Name = "";
            MissingValue = ;
            NullValue = null;
            EmptyList ={
            };
            RawData ={
              NumberOfDimensions = 0;
              NumberOfPoints = 0;
              Points[] ={
              };
            };
          };"""
        
        # Act
        reader = PinnacleFileReader()
        result = reader.parse_key_value_content(content)
        
        # Assert
        assert result is not None
        
        trial = result["TrialList"][0]
        assert trial["Name"] == ""
        assert trial["MissingValue"] is None
        assert trial["NullValue"] is None
        assert trial["EmptyList"] == []
    
    def test_parse_content_ignore_store(self):
        """Test that Store objects are ignored."""
        # Arrange
        content = """
          Trial ={
            Name = "Trial_1";
            Store = {
              At .PlanType = SimpleString {
                String = "3D";
              };
              At .TreatmentSite = SimpleString {
                String = "Lung";
              };
            };
          };
          Trial ={
            Name = "Trial_2";
            Store = {
              At .PlanType = SimpleString {
                String = "VMAT";
              };
              At .TreatmentSite = SimpleString {
                String = "Head&Neck";
              };
            };
          };"""
        
        # Act
        reader = PinnacleFileReader()
        result = reader.parse_key_value_content(content)
        
        # Assert
        assert result is not None
        
        trials = result["TrialList"]
        assert len(trials) == 2
        
        trial1 = trials[0]
        trial2 = trials[1]
        assert "Store" not in trial1
        assert "Store" not in trial2
    
    def test_parse_content_max_depth(self):
        """Test limiting parse depth."""
        # Arrange
        content = """
          Trial ={
            Name = "Trial_1";
            PrescriptionList ={
              Prescription ={
                Name = "Brain";
              };
            };
            BeamList ={
              Beam ={
                Name = "02  Lao Brain";
                IsocenterName = "iso";
                PrescriptionName = "Brain";
                MonitorUnitInfo ={
                  PrescriptionDose = 126.27;
                  SourceToPrescriptionPointDistance = 100;
                };
                DoseVolume = \\XDR:8\\;
                DoseVarVolume = \\XDR:9\\;
                Weight = 50;
              };
            };
          };"""
        
        # Act
        reader = PinnacleFileReader()
        result = reader.parse_key_value_content(content, max_depth=3)
        
        # Assert
        assert result is not None
        
        trial = result["TrialList"][0]
        beam = trial["BeamList"][0]
        assert "MonitorUnitInfo" not in beam
    
    def test_parse_content_ignore_keys(self):
        """Test ignoring specific keys."""
        # Arrange
        content = """
          Trial ={
            Name = "Trial_1";
            PrescriptionList ={
              Prescription ={
                Name = "Brain";
              };
            };
            BeamList ={
              Beam ={
                Name = "02  Lao Brain";
                IsocenterName = "iso";
                PrescriptionName = "Brain";
                MonitorUnitInfo ={
                  PrescriptionDose = 126.27;
                  SourceToPrescriptionPointDistance = 100;
                };
                DoseVolume = \\XDR:8\\;
                DoseVarVolume = \\XDR:9\\;
                Weight = 50;
              };
            };
          };"""
        
        # Act
        reader = PinnacleFileReader()
        result = reader.parse_key_value_content(content, ignore_keys=["MonitorUnitInfo"])
        
        # Assert
        assert result is not None
        
        trial = result["TrialList"][0]
        beam = trial["BeamList"][0]
        assert "MonitorUnitInfo" not in beam
    
    def test_parse_content_nested_dot_notation(self):
        """Test parsing nested values with dot notation."""
        # Arrange
        content = """
          Trial ={
            Name = "Trial_1";
            DoseGrid .VoxelSize .X = 0.3;
            DoseGrid .VoxelSize .Y = 0.3;
            DoseGrid .VoxelSize .Z = 0.3;
            DoseGrid .Dimension .X = 93;
            DoseGrid .Dimension .Y = 110;
            DoseGrid .Dimension .Z = 89;
            DoseGrid .Origin .X = -14.9044;
            DoseGrid .Origin .Y = -17.5729;
            DoseGrid .Origin .Z = -10.7747;
            DoseGrid .VolRotDelta .X = 0;
            DoseGrid .VolRotDelta .Y = 0;
            DoseGrid .VolRotDelta .Z = 0;
            DoseGrid .Display2d = 1;
            DoseGrid .DoseSummationType = 1;
            DoseStartSlice = 49;
            DoseEndSlice = 49;
          };"""
        
        # Act
        reader = PinnacleFileReader()
        result = reader.parse_key_value_content(content)
        
        # Assert
        assert result is not None
        assert isinstance(result, dict)
        
        trial = result['TrialList'][0]
        assert trial["Name"] == "Trial_1"
        
        # Check nested values with dot notation
        dose_grid = trial.get("DoseGrid", {})
        
        # Check VoxelSize
        voxel_size = dose_grid.get("VoxelSize", {})
        assert voxel_size["X"] == 0.3
        assert voxel_size["Y"] == 0.3
        assert voxel_size["Z"] == 0.3
        
        # Check Dimension
        dimension = dose_grid.get("Dimension", {})
        assert dimension["X"] == 93
        assert dimension["Y"] == 110
        assert dimension["Z"] == 89
        
        # Check Origin
        origin = dose_grid.get("Origin", {})
        assert origin["X"] == -14.9044
        assert origin["Y"] == -17.5729
        assert origin["Z"] == -10.7747
        
        # Check VolRotDelta
        vol_rot_delta = dose_grid.get("VolRotDelta", {})
        assert vol_rot_delta["X"] == 0
        assert vol_rot_delta["Y"] == 0
        assert vol_rot_delta["Z"] == 0
        
        # Check direct properties
        assert dose_grid["Display2d"] == 1
        assert dose_grid["DoseSummationType"] == 1
        
        # Check non-nested values
        assert trial["DoseStartSlice"] == 49
        assert trial["DoseEndSlice"] == 49
    
    def test_to_json(self):
        """Test converting parsed data to JSON."""
        # Arrange
        data = {
            "TrialList": [
                {
                    "Name": "Trial_1",
                    "PrescriptionList": [
                        {"Name": "Brain"}
                    ]
                }
            ]
        }
        
        # Act
        reader = PinnacleFileReader()
        json_str = reader.to_json(data)
        parsed_json = json.loads(json_str)
        
        # Assert
        assert parsed_json is not None
        assert parsed_json["TrialList"][0]["Name"] == "Trial_1"
        assert parsed_json["TrialList"][0]["PrescriptionList"][0]["Name"] == "Brain"
