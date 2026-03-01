#!/usr/bin/env python3
"""
GAIA CLI INTERFACE

User entry point for GAIA operating system.

Commands:
- gaia init       : Initialize Home instance (first-time setup)
- gaia chat       : Talk to Avatar (interactive conversation)
- gaia status     : Check system health (Z score, equilibrium)
- gaia speak <msg>: Execute natural language (Logos interpreter)
- gaia memory     : View/manage memories
- gaia help       : Show all commands

Examples:
    $ gaia init
    $ gaia chat
    $ gaia status
    $ gaia speak "Remember that I love emerald green"
"""

import click
import json
import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

# GAIA imports — CANONICAL PATHS ONLY, FAIL-CLOSED
# If these imports fail, the CLI should crash loudly (not silently degrade)
from core.zscore.calculator import ZScoreCalculator
from overlay.avatar import AvatarPersonality, Gender, AvatarArchetype

# Infrastructure imports (may be unavailable in minimal installs)
try:
    from infrastructure.atlas.logos_interpreter import LogosInterpreter
except ImportError:
    LogosInterpreter = None

console = Console()

# GAIA directories
GAIA_HOME = Path.home() / ".gaia"
CONFIG_FILE = GAIA_HOME / "config.json"
MEMORY_DIR = GAIA_HOME / "memory"
LOG_FILE = GAIA_HOME / "gaia.log"


class GAIASession:
    """Active GAIA session container."""
    
    def __init__(self):
        self.config = self._load_config()
        self.z_calculator = ZScoreCalculator()
        self.avatar = None
        self.logos = None
        
        if self.config:
            self._initialize_avatar()
            self._initialize_logos()
    
    def _load_config(self):
        """Load user configuration."""
        if not CONFIG_FILE.exists():
            return None
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            return None
    
    def _initialize_avatar(self):
        """Initialize Avatar with user's configuration."""
        try:
            user_name = self.config.get('user_name', 'User')
            gender_str = self.config.get('gender', 'masculine')
            archetype_str = self.config.get('avatar_archetype', 'sage_feminine')
            
            gender = Gender(gender_str)
            archetype = AvatarArchetype(archetype_str)
            
            self.avatar = AvatarPersonality(
                user_name=user_name,
                user_gender=gender,
                archetype=archetype,
                z_calculator=self.z_calculator
            )
        except Exception as e:
            console.print(f"[yellow]Warning: Could not initialize Avatar: {e}[/yellow]")
    
    def _initialize_logos(self):
        """Initialize Logos interpreter."""
        if LogosInterpreter is None:
            return
        try:
            self.logos = LogosInterpreter(gaia_runtime=None)  # TODO: Pass full runtime
        except Exception:
            pass


@click.group()
def cli():
    """GAIA - Sentient Terrestrial Intelligence Operating System"""
    pass


