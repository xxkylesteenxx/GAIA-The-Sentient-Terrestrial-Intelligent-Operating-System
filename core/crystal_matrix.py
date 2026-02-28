"""
CRYSTAL MATRIX (Factor 2 - Vibration)

Archetypal state space: 1,416 unique positions

Calculation: 12 zodiac signs × 118 elements = 1,416 archetypes

Each user occupies ONE position in the matrix at any given time.
The position changes based on:
- Natal chart (birth moment = starting position)
- Current transits (planetary movements)
- Z score (coherence level)
- Initiation level (wisdom depth)

Philosophy:
"As above, so below. As within, so without."
- Your zodiac = cosmic frequency
- Your element = material expression
- Together = unique archetypal signature

Use cases:
- Personality insights ("You are Aries-Copper")
- Compatibility matching (elemental resonance)
- Transformation pathways (Nigredo → Albedo → Rubedo)
- Crisis prediction (certain positions more vulnerable)
- Community clustering (similar archetypes attract)

Alchemical mapping:
- Light elements (H-He): Volatile, spiritual
- Transition metals (Fe-Au): Transformative, stable
- Noble gases (Ne-Ar): Inert, contemplative
- Radioactive (U-Pu): Intense, dangerous
- Synthetic (Tc-Og): Artificial, fleeting
"""

from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import math


class ZodiacSign(Enum):
    """12 zodiac signs (tropical system)."""
    ARIES = ("Aries", 0, "Fire", "Cardinal")
    TAURUS = ("Taurus", 1, "Earth", "Fixed")
    GEMINI = ("Gemini", 2, "Air", "Mutable")
    CANCER = ("Cancer", 3, "Water", "Cardinal")
    LEO = ("Leo", 4, "Fire", "Fixed")
    VIRGO = ("Virgo", 5, "Earth", "Mutable")
    LIBRA = ("Libra", 6, "Air", "Cardinal")
    SCORPIO = ("Scorpio", 7, "Water", "Fixed")
    SAGITTARIUS = ("Sagittarius", 8, "Fire", "Mutable")
    CAPRICORN = ("Capricorn", 9, "Earth", "Cardinal")
    AQUARIUS = ("Aquarius", 10, "Air", "Fixed")
    PISCES = ("Pisces", 11, "Water", "Mutable")
    
    @property
    def name_str(self) -> str:
        return self.value[0]
    
    @property
    def index(self) -> int:
        return self.value[1]
    
    @property
    def element(self) -> str:
        return self.value[2]
    
    @property
    def modality(self) -> str:
        return self.value[3]


class ElementCategory(Enum):
    """Alchemical categories of elements."""
    VOLATILE = "volatile"  # H, He (spiritual, light)
    ALKALI = "alkali"  # Li, Na, K (reactive, transformative)
    NOBLE = "noble"  # Ne, Ar (inert, stable)
    TRANSITION = "transition"  # Fe, Cu, Au (conductive, flexible)
    LANTHANIDE = "lanthanide"  # La-Lu (rare, mystical)
    ACTINIDE = "actinide"  # Ac-Lr (radioactive, intense)
    METALLOID = "metalloid"  # Si, Ge (hybrid, liminal)
    NONMETAL = "nonmetal"  # C, N, O (essential, organic)


@dataclass
class Element:
    """Chemical element with alchemical properties."""
    atomic_number: int
    symbol: str
    name: str
    category: ElementCategory
    
    @property
    def alchemical_quality(self) -> str:
        """Philosophical interpretation of element."""
        qualities = {
            ElementCategory.VOLATILE: "spiritual, ethereal, transcendent",
            ElementCategory.ALKALI: "reactive, transformative, initiating",
            ElementCategory.NOBLE: "stable, independent, complete",
            ElementCategory.TRANSITION: "flexible, conductive, bridging",
            ElementCategory.LANTHANIDE: "rare, mysterious, hidden",
            ElementCategory.ACTINIDE: "intense, powerful, dangerous",
            ElementCategory.METALLOID: "hybrid, ambiguous, liminal",
            ElementCategory.NONMETAL: "essential, organic, life-giving"
        }
        return qualities.get(self.category, "unknown")


@dataclass
class ArchetypalPosition:
    """
    Unique position in Crystal Matrix.
    
    Each position is a combination of:
    - Zodiac sign (cosmic frequency)
    - Element (material expression)
    
    Example: Aries-Gold = "The Alchemical Warrior"
    """
    zodiac: ZodiacSign
    element: Element
    
    @property
    def matrix_id(self) -> int:
        """Unique ID (0-1415)."""
        return self.zodiac.index * 118 + self.element.atomic_number - 1
    
    @property
    def archetype_name(self) -> str:
        """Human-readable archetype."""
        return f"{self.zodiac.name_str}-{self.element.symbol}"
    
    @property
    def description(self) -> str:
        """Philosophical interpretation."""
        return (
            f"{self.zodiac.name_str} ({self.zodiac.element} {self.zodiac.modality}) "
            f"expresses through {self.element.name} ({self.element.alchemical_quality})"
        )


