#! /home/tadeasf/Documents/coding-projects/translate-clix/.venv/bin/python3
from rich.panel import Panel
import typer
from rich.console import Console
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
import yaml
import json
import clipboard
from .lib import (
    V1Handler, 
    V2Handler, 
    FreeHandler, 
    CONFIG_DIR, 
    CONFIG_FILE, 
    HISTORY_FILE, 
    DEFAULT_CONFIG, 
    LANGUAGES
)

# Initialize Typer app
app = typer.Typer(help="translate-cliX - CLI interface for DeepLX/DeepL.")
console = Console()

class TranslateCliX:
    """Main class for the translate deepl free CLI tool."""
    
    def __init__(self, reset_config: bool = False):
        self.config = {}
        self.usage_data = {"translations": 0, "characters": 0}
        self.handler = None
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if reset_config and CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        self._load_or_create_config()
        self._load_usage_history()
        self._setup_handler()
    
    def _load_or_create_config(self) -> None:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                self.config = yaml.safe_load(f)
                
            # Ensure all default config keys exist
            for key, value in DEFAULT_CONFIG.items():
                if key not in self.config:
                    self.config[key] = value
                elif isinstance(value, dict) and isinstance(self.config[key], dict):
                    # Merge nested dictionaries
                    for sub_key, sub_value in value.items():
                        if sub_key not in self.config[key]:
                            self.config[key][sub_key] = sub_value
                            
            # Save updated config
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(self.config, f)
                
            console.print(f"[bold green]Loaded configuration from {CONFIG_FILE}[/bold green]")
        else:
            console.print("[bold yellow]No configuration found. Let's set up your preferences.[/bold yellow]")
            self._setup_config()

    def _setup_config(self) -> None:
        # Start with default config
        self.config = DEFAULT_CONFIG.copy()
        
        source_lang = self._prompt_language("Select your source language", default="CS")
        target_lang = self._prompt_language("Select your target language", default="EN-US")
        
        # Prompt for API endpoint
        endpoint_completer = WordCompleter(["v1", "v2"], ignore_case=True)
        endpoint = prompt(
            "Select API version (v1/v2): ",
            default="v2",
            completer=endpoint_completer
        )
        
        self.config.update({
            "source_lang": source_lang,
            "target_lang": target_lang,
            "api_type": endpoint
        })
        
        # Add API key prompt for v1/v2
        if endpoint in ["v1", "v2"]:
            api_key = prompt(
                "Enter your DeepL API key: ",
                is_password=True
            )
            self.config["api_key"] = api_key
            
            if endpoint == "v2":
                # For v2, ask if using free or pro plan
                is_free = prompt(
                    "Are you using the free plan? (y/n): ",
                    default="y"
                ).lower() == "y"
                self.config["is_free"] = is_free
        
        # Allow custom DeepLX URL
        custom_url = prompt(
            f"Enter custom DeepLX URL (leave empty for default: {self.config['api_urls']['deeplx']}): "
        )
        if custom_url:
            self.config["api_urls"]["deeplx"] = custom_url
        
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(self.config, f)
        console.print(f"[bold green]Configuration saved to {CONFIG_FILE}[/bold green]")

    def _setup_handler(self) -> None:
        """Setup the appropriate API handler based on configuration"""
        api_type = self.config.get("api_type", "v2")
        api_key = self.config.get("api_key", "")
        api_urls = self.config.get("api_urls", DEFAULT_CONFIG["api_urls"])
        api_endpoints = self.config.get("api_endpoints", DEFAULT_CONFIG["api_endpoints"])
        
        if api_type == "v1":
            self.handler = V1Handler(
                api_key=api_key,
                base_url=api_urls["deeplx"]  # Using DeepLX with V1 endpoint for now
            )
            # Set endpoint from config
            self.handler.endpoint = api_endpoints["v1"]
        elif api_type == "v2":
            is_free = self.config.get("is_free", True)
            self.handler = V2Handler(
                api_key=api_key,
                is_free=is_free,
                base_url=api_urls["deeplx"]  # Using DeepLX with V2 endpoint for now
            )
            # Set endpoint from config
            self.handler.endpoint = api_endpoints["v2"]
        else:  # free
            self.handler = FreeHandler(base_url=api_urls["deeplx"])
            # Set endpoint from config
            self.handler.endpoint = api_endpoints["free"]

    def _prompt_language(self, message: str, default: str) -> str:
        language_completer = WordCompleter(list(LANGUAGES.keys()), ignore_case=True)
        selected_language = prompt(
            f"{message}: ",
            default=default,
            completer=language_completer,
            complete_while_typing=True,        )
        return selected_language if selected_language in LANGUAGES else default

    def _load_usage_history(self) -> None:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r") as f:
                self.usage_data = json.load(f)
        else:
            with open(HISTORY_FILE, "w") as f:
                json.dump(self.usage_data, f)

    def _update_usage_history(self, characters: int) -> None:
        self.usage_data["translations"] += 1
        self.usage_data["characters"] += characters
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.usage_data, f)

    def translate_text(self, text: str) -> None:
        if not text:
            console.print("[bold red]Error: Empty text input.[/bold red]")
            return

        if not self.handler:
            console.print("[bold red]Error: No API handler configured.[/bold red]")
            return
            
        try:
            # Get language codes from language names
            source_lang = LANGUAGES.get(self.config["source_lang"], "CS")
            target_lang = LANGUAGES.get(self.config["target_lang"], "EN-US")
            
            # Translate using the appropriate handler
            translated_text = self.handler.translate(text, source_lang, target_lang)

            clipboard.copy(translated_text)
            self._display_translation_result(text, translated_text)
            self._update_usage_history(len(text))

        except Exception as e:
            console.print(f"Error: {str(e)}")

    def _display_translation_result(self, original: str, translated: str) -> None:
        console.print(Panel(original, title="Original Text"))
        console.print(Panel(translated, title="Translated", border_style="green"))
        console.print("Translation copied to clipboard!")

    def interactive_session(self) -> None:
        while True:
            try:
                text = prompt("Enter text to translate: ")
                if text:
                    self.translate_text(text)
            except KeyboardInterrupt:
                console.print("\nExiting. Thanks for using DeepL Easy CLI!")
                break

@app.command()
def translate(reset_config: bool = typer.Option(False, "-c", "--reset-config", help="Reset configuration before starting")):
    cli = TranslateCliX(reset_config)
    cli.interactive_session()

def main():
    app()

if __name__ == "__main__":
    main()


