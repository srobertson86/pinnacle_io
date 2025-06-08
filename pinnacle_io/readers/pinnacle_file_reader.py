"""
Pinnacle file reader.
"""

import logging
import re
import json
from typing import Dict, List, Any, Optional

DEFAULT_ENCODING = 'latin1'

logger = logging.getLogger(__name__)

class PinnacleFileReader:
    """
    Base class for reading Pinnacle data files.
    
    This class provides common functionality for parsing Pinnacle files,
    which typically use a hierarchical key-value format with nested structures.
    It handles complex Pinnacle file structures including nested dictionaries,
    lists, and various data types.
    """
    
    # Compile regex patterns for better performance
    _line_is_trial = re.compile(r'^\s*Trial\s*=\s*{$')
    _line_is_poi = re.compile(r'^\s*Poi\s*=\s*{$')
    _line_is_image_info = re.compile(r'^\s*ImageInfo\s*=\s*{$')
    
    _line_ends_with_opening_brace = re.compile(r'=\s*{$')
    _line_contains_closing_brace = re.compile(r'^\s*};') # Closing brace is always on a new line. A comment may follow (}; // ...)
    _line_contains_key_value_pair = re.compile(r'^\s*([\w]+(?:\s*\.\s*\w+)*)\s*[=:]\s*(.+)$')
    
    @staticmethod
    def parse_key_value_file(file_path: str, max_depth: Optional[int] = None, 
                            ignore_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Parse a Pinnacle key-value file.
        
        Pinnacle files typically use a hierarchical format with nested structures.
        
        Args:
            file_path: Path to the file to parse.
            max_depth: Optional parameter to limit the depth of nested levels to parse.
            ignore_keys: Optional parameter to specify keys to ignore during parsing.
            
        Returns:
            Dictionary of key-value pairs with nested structures.
        """
        try:
            with open(file_path, 'r', encoding=DEFAULT_ENCODING, errors='ignore') as f:
                lines = f.readlines()
                return PinnacleFileReader.parse_key_value_content_lines(lines, max_depth, ignore_keys)
        except Exception as e:
            logger.error(f"Error parsing Pinnacle file {file_path}: {e}")
            raise
    
    @staticmethod
    def parse_key_value_content(content: str, max_depth: Optional[int] = None, 
                               ignore_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Parse Pinnacle key-value content.
        
        Args:
            content: Content to parse.
            max_depth: Optional parameter to limit the depth of nested levels to parse.
            ignore_keys: Optional parameter to specify keys to ignore during parsing.
            
        Returns:
            Dictionary of key-value pairs with nested structures.
        """
        lines = content.splitlines()
        return PinnacleFileReader.parse_key_value_content_lines(lines, max_depth, ignore_keys)
    
    @staticmethod
    def parse_key_value_content_lines(lines: List[str], max_depth: Optional[int] = None, 
                                     ignore_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Parse Pinnacle key-value content from a list of lines.
        
        Args:
            lines: List of lines to parse.
            max_depth: Optional parameter to limit the depth of nested levels to parse.
            ignore_keys: Optional parameter to specify keys to ignore during parsing.
            
        Returns:
            Dictionary of key-value pairs with nested structures.
        """
        root = {}
        block_stack = [root]  # Stack of dictionaries to keep track of nesting
        key_stack = []        # Stack of keys to keep track of the path
        
        i = 0
        
        # Check for and handle top-level lists (TrialList, PoiList, ImageInfoList)
        PinnacleFileReader._check_for_list(lines, i, block_stack, key_stack)
        
        try:
            # Evaluate all remaining lines
            while i < len(lines):
                line = lines[i].rstrip()
                
                # Skip empty lines
                if not line.strip() or line.startswith("//"):
                    i += 1
                    continue
                
                if PinnacleFileReader._line_ends_with_opening_brace.search(line):
                    i = PinnacleFileReader._handle_opening_brace(block_stack, key_stack, lines, i, max_depth, ignore_keys)
                elif PinnacleFileReader._line_contains_closing_brace.search(line):
                    PinnacleFileReader._handle_closing_brace(block_stack, key_stack)
                else:
                    match = PinnacleFileReader._line_contains_key_value_pair.match(line)
                    if match:
                        PinnacleFileReader._handle_key_value_pair(block_stack[-1], match, ignore_keys)
                
                i += 1
        except Exception as e:
            line_info = f"line {i+1}: {lines[i]}" if i < len(lines) else "end of file"
            logger.error(f"Error parsing {line_info}: {e}")
            raise Exception(f"Error parsing {line_info}", e)
        
        return root
    
    @staticmethod
    def _check_for_list(lines: List[str], i: int, block_stack: List[Dict[str, Any]], 
                             key_stack: List[str]) -> bool:
        """
        Check if the content contains a list of Trials and add a "TrialList" key to the root object if needed.
        
        Args:
            lines: List of lines to parse.
            i: Current line index.
            block_stack: Stack of dictionaries to keep track of nesting.
            key_stack: Stack of keys to keep track of the path.
        """
        # Ignore blank lines at the beginning of the content
        while i < len(lines) and not lines[i].strip():
            i += 1
            
        # If we've reached the end of the file, return False
        if i >= len(lines):
            return False
            
        # If the content contains a list of Trials, add a "TrialList" key to the root object
        temp_i = 0
        if PinnacleFileReader._line_is_trial.match(lines[i]):
            PinnacleFileReader._handle_opening_brace(block_stack, key_stack, ["TrialList ={"], temp_i)
        elif PinnacleFileReader._line_is_poi.match(lines[i]):
            PinnacleFileReader._handle_opening_brace(block_stack, key_stack, ["PoiList ={"], temp_i)
        elif PinnacleFileReader._line_is_image_info.match(lines[i]):
            PinnacleFileReader._handle_opening_brace(block_stack, key_stack, ["ImageInfoList ={"], temp_i)

    @staticmethod
    def _is_list(key: str) -> bool:
        """Check if a key represents a list."""
        return key.endswith("List") or key.endswith("Array")
    
    @staticmethod
    def _is_list_item(parent_key: str, new_key: str) -> bool:
        """Check if a key is an item in a list."""
        return parent_key.endswith("List") and (parent_key == new_key + "List" or new_key.startswith('#'))
    
    @staticmethod
    def _is_points_array(key: str) -> bool:
        """Check if a key represents a points array."""
        return key == "Points[]"
    
    @staticmethod
    def _ignore_key(key: str, additional_ignore_keys: Optional[List[str]] = None) -> bool:
        """Check if a key should be ignored."""
        ignore_keys = ["Float", "SimpleString"]
        if additional_ignore_keys:
            ignore_keys.extend(additional_ignore_keys)
        return key in ignore_keys
    
    @staticmethod
    def _handle_opening_brace(block_stack: List[Dict[str, Any]], key_stack: List[str], 
                             lines: List[str], current_index: int, max_depth: Optional[int] = None, 
                             ignore_keys: Optional[List[str]] = None) -> int:
        """
        Handle a line that ends with an opening brace.
        
        Args:
            block_stack: Stack of dictionaries to keep track of nesting.
            key_stack: Stack of keys to keep track of the path.
            lines: List of lines to parse.
            current_index: Current line index.
            max_depth: Optional parameter to limit the depth of nested levels to parse.
            ignore_keys: Optional parameter to specify keys to ignore during parsing.
            
        Returns:
            Updated line index.
        """
        line = lines[current_index]
        new_key = line.strip().rstrip('= {')
        
        if ignore_keys and new_key in ignore_keys:
            return PinnacleFileReader._ignore_child_object(lines, current_index)
        
        parent_key = key_stack[-1] if key_stack else ""
        new_block = {}
        parent_block = block_stack[-1]
        
        # Ignore the child object if:
        # 1. The current object depth exceeds the maximum depth
        # 2. The child object is a "Store"
        if (max_depth is not None and len(key_stack) > max_depth) or new_key == "Store":
            return PinnacleFileReader._ignore_child_object(lines, current_index)
        
        # Always keep track of the new keys
        key_stack.append(new_key)
        
        if PinnacleFileReader._is_list(new_key):
            # Initialize *List keys as an empty list
            if new_key not in parent_block:
                parent_block[new_key] = []
        elif PinnacleFileReader._is_list(parent_key):
            # If the parent key is a list, add a new block to the list
            parent_block[parent_key].append(new_block)
            block_stack.append(new_block)
            
            # If the new key is not a direct child of the parent list and should not be ignored, add it to the new block
            if not (PinnacleFileReader._is_list_item(parent_key, new_key) or PinnacleFileReader._ignore_key(new_key, ignore_keys)):
                item_block = {}
                new_block[new_key] = item_block
                block_stack.append(item_block)
        elif PinnacleFileReader._is_points_array(new_key):
            parent_block["Points"] = []
            while current_index < len(lines) - 1 and not lines[current_index + 1].rstrip().endswith("};"):
                current_index += 1
                line = lines[current_index]
                points = [float(p.strip()) for p in line.split(",") if p.strip()]
                parent_block["Points"].extend(points)
        elif not PinnacleFileReader._ignore_key(new_key, ignore_keys):
            # All other keys should be initialized as an empty dictionary
            parent_block[new_key] = new_block
            block_stack.append(new_block)
            
        return current_index
    
    @staticmethod
    def _ignore_child_object(lines: List[str], current_index: int) -> int:
        """
        Step over all lines until the end of the child object is reached.
        
        Args:
            lines: List of lines to parse.
            current_index: Current line index.
            
        Returns:
            Updated line index.
        """
        brace_counter = 1
        while current_index < len(lines) - 1:
            current_index += 1
            next_line = lines[current_index].rstrip()
            if next_line.endswith('{'):
                brace_counter += 1
            elif next_line.endswith("};"):
                brace_counter -= 1
                
            if brace_counter == 0:
                break
                
        return current_index
    
    @staticmethod
    def _handle_closing_brace(block_stack: List[Dict[str, Any]], key_stack: List[str]) -> None:
        """
        Handle a line that ends with a closing brace.
        
        Args:
            block_stack: Stack of dictionaries to keep track of nesting.
            key_stack: Stack of keys to keep track of the path.
        """
        if not key_stack:
            return
        
        key = key_stack.pop()
        parent_key = key_stack[-1] if key_stack else ""
        
        # Following the logic of _handle_opening_brace, only pop a block from the stack if it was added when handling the opening brace
        if PinnacleFileReader._is_list(key):
            # Do nothing
            pass
        elif PinnacleFileReader._is_list(parent_key):
            if not (PinnacleFileReader._is_list_item(parent_key, key) or PinnacleFileReader._ignore_key(key)):
                block_stack.pop()
            block_stack.pop()
        elif PinnacleFileReader._is_points_array(key):
            # Do nothing
            pass
        elif key == "Store":
            # Do nothing
            pass
        elif not PinnacleFileReader._ignore_key(key):
            block_stack.pop()
    
    @staticmethod
    def _handle_key_value_pair(dict_obj: Dict[str, Any], match: re.Match, 
                              ignore_keys: Optional[List[str]] = None) -> None:
        """
        Handle a line that contains a key-value pair.
        
        Args:
            dict_obj: Dictionary to add the key-value pair to.
            match: Regex match object containing the key and value.
            ignore_keys: Optional parameter to specify keys to ignore during parsing.
        """
        key = match.group(1)
        value = match.group(2).strip().rstrip(';').strip('\\')
        
        # The parsed value will be either None, a float, or a string
        if value == "null" or not value.strip():
            parsed_value = None
        else:
            try:
                parsed_value = int(value.strip())
            except ValueError:
                try:
                    parsed_value = float(value)
                except ValueError:
                    parsed_value = value.strip('"')
        
        # If no nested keys are present, then just add the value
        if '.' not in key:
            if not ignore_keys or key not in ignore_keys:
                dict_obj[key] = parsed_value
            return
        
        # If nested keys need to be accounted for, then split the key into its components
        all_keys = [k.strip() for k in key.split(".") if k.strip()]
        keys = []
        for k in all_keys:
            if ignore_keys and k in ignore_keys:
                break
            keys.append(k)
        
        PinnacleFileReader._insert_nested_value(dict_obj, keys, parsed_value)
    
    @staticmethod
    def _insert_nested_value(dict_obj: Dict[str, Any], keys: List[str], value: Any) -> None:
        """
        Insert a value into a nested dictionary structure.
        
        Args:
            dict_obj: Dictionary to insert the value into.
            keys: List of keys representing the path to the value.
            value: Value to insert.
        """
        for i in range(len(keys) - 1):
            if keys[i] not in dict_obj:
                dict_obj[keys[i]] = {}
            dict_obj = dict_obj[keys[i]]
        
        dict_obj[keys[-1]] = value
    
    @staticmethod
    def to_json(data: Dict[str, Any], indent: int = 2) -> str:
        """
        Convert the parsed data to a JSON string.
        
        Args:
            data: Dictionary of parsed data.
            indent: Number of spaces to use for indentation.
            
        Returns:
            JSON string representation of the data.
        """
        return json.dumps(data, indent=indent)