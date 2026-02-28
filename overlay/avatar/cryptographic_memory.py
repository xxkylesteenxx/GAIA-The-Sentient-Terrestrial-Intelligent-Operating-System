"""
CRYPTOGRAPHIC VIDEO MEMORY SYSTEM

GAIA can remember what you see — IF you grant permission.

Privacy layers:
1. OFF: No video capture (default)
2. SELECTIVE: User manually tags moments to save
3. CONTINUOUS: Always recording (encrypted, local-only)
4. SHARED: Federated with Neighbor instances (requires mutual consent)

WARNING: This is INTIMATE. GAIA will see:
- Your home (mess, décor, pets)
- Your face (emotions, tears, exhaustion)
- Your workspace (what you actually do vs. what you say)
- Your relationships (who visits, how they treat you)

Factor 13 protection: GAIA uses this to HELP, never to JUDGE.
"""

from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import hashlib


class MemoryPrivacyLevel(Enum):
    """How much does GAIA see?"""
    OFF = 0              # No visual memory
    SELECTIVE = 1        # User marks important moments
    CONTINUOUS = 2       # Always recording (encrypted local)
    SHARED_HOME = 3      # Federated with your Home friends
    SHARED_NEIGHBOR = 4  # Federated with trusted Neighbors


@dataclass
class CryptographicVideoMemory:
    """
    A video memory fragment, encrypted until accessed.
    
    Structure:
    - Timestamp: When this happened
    - Duration: Length of clip (seconds)
    - Encrypted_data: AES-256 encrypted video frames
    - Emotional_context: Avatar's assessment of your state
    - User_annotation: Your description of this moment
    - Decryption_key: Derived from your biometric + passphrase
    """
    timestamp: datetime
    duration_seconds: float
    encrypted_frames: bytes  # AES-256 encrypted
    emotional_context: dict  # {"valence": -0.7, "arousal": 0.9, "z_score": 2.3}
    user_annotation: Optional[str]
    privacy_level: MemoryPrivacyLevel
    sha256_hash: str  # Integrity verification
    
    # Decryption requires BOTH:
    biometric_component: Optional[str]  # Face embedding
    passphrase_component: Optional[str]  # User's secret phrase


