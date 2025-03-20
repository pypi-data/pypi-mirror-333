# Snowpack Stack

`snowpack_stack` is Snowpack Data's internal AI-enhanced automations for comprehensive, robust, and highly automated Data stack deployments.

## Installation Guide

### Prerequisites

- Python 3.11 or higher

### Simple Installation

Install Snowpack Stack directly with pip:

```bash
pip install snowpack_stack
```

That's it! Snowpack Stack is now installed and ready to use.

### Verifying Installation

You can verify your installation by running:

```bash
snowpack setup verify
```

### Setting User Information (Optional)

You can optionally set your email for identification and usage tracking:

```bash
snowpack setup auth --email your.email@example.com
```

## Basic Usage Example

After installing, you can start using Snowpack Stack to generate assets:

```python
import snowpack_stack

# Optional: set your email for identification
# snowpack_stack.set_user_email("your.email@example.com")

# Generate YAML assets for database tables
yaml_results = snowpack_stack.generate_yaml_assets()
print(f"Generated {len(yaml_results)} YAML assets")

# Generate SQL transformation assets
sql_results = snowpack_stack.generate_sql_assets()
print(f"Generated {len(sql_results)} SQL assets")

# Or run all generators at once
all_results = snowpack_stack.run_all()
print(f"Generated {len(all_results)} total assets")
```

## Command-Line Interface

Snowpack Stack provides a CLI for building assets and setting up the environment.

### Public Commands

The following commands are available to all users:

### Build Commands

Build commands are used to generate assets:

```bash
# Build all assets
snowpack build

# Build only Bruin assets
snowpack build bruin

# Build only Bruin YAML assets
snowpack build bruin yaml

# Build only Bruin SQL assets
snowpack build bruin sql
```

### Setup Commands

Setup commands are used to configure the environment:

```bash
# Run the complete setup process (optional)
snowpack setup

# Set your email for identification (optional)
snowpack setup auth --email your.email@example.com

# Run verification to check installation
snowpack setup verify

# Verify internal developer access
snowpack setup verify-internal
```

## Output Files

The system generates files in the following location:

```
{parent_directory}/bruin-pipeline/assets/
```

Where `{parent_directory}` is typically the parent of the `snowpack_stack_product` directory.

### YAML Asset Files

YAML asset files (`raw_{table}.asset.yml`) are generated for each source table. These files contain:

- Table metadata (name, owner, description)
- Ingestion settings (source connection, source table)
- Column definitions with data types
- Primary key and constraint information

### SQL Asset Files

SQL transformation files (`{table}.sql`) are generated for each source table. These files contain:

- A YAML metadata block inside `@bruin` tags
- A SQL query that selects from the raw table
- Filtering to exclude deleted records

## High-Level Architecture

Snowpack Stack follows a modular, layered approach:

- **Core Layer**: Handles configuration loading, validation, and common utilities
- **Generator Layer**: Contains the implementation logic for creating different asset types
- **CLI Layer**: Provides command-line interfaces for executing generators
- **Authentication Layer**: Manages email-based authorization for package usage
- **Utilities**: Common tools for database connections, logging, etc.

## Key Features

### 1. YAML Asset Generation
- Generates Bruin-compatible YAML asset files for raw tables
- Supports automatic schema and table discovery
- Configures proper data types and column metadata

### 2. SQL Asset Generation
- Creates Bruin-compatible SQL transformation files
- Implements the `@bruin` metadata block format
- Generates simple SQL queries for cleaned data access

### 3. Environment Management
- Supports environment variables for secure credential management
- Flexible configuration with parent directory discovery
- Symbolic link support for shared environment files

## Authentication

Snowpack Stack uses basic authentication for identifying users:

### User Authentication

The easiest way to set up authentication is with the built-in verification command:

```bash
snowpack setup verify
```

This command will guide you through the authentication process and verify your installation.

You can also use the dedicated authentication command:

```bash
snowpack setup auth --email your.email@example.com
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**:
   - Check if your email is valid
   - Ensure you've called `set_user_email()` before using generators
   - Check if the environment variable `SNOWPACK_USER_EMAIL` is set correctly

2. **Environment Variables Not Found**:
   - Ensure your `.env` file is in the correct location
   - Check if there are multiple `.env` files causing conflicts
   - For parent directory setup, verify the symbolic link exists

3. **Database Connection Issues**:
   - Verify database credentials in your `.env` file
   - Check network connectivity to the database server
   - Ensure the database server is running

4. **Output Files Not Generated**:
   - Check the log output for errors
   - Verify the `bruin-pipeline/assets` directory exists in the parent directory
   - Ensure the user running the command has write permissions

## Internal Features

Some advanced features of Snowpack Stack, such as release management, are restricted to Snowpack developers. If you need access to these features, please contact the Snowpack team. 