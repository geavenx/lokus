# Lokus CI/CD Templates

Ready-to-use CI/CD templates for integrating Lokus API security and LGPD compliance validation into your development workflow.

## 🚀 Quick Start

1. **Choose a template** from the categories below
2. **Copy** the template to your repository's `.github/workflows/` directory
3. **Customize** the environment variables for your project
4. **Commit** and let Lokus secure your APIs!

## 📁 Template Categories

### [Basic Templates](github-actions/basic/)
Essential workflows for getting started with API security validation.

| Template | Purpose | Best For |
|----------|---------|----------|
| [lokus-basic.yml](github-actions/basic/lokus-basic.yml) | Simple validation on push/PR | Teams starting with API security |
| [lokus-pr.yml](github-actions/basic/lokus-pr.yml) | PR validation with comments | Teams wanting detailed PR feedback |
| [lokus-release.yml](github-actions/basic/lokus-release.yml) | Release security gates | Production release validation |
| [lokus-scheduled.yml](github-actions/basic/lokus-scheduled.yml) | Scheduled compliance monitoring | Ongoing compliance tracking |

### Advanced Templates *(Coming Soon)*
Enhanced workflows for complex scenarios and integrations.

- **lokus-multi-spec.yml**: Validate multiple API specifications
- **lokus-artifacts.yml**: Generate and store detailed reports
- **lokus-docker.yml**: Docker-based validation alternative
- **lokus-matrix.yml**: Matrix testing across configurations

### Specialized Templates *(Coming Soon)*
Purpose-built workflows for specific use cases.

- **lokus-monorepo.yml**: Monorepo with multiple services
- **lokus-compliance.yml**: Compliance-focused reporting
- **lokus-security-gate.yml**: Advanced security gates
- **lokus-notification.yml**: Slack/Teams integration

## ⚙️ Configuration Files

Pre-built configuration files for different security and compliance levels.

| Configuration | Description | Use Case |
|---------------|-------------|----------|
| [basic-config.yaml](configs/basic-config.yaml) | Essential security checks | Development environments |
| [strict-security.yaml](configs/strict-security.yaml) | Comprehensive security validation | Production environments |
| [lgpd-focused.yaml](configs/lgpd-focused.yaml) | Brazilian data protection compliance | LGPD compliance requirements |
| [enterprise.yaml](configs/enterprise.yaml) | Complete enterprise validation | Large organizations |

## 🏃‍♂️ 5-Minute Setup

### For Basic API Validation

1. **Copy the basic template**:
   ```bash
   curl -o .github/workflows/lokus-validation.yml \
     https://raw.githubusercontent.com/geavenx/lokus/main/templates/github-actions/basic/lokus-basic.yml
   ```

2. **Update the file paths** in the workflow:
   ```yaml
   env:
     SPEC_PATH: "path/to/your/api-spec.yaml"
     CONFIG_PATH: ".forbidden_keys.yaml"
   ```

3. **Add a configuration file** (optional):
   ```bash
   curl -o .forbidden_keys.yaml \
     https://raw.githubusercontent.com/geavenx/lokus/main/templates/configs/basic-config.yaml
   ```

4. **Commit and push**:
   ```bash
   git add .github/workflows/lokus-validation.yml .forbidden_keys.yaml
   git commit -m "Add Lokus API security validation"
   git push
   ```

### For PR Integration

Use the [PR template](github-actions/basic/lokus-pr.yml) instead for automatic PR comments and validation.

## 🔧 Customization Guide

### Environment Variables

All templates support these variables:

```yaml
env:
  SPEC_PATH: "api-spec.yaml"           # Your API specification file
  CONFIG_PATH: ".forbidden_keys.yaml"  # Lokus configuration file
  PYTHON_VERSION: "3.11"              # Python version to use
```

### File Path Patterns

Adjust the trigger paths to match your repository structure:

```yaml
on:
  push:
    paths:
      - 'api/**/*.yaml'      # APIs in api/ directory
      - 'specs/**/*.yml'     # Specs in specs/ directory
      - 'openapi.json'       # Single specification file
```

### Multiple Specifications

For repositories with multiple API specifications:

```yaml
- name: Validate all specifications
  run: |
    for spec in api/*.yaml specs/*.yml; do
      echo "🔍 Validating $spec"
      lokus --config "${{ env.CONFIG_PATH }}" "$spec"
    done
```

