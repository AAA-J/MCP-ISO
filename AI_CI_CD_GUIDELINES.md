# AI CI/CD Guidelines

**⚠️ IMPORTANT: AI assistants working on this repository MUST read and follow these CI/CD guidelines for every task.**

This file serves as a continuous integration/continuous deployment checklist to ensure consistency, quality, and proper maintenance of the MCP-ISO repository and all MCP servers within it. Think of this as your automated quality gate that must pass before any work is considered complete.

---

## 📋 Pre-Task Checklist

Before starting any work, ensure you:

- [ ] Read this file completely
- [ ] Understand the task requirements
- [ ] Check existing code patterns and structure
- [ ] Review related documentation

---

## 🔢 Version Tracking (REQUIRED)

### Version Format
- Use [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Where to Track Versions

1. **Python MCP Servers** (`mcp-servers/*/src/`):
   - Add `__version__ = "X.Y.Z"` to the main `index.py` file
   - Include version in server initialization: `Server("server-name", version="X.Y.Z")`
   - Update version when making changes

2. **Git Tags**:
   - Create version tags for releases: `git tag -a v1.2.3 -m "Release version 1.2.3"`
   - Tag both individual servers and repository milestones

3. **Documentation**:
   - Update version in README.md files
   - Include version in changelog/update notes

4. **Requirements Files**:
   - Pin dependency versions in `requirements.txt` when stable
   - Document version ranges for flexibility

### Version Update Rules

- **Always increment version** when:
  - Adding new features → MINOR version
  - Fixing bugs → PATCH version
  - Breaking changes → MAJOR version
  - Updating dependencies significantly → MINOR or PATCH

- **Version Check Commands**:
  ```bash
  # Check current version in code
  grep -r "__version__" mcp-servers/*/src/
  
  # Check Git tags
  git tag -l
  
  # Check latest commit
  git log -1 --oneline
  ```

---

## 📝 Code Quality Standards

### Python Code

- [ ] Follow PEP 8 style guidelines
- [ ] Use type hints where appropriate
- [ ] Add docstrings to all functions and classes
- [ ] Keep functions focused and single-purpose
- [ ] Handle errors gracefully with try/except blocks
- [ ] Use meaningful variable and function names

### MCP Server Structure

- [ ] Each tool module in its own directory with `__init__.py`
- [ ] Tools organized by functionality
- [ ] Consistent naming: `tool_name_tools` for lists, `handle_tool_name` for handlers
- [ ] All tools properly registered in main `index.py`

### Error Handling

- [ ] Validate all inputs
- [ ] Return clear error messages
- [ ] Log errors appropriately
- [ ] Don't expose sensitive information in errors

---

## 📚 Documentation Requirements

### Required Documentation Updates

When making changes, update:

1. **README.md** (server-specific):
   - [ ] Feature list
   - [ ] Installation instructions
   - [ ] Usage examples
   - [ ] Version number

2. **SETUP.md** (repository-level):
   - [ ] Installation steps
   - [ ] Configuration examples
   - [ ] Troubleshooting section

3. **Code Documentation**:
   - [ ] Function docstrings
   - [ ] Module-level documentation
   - [ ] Inline comments for complex logic

4. **Examples**:
   - [ ] Update or add examples for new features
   - [ ] Ensure examples are working and tested

### Documentation Format

- Use Markdown for all documentation
- Include code examples with syntax highlighting
- Add links to relevant resources
- Keep documentation up-to-date with code changes

---

## 🧪 Testing Requirements

### Before Committing

- [ ] Test server starts without errors: `python src/index.py`
- [ ] Verify tools are callable and return expected results
- [ ] Check for import errors
- [ ] Validate JSON-RPC compliance
- [ ] Test error handling paths

### Test Checklist

- [ ] Server initializes correctly
- [ ] All tools are listed
- [ ] Tool calls work with valid inputs
- [ ] Error handling works with invalid inputs
- [ ] Resources can be read
- [ ] No console errors or warnings

---

## 🔄 Git & Version Control

### Commit Messages

Use clear, descriptive commit messages:

```
Format: <type>: <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- refactor: Code refactoring
- test: Test additions/changes
- chore: Maintenance tasks
- version: Version bump

Examples:
- feat: Add version tracking to dev-mcp-server
- fix: Resolve import error in discord-mcp-server
- docs: Update SETUP.md with IDE installation guide
- version: Bump dev-mcp-server to v1.1.0
```

### Branch Strategy

- Use descriptive branch names: `feature/version-tracking`, `fix/import-error`
- Keep commits focused and atomic
- Test before merging to main

### Before Pushing

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] No sensitive data committed
- [ ] Commit messages are clear

