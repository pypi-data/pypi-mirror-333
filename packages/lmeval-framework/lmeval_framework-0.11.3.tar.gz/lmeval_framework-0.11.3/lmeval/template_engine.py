# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

class TemplateEngine:
    """
    A class that provides template rendering functionality.

    The TemplateEngine class allows you to create a template string with placeholders
    and replace those placeholders with actual values from objects passed as keyword arguments.

    Attributes:
        template_string (str): The template string containing placeholders.

    Methods:
        render(**kwargs): Renders the template string by replacing placeholders with values from the passed objects.
    """

    def __init__(self, template_string):
        """
        Initializes a new instance of the TemplateEngine class.

        Args:
            template_string (str): The template string containing placeholders.
        """
        self.template_string = template_string


    def render(self, **kwargs):
        """
        Renders the template string by replacing placeholders with values from the passed objects.

        Args:
            **kwargs: Keyword arguments representing the objects to extract values from.

        Returns:
            str: The rendered template string with placeholders replaced by actual values.
        """
        def replace_variables(match):
            """
            Inner function to replace placeholders with actual values from the passed objects.

            Args:
                match: A match object representing a placeholder found in the template string.

            Returns:
                str: The actual value to replace the placeholder with.
            """
            # Remove leading/trailing spaces from the placeholder
            variable_name = match.group(1).strip()

            # Split the variable name into class name and attribute name
            parts = variable_name.split(".")

            # Get the class name and attribute name
            class_name = parts[0]
            attribute_name = parts[1] if len(parts) > 1 else None

            # Get the object from the keyword arguments based on the class name
            obj = kwargs.get(class_name)

            if obj is None:
                # If the object is not found, keep the placeholder as is
                return match.group(0)

            if attribute_name is None:
                # If no attribute name is provided, return the object itself
                return obj

            # Get the attribute value from the object using getattr()
            value = getattr(obj, attribute_name, None)

            if value is None:
                # If the attribute is not found, keep the placeholder as is
                return match.group(0)

            # Return the value as is (without converting to string)
            return value

        # Use regular expression to find all placeholders in the template string
        # and replace them with actual values using the replace_variables function
        rendered_text = re.sub(r"\{\{\s*([\w.]+)\s*\}\}", replace_variables, self.template_string)

        # Return the rendered template string after cleaning it
        rendered_text = self._clean_rendered_text(rendered_text)
        return rendered_text

    def _clean_rendered_text(self, text):
        # Split the text into lines
        lines = text.split('\n')

        # Process each line
        cleaned_lines = []
        for line in lines:
            # Remove leading and trailing whitespace from each line
            line = line.strip()

            # Skip empty lines at the beginning and end
            if not line and not cleaned_lines:
                continue

            # Replace multiple spaces with a single space within the line
            line = re.sub(r'\s+', ' ', line)

            cleaned_lines.append(line)

        # Remove trailing empty lines
        while cleaned_lines and not cleaned_lines[-1]:
            cleaned_lines.pop()

        # Join the lines back together
        cleaned_text = '\n'.join(cleaned_lines)

        # Ensure there's exactly one blank line between sections
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

        return cleaned_text.strip()