"""
Quality Control Service - Main business logic for quality control
"""

from datetime import datetime
from ..models import Piece, Box


class QualityControlSystem:
    """Main quality control system service"""
    
    def __init__(self):
        """Initialize the quality control system"""
        self.pieces = []
        self.boxes = [Box(1)]  # Start with first box
        self.next_id = 1
    
    def generate_piece_id(self):
        """
        Generate a unique piece ID
        
        Returns:
            str: Unique piece ID in format P0001, P0002, etc.
        """
        piece_id = f"P{self.next_id:04d}"
        self.next_id += 1
        return piece_id
    
    def register_piece(self, weight, color, length):
        """
        Register a new piece in the system
        
        Args:
            weight (float): Weight in grams
            color (str): Color of the piece
            length (float): Length in centimeters
            
        Returns:
            dict: Dictionary with piece data and status
        """
        piece_id = self.generate_piece_id()
        piece = Piece(piece_id, weight, color, length)
        self.pieces.append(piece)
        
        result = {
            'piece': piece,
            'approved': piece.is_approved(),
            'box_closed': False,
            'new_box_created': False
        }
        
        # If approved, add to box
        if piece.is_approved():
            box_info = self._add_piece_to_box(piece)
            result.update(box_info)
        
        return result
    
    def _add_piece_to_box(self, piece):
        """
        Add an approved piece to the current box
        
        Args:
            piece (Piece): The approved piece to add
            
        Returns:
            dict: Information about box status
        """
        current_box = self.boxes[-1]
        
        if current_box.add_piece(piece):
            result = {
                'box_closed': current_box.is_closed(),
                'new_box_created': False,
                'current_box': current_box
            }
            
            # If box is closed, create a new one
            if current_box.is_closed():
                new_box = Box(len(self.boxes) + 1)
                self.boxes.append(new_box)
                result['new_box_created'] = True
                result['new_box'] = new_box
            
            return result
        
        return {'box_closed': False, 'new_box_created': False}
    
    def remove_piece(self, piece_index):
        """
        Remove a piece from the system
        
        Args:
            piece_index (int): Index of the piece to remove (0-based)
            
        Returns:
            dict: Result of the operation
        """
        if 0 <= piece_index < len(self.pieces):
            piece = self.pieces.pop(piece_index)
            
            # If piece was approved, remove from boxes too
            if piece.is_approved():
                self._remove_piece_from_boxes(piece)
            
            return {
                'success': True,
                'piece': piece,
                'message': f"Piece {piece.id} removed successfully"
            }
        
        return {
            'success': False,
            'message': "Invalid piece index"
        }
    
    def _remove_piece_from_boxes(self, piece):
        """
        Remove a piece from boxes
        
        Args:
            piece (Piece): The piece to remove
        """
        for box in self.boxes:
            if box.remove_piece(piece):
                break
    
    def get_all_pieces(self):
        """Get all pieces"""
        return self.pieces
    
    def get_approved_pieces(self):
        """Get only approved pieces"""
        return [p for p in self.pieces if p.is_approved()]
    
    def get_rejected_pieces(self):
        """Get only rejected pieces"""
        return [p for p in self.pieces if not p.is_approved()]
    
    def get_closed_boxes(self):
        """Get all closed boxes"""
        return [b for b in self.boxes if b.is_closed()]
    
    def get_open_boxes(self):
        """Get all open boxes"""
        return [b for b in self.boxes if not b.is_closed()]
    
    def get_current_box(self):
        """Get the current active box"""
        return self.boxes[-1] if self.boxes else None
    
    def get_statistics(self):
        """
        Get system statistics
        
        Returns:
            dict: Dictionary with various statistics
        """
        approved_pieces = self.get_approved_pieces()
        rejected_pieces = self.get_rejected_pieces()
        total_pieces = len(self.pieces)
        
        stats = {
            'total_pieces': total_pieces,
            'approved_count': len(approved_pieces),
            'rejected_count': len(rejected_pieces),
            'approval_rate': (len(approved_pieces) / total_pieces * 100) if total_pieces > 0 else 0,
            'closed_boxes': len(self.get_closed_boxes()),
            'open_boxes': len(self.get_open_boxes())
        }
        
        # Rejection reasons analysis
        if rejected_pieces:
            rejection_analysis = self._analyze_rejection_reasons(rejected_pieces)
            stats['rejection_analysis'] = rejection_analysis
        
        # Quality statistics for approved pieces
        if approved_pieces:
            quality_stats = self._calculate_quality_statistics(approved_pieces)
            stats['quality_statistics'] = quality_stats
        
        return stats
    
    def _analyze_rejection_reasons(self, rejected_pieces):
        """
        Analyze rejection reasons
        
        Args:
            rejected_pieces (list): List of rejected pieces
            
        Returns:
            dict: Analysis of rejection reasons
        """
        weight_issues = 0
        color_issues = 0
        length_issues = 0
        
        for piece in rejected_pieces:
            for reason in piece.get_rejection_reasons():
                if 'Weight' in reason or 'weight' in reason:
                    weight_issues += 1
                if 'Color' in reason or 'color' in reason:
                    color_issues += 1
                if 'Length' in reason or 'length' in reason:
                    length_issues += 1
        
        return {
            'weight_issues': weight_issues,
            'color_issues': color_issues,
            'length_issues': length_issues
        }
    
    def _calculate_quality_statistics(self, approved_pieces):
        """
        Calculate quality statistics for approved pieces
        
        Args:
            approved_pieces (list): List of approved pieces
            
        Returns:
            dict: Quality statistics
        """
        weights = [p.weight for p in approved_pieces]
        lengths = [p.length for p in approved_pieces]
        colors = {}
        
        for piece in approved_pieces:
            colors[piece.color] = colors.get(piece.color, 0) + 1
        
        return {
            'average_weight': sum(weights) / len(weights),
            'min_weight': min(weights),
            'max_weight': max(weights),
            'average_length': sum(lengths) / len(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'color_distribution': colors
        }
    
    def generate_report(self):
        """
        Generate a comprehensive report
        
        Returns:
            dict: Complete report with all statistics
        """
        stats = self.get_statistics()
        
        report = {
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'summary': {
                'total_pieces': stats['total_pieces'],
                'approved': stats['approved_count'],
                'rejected': stats['rejected_count'],
                'approval_rate': stats['approval_rate']
            },
            'storage': {
                'closed_boxes': stats['closed_boxes'],
                'open_boxes': stats['open_boxes'],
                'current_box': self.get_current_box()
            },
            'pieces': {
                'approved': self.get_approved_pieces(),
                'rejected': self.get_rejected_pieces()
            }
        }
        
        if 'rejection_analysis' in stats:
            report['rejection_analysis'] = stats['rejection_analysis']
        
        if 'quality_statistics' in stats:
            report['quality_statistics'] = stats['quality_statistics']
        
        return report

