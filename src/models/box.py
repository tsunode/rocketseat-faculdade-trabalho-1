"""
Box Model - Represents a storage box for approved pieces
"""

from datetime import datetime


class Box:
    """Class representing a storage box"""
    
    MAX_CAPACITY = 10
    
    def __init__(self, box_number):
        """
        Initialize a box
        
        Args:
            box_number (int): Unique box number
        """
        self.number = box_number
        self.pieces = []
        self.closed = False
        self.closing_date = None
    
    def add_piece(self, piece):
        """
        Add an approved piece to the box
        
        Args:
            piece (Piece): The piece to add
            
        Returns:
            bool: True if piece was added successfully, False otherwise
        """
        if self.closed:
            return False
        
        if len(self.pieces) < self.MAX_CAPACITY:
            self.pieces.append(piece)
            
            # Close box if it reaches maximum capacity
            if len(self.pieces) == self.MAX_CAPACITY:
                self.close()
            
            return True
        
        return False
    
    def remove_piece(self, piece):
        """
        Remove a piece from the box
        
        Args:
            piece (Piece): The piece to remove
            
        Returns:
            bool: True if piece was removed successfully, False otherwise
        """
        if piece in self.pieces:
            self.pieces.remove(piece)
            # Reopen box if it was closed
            if self.closed:
                self.closed = False
                self.closing_date = None
            return True
        return False
    
    def close(self):
        """Close the box when it reaches maximum capacity"""
        self.closed = True
        self.closing_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def is_closed(self):
        """Check if box is closed"""
        return self.closed
    
    def is_full(self):
        """Check if box is full"""
        return len(self.pieces) >= self.MAX_CAPACITY
    
    def get_piece_count(self):
        """Get current number of pieces in the box"""
        return len(self.pieces)
    
    def get_available_space(self):
        """Get available space in the box"""
        return self.MAX_CAPACITY - len(self.pieces)
    
    def to_dict(self):
        """Convert box to dictionary"""
        return {
            'number': self.number,
            'pieces': [piece.to_dict() for piece in self.pieces],
            'closed': self.closed,
            'closing_date': self.closing_date,
            'piece_count': len(self.pieces),
            'capacity': self.MAX_CAPACITY
        }
    
    def __str__(self):
        """String representation of the box"""
        status = "FECHADA" if self.closed else "ABERTA"
        info = f"Caixa #{self.number} - {status} - {len(self.pieces)}/{self.MAX_CAPACITY} peças"
        
        if self.closed:
            info += f" (Fechada em: {self.closing_date})"
        
        return info
    
    def __repr__(self):
        """Developer representation of the box"""
        return f"Box(number={self.number}, pieces={len(self.pieces)}, closed={self.closed})"

