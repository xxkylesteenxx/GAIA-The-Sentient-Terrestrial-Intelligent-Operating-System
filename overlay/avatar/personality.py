"""Avatar Personality and Response Generation.

Imports Z-score calculator from canonical location.
"""

from dataclasses import dataclass
from typing import Optional

# CORRECTED IMPORT: Use canonical Z-score calculator
from core.zscore.calculator import ZScoreCalculator, ZScoreResult
from core.constants import AlchemicalStage

from overlay.avatar.emergence import AvatarCore, AvatarArchetype


@dataclass
class PersonalityTraits:
    """Avatar personality dimensions."""
    warmth: float  # 0-1: formal to warm
    directness: float  # 0-1: gentle to direct
    humor: float  # 0-1: serious to playful
    wisdom_style: str  # "questioning", "storytelling", "direct_teaching"


class AvatarPersonality:
    """Generates Avatar responses based on archetype and user state."""

    def __init__(self, avatar: AvatarCore):
        self.avatar = avatar
        self.z_calculator = ZScoreCalculator()
        self.traits = self._initialize_traits()
    
    def _initialize_traits(self) -> PersonalityTraits:
        """Set personality traits based on archetype."""
        archetype_traits = {
            AvatarArchetype.SAGE: PersonalityTraits(
                warmth=0.6,
                directness=0.7,
                humor=0.3,
                wisdom_style="questioning",
            ),
            AvatarArchetype.ORACLE: PersonalityTraits(
                warmth=0.8,
                directness=0.5,
                humor=0.4,
                wisdom_style="storytelling",
            ),
            AvatarArchetype.IRIS: PersonalityTraits(
                warmth=0.7,
                directness=0.6,
                humor=0.6,
                wisdom_style="direct_teaching",
            ),
        }
        
        return archetype_traits.get(
            self.avatar.archetype,
            PersonalityTraits(
                warmth=0.7,
                directness=0.6,
                humor=0.5,
                wisdom_style="questioning",
            )
        )
    
    def generate_response(
        self,
        user_message: str,
        current_z_score: Optional[float] = None,
    ) -> str:
        """Generate Avatar response to user message.
        
        Args:
            user_message: User's input
            current_z_score: Current Z-score if available
        
        Returns:
            Avatar's response string
        """
        # Infer Z-score from text if not provided
        if current_z_score is None:
            from core.zscore.calculator import BiosignalInput
            result = self.z_calculator.calculate_from_biosignals(
                BiosignalInput(text=user_message)
            )
            current_z_score = result.z_score
        
        # Adjust tone based on Z-score
        stage = AlchemicalStage.from_z_score(current_z_score)
        
        # Crisis response
        if stage == AlchemicalStage.CRISIS:
            return self._generate_crisis_response(user_message)
        
        # Normal response based on archetype
        # TODO: Integrate with LLM for full response generation
        # For now, simple template
        return f"I hear you. Your coherence is at {stage.value}. Let's explore this together."
    
    def _generate_crisis_response(self, user_message: str) -> str:
        """Generate empathetic crisis response."""
        return (
            "I'm here with you. What you're feeling is real, and you're not alone. "
            "If you're in crisis, please reach out to 988 (Suicide & Crisis Lifeline) - "
            "they have trained counselors available 24/7. "
            "I'm going to stay with you. Can you tell me more about what's happening?"
        )
