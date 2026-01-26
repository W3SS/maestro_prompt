# Maestro Console App Guide

## Overview

The Maestro Console App (`maestro_cli.py`) provides an interactive command-line interface for designing albums and generating songs using the Maestro AI system.

## Features

### 1. Design New Album

* Select from 60+ pop culture archetypes (cosmic_horror, cyberpunk_noir, etc.)
* Specify custom album title or auto-generate
* Configure number of tracks (default: 8)
* Automatic deduplication prevents duplicate tracks
* All tracks saved to centralized `fila_suno_v2.csv`

### 2. Generate Songs from Queue

* Process pending tracks from `fila_suno_v2.csv`
* Generate style prompts and lyrics using Ollama LLM
* Export to `suno_batch_v2.json` for Suno injection
* Automatic retry logic for failed generations

### 3. View Queue Status

* Display total tracks and albums in queue
* Show pending vs. processed track counts
* Preview next 5 tracks to be generated

### 4. Export to Suno JSON

* Check if `suno_batch_v2.json` exists
* Provides next steps for Suno automation

## Usage

### Starting the Console App

```bash
python maestro_cli.py
```

### Example Workflow

1. **Design an Album**
   * Select option 1
   * Choose archetype: `cosmic_horror`
   * Enter album title: `Echoes from the Abyss`
   * Set tracks: `8`

2. **View Queue**
   * Select option 3
   * Review pending tracks

3. **Generate Songs**
   * Select option 2
   * Confirm generation
   * Wait for Ollama to process each track

4. **Export to Suno**
   * Select option 4
   * Run `python maestro_brave_automator.py`

## Architecture

```
maestro_cli.py (Console Interface)
    ↓
maestro_ollama_enhanced.py (Core Logic)
    ↓
fila_suno_v2.csv (Central Queue)
    ↓
suno_batch_v2.json (Export Format)
```

## Configuration

### Ollama Connection

* Default: `http://localhost:11434`
* Modify `OLLAMA_URL` in `maestro_ollama_enhanced.py`

### Model Selection

* Default: `mistral-nemo:12b`
* Modify `MODEL_NAME` in `maestro_ollama_enhanced.py`

## Troubleshooting

### "Queue file not found"

* Run option 1 to create your first album

### "Ollama connection refused"

* Ensure Ollama is running: `docker-compose up -d`
* Check port 11434 is accessible

### "Timeout errors"

* Increase timeout in `maestro_ollama_enhanced.py` (line 638)
* Default: 300s for song generation

## Next Steps

See [Flask Web App Roadmap](FLASK_WEB_APP_ROADMAP.md) for web interface evolution.
