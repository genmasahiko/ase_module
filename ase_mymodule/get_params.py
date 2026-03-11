import re

def parse_input_namelist(filename):
    with open(filename, 'r') as f:
        data = f.read()
    
    sections = {}
    
    section_pattern = re.compile(r'&(\w+)\s+([\s\S]*?)\s*/', re.MULTILINE)
    
    for match in section_pattern.finditer(data):
        section_name = match.group(1).lower()  # セクション名（小文字で統一）
        section_content = match.group(2)
        
        param_dict = {}
        param_pattern = re.compile(r'(\w+)\s*=\s*([^\s,]+)', re.MULTILINE)
        
        for param_match in param_pattern.finditer(section_content):
            key = param_match.group(1).lower()  # キーを小文字に変換
            value = param_match.group(2)
            
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                value = value.strip('"').strip("'")
            
            param_dict[key] = value
        
        sections[section_name] = param_dict
    
    return sections