---

## 🏗️ MCP Server Development

### Adding New Tools

When adding a new tool:

1. [ ] Create tool definition in appropriate module
2. [ ] Implement handler function
3. [ ] Register tool in main `index.py`
4. [ ] Add to module's tool list
5. [ ] Update documentation
6. [ ] Add example usage
7. [ ] Test the tool
8. [ ] Update version (MINOR increment)

### Adding New Servers

When adding a new MCP server:

1. [ ] Create directory structure: `mcp-servers/<server-name>/`
2. [ ] Add `src/` with `index.py` and tool modules
3. [ ] Create `requirements.txt`
4. [ ] Add `README.md` with full documentation
5. [ ] Add to repository README.md
6. [ ] Update SETUP.md with installation instructions
7. [ ] Set initial version: `__version__ = "0.1.0"`
8. [ ] Test installation and functionality

### Server Initialization

Every MCP server should:

- [ ] Include version in server initialization
- [ ] Have proper error handling
- [ ] Log important events (to stderr for stdio)
- [ ] Validate configuration on startup
- [ ] Provide clear error messages

---

## 🔍 Code Review Checklist

Before considering work complete:

- [ ] Code follows style guidelines
- [ ] All functions have docstrings
- [ ] Error handling is comprehensive
- [ ] No hardcoded values (use config/env vars)
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Version numbers updated
- [ ] Documentation updated
- [ ] Examples updated/tested
- [ ] Git commits are clean and descriptive

---

## 🚨 Common Pitfalls to Avoid

- ❌ **Don't** skip version updates
- ❌ **Don't** commit without testing
- ❌ **Don't** leave TODO comments without context
- ❌ **Don't** break existing functionality
- ❌ **Don't** expose sensitive information
- ❌ **Don't** ignore error handling
- ❌ **Don't** forget to update documentation
- ❌ **Don't** use vague commit messages

---

## 📦 Dependency Management

### Adding Dependencies

- [ ] Add to appropriate `requirements.txt`
- [ ] Pin version if stable: `package==1.2.3`
- [ ] Use version range if needed: `package>=1.2.0,<2.0.0`
- [ ] Document why dependency is needed
- [ ] Update version (PATCH for bug fixes, MINOR for new features)

### Updating Dependencies

- [ ] Test thoroughly after updates
- [ ] Check for breaking changes
- [ ] Update version appropriately
- [ ] Document any required changes

---

## 🔐 Security Considerations

- [ ] Never commit API keys, tokens, or secrets
- [ ] Use environment variables for sensitive data
- [ ] Validate all user inputs
- [ ] Sanitize outputs when necessary
- [ ] Keep dependencies up-to-date for security patches
- [ ] Review third-party code before including

---

## 📊 CI/CD Workflow

When working on tasks, follow this CI/CD-like workflow:

1. **Pre-commit Checks**:
   - [ ] Read this file and understand requirements
   - [ ] Plan task breakdown
   - [ ] Check existing patterns

2. **Development Phase**:
   - [ ] Implement following all guidelines
   - [ ] Write/update tests
   - [ ] Update documentation

3. **Quality Gates** (Must pass all):
   - [ ] Code quality standards met
   - [ ] All tests pass
   - [ ] Documentation updated
   - [ ] Version numbers updated
   - [ ] No security issues

4. **Pre-deploy Checks**:
   - [ ] Self-review against checklist
   - [ ] Verify Git commits are clean
   - [ ] Ensure no sensitive data

5. **Deploy/Commit**:
   - [ ] Clear commit messages
   - [ ] All checks passed
   - [ ] Ready for integration

---

## 🎯 Quick Reference

### Version Update Command
```bash
# Find all version references
grep -r "__version__" mcp-servers/*/src/

# Update version in file
# Then commit with: git commit -m "version: Bump to vX.Y.Z"
```

### Test Server
```bash
cd mcp-servers/<server-name>
source venv/bin/activate
python src/index.py
```

### Check Documentation
```bash
# Verify all READMEs exist
find mcp-servers -name "README.md"

# Check for broken links (if tool available)
# markdown-link-check README.md
```

---

## 📞 Questions?

If unsure about any guideline:

1. Check existing code for patterns
2. Review similar implementations
3. Consult MCP specification: https://modelcontextprotocol.io
4. Ask for clarification before proceeding

---

**Last Updated**: 2024-12-19
**Version**: 1.0.0

---

*This CI/CD checklist must be read and followed at the start of every AI-assisted development session. All quality gates must pass before work is considered complete.*