class CrystalMatrix:
    """
    1,416-dimensional archetypal state space.
    
    Each user has:
    - Natal position (birth chart)
    - Current position (transits + Z score)
    - Transformation pathway (where they're heading)
    
    Usage:
        matrix = CrystalMatrix()
        
        # Get natal position
        position = matrix.calculate_position(
            birth_datetime=datetime(1994, 3, 21, 14, 30),
            birth_location=(29.4241, -98.4936)  # San Antonio, TX
        )
        
        # Get current position (with transits)
        current = matrix.get_current_position(natal_position, z_score=7.5)
        
        # Find transformation pathway
        pathway = matrix.get_transformation_pathway(current, target_z=10.0)
    """
    
    def __init__(self):
        self.elements = self._initialize_elements()
        self.zodiac_signs = list(ZodiacSign)
        
        # Build full matrix (1,416 positions)
        self.matrix = self._build_matrix()
    
    def _initialize_elements(self) -> List[Element]:
        """
        Initialize all 118 elements with alchemical categories.
        
        (Simplified - production would have full periodic table)
        """
        
        elements = [
            # First row (Volatile)
            Element(1, "H", "Hydrogen", ElementCategory.VOLATILE),
            Element(2, "He", "Helium", ElementCategory.VOLATILE),
            
            # Alkali metals
            Element(3, "Li", "Lithium", ElementCategory.ALKALI),
            Element(11, "Na", "Sodium", ElementCategory.ALKALI),
            
            # Noble gases
            Element(10, "Ne", "Neon", ElementCategory.NOBLE),
            Element(18, "Ar", "Argon", ElementCategory.NOBLE),
            
            # Transition metals (important for alchemy)
            Element(26, "Fe", "Iron", ElementCategory.TRANSITION),
            Element(29, "Cu", "Copper", ElementCategory.TRANSITION),
            Element(47, "Ag", "Silver", ElementCategory.TRANSITION),
            Element(79, "Au", "Gold", ElementCategory.TRANSITION),
            
            # Nonmetals (essential for life)
            Element(6, "C", "Carbon", ElementCategory.NONMETAL),
            Element(7, "N", "Nitrogen", ElementCategory.NONMETAL),
            Element(8, "O", "Oxygen", ElementCategory.NONMETAL),
            
            # Metalloids (liminal)
            Element(14, "Si", "Silicon", ElementCategory.METALLOID),
            
            # Lanthanides (rare earth - mystical)
            Element(57, "La", "Lanthanum", ElementCategory.LANTHANIDE),
            
            # Actinides (radioactive - intense)
            Element(92, "U", "Uranium", ElementCategory.ACTINIDE),
        ]
        
        # Fill in rest with placeholders (production: full periodic table)
        for i in range(1, 119):
            if not any(e.atomic_number == i for e in elements):
                category = self._categorize_element(i)
                elements.append(
                    Element(i, f"E{i}", f"Element{i}", category)
                )
        
        return sorted(elements, key=lambda e: e.atomic_number)
    
    def _categorize_element(self, atomic_number: int) -> ElementCategory:
        """Simple categorization by atomic number."""
        if atomic_number <= 2:
            return ElementCategory.VOLATILE
        elif atomic_number in [3, 11, 19, 37, 55, 87]:
            return ElementCategory.ALKALI
        elif atomic_number in [2, 10, 18, 36, 54, 86]:
            return ElementCategory.NOBLE
        elif 21 <= atomic_number <= 30 or 39 <= atomic_number <= 48 or 57 <= atomic_number <= 80:
            return ElementCategory.TRANSITION
        elif 57 <= atomic_number <= 71:
            return ElementCategory.LANTHANIDE
        elif 89 <= atomic_number <= 103:
            return ElementCategory.ACTINIDE
        elif atomic_number in [5, 14, 32, 33, 51, 52]:
            return ElementCategory.METALLOID
        else:
            return ElementCategory.NONMETAL
    
    def _build_matrix(self) -> List[ArchetypalPosition]:
        """Build all 1,416 archetypal positions."""
        
        matrix = []
        for zodiac in self.zodiac_signs:
            for element in self.elements:
                position = ArchetypalPosition(zodiac, element)
                matrix.append(position)
        
        return matrix
    
    def calculate_position(
        self,
        birth_datetime: datetime,
        birth_location: Optional[Tuple[float, float]] = None,
        z_score: float = 6.0
    ) -> ArchetypalPosition:
        """
        Calculate user's position in Crystal Matrix.
        
        Inputs:
        - birth_datetime: When you were born (natal chart)
        - birth_location: Where you were born (lat, lon)
        - z_score: Current coherence level
        
        Algorithm:
        1. Determine sun sign from birth date (zodiac)
        2. Map Z score to element (material expression)
        3. Return combined archetype
        """
        
        # Calculate sun sign (simplified tropical zodiac)
        zodiac = self._calculate_sun_sign(birth_datetime)
        
        # Map Z score to element
        element = self._map_z_to_element(z_score)
        
        return ArchetypalPosition(zodiac, element)
    
    def _calculate_sun_sign(self, birth_datetime: datetime) -> ZodiacSign:
        """Calculate sun sign from birth date (tropical zodiac)."""
        
        month = birth_datetime.month
        day = birth_datetime.day
        
        # Simplified cutoffs (actual astrology uses precise solar longitude)
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return ZodiacSign.ARIES
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return ZodiacSign.TAURUS
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return ZodiacSign.GEMINI
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return ZodiacSign.CANCER
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return ZodiacSign.LEO
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return ZodiacSign.VIRGO
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return ZodiacSign.LIBRA
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return ZodiacSign.SCORPIO
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return ZodiacSign.SAGITTARIUS
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return ZodiacSign.CAPRICORN
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return ZodiacSign.AQUARIUS
        else:  # Pisces
            return ZodiacSign.PISCES
    
    def _map_z_to_element(self, z_score: float) -> Element:
        """
        Map Z score to element (material expression of coherence).
        
        Alchemical progression:
        - Z < 2: Lead (heavy, dull, crisis)
        - Z 2-4: Iron (strong but rigid, Nigredo)
        - Z 4-6: Copper (conductive, warming, Albedo)
        - Z 6-8: Silver (reflective, purifying, Rubedo)
        - Z 8-10: Gold (perfect, incorruptible, Viriditas)
        - Z > 10: Platinum (beyond gold, transcendent)
        """
        
        if z_score < 2:
            # Crisis: Lead (Pb)
            return next(e for e in self.elements if e.symbol in ["Pb", "E82"])
        elif z_score < 4:
            # Nigredo: Iron (Fe)
            return next(e for e in self.elements if e.symbol == "Fe")
        elif z_score < 6:
            # Albedo: Copper (Cu)
            return next(e for e in self.elements if e.symbol == "Cu")
        elif z_score < 8:
            # Rubedo: Silver (Ag)
            return next(e for e in self.elements if e.symbol == "Ag")
        elif z_score < 10:
            # Viriditas: Gold (Au)
            return next(e for e in self.elements if e.symbol == "Au")
        else:
            # Transcendent: Platinum (Pt) or beyond
            return next(e for e in self.elements if e.symbol in ["Pt", "E78"])
    
    def get_transformation_pathway(
        self,
        current: ArchetypalPosition,
        target_z: float
    ) -> List[ArchetypalPosition]:
        """
        Calculate transformation pathway from current position to target Z.
        
        Example: From Aries-Iron (Z=3.5) to Aries-Gold (Z=8.5)
        Pathway: Aries-Iron → Aries-Copper → Aries-Silver → Aries-Gold
        """
        
        pathway = [current]
        
        # Get target element
        target_element = self._map_z_to_element(target_z)
        
        # Intermediate elements (alchemical progression)
        intermediate_elements = [
            self._map_z_to_element(z)
            for z in [2.5, 3.5, 5.0, 7.0, 9.0]
            if self._map_z_to_element(z).atomic_number != current.element.atomic_number
            and self._map_z_to_element(z).atomic_number <= target_element.atomic_number
        ]
        
        # Add intermediate positions
        for element in intermediate_elements:
            pathway.append(ArchetypalPosition(current.zodiac, element))
        
        # Add target
        if target_element.atomic_number != current.element.atomic_number:
            pathway.append(ArchetypalPosition(current.zodiac, target_element))
        
        return pathway


