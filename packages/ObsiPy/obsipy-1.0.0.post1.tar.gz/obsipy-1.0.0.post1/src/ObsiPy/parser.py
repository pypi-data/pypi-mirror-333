from pathlib import Path
from ruamel.yaml import YAML
from io import StringIO


class ObsidianParser():
    '''Parser for Obsidian Markdown files.

    Attributes:
        header_marker: String pattern that marks the beginning and end of the metadata header (defaukt is "---")
        endocing: encoding in which the files are read and written (defaukt: "uft-8")
    '''

    def __init__(self, header_marker: str = '---', encoding: str = 'utf-8'):
        self.header_marker = header_marker
        self.encoding = encoding
        self.yaml = YAML(typ='rt')
        self.yaml.indent(mapping=2, sequence=4, offset=2) # Formatierung des yaml outputs
        self.yaml.default_flow_style = False # Listen werden im Block-Style angezeigt
        self.yaml.sort_base_mapping_type_on_output = False # Der yaml output wird in der selben Reihenfolge erzeugt wie das input dict



    def _back_to_string(self, lines: list) -> str:
        return self.header_marker.join(lines)


    def _has_header(self, file_text: str) -> bool:
        text_lines = file_text.splitlines()

        empty = bool(not text_lines)
        if empty:
            return False
        first_item_is_marker = text_lines[0] == self.header_marker
        marker_repeats = text_lines.count(self.header_marker) >= 2
        
        return bool(not empty and first_item_is_marker and marker_repeats)


    def _has_content(self, header: bool, file_sections: list) -> bool:
        return True if len(file_sections) > 1 and header or file_sections and not header else False

    
    def _get_yaml_header(self, header_string: str) -> dict:
        return self.yaml.load(header_string)


    def _get_sections(self, header: bool, file_text: str) -> list:
        if not header:
            return [] if not file_text else [file_text]

        separator = '\n'
        file_lines = file_text.splitlines()
        
        marker_positions = [index for index, line in enumerate(file_lines) if line == self.header_marker]
        header_end = marker_positions[1] + 1
        
        header_lines_framed = file_lines[:header_end]
        header_lines_plain = header_lines_framed[1:-1]
        header_string = separator.join(header_lines_plain)
        
        header_string_framed = separator.join(header_lines_framed)
        content_string = file_text[len(header_string_framed) + 1:]

        sections = []
        if header_string:
            sections.append(header_string)

        if content_string:
            sections.append(content_string)


        return sections
    
    
    def read(self, file_path: str) -> dict:
        '''Read obsidian markdown files. 

        Arguments:
        file: a Path object pointing on the obsidian markdown file

        Returns:
            Dictionary with 2 fields. "header" contains the
            registerd metadata and contend the text content.

        Raises:
            FileNotFoundError: When the given file does not exist
        '''

        file = Path(file_path)
        file_text = file.read_text(encoding=self.encoding)
        has_header = self._has_header(file_text)
        
        file_sections = self._get_sections(has_header, file_text)

        has_content = self._has_content(has_header, file_sections)

        if not has_header:
            header =  None
        else:
            header = self._get_yaml_header(header_string=file_sections[0])
 
        if not has_content:
            content = None
        else:
            content = file_sections[-1]

        if has_header and has_content:
            content = content[1:] if content[0] == '\n' else content

        return {'header': header, 'content': content}
    

    def has_header(self, file_path: str) -> bool:
        '''Checks if a given obsidian markdown file contains a metadata header or not.
        
        Args:
            file: a Path object pointing on the obsidian markdown file
        
        Returns:
            bool
        
        Raises:
            FileNotFoundError: When the given file does not exist
        '''

        file = Path(file_path)
        file_text = file.read_text(encoding=self.encoding)
        return self._has_header(file_text)
    

    def has_content(self, file_path: str) -> bool:
        '''Checks if a given obsidian markdown file contains content beside the metadata header or not.
        
        Args:
            file: a Path object pointing on the obsidian markdown file
        
        Returns:
            bool
        
        Raises:
            FileNotFoundError: When the given file does not exist
        '''

        file = Path(file_path)
        file_text = file.read_text(encoding=self.encoding)
        header = self._has_header(file_text)
        file_sections = self._get_sections(header, file_text)

        return self._has_content(header, file_sections)
    

    def _frame_header(self, header_string: str) -> str:
        return f"{self.header_marker}\n{header_string}{self.header_marker}"


    def _make_yaml_header(self, header:dict) -> str:
        buffer = StringIO()

        self.yaml.dump(header, stream=buffer, transform=self._frame_header)

        return buffer.getvalue()

    
    def _pack(self, header: dict = None, content: str = None) -> str:
        content = None if content == '' else content
        
        if not header and not content:
            return ''

        if not header:
            return content
        
        header_string_framed = self._make_yaml_header(header)

        return f"{header_string_framed}" if content is None else f"{header_string_framed}\n{content}"

    
    def write(self, file_path: str, header: dict, content: str) -> bool:
        '''Writes obsidian markdown files. Returns True if succeeded, else False.

        Args:
            file: a Path object pointing on the target obsidian markdown file
            header: a dict containg the metadata, leave empty for None
            content: a str containg the content, leave empty for None
        
        Raises:
            FileNotFoundError: When the given file is not a file
        '''
        
        file = Path(file_path)
        if not file.is_file:
            raise FileNotFoundError("The given file is not a file")
        
        data = self._pack(header, content)
        file.parent.mkdir(parents=True, exist_ok=True)
        written_charakters = file.write_text(data, encoding=self.encoding)
        return True if written_charakters is len(data) else False