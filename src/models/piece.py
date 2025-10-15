"""
Piece Model - Represents a manufactured piece
"""


class Piece:
    """Class representing a manufactured piece"""
    
    # Quality criteria constants
    MIN_WEIGHT = 95
    MAX_WEIGHT = 105
    VALID_COLORS = ['blue', 'green', 'azul', 'verde']
    MIN_LENGTH = 10
    MAX_LENGTH = 20
    
    def __init__(self, piece_id, weight, color, length):
        """
        Initialize a piece with its attributes
        
        Args:
            piece_id (str): Unique identifier for the piece
            weight (float): Weight in grams
            color (str): Color of the piece
            length (float): Length in centimeters
        """
        self.id = piece_id
        self.weight = weight
        self.color = color.lower()
        self.length = length
        self.approved = False
        self.rejection_reasons = []
        self._evaluate_quality()
    
    def _evaluate_quality(self):
        """Evaluate if the piece meets quality criteria"""
        self.approved = True
        self.rejection_reasons = []
        
        # Normalize color to English
        color_map = {'azul': 'blue', 'verde': 'green'}
        if self.color in color_map:
            self.color = color_map[self.color]
        
        # Check weight (95g to 105g)
        if self.weight < self.MIN_WEIGHT or self.weight > self.MAX_WEIGHT:
            self.approved = False
            self.rejection_reasons.append(
                f"Peso fora do padrão ({self.weight}g - esperado: {self.MIN_WEIGHT}g-{self.MAX_WEIGHT}g)"
            )
        
        # Check color (blue or green)
        if self.color not in ['blue', 'green']:
            self.approved = False
            self.rejection_reasons.append(
                f"Cor inválida ({self.color} - esperado: azul ou verde)"
            )
        
        # Check length (10cm to 20cm)
        if self.length < self.MIN_LENGTH or self.length > self.MAX_LENGTH:
            self.approved = False
            self.rejection_reasons.append(
                f"Comprimento fora do padrão ({self.length}cm - esperado: {self.MIN_LENGTH}cm-{self.MAX_LENGTH}cm)"
            )
    
    def is_approved(self):
        """Check if piece is approved"""
        return self.approved
    
    def get_rejection_reasons(self):
        """Get list of rejection reasons"""
        return self.rejection_reasons
    
    def to_dict(self):
        """Convert piece to dictionary"""
        return {
            'id': self.id,
            'weight': self.weight,
            'color': self.color,
            'length': self.length,
            'approved': self.approved,
            'rejection_reasons': self.rejection_reasons
        }
    
    def __str__(self):
        """String representation of the piece"""
        status = "✓ APROVADA" if self.approved else "✗ REPROVADA"
        color_name = "azul" if self.color == "blue" else "verde" if self.color == "green" else self.color
        info = f"ID: {self.id} | Peso: {self.weight}g | Cor: {color_name} | Comprimento: {self.length}cm | {status}"
        
        if not self.approved:
            info += f"\n  Motivos: {'; '.join(self.rejection_reasons)}"
        
        return info
    
    def __repr__(self):
        """Developer representation of the piece"""
        return f"Piece(id={self.id}, weight={self.weight}, color={self.color}, length={self.length}, approved={self.approved})"

