"""
UI Utilities - User interface helper functions
"""

import os


class UI:
    """User Interface utility class"""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    @staticmethod
    def pause():
        """Pause execution until user presses Enter"""
        input("\nPressione ENTER para continuar...")
    
    @staticmethod
    def print_header(title, width=60):
        """
        Print a formatted header
        
        Args:
            title (str): The title text
            width (int): Width of the header
        """
        print("=" * width)
        print(title)
        print("=" * width)
    
    @staticmethod
    def print_separator(width=60, char="-"):
        """
        Print a separator line
        
        Args:
            width (int): Width of the separator
            char (str): Character to use for separator
        """
        print(char * width)
    
    @staticmethod
    def print_section(title, width=60):
        """
        Print a section header
        
        Args:
            title (str): The section title
            width (int): Width of the section
        """
        print(f"\n{title}")
        print("-" * width)
    
    @staticmethod
    def print_success(message):
        """
        Print a success message
        
        Args:
            message (str): The success message
        """
        print(f"✓ {message}")
    
    @staticmethod
    def print_error(message):
        """
        Print an error message
        
        Args:
            message (str): The error message
        """
        print(f"✗ {message}")
    
    @staticmethod
    def print_info(message):
        """
        Print an info message
        
        Args:
            message (str): The info message
        """
        print(f"ℹ {message}")
    
    @staticmethod
    def print_warning(message):
        """
        Print a warning message
        
        Args:
            message (str): The warning message
        """
        print(f"⚠ {message}")
    
    @staticmethod
    def get_input(prompt, input_type=str, validator=None):
        """
        Get validated input from user
        
        Args:
            prompt (str): The input prompt
            input_type (type): Expected type of input (int, float, str)
            validator (function): Optional validation function
            
        Returns:
            The validated input value
        """
        while True:
            try:
                value = input(prompt).strip()
                
                # Convert to desired type
                if input_type != str:
                    value = input_type(value)
                
                # Apply custom validator if provided
                if validator and not validator(value):
                    UI.print_error("Entrada inválida. Tente novamente.")
                    continue
                
                return value
            
            except ValueError:
                UI.print_error(f"Digite um valor válido do tipo {input_type.__name__}.")
            except KeyboardInterrupt:
                raise
            except Exception as e:
                UI.print_error(f"Erro: {e}")
    
    @staticmethod
    def display_menu(title, options):
        """
        Display a menu with options
        
        Args:
            title (str): Menu title
            options (list): List of menu options
        """
        UI.clear_screen()
        UI.print_header(title)
        print()
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        print("0. Sair")
        print()
        UI.print_separator()
    
    @staticmethod
    def confirm_action(message="Tem certeza?"):
        """
        Ask user for confirmation
        
        Args:
            message (str): Confirmation message
            
        Returns:
            bool: True if user confirms, False otherwise
        """
        response = input(f"{message} (s/n): ").strip().lower()
        return response in ['y', 'yes', 's', 'sim']
    
    @staticmethod
    def display_table(headers, rows, column_widths=None):
        """
        Display data in a table format
        
        Args:
            headers (list): Column headers
            rows (list): List of rows (each row is a list of values)
            column_widths (list): Optional list of column widths
        """
        if not column_widths:
            # Calculate column widths automatically
            column_widths = [len(str(h)) for h in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    column_widths[i] = max(column_widths[i], len(str(cell)))
        
        # Print headers
        header_row = " | ".join(
            str(h).ljust(w) for h, w in zip(headers, column_widths)
        )
        print(header_row)
        print("-" * len(header_row))
        
        # Print rows
        for row in rows:
            row_str = " | ".join(
                str(cell).ljust(w) for cell, w in zip(row, column_widths)
            )
            print(row_str)

