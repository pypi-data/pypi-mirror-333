#!/usr/bin/env python3
import argparse
from pathlib import Path
from .core import count_tokens_in_folder, get_available_models


def main():
    """Command-line interface for tokencount."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Count tokens in files using tiktoken.')
    parser.add_argument('folder', type=str, help='Path to the folder to process')
    parser.add_argument('--encoding', type=str, default='cl100k_base',
                        help='Tiktoken encoding to use (default: cl100k_base)')
    parser.add_argument('--ignore-gitignore', action='store_true',
                        help='Ignore .gitignore file even if it exists')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress progress output, only show summary')
    args = parser.parse_args()
    
    folder_path = Path(args.folder).resolve()
    
    if not folder_path.is_dir():
        print(f"Error: {folder_path} is not a valid directory")
        return
    
    print(f"Counting tokens in {folder_path} using {args.encoding} encoding...")
    
    # Run the token counter
    results = count_tokens_in_folder(
        folder_path, 
        args.encoding,
        verbose=not args.quiet
    )
    
    # Print summary
    print("\nSummary:")
    print(f"Total tokens: {results['total_tokens']}")
    print(f"Files processed: {results['processed_files']}")
    print(f"Files with errors: {results['errors']}")
    print(f"Files skipped (gitignore): {results['skipped_files']}")
    print(f"Files skipped (.git): {results['git_files_skipped']}")
    
    # Print cost estimates
    if results['total_tokens'] > 0:
        print("\nEstimated costs:")
        for model, cost in results['cost_estimates'].items():
            # Format cost with appropriate precision based on magnitude
            if cost < 0.01:
                cost_str = f"${cost:.6f}"
            elif cost < 1:
                cost_str = f"${cost:.4f}"
            else:
                cost_str = f"${cost:.2f}"
                
            print(f"{model}: {cost_str}")


if __name__ == "__main__":
    main()
