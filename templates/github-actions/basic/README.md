# Basic GitHub Actions Templates for Lokus

This directory contains basic GitHub Actions workflow templates for integrating Lokus API security and LGPD compliance validation into your CI/CD pipeline.

## Templates Overview

### 🔍 `lokus-basic.yml` - Basic API Validation
**Purpose**: Simple validation of API specifications on push and pull requests.

**Features**:
- Triggers on push/PR to main/develop branches
- Validates YAML/JSON specification files
- Creates default configuration if none exists
- Provides clear success/failure feedback

**Best for**: Teams getting started with API security validation.

### 💬 `lokus-pr.yml` - Pull Request Validation with Comments
**Purpose**: Enhanced PR validation with automated comments.

**Features**:
- Detects API specification changes in PRs
- Posts detailed validation results as PR comments
- JSON output for structured reporting
- Skip validation if no API changes detected

**Best for**: Teams wanting detailed PR feedback and review integration.

### 🚀 `lokus-release.yml` - Release Security Gate
**Purpose**: Strict validation before releases with blocking capability.

**Features**:
- Triggers on releases or manual dispatch
- Strict validation mode for production
- Generates detailed security reports
- Blocks releases if validation fails
- Stores reports as artifacts

**Best for**: Production environments requiring strict security gates.

### 📅 `lokus-scheduled.yml` - Scheduled Compliance Monitoring
**Purpose**: Regular compliance monitoring with automated issue creation.

**Features**:
- Runs on schedule (weekly by default)
- Generates PDF compliance reports
- Creates GitHub issues for compliance failures
- Stores historical compliance data
- Manual execution support

**Best for**: Ongoing compliance monitoring and audit trails.

## Quick Start

### 1. Choose Your Template

Pick the template that best fits your workflow:
- **Simple validation**: Use `lokus-basic.yml`
- **PR integration**: Use `lokus-pr.yml`
- **Release gates**: Use `lokus-release.yml`
- **Compliance monitoring**: Use `lokus-scheduled.yml`

### 2. Copy and Customize

1. Copy your chosen template to `.github/workflows/` in your repository
2. Rename the file (e.g., `lokus-validation.yml`)
3. Update the environment variables:

```yaml
env:
  SPEC_PATH: "your-api-spec.yaml"  # Path to your API specification
  CONFIG_PATH: ".forbidden_keys.yaml"  # Path to your Lokus configuration
  PYTHON_VERSION: "3.11"  # Python version to use
```

### 3. Add Your API Specification

Ensure your API specification file exists at the path specified in `SPEC_PATH`.

### 4. Configure Validation Rules (Optional)

Create a `.forbidden_keys.yaml` file in your repository root, or let the workflow create a default one. See the [configs directory](../../configs/) for examples.

### 5. Commit and Test

Commit the workflow file and test it by:
- Pushing changes (for `lokus-basic.yml`)
- Creating a PR (for `lokus-pr.yml`)
- Creating a release (for `lokus-release.yml`)
- Running manually (for `lokus-scheduled.yml`)

## Environment Variables

All templates support these customizable environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SPEC_PATH` | `api-spec.yaml` | Path to your OpenAPI/Swagger specification |
| `CONFIG_PATH` | `.forbidden_keys.yaml` | Path to your Lokus configuration file |
| `PYTHON_VERSION` | `3.11` | Python version for the workflow |

### Template-Specific Variables

#### Release Template (`lokus-release.yml`)
- `STRICT_MODE`: Enable strict validation (default: `true`)

#### Scheduled Template (`lokus-scheduled.yml`)
- `GENERATE_PDF`: Generate PDF reports (default: `true`)

## Configuration Files

The templates work with Lokus configuration files that define validation rules. If no configuration exists, templates will create a default one.

### Configuration Examples

- **[Basic Config](../../configs/basic-config.yaml)**: Essential security checks
- **[Strict Security](../../configs/strict-security.yaml)**: Comprehensive security validation
- **[LGPD Focused](../../configs/lgpd-focused.yaml)**: Brazilian data protection compliance
- **[Enterprise](../../configs/enterprise.yaml)**: Complete enterprise-grade validation

## Permissions

### Required Permissions

Most templates need minimal permissions:
```yaml
permissions:
  contents: read
```

### Additional Permissions

Some templates require additional permissions:

#### PR Template (`lokus-pr.yml`)
```yaml
permissions:
  contents: read
  pull-requests: write  # For PR comments
```

#### Scheduled Template (`lokus-scheduled.yml`)
```yaml
permissions:
  contents: read
  issues: write  # For creating compliance issues
```

## Customization Tips

### 1. Adjust Trigger Paths
Modify the `paths` filter to match your file structure:
```yaml
on:
  push:
    paths:
      - 'api/**/*.yaml'      # APIs in api/ directory
      - 'specs/**/*.yml'     # Specs in specs/ directory
      - 'openapi.json'       # Specific files
```

### 2. Multiple Specifications
For multiple API specs, modify the validation step:
```yaml
- name: Run Lokus validation
  run: |
    for spec in api/*.yaml; do
      echo "Validating $spec"
      lokus --config "${{ env.CONFIG_PATH }}" "$spec"
    done
```

### 3. Custom Notifications
Add Slack/Teams notifications to any template:
```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    text: "API validation failed!"
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 4. Matrix Testing
Test multiple configurations:
```yaml
strategy:
  matrix:
    config: ['basic-config.yaml', 'strict-security.yaml']
steps:
  - name: Run validation
    run: lokus --config "configs/${{ matrix.config }}" "${{ env.SPEC_PATH }}"
```

## Troubleshooting

### Common Issues

#### 1. Spec File Not Found
```
❌ API specification file not found: api-spec.yaml
```
**Solution**: Update `SPEC_PATH` to point to your actual specification file.

#### 2. Permission Denied
```
Error: Resource not accessible by integration
```
**Solution**: Add required permissions to the workflow:
```yaml
permissions:
  contents: read
  pull-requests: write  # If using PR template
  issues: write         # If using scheduled template
```

#### 3. Validation Fails
```
❌ Lokus validation failed!
```
**Solution**: Review the validation output, fix the identified issues, or update your configuration to allow exceptions.

#### 4. Python/uv Installation Issues
```
Error: Could not find uv
```
**Solution**: The templates use pinned versions of actions. Ensure your repository has access to GitHub Actions marketplace.

### Debug Mode

Enable debug mode by adding this to any template:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## Support

- 📚 [Lokus Documentation](https://github.com/geavenx/lokus)
- 🐛 [Report Issues](https://github.com/geavenx/lokus/issues)
- 💬 [Discussions](https://github.com/geavenx/lokus/discussions)
- 📧 Contact: See repository maintainers

## Contributing

Found an issue or want to improve these templates?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with real projects
5. Submit a pull request

## License

These templates are provided under the same license as the Lokus project. See the main repository for details.