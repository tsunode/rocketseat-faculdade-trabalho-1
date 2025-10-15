"""
Industrial Quality Control System
Main application entry point
"""

from src.services import QualityControlSystem
from src.utils import UI


class Application:
    """Main application class with menu interface"""
    
    def __init__(self):
        """Initialize the application"""
        self.system = QualityControlSystem()
        self.ui = UI()
        self.running = True
    
    def register_new_piece(self):
        """Handle new piece registration"""
        self.ui.clear_screen()
        self.ui.print_header("CADASTRAR NOVA PEÇA")
        
        try:
            # Generate and display piece ID
            piece_id = f"P{self.system.next_id:04d}"
            print(f"\nID da peça: {piece_id}")
            
            # Collect piece data
            weight = self.ui.get_input(
                "Peso (g): ",
                input_type=float,
                validator=lambda x: x > 0
            )
            
            color = self.ui.get_input("Cor (azul/verde): ", input_type=str)
            
            length = self.ui.get_input(
                "Comprimento (cm): ",
                input_type=float,
                validator=lambda x: x > 0
            )
            
            # Register piece in the system
            result = self.system.register_piece(weight, color, length)
            piece = result['piece']
            
            print()
            self.ui.print_separator()
            
            if piece.is_approved():
                self.ui.print_success("PEÇA APROVADA!")
                
                # Check if box was closed
                if result.get('box_closed'):
                    box = result['current_box']
                    print(f"\n📦 Caixa #{box.number} FECHADA (capacidade máxima atingida)")
                
                # Check if new box was created
                if result.get('new_box_created'):
                    new_box = result['new_box']
                    print(f"📦 Nova caixa #{new_box.number} iniciada")
            else:
                self.ui.print_error("PEÇA REPROVADA!")
                print("\nMotivos da reprovação:")
                for reason in piece.get_rejection_reasons():
                    print(f"  • {reason}")
            
            self.ui.print_separator()
            print(f"\nPeça {piece.id} cadastrada com sucesso!")
        
        except ValueError as e:
            self.ui.print_error(f"Valores inválidos! {e}")
        except Exception as e:
            self.ui.print_error(f"Erro ao cadastrar peça: {e}")
        
        self.ui.pause()
    
    def list_pieces(self):
        """List all approved and rejected pieces"""
        self.ui.clear_screen()
        self.ui.print_header("LISTAGEM DE PEÇAS")
        
        all_pieces = self.system.get_all_pieces()
        
        if not all_pieces:
            print("\nNenhuma peça cadastrada ainda.")
            self.ui.pause()
            return
        
        approved_pieces = self.system.get_approved_pieces()
        rejected_pieces = self.system.get_rejected_pieces()
        
        # List approved pieces
        self.ui.print_section(f"✓ PEÇAS APROVADAS ({len(approved_pieces)})")
        if approved_pieces:
            for piece in approved_pieces:
                print(piece)
        else:
            print("Nenhuma peça aprovada.")
        
        # List rejected pieces
        self.ui.print_section(f"✗ PEÇAS REPROVADAS ({len(rejected_pieces)})")
        if rejected_pieces:
            for piece in rejected_pieces:
                print(piece)
        else:
            print("Nenhuma peça reprovada.")
        
        self.ui.pause()
    
    def remove_piece(self):
        """Remove a registered piece"""
        self.ui.clear_screen()
        self.ui.print_header("REMOVER PEÇA CADASTRADA")
        
        all_pieces = self.system.get_all_pieces()
        
        if not all_pieces:
            print("\nNenhuma peça cadastrada para remover.")
            self.ui.pause()
            return
        
        # Display available pieces
        print("\nPeças cadastradas:")
        for i, piece in enumerate(all_pieces, 1):
            status = "APROVADA" if piece.is_approved() else "REPROVADA"
            print(f"{i}. {piece.id} - {status}")
        
        try:
            option = int(input("\nDigite o número da peça a remover (0 para cancelar): "))
            
            if option == 0:
                print("Operação cancelada.")
                self.ui.pause()
                return
            
            if 1 <= option <= len(all_pieces):
                result = self.system.remove_piece(option - 1)
                
                if result['success']:
                    self.ui.print_success(f"Peça {result['piece'].id} removida com sucesso!")
                else:
                    self.ui.print_error(result['message'])
            else:
                self.ui.print_error("Número inválido!")
        
        except ValueError:
            self.ui.print_error("Digite um número válido!")
        except Exception as e:
            self.ui.print_error(f"Erro ao remover peça: {e}")
        
        self.ui.pause()
    
    def list_closed_boxes(self):
        """List all closed boxes"""
        self.ui.clear_screen()
        self.ui.print_header("CAIXAS FECHADAS")
        
        closed_boxes = self.system.get_closed_boxes()
        
        if not closed_boxes:
            print("\nNenhuma caixa fechada ainda.")
            self.ui.pause()
            return
        
        print(f"\nTotal de caixas fechadas: {len(closed_boxes)}\n")
        
        for box in closed_boxes:
            self.ui.print_separator()
            print(box)
            print("Peças na caixa:")
            for piece in box.pieces:
                print(f"  • {piece.id} - Peso: {piece.weight}g | Cor: {piece.color} | Comprimento: {piece.length}cm")
        
        self.ui.print_separator()
        self.ui.pause()
    
    def generate_report(self):
        """Generate and display comprehensive report"""
        self.ui.clear_screen()
        self.ui.print_header("RELATÓRIO FINAL DE PRODUÇÃO E QUALIDADE")
        
        report = self.system.generate_report()
        
        print(f"Data/Hora: {report['timestamp']}")
        self.ui.print_separator()
        
        # General summary
        summary = report['summary']
        self.ui.print_section("📊 RESUMO GERAL")
        print(f"Total de peças processadas: {summary['total_pieces']}")
        
        if summary['total_pieces'] > 0:
            print(f"✓ Peças aprovadas: {summary['approved']} ({summary['approval_rate']:.1f}%)")
            print(f"✗ Peças reprovadas: {summary['rejected']} ({100 - summary['approval_rate']:.1f}%)")
        else:
            print("✓ Peças aprovadas: 0")
            print("✗ Peças reprovadas: 0")
        
        # Rejection analysis
        if 'rejection_analysis' in report:
            analysis = report['rejection_analysis']
            self.ui.print_section("📋 ANÁLISE DE REPROVAÇÕES")
            print(f"Reprovações por peso inadequado: {analysis['weight_issues']}")
            print(f"Reprovações por cor inadequada: {analysis['color_issues']}")
            print(f"Reprovações por comprimento inadequado: {analysis['length_issues']}")
            
            # Detailed rejected pieces
            rejected_pieces = report['pieces']['rejected']
            if rejected_pieces:
                print("\nDetalhamento das peças reprovadas:")
                for piece in rejected_pieces:
                    print(f"\n  {piece.id}:")
                    for reason in piece.get_rejection_reasons():
                        print(f"    • {reason}")
        
        # Storage information
        storage = report['storage']
        self.ui.print_section("📦 ARMAZENAMENTO")
        print(f"Caixas fechadas: {storage['closed_boxes']}")
        print(f"Caixas em uso: {storage['open_boxes']}")
        
        current_box = storage['current_box']
        if current_box and not current_box.is_closed():
            print(f"Caixa atual (#{current_box.number}): {current_box.get_piece_count()}/10 peças")
        
        # Quality statistics
        if 'quality_statistics' in report:
            stats = report['quality_statistics']
            self.ui.print_section("📈 ESTATÍSTICAS DE QUALIDADE (peças aprovadas)")
            print(f"Peso médio: {stats['average_weight']:.2f}g")
            print(f"Peso mínimo: {stats['min_weight']}g")
            print(f"Peso máximo: {stats['max_weight']}g")
            print(f"Comprimento médio: {stats['average_length']:.2f}cm")
            print(f"Comprimento mínimo: {stats['min_length']}cm")
            print(f"Comprimento máximo: {stats['max_length']}cm")
            
            print("Distribuição de cores:")
            total_approved = summary['approved']
            for color, count in stats['color_distribution'].items():
                percentage = (count / total_approved * 100) if total_approved > 0 else 0
                color_name = "Azul" if color == "blue" else "Verde" if color == "green" else color.capitalize()
                print(f"  • {color_name}: {count} peças ({percentage:.1f}%)")
        
        print()
        self.ui.print_separator()
        self.ui.pause()
    
    def display_main_menu(self):
        """Display main menu"""
        menu_options = [
            "Cadastrar nova peça",
            "Listar peças aprovadas/reprovadas",
            "Remover peça cadastrada",
            "Listar caixas fechadas",
            "Gerar relatório final"
        ]
        
        self.ui.display_menu("SISTEMA DE CONTROLE DE QUALIDADE INDUSTRIAL", menu_options)
    
    def run(self):
        """Main application loop"""
        while self.running:
            self.display_main_menu()
            
            try:
                option = input("\nEscolha uma opção: ").strip()
                
                if option == "1":
                    self.register_new_piece()
                elif option == "2":
                    self.list_pieces()
                elif option == "3":
                    self.remove_piece()
                elif option == "4":
                    self.list_closed_boxes()
                elif option == "5":
                    self.generate_report()
                elif option == "0":
                    self.exit_application()
                else:
                    self.ui.print_error("Opção inválida! Escolha uma opção válida do menu.")
                    self.ui.pause()
            
            except KeyboardInterrupt:
                print("\n\nSistema interrompido pelo usuário.")
                self.running = False
            except Exception as e:
                self.ui.print_error(f"Erro inesperado: {e}")
                self.ui.pause()
    
    def exit_application(self):
        """Exit the application"""
        self.ui.clear_screen()
        self.ui.print_header("SISTEMA DE CONTROLE DE QUALIDADE INDUSTRIAL")
        print("\nEncerrando o sistema...")
        print("Obrigado por usar o Sistema de Controle de Qualidade!")
        self.ui.print_separator()
        self.running = False


def main():
    """Main function - application entry point"""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