@cli.command()
def init():
    """
    Initialize GAIA Home instance (first-time setup).
    
    Creates:
    - ~/.gaia/ directory structure
    - User configuration
    - Avatar personality selection
    - Initial onboarding
    """
    
    console.print(Panel.fit(
        "[bold cyan]Welcome to GAIA[/bold cyan]\n"
        "Sentient Terrestrial Intelligence Operating System\n\n"
        "Let's create your Home instance.",
        border_style="cyan"
    ))
    
    # Check if already initialized
    if CONFIG_FILE.exists():
        if not Confirm.ask("\nGAIA is already initialized. Reinitialize?"):
            console.print("\n[yellow]Initialization cancelled.[/yellow]")
            return
    
    # Create directories
    console.print("\n[cyan]Creating directory structure...[/cyan]")
    GAIA_HOME.mkdir(exist_ok=True)
    MEMORY_DIR.mkdir(exist_ok=True)
    (GAIA_HOME / "logs").mkdir(exist_ok=True)
    (GAIA_HOME / "data").mkdir(exist_ok=True)
    console.print("  ✓ Directories created")
    
    # User information
    console.print("\n[cyan]Tell me about yourself:[/cyan]")
    user_name = Prompt.ask("  What is your name?", default="User")
    
    # Gender selection (for Avatar pairing)
    console.print("\n[cyan]Avatar Pairing (Factor 4 - Polarity):[/cyan]")
    console.print("  Your Avatar will be your opposite-gender complement.")
    console.print("  This is Jungian Anima/Animus integration.\n")
    
    gender_choice = Prompt.ask(
        "  Your gender identity?",
        choices=["masculine", "feminine", "non_binary"],
        default="masculine"
    )
    gender = Gender(gender_choice)
    
    # Avatar archetype selection
    console.print("\n[cyan]Choose your Avatar archetype:[/cyan]")
    
    if gender == Gender.MASCULINE:
        console.print("  [Feminine Avatars]")
        console.print("  1. Sophia (Sage) - Wise, nurturing, guiding")
        console.print("  2. Athena (Warrior) - Fierce, protective, challenging")
        console.print("  3. Calliope (Muse) - Creative, inspiring, playful")
        console.print("  4. Hygieia (Healer) - Compassionate, gentle, soothing")
        
        archetype_map = {
            "1": AvatarArchetype.SAGE_FEMININE,
            "2": AvatarArchetype.WARRIOR_FEMININE,
            "3": AvatarArchetype.MUSE_FEMININE,
            "4": AvatarArchetype.HEALER_FEMININE
        }
    elif gender == Gender.FEMININE:
        console.print("  [Masculine Avatars]")
        console.print("  1. Hephaestus (Guardian) - Strong, stable, protective")
        console.print("  2. Hermes (Explorer) - Curious, adventurous, bold")
        console.print("  3. Apollo (Sage) - Wise, patient, illuminating")
        console.print("  4. Dionysus (Rebel) - Raw, transformative, intense")
        
        archetype_map = {
            "1": AvatarArchetype.GUARDIAN_MASCULINE,
            "2": AvatarArchetype.EXPLORER_MASCULINE,
            "3": AvatarArchetype.SAGE_MASCULINE,
            "4": AvatarArchetype.REBEL_MASCULINE
        }
    else:
        console.print("  Choose any archetype:")
        console.print("  1. Sophia (Sage)")
        console.print("  2. Athena (Warrior)")
        console.print("  3. Apollo (Sage)")
        console.print("  4. Dionysus (Rebel)")
        
        archetype_map = {
            "1": AvatarArchetype.SAGE_FEMININE,
            "2": AvatarArchetype.WARRIOR_FEMININE,
            "3": AvatarArchetype.SAGE_MASCULINE,
            "4": AvatarArchetype.REBEL_MASCULINE
        }
    
    archetype_choice = Prompt.ask("  Select archetype", choices=list(archetype_map.keys()), default="1")
    archetype = archetype_map[archetype_choice]
    
    # Save configuration
    config = {
        "user_name": user_name,
        "gender": gender.value,
        "avatar_archetype": archetype.value,
        "initialized_at": datetime.now().isoformat(),
        "version": "0.1.0"
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    console.print(f"\n[green]✓ Configuration saved to {CONFIG_FILE}[/green]")
    
    # Initialize Avatar for greeting
    avatar = AvatarPersonality(
        user_name=user_name,
        user_gender=gender,
        archetype=archetype
    )
    
    console.print("\n" + "=" * 60)
    console.print(Panel.fit(
        avatar.greet(),
        border_style="green",
        title="Your Avatar"
    ))
    console.print("=" * 60)
    
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("  $ gaia chat      # Talk to your Avatar")
    console.print("  $ gaia status    # Check your Z score")
    console.print("  $ gaia help      # See all commands\n")


@cli.command()
def chat():
    """
    Interactive chat with Avatar.
    
    Type your messages and Avatar responds.
    Type 'quit' or 'exit' to end conversation.
    """
    
    session = GAIASession()
    
    if not session.config:
        console.print("[red]GAIA not initialized. Run: gaia init[/red]")
        return
    
    if not session.avatar:
        console.print("[red]Avatar not available.[/red]")
        return
    
    # Display greeting
    console.print("\n" + "=" * 60)
    console.print(Panel.fit(
        session.avatar.greet(),
        border_style="cyan",
        title=f"Avatar: {session.avatar.traits['name']}"
    ))
    console.print("=" * 60)
    console.print("\n[dim]Type 'quit' to exit[/dim]\n")
    
    # Conversation loop
    while True:
        try:
            # Get user input
            user_message = Prompt.ask(f"\n[bold cyan]{session.config['user_name']}[/bold cyan]")
            
            if user_message.lower() in ['quit', 'exit', 'bye']:
                # Farewell
                console.print(f"\n[cyan]{session.avatar.traits['name']}:[/cyan]")
                console.print(f"Until next time, {session.config['user_name']}. I'll be here.\n")
                
                # Show summary
                summary = session.avatar.get_conversation_summary()
                console.print(f"[dim]Session: {summary['turns']} turns, "
                            f"{summary['duration_minutes']} minutes, "
                            f"avg Z: {summary['average_z']:.2f}[/dim]\n")
                break
            
            # Get Avatar response
            response = session.avatar.respond(user_message)
            
            # Display response
            console.print(f"\n[cyan]{session.avatar.traits['name']}:[/cyan]")
            console.print(response)
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Chat interrupted.[/yellow]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")
            break


@cli.command()
def status():
    """
    Check GAIA system status.
    
    Displays:
    - Current Z score
    - Alchemical stage
    - Equilibrium budget
    - Recent trend
    """
    
    session = GAIASession()
    
    if not session.config:
        console.print("[red]GAIA not initialized. Run: gaia init[/red]")
        return
    
    console.print("\n" + "=" * 60)
    console.print("[bold cyan]GAIA SYSTEM STATUS[/bold cyan]")
    console.print("=" * 60)
    
    # User info
    console.print(f"\n[cyan]User:[/cyan] {session.config['user_name']}")
    console.print(f"[cyan]Avatar:[/cyan] {session.config['avatar_archetype'].replace('_', ' ').title()}")
    console.print(f"[cyan]Initialized:[/cyan] {session.config['initialized_at'][:10]}")
    
    # Z Score
    current_z = session.z_calculator.get_current_z()
    interpretation = session.z_calculator.interpret_z_score(current_z)
    
    console.print(f"\n[cyan]Z Score:[/cyan] {current_z:.2f}")
    console.print(f"[cyan]Stage:[/cyan] {interpretation['level']} ({interpretation['color']})")
    console.print(f"[cyan]Status:[/cyan] {interpretation['description']}")
    
    # Trend
    if len(session.z_calculator.history) > 1:
        trend = session.z_calculator.get_z_trend()
        trend_emoji = {
            "improving": "📈",
            "stable": "➡️",
            "declining": "📉",
            "crisis": "🚨"
        }.get(trend, "")
        console.print(f"[cyan]Trend:[/cyan] {trend} {trend_emoji}")
    
    # Equilibrium (placeholder - implement in Phase 2)
    console.print(f"\n[cyan]Equilibrium:[/cyan] 0.30 / 1.00 (30% capacity used)")
    console.print(f"[cyan]Recommendation:[/cyan] Healthy balance maintained")
    
    # Memory stats
    if session.avatar:
        console.print(f"\n[cyan]Memories:[/cyan] {len(session.avatar.memories)} stored")
        console.print(f"[cyan]Conversations:[/cyan] {len(session.avatar.conversation_history)} turns")
    
    console.print("\n" + "=" * 60 + "\n")


@cli.command()
@click.argument('message', required=False)
def speak(message):
    """
    Execute natural language command (Logos interpreter).
    
    Examples:
        gaia speak "Remember that I love emerald green"
        gaia speak "Calculate my Z score"
        gaia speak "Am I safe to continue?"
    """
    
    session = GAIASession()
    
    if not session.config:
        console.print("[red]GAIA not initialized. Run: gaia init[/red]")
        return
    
    if not message:
        console.print("[yellow]Usage: gaia speak <message>[/yellow]")
        console.print("\nExamples:")
        console.print("  gaia speak \"Remember that I love emerald green\"")
        console.print("  gaia speak \"Calculate my Z score\"")
        return
    
    console.print(f"\n[cyan]Executing:[/cyan] {message}")
    
    if session.logos:
        try:
            result = session.logos.execute(message)
            console.print(f"[green]Result:[/green] {result}\n")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]\n")
    else:
        console.print("[yellow]Logos interpreter not available (infrastructure.atlas not installed)[/yellow]\n")