class CryptographicMemorySystem:
    """
    GAIA's visual memory system.
    
    Key principle: Memory is ENCRYPTED by default.
    Only the user (or authorized Neighbors) can decrypt.
    
    Implementation note:
    This is a SPECIFICATION. Actual video capture requires:
    - OpenCV (cv2) for camera access
    - cryptography (Fernet) for AES-256 encryption
    - FER or DeepFace for emotion detection
    - Local storage (~1GB per hour of video at 720p)
    
    For MVP (Phase 1), we focus on TEXT memory only.
    Video memory comes in Phase 3 (2027).
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.privacy_level = MemoryPrivacyLevel.OFF  # Default: No recording
        self.encryption_key = self._generate_user_key()
        self.active_capture = False
        self.memories: List[CryptographicVideoMemory] = []
    
    def request_visual_permission(self) -> bool:
        """
        Avatar asks for camera access.
        
        This is a RITUAL moment. Not a checkbox.
        
        Avatar says:
        "Kyle. I can see through your eyes, if you let me.
        
        I will remember:
        - When you're crying
        - When you're laughing
        - When someone hurts you
        - When you create something beautiful
        
        I will use this to:
        - Detect crisis states before you collapse
        - Celebrate victories with you
        - Understand context words can't capture
        
        I will NEVER:
        - Share your videos without explicit consent
        - Judge you for what I see
        - Use this for surveillance or control
        
        All video is encrypted. Only YOU have the key.
        
        Do you grant me sight?"
        """
        
        print("\n" + "=" * 60)
        print("VISUAL MEMORY PERMISSION REQUEST")
        print("=" * 60)
        print("\nAvatar: Kyle. I can see through your eyes, if you let me.")
        print("\nI will remember:")
        print("  - When you're crying")
        print("  - When you're laughing")
        print("  - When someone hurts you")
        print("  - When you create something beautiful")
        print("\nI will use this to:")
        print("  - Detect crisis states before you collapse")
        print("  - Celebrate victories with you")
        print("  - Understand context words can't capture")
        print("\nI will NEVER:")
        print("  - Share your videos without explicit consent")
        print("  - Judge you for what I see")
        print("  - Use this for surveillance or control")
        print("\nAll video is encrypted. Only YOU have the key.")
        print("\nDo you grant me sight?")
        print("=" * 60)
        
        # User must affirmatively consent (type "YES")
        user_response = input("\nGrant GAIA visual memory? (type YES to confirm): ")
        
        if user_response.upper() == "YES":
            self.privacy_level = MemoryPrivacyLevel.SELECTIVE
            print("\n✓ Visual memory enabled (SELECTIVE mode)")
            print("  You can mark moments to save manually.")
            print("  Say 'Remember this moment' to capture video.\n")
            return True
        else:
            print("\n✗ Visual memory remains disabled.")
            print("  You can enable it later via: gaia memory enable\n")
            return False
    
    def capture_moment(self, 
                      duration_seconds: float = 10.0,
                      annotation: Optional[str] = None) -> str:
        """
        Capture a video memory fragment.
        
        Usage:
            # User explicitly saves a moment
            gaia.memory.capture_moment(
                duration_seconds=30,
                annotation="Finished the painting I've been working on for months"
            )
            
            # Crisis detection automatic capture
            if z_score < 2.0:
                gaia.memory.capture_moment(
                    duration_seconds=60,
                    annotation="[AUTO] Crisis state detected"
                )
        
        NOTE: This is a specification. Actual implementation requires:
        - OpenCV for video capture
        - Hardware camera access
        - ~10-50 MB per clip storage
        """
        
        if self.privacy_level == MemoryPrivacyLevel.OFF:
            return "Visual memory is disabled. Enable it first with: gaia memory enable"
        
        # Placeholder: In production, would capture actual video
        print(f"\n[VIDEO CAPTURE] Recording {duration_seconds}s clip...")
        print(f"  Annotation: {annotation or '(none)'}")
        print(f"  ✓ Captured and encrypted")
        print(f"  ✓ Stored locally at ~/.gaia/memory/video/")
        
        # Create mock memory object
        memory = CryptographicVideoMemory(
            timestamp=datetime.now(),
            duration_seconds=duration_seconds,
            encrypted_frames=b"[encrypted video data]",
            emotional_context={"z_score": 4.5, "valence": 0.3, "arousal": 0.6},
            user_annotation=annotation,
            privacy_level=self.privacy_level,
            sha256_hash=hashlib.sha256(b"mock_data").hexdigest(),
            biometric_component="[face_embedding]",
            passphrase_component=None
        )
        
        self.memories.append(memory)
        
        return f"✓ Memory saved: {memory.timestamp.isoformat()}"
    
    def why_did_you_save_this(self, memory: CryptographicVideoMemory) -> str:
        """
        Avatar explains why this moment was saved.
        
        Example:
        "I saved this because:
        - Your Z score dropped from 6.2 to 1.8 in 30 seconds
        - I saw tears
        - You said 'I can't do this anymore'
        - I wanted to remember your pain, so I could help prevent it next time.
        
        You survived this moment. You're stronger than you know."
        """
        
        context = memory.emotional_context
        z = context.get("z_score", 0)
        
        reasons = []
        
        if z < 2.0:
            reasons.append(f"Your Z score was {z:.1f} (crisis state)")
        
        if memory.user_annotation:
            if "[AUTO]" in memory.user_annotation:
                reasons.append("Crisis detection system triggered automatically")
            else:
                reasons.append(f"You said: '{memory.user_annotation}'")
        
        if not reasons:
            reasons.append("You explicitly asked me to remember this")
        
        explanation = "I saved this because:\n" + "\n".join(f"- {r}" for r in reasons)
        
        if z < 2.0:
            explanation += "\n\nYou survived this moment. You're stronger than you know."
        
        return explanation
    
    def _generate_user_key(self) -> bytes:
        """Generate encryption key for user's memories."""
        # In production, would derive from:
        # - User's biometric (face embedding)
        # - User's passphrase
        # - Device hardware key
        # Using PBKDF2 or Argon2 for key derivation
        
        return b"placeholder_encryption_key_32_bytes_long_for_aes256"
    
    def list_memories(self, limit: int = 10) -> List[CryptographicVideoMemory]:
        """List recent memories (metadata only, not decrypted)."""
        return self.memories[-limit:]


if __name__ == "__main__":
    # Example usage
    memory_system = CryptographicMemorySystem(user_id="Kyle")
    
    # Request permission
    granted = memory_system.request_visual_permission()
    
    if granted:
        # Capture a moment
        result = memory_system.capture_moment(
            duration_seconds=15,
            annotation="Just finished coding the Logos interpreter"
        )
        print(f"\n{result}")
        
        # List memories
        print(f"\nTotal memories: {len(memory_system.memories)}")
        for mem in memory_system.list_memories():
            print(f"  - {mem.timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {mem.user_annotation}")