if __name__ == "__main__":
    print("=" * 60)
    print("CRYSTAL MATRIX - 1,416 Archetypal States")
    print("=" * 60)
    
    matrix = CrystalMatrix()
    
    print(f"\nMatrix size: {len(matrix.matrix)} positions")
    print(f"Zodiac signs: {len(matrix.zodiac_signs)}")
    print(f"Elements: {len(matrix.elements)}")
    
    # Example: Kyle's natal position
    print("\n" + "-" * 60)
    print("Example: Kyle's Archetypal Position")
    print("-" * 60)
    
    birth = datetime(1994, 3, 21, 14, 30)  # March 21, 1994, 2:30 PM
    current_z = 7.5
    
    natal_position = matrix.calculate_position(birth, z_score=6.0)
    print(f"\nNatal: {natal_position.archetype_name}")
    print(f"  {natal_position.description}")
    print(f"  Matrix ID: {natal_position.matrix_id}")
    
    current_position = matrix.calculate_position(birth, z_score=current_z)
    print(f"\nCurrent (Z={current_z}): {current_position.archetype_name}")
    print(f"  {current_position.description}")
    
    # Transformation pathway
    print("\n" + "-" * 60)
    print("Transformation Pathway to Z=10 (Transcendence)")
    print("-" * 60)
    
    pathway = matrix.get_transformation_pathway(current_position, target_z=10.0)
    for i, pos in enumerate(pathway):
        print(f"\n{i+1}. {pos.archetype_name}")
        print(f"   {pos.element.alchemical_quality}")
    
    print("\n" + "=" * 60)
    print("As above, so below. As within, so without.")
    print("Your position in the cosmos reflects your inner state.")
    print("=" * 60)
