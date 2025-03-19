#!/usr/bin/env python3
"""
SJM AI Client - Command Line Interface
"""

import os
import sys
import json
import click
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box
import pkg_resources

from .client import SJM
from .exceptions import SJMError, SJMAuthenticationError, SJMRateLimitError

console = Console()

# Get version from package metadata
try:
    __version__ = pkg_resources.get_distribution("sjm").version
except pkg_resources.DistributionNotFound:
    __version__ = "1.0.0"  # Default version if not installed as package

# Environment variable for API key
ENV_API_KEY = "SJM_API_KEY"

def get_api_key(api_key: Optional[str]) -> str:
    """Get API key from argument or environment variable"""
    if api_key:
        return api_key
    
    env_api_key = os.environ.get(ENV_API_KEY)
    if env_api_key:
        return env_api_key
    
    console.print(f"[bold red]Error:[/] No API key provided. Please provide an API key with --api-key or set the {ENV_API_KEY} environment variable.")
    sys.exit(1)

@click.group()
@click.version_option(version=__version__, prog_name="SJM")
@click.option("--api-key", "-k", help=f"SJM API key (can also be set via {ENV_API_KEY} environment variable)")
@click.pass_context
def cli(ctx: click.Context, api_key: Optional[str], base_url: str) -> None:
    """
    SJM AI Client - Access the SJM AI platform from the command line
    
    Use this tool to interact with SJM's AI services for freelancer matching,
    skill verification, and AI-powered interviews.
    """
    # Store configuration for subcommands
    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url
    ctx.obj["api_key"] = api_key  # Will be resolved in subcommands

@cli.command()
@click.pass_context
def health(ctx: click.Context) -> None:
    """Check the health status of the SJM API"""
    api_key = get_api_key(ctx.obj["api_key"])
    client = SJM(api_key=api_key, base_url=ctx.obj["base_url"])
    
    with console.status("[bold blue]Checking API health...[/]"):
        try:
            result = client.health()
            
            # Create a nice table display
            table = Table(title="SJM API Health Status", box=box.ROUNDED)
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Details", style="yellow")
            
            # Add overall status
            status_color = "green" if result["status"] == "healthy" else "red"
            table.add_row(
                "Overall", 
                f"[{status_color}]{result['status']}[/{status_color}]",
                ""
            )
            
            # Add component statuses
            if "components" in result:
                for component, details in result["components"].items():
                    component_status = details.get("status", "unknown")
                    status_color = "green" if component_status == "healthy" or component_status == "ready" else "red"
                    
                    # Format details
                    details_str = ""
                    for k, v in details.items():
                        if k != "status":
                            details_str += f"{k}: {v}, "
                    if details_str:
                        details_str = details_str[:-2]  # Remove trailing comma and space
                    
                    table.add_row(
                        component.replace("_", " ").title(),
                        f"[{status_color}]{component_status}[/{status_color}]",
                        details_str
                    )
            
            console.print(table)
            
        except SJMError as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
            sys.exit(1)

@cli.command()
@click.option("--description", "-d", required=True, help="Project description")
@click.option("--skills", "-s", required=True, help="Comma-separated list of required skills")
@click.option("--budget-min", type=int, default=5000, help="Minimum budget")
@click.option("--budget-max", type=int, default=10000, help="Maximum budget")
@click.option("--complexity", type=click.Choice(["low", "medium", "high"]), default="medium", help="Project complexity")
@click.option("--timeline", type=int, default=30, help="Project timeline in days")
@click.option("--limit", "-l", type=int, default=5, help="Number of matches to display")
@click.option("--output", "-o", type=click.File("w"), help="Output file for JSON results")
@click.pass_context
def match(
    ctx: click.Context,
    description: str,
    skills: str,
    budget_min: int,
    budget_max: int,
    complexity: str,
    timeline: int,
    limit: int,
    output: Optional[click.File]
) -> None:
    """Match freelancers to a project based on provided criteria"""
    api_key = get_api_key(ctx.obj["api_key"])
    client = SJM(api_key=api_key, base_url=ctx.obj["base_url"])
    
    # Parse skills
    skills_list = [s.strip() for s in skills.split(",")]
    
    with console.status(f"[bold blue]Finding freelancers matching project criteria...[/]"):
        try:
            result = client.match(
                description=description,
                required_skills=skills_list,
                budget_range=(budget_min, budget_max),
                complexity=complexity,
                timeline=timeline
            )
            
            if output:
                json.dump(result, output, indent=2)
                console.print(f"[green]Results saved to {output.name}[/]")
            
            # Display matches
            if "matches" in result and result["matches"]:
                matches = result["matches"][:limit]
                
                console.print(Panel(
                    f"[bold green]Found {len(result['matches'])} matches[/] (showing top {min(limit, len(result['matches']))})",
                    title="Match Results", 
                    subtitle=f"Project: {description[:50] + '...' if len(description) > 50 else description}"
                ))
                
                for i, match in enumerate(matches, 1):
                    freelancer = match["freelancer"]
                    score = match["score"]
                    matching_skills = match["matching_skills"]
                    
                    # Create a panel for each match
                    match_details = [
                        f"[bold]ID:[/] {freelancer['id']}",
                        f"[bold]Name:[/] {freelancer['name']}",
                        f"[bold]Job Title:[/] {freelancer['job_title']}",
                        f"[bold]Experience:[/] {freelancer['experience']} years",
                        f"[bold]Rating:[/] {freelancer['rating']}/5.0",
                        f"[bold]Hourly Rate:[/] ${freelancer['hourly_rate']}/hr",
                        f"[bold]Skills:[/] {', '.join(freelancer['skills'][:5])}{'...' if len(freelancer['skills']) > 5 else ''}",
                        f"[bold]Match Score:[/] [green]{score*100:.1f}%[/]",
                        f"[bold]Matching Skills:[/] {matching_skills} of {len(skills_list)}"
                    ]
                    
                    console.print(Panel(
                        "\n".join(match_details),
                        title=f"Match #{i}",
                        border_style="green" if i == 1 else "blue",
                        width=100
                    ))
            else:
                console.print("[yellow]No matches found.[/]")
                
        except SJMError as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
            sys.exit(1)

@cli.command()
@click.argument("skill")
@click.pass_context
def verify(ctx: click.Context, skill: str) -> None:
    """Verify if a skill exists in the SJM database"""
    api_key = get_api_key(ctx.obj["api_key"])
    client = SJM(api_key=api_key, base_url=ctx.obj["base_url"])
    
    with console.status(f"[bold blue]Verifying skill: {skill}...[/]"):
        try:
            result = client.verify_skill(skill)
            
            if "data" in result:
                data = result["data"]
                exists = data.get("exists", False)
                
                if exists:
                    console.print(f"[bold green]✓ Skill Verified:[/] \"{skill}\" is a recognized skill")
                    
                    if "skills" in data and data["skills"]:
                        console.print(f"[bold]Matches:[/] {', '.join(data['skills'])}")
                else:
                    console.print(f"[bold yellow]✗ Skill Not Found:[/] \"{skill}\" is not recognized")
                    
                    if "similar_terms" in data and data["similar_terms"]:
                        console.print(f"[bold]Did you mean:[/] {', '.join(data['similar_terms'])}")
            else:
                console.print("[yellow]Unexpected response format.[/]")
                
        except SJMError as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
            sys.exit(1)

@cli.command()
@click.option("--count", "-c", type=int, default=10, help="Number of freelancers to generate")
@click.option("--output", "-o", type=click.File("w"), help="Output file for JSON results")
@click.pass_context
def generate(ctx: click.Context, count: int, output: Optional[click.File]) -> None:
    """Generate test freelancer data"""
    api_key = get_api_key(ctx.obj["api_key"])
    client = SJM(api_key=api_key, base_url=ctx.obj["base_url"])
    
    with console.status(f"[bold blue]Generating {count} test freelancers...[/]"):
        try:
            result = client.generate_test_data(num_freelancers=count)
            
            if output:
                json.dump(result, output, indent=2)
                console.print(f"[green]Results saved to {output.name}[/]")
            
            # Display summary
            if "data" in result and result["data"]:
                freelancers = result["data"]
                console.print(f"[bold green]Generated {len(freelancers)} test freelancers[/]")
                
                # Create a table with a sample of freelancers
                table = Table(title="Sample Generated Freelancers", box=box.ROUNDED)
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Job Title", style="blue")
                table.add_column("Experience", style="yellow")
                table.add_column("Rating", style="magenta")
                
                for freelancer in freelancers[:5]:  # Show first 5
                    table.add_row(
                        freelancer["id"],
                        freelancer["name"],
                        freelancer["job_title"],
                        str(freelancer["experience"]) + " years",
                        str(freelancer["rating"])
                    )
                
                console.print(table)
                
                if len(freelancers) > 5:
                    console.print(f"[dim]...and {len(freelancers) - 5} more[/]")
            else:
                console.print("[yellow]No data generated.[/]")
                
        except SJMError as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
            sys.exit(1)

def main():
    """Main entry point for the CLI"""
    try:
        cli(obj={})
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
