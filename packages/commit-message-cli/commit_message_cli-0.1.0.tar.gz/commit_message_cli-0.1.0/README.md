# Commit Message CLI

A command-line tool to generate commit messages using AI.

## Configuration

The tool can be configured in two ways:

### 1. Environment Variables

Set the following environment variables to configure the tool:

```bash
export SMOOTHDEV_AUTH0_DOMAIN="your-domain"
export SMOOTHDEV_AUTH0_CLIENT_ID="your-client-id"
export SMOOTHDEV_AUTH0_AUDIENCE="your-audience"
export SMOOTHDEV_REDIRECT_URI="your-redirect-uri"
```

### 2. Configuration File

You can create a configuration file at `~/.smoothdevio/config.json`. A template is provided in `config.template.json`:

1. Create your configuration directory:
```bash
mkdir -p ~/.smoothdevio
```

2. Copy the template:
```bash
cp config.template.json ~/.smoothdevio/config.json
```

3. Edit the configuration file with your settings:
```json
{
    "aws_profile": "default",
    "aws_region": "us-east-1",
    "auth0_domain": "your-domain",
    "auth0_audience": "your-audience",
    "redirect_uri": "your-redirect-uri"
}
```

Note: Environment variables take precedence over the configuration file.

## Installation

### Using pip
```bash
pip install commit-message-cli
```

### Using Homebrew
```bash
brew install commit-message-cli
```

## Usage

```bash
generate-commit-message [options]
```

For more details on usage and options, run:
```bash
generate-commit-message --help