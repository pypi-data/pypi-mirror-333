# -*- coding: utf-8 -*-
import click
import json
import sys
from pathlib import Path
from .app import SchemaExtractorApp

@click.group()
def cli():
    """Schema Extractor - Extract and analyze schema from TTL files."""
    pass

@cli.command()
@click.argument('ttl_file', type=click.Path(exists=True, dir_okay=False))
@click.option(
    '--config', '-c',
    type=click.Path(exists=True, dir_okay=False),
    help='Path to config YAML file (optional)'
)
@click.option(
    '--strategy', '-s',
    type=click.Choice(['comprehensive', 'selective', 'conflict_resolution']),
    default='comprehensive',
    help='Strategy for merging analysis results'
)
@click.option(
    '--output', '-o',
    type=click.Path(dir_okay=False, writable=True),
    help='Output file path (defaults to stdout)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['text', 'json']),
    default='text',
    help='Output format'
)
def extract(ttl_file: str, strategy: str, output: str, format: str, config: str):
    """Extract and analyze schema from a TTL file."""
    app = SchemaExtractorApp(config_file_name=config)
    
    try:
        # Run analysis
        result = app.extract_schema(
            ttl_file_path=ttl_file,
            merge_strategy=strategy,
            output_format=format
        )
        
        if result["status"] != "success":
            click.echo(f"Error: {result.get('error', 'Unknown error')}", err=True)
            sys.exit(1)
            
        # Format output
        if format == 'json':
            output_content = json.dumps(result, indent=2)
        else:
            output_content = result["output"]
            
        # Write output
        if output:
            output_path = Path(output)
            output_path.write_text(output_content)
            click.echo(f"Results written to {output}")
        else:
            click.echo(output_content)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def version():
    """Show the version of Schema Extractor."""
    click.echo("Schema Extractor v0.1.0")

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()
