"""
Command-line interface for the MindRoot SDK.
"""

import json
import argparse
import sys

from .client import MindRootClient
from .exceptions import MindRootError


def main():
    """Run the MindRoot CLI."""
    parser = argparse.ArgumentParser(description="MindRoot API Command Line Interface")
    parser.add_argument("instructions", help="Instructions for the AI agent")
    parser.add_argument("--agent", default="Assistant", help="Name of the agent (default: Assistant)")
    parser.add_argument("--trace", action="store_true", help="Include full trace in results")
    parser.add_argument("--url", default="http://localhost:8012", help="Base URL of the MindRoot API")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    try:
        # Create client
        client = MindRootClient(base_url=args.url)
        
        # Run task
        result = client.run_task(args.agent, args.instructions, include_trace=args.trace)
        
        # Output as JSON if requested
        if args.json:
            print(json.dumps(result, indent=2))
            return
            
        # Print results
        print("Results:")
        print(result["results"])
        
        if args.trace and "full_results" in result:
            print("\nFull Trace:")
            for cmd in result["full_results"]:
                print(json.dumps(cmd, indent=2))
                
    except MindRootError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