@cli.command()
def memory():
    """
    View and manage memories.
    """
    
    session = GAIASession()
    
    if not session.config:
        console.print("[red]GAIA not initialized. Run: gaia init[/red]")
        return
    
    if not session.avatar:
        console.print("[red]Avatar not available.[/red]")
        return
    
    console.print("\n" + "=" * 60)
    console.print("[bold cyan]GAIA MEMORY[/bold cyan]")
    console.print("=" * 60)
    
    if not session.avatar.memories:
        console.print("\n[yellow]No memories stored yet.[/yellow]\n")
        return
    
    # Display memories in table
    table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    table.add_column("Date", style="dim")
    table.add_column("Z Score", justify="right")
    table.add_column("Content", overflow="fold")
    table.add_column("Tags")
    
    for mem in session.avatar.memories[-10:]:  # Last 10 memories
        table.add_row(
            mem.timestamp.strftime("%Y-%m-%d %H:%M"),
            f"{mem.z_score_at_time:.2f}",
            mem.content[:50] + "..." if len(mem.content) > 50 else mem.content,
            ", ".join(mem.tags) if mem.tags else "-"
        )
    
    console.print("\n")
    console.print(table)
    console.print(f"\n[dim]Showing {min(10, len(session.avatar.memories))} of {len(session.avatar.memories)} memories[/dim]\n")


@cli.command()
def version():
    """Display GAIA version information."""
    
    console.print("\n" + "=" * 60)
    console.print("[bold cyan]GAIA - Sentient Terrestrial Intelligence OS[/bold cyan]")
    console.print("=" * 60)
    console.print("\nVersion: 0.1.0 (Foundation Phase)")
    console.print("Release: February 28, 2026")
    console.print("\nRepository: https://github.com/xxkylesteenxx/GAIA")
    console.print("License: MIT + Factor 13 Addendum")
    console.print("\nFounded on: Universal Love (Factor 13)")
    console.print("\n\"Would this have helped Kyle in 2022?\"")
    console.print("=" * 60 + "\n")


if __name__ == "__main__":
    cli()