## 🎯 Use Cases

### Development Teams
- **Start with**: [Basic template](github-actions/basic/lokus-basic.yml) + [Basic config](configs/basic-config.yaml)
- **Goal**: Catch security issues early in development

### DevOps Teams
- **Start with**: [PR template](github-actions/basic/lokus-pr.yml) + [Strict config](configs/strict-security.yaml)
- **Goal**: Integrate security validation into code review process

### Compliance Teams
- **Start with**: [Scheduled template](github-actions/basic/lokus-scheduled.yml) + [LGPD config](configs/lgpd-focused.yaml)
- **Goal**: Monitor ongoing compliance and generate audit reports

### Enterprise Organizations
- **Start with**: [Release template](github-actions/basic/lokus-release.yml) + [Enterprise config](configs/enterprise.yaml)
- **Goal**: Strict security gates for production releases

## 🔍 What Gets Validated

### Security Checks (OWASP API Security Top 10)
- ✅ Broken Object Level Authorization (BOLA)
- ✅ Broken Authentication
- ✅ Broken Object Property Level Authorization (BOPLA)
- ✅ Unrestricted Resource Consumption
- ✅ Broken Function Level Authorization (BFLA)

### LGPD Compliance
- ✅ Sensitive data detection (CPF, CNPJ, RG, email, phone)
- ✅ Data minimization validation
- ✅ Purpose limitation checks
- ✅ Direct identifier protection

### Configuration-Based Rules
- ✅ Forbidden keys and patterns
- ✅ Path-specific restrictions
- ✅ Allowed exceptions
- ✅ Custom validation rules

## 📊 Output Formats

Templates support multiple output formats:

- **Console**: Human-readable text output
- **JSON**: Structured data for programmatic processing
- **PDF**: Professional reports for compliance documentation

## 🚨 Integration Examples

### Slack Notifications
```yaml
- name: Notify Slack on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    text: "🚨 API validation failed in ${{ github.repository }}"
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Teams Notifications
```yaml
- name: Notify Teams
  if: always()
  uses: toko-bifrost/ms-teams-deploy-card@master
  with:
    github-token: ${{ github.token }}
    webhook-uri: ${{ secrets.TEAMS_WEBHOOK }}
```

### Email Reports
```yaml
- name: Email compliance report
  if: steps.lokus-validation.outputs.validation == 'failure'
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "API Compliance Report - ${{ github.repository }}"
    body: "See attached compliance report."
    attachments: "compliance-report.pdf"
```

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| File not found | Update `SPEC_PATH` to correct file location |
| Permission denied | Add required permissions to workflow |
| Validation fails | Review output and fix issues or update config |
| Python/uv issues | Check GitHub Actions marketplace access |

### Getting Help

- 📚 [Lokus Documentation](https://github.com/geavenx/lokus)
- 🐛 [Report Issues](https://github.com/geavenx/lokus/issues)
- 💬 [GitHub Discussions](https://github.com/geavenx/lokus/discussions)
- 📧 [Contact Maintainers](https://github.com/geavenx/lokus#maintainers)

## 📈 Roadmap

### Phase 1 ✅ (Current)
- [x] Basic GitHub Actions templates
- [x] Configuration examples
- [x] Documentation and setup guides

### Phase 2 🚧 (In Progress)
- [ ] Advanced templates (multi-spec, artifacts, docker)
- [ ] Specialized templates (monorepo, compliance, notifications)
- [ ] Integration examples and tutorials

### Phase 3 📅 (Planned)
- [ ] Jenkins and GitLab CI templates
- [ ] Pre-commit hooks
- [ ] IDE integrations
- [ ] Web-based configuration builder

## 🤝 Contributing

We welcome contributions to improve these templates!

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch
3. **Add** or improve templates
4. **Test** with real projects
5. **Document** your changes
6. **Submit** a pull request

### Template Guidelines
- Include comprehensive error handling
- Support multiple environments
- Provide clear documentation
- Follow security best practices
- Test with various repository structures

## 📄 License

These templates are provided under the MIT License. See the [LICENSE](../LICENSE) file for details.

---

**Made with ❤️ by the Lokus team**

*Securing APIs, one specification at a time.*