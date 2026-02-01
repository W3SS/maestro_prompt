#!/usr/bin/env python3
"""
MAESTRO AI - Console Application
Interactive CLI for album design and song generation
"""

import os
import sys
import pandas as pd
from maestro_ollama_enhanced import MaestroAlbumArchitect, gerar_lote_ollama, MaestroDataLoader

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("🎹 MAESTRO AI - Neural Audio Workstation")
    print("=" * 60)
    print()

def view_queue_status():
    """Display current queue status from fila_suno_v2.csv"""
    csv_path = "fila_suno_v2.csv"
    
    if not os.path.exists(csv_path):
        print("❌ Queue file not found. Create an album first!")
        return
    
    df = pd.read_csv(csv_path)
    
    print(f"\n📊 Queue Status: {len(df)} total tracks")
    print("-" * 60)
    
    # Group by album
    albums = df.groupby('album').size()
    print(f"\n📀 Albums in queue ({len(albums)}):")
    for album, count in albums.items():
        pending = len(df[(df['album'] == album) & (df['processada'] != 'sim')])
        print(f"   • {album}: {count} tracks ({pending} pending)")
    
    # Show pending tracks
    pending_df = df[df['processada'] != 'sim']
    if not pending_df.empty:
        print(f"\n⏳ Next {min(5, len(pending_df))} tracks to process:")
        for idx, row in pending_df.head(5).iterrows():
            print(f"   {idx+1}. [{row['album']}] {row['titulo']} ({row['genero']})")
    else:
        print("\n✅ All tracks have been processed!")

def design_new_album():
    """Interactive album design workflow"""
    print("\n🎨 Album Design Wizard")
    print("-" * 60)
    
    # Load available archetypes
    data_loader = MaestroDataLoader()
    archetypes = data_loader.aesthetics_semiotics.get('pop_culture_archetypes', {})
    
    print(f"\n📚 Available Archetypes ({len(archetypes)}):")
    archetype_list = list(archetypes.keys())
    
    # Show first 10 archetypes
    for i, arch in enumerate(archetype_list[:10], 1):
        print(f"   {i}. {arch}")
    
    if len(archetype_list) > 10:
        print(f"   ... and {len(archetype_list) - 10} more")
    
    print("\nType archetype name (or press Enter to see full list):")
    archetype_input = input("Archetype: ").strip()
    
    if not archetype_input:
        print("\nFull archetype list:")
        for i, arch in enumerate(archetype_list, 1):
            print(f"   {i}. {arch}")
        archetype_input = input("\nArchetype: ").strip()
    
    if archetype_input not in archetypes:
        print(f"❌ Archetype '{archetype_input}' not found!")
        return
    
    # Get album details
    album_title = input("Album Title (optional, press Enter to auto-generate): ").strip() or None
    
    try:
        num_tracks = int(input("Number of tracks (default 8): ").strip() or "8")
    except ValueError:
        num_tracks = 8
    
    print(f"\n🚀 Designing album with archetype '{archetype_input}'...")
    
    # Instantiate architect
    architect = MaestroAlbumArchitect(data_loader)
    result = architect.design_album(archetype_input, album_title, num_tracks)
    
    if result:
        print(f"\n✅ Album successfully added to queue!")
        input("\nPress Enter to continue...")

def generate_songs():
    """Generate songs from queue"""
    csv_path = "fila_suno_v2.csv"
    
    if not os.path.exists(csv_path):
        print("❌ Queue file not found. Create an album first!")
        return
    
    df = pd.read_csv(csv_path)
    pending = df[df['processada'] != 'sim']
    
    if pending.empty:
        print("✅ All tracks have been processed!")
        return
    
    print(f"\n🎵 Found {len(pending)} pending tracks")
    confirm = input("Start generation? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\n🚀 Starting song generation...")
        gerar_lote_ollama(csv_path)
        print("\n✅ Generation complete!")
        input("\nPress Enter to continue...")

def export_to_suno():
    """Export queue to Suno JSON format"""
    print("\n📦 Export to Suno JSON")
    print("-" * 60)
    
    if os.path.exists("suno_batch_v2.json"):
        print("✅ suno_batch_v2.json found!")
        print("\nNext step: Run 'python maestro_brave_automator.py' to inject into Suno")
    else:
        print("❌ No suno_batch_v2.json found. Generate songs first!")
    
    input("\nPress Enter to continue...")

def main_menu():
    """Main interactive menu"""
    while True:
        clear_screen()
        print_header()
        
        print("Main Menu:")
        print("  1. 🎨 Design New Album")
        print("  2. 🎵 Generate Songs from Queue")
        print("  3. 📊 View Queue Status")
        print("  4. 📦 Export to Suno JSON")
        print("  5. 🚪 Exit")
        print()
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            design_new_album()
        elif choice == '2':
            generate_songs()
        elif choice == '3':
            view_queue_status()
            input("\nPress Enter to continue...")
        elif choice == '4':
            export_to_suno()
        elif choice == '5':
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
