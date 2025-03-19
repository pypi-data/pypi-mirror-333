#!/usr/bin/env python3
import os
import tiktoken
import fnmatch
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple


def count_tokens_in_file(file_path, encoding_name="cl100k_base"):
    """Count the number of tokens in a file using the specified encoding."""
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get the encoding
        encoding = tiktoken.get_encoding(encoding_name)
        
        # Count tokens
        tokens = encoding.encode(content)
        return len(tokens)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0


def parse_gitignore(gitignore_path):
    """Parse .gitignore file and return a list of patterns to ignore."""
    if not os.path.exists(gitignore_path):
        return []
    
    patterns = []
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns


def is_ignored(file_path, ignore_patterns, base_dir):
    """Check if a file should be ignored based on gitignore patterns."""
    if not ignore_patterns:
        return False
    
    # Convert to relative path from the base directory
    rel_path = os.path.relpath(file_path, base_dir)
    
    for pattern in ignore_patterns:
        # Handle negation patterns (those starting with !)
        negated = pattern.startswith('!')
        if negated:
            pattern = pattern[1:]
        
        # Handle directory-specific patterns (those ending with /)
        dir_only = pattern.endswith('/')
        if dir_only:
            pattern = pattern[:-1]
            if os.path.isdir(file_path) and fnmatch.fnmatch(rel_path, pattern):
                return not negated
            continue
        
        # Handle patterns with wildcards
        if fnmatch.fnmatch(rel_path, pattern):
            return not negated
        
        # Handle directory patterns (e.g., **/node_modules/)
        parts = rel_path.split(os.sep)
        for i in range(len(parts)):
            subpath = os.path.join(*parts[:i+1]) if i > 0 else parts[0]
            if fnmatch.fnmatch(subpath, pattern):
                return not negated
    
    return False


# Model pricing in USD per million tokens
MODEL_PRICING = {
    "gpt-4o": 10.0,  # $10 per million tokens
    "claude-3-7-sonnet": 15.0,  # $15 per million tokens
    # Add more models as needed
}


def estimate_cost(tokens: int, model: str) -> float:
    """Estimate the cost of processing tokens with a specific model.
    
    Args:
        tokens: Number of tokens
        model: Model name (must be in MODEL_PRICING)
        
    Returns:
        Estimated cost in USD
    """
    if model not in MODEL_PRICING:
        raise ValueError(f"Unknown model: {model}. Available models: {', '.join(MODEL_PRICING.keys())}")
    
    # Convert to millions and multiply by cost per million
    return (tokens / 1_000_000) * MODEL_PRICING[model]


def get_available_models() -> List[str]:
    """Get a list of available models for cost estimation."""
    return list(MODEL_PRICING.keys())


def count_tokens_in_folder(folder_path, encoding_name="cl100k_base", verbose=True):
    """Count tokens in all files within a folder and its subfolders."""
    total_tokens = 0
    processed_files = 0
    errors = 0
    skipped_files = 0
    git_files_skipped = 0
    
    # Parse .gitignore if it exists
    gitignore_path = os.path.join(folder_path, '.gitignore')
    ignore_patterns = parse_gitignore(gitignore_path)
    if ignore_patterns and verbose:
        print(f"Found .gitignore with {len(ignore_patterns)} patterns. Will ignore matching files.")
    
    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        # Always skip .git directories
        if '.git' in dirs:
            try:
                git_files_skipped += len(os.listdir(os.path.join(root, '.git')))
                if verbose:
                    print(f"Skipping .git directory: {os.path.join(root, '.git')}")
            except:
                pass
            dirs.remove('.git')
        
        # Remove ignored directories to avoid traversing them
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignore_patterns, folder_path)]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip ignored files
            if is_ignored(file_path, ignore_patterns, folder_path):
                skipped_files += 1
                if verbose:
                    print(f"Ignored (gitignore): {file_path}")
                continue
            
            # Skip binary files and other non-text files
            if os.path.isfile(file_path):
                try:
                    token_count = count_tokens_in_file(file_path, encoding_name)
                    total_tokens += token_count
                    processed_files += 1
                    if verbose:
                        print(f"Processed: {file_path} - {token_count} tokens")
                except Exception as e:
                    errors += 1
                    if verbose:
                        print(f"Skipped (error): {file_path} - {str(e)}")
    
    # Calculate cost estimates for each model
    cost_estimates = {}
    for model in MODEL_PRICING:
        cost_estimates[model] = estimate_cost(total_tokens, model)
    
    return {
        "total_tokens": total_tokens,
        "processed_files": processed_files,
        "errors": errors,
        "skipped_files": skipped_files,
        "git_files_skipped": git_files_skipped,
        "cost_estimates": cost_estimates
    }
