# Quickstart: Rename Skill to 'Conversation'

**Feature**: 003-rename-skill-conversation  
**Date**: 2026-03-10  
**Estimated Time**: 5-10 minutes

## Prerequisites

- Access to repository: `whatsapp-audio-sender`
- Text editor or IDE
- Git (for committing changes)

## Step-by-Step Instructions

### Step 1: Backup Current SKILL.md

```powershell
# Create a backup of the current file
Copy-Item SKILL.md SKILL.md.backup
```

**Verification**: Confirm `SKILL.md.backup` exists in repository root.

### Step 2: Update YAML Frontmatter

Open `SKILL.md` and locate the YAML frontmatter (lines 1-4):

**Before**:
```yaml
---
name: whatsapp-audio-sender
description: Sends text-to-speech (TTS) audio to WhatsApp, ensuring compatibility with OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp.
---
```

**After**:
```yaml
---
name: conversation
description: Enables conversation with users via WhatsApp by sending text-to-speech (TTS) audio messages in OGG (Opus) format. Use to send text-generated audio messages directly to the user's WhatsApp.
---
```

**Changes**:
- Line 2: `whatsapp-audio-sender` → `conversation`
- Line 3: Updated description to emphasize conversation capability

### Step 3: Update Title (H1 Heading)

Locate line 6 (the main heading):

**Before**:
```markdown
# WhatsApp Audio Sender
```

**After**:
```markdown
# Conversation
```

### Step 4: Update Overview Paragraph

Locate line 8 (the overview paragraph):

**Before**:
```markdown
This skill automates the process of sending text-generated audio messages to the user's WhatsApp, ensuring the format is compatible (OGG with Opus codec).
```

**After**:
```markdown
This skill enables conversation with users by automating the process of sending text-generated audio messages to the user's WhatsApp, ensuring the format is compatible (OGG with Opus codec).
```

**Change**: Add "enables conversation with users by" before "automating"

### Step 5: Verify Agent Workflow Section Unchanged

**CRITICAL**: Verify that lines 10-32 (the entire `## Agent Workflow` section) remain **completely unchanged**.

This section contains:
- Workflow steps
- Python code examples
- API calls to `tts`, `exec`, `message`
- File paths and dependencies

**Verification Command**:
```powershell
# Compare workflow section (lines 10-32) with backup
Get-Content SKILL.md -TotalCount 32 | Select-Object -Skip 9 | Out-File temp_workflow.txt
Get-Content SKILL.md.backup -TotalCount 32 | Select-Object -Skip 9 | Out-File temp_workflow_backup.txt
Compare-Object (Get-Content temp_workflow.txt) (Get-Content temp_workflow_backup.txt)
# Should return no differences
Remove-Item temp_workflow.txt, temp_workflow_backup.txt
```

### Step 6: Validate Changes

Run validation checks:

```powershell
# Check 1: Verify new name is present
Select-String -Path SKILL.md -Pattern "^name: conversation$"
# Expected: Match on line 2

# Check 2: Verify old name is gone from frontmatter
Select-String -Path SKILL.md -Pattern "^name: whatsapp-audio-sender$"
# Expected: No matches

# Check 3: Verify description updated
Select-String -Path SKILL.md -Pattern "Enables conversation with users via WhatsApp"
# Expected: Match on line 3

# Check 4: Verify workflow preserved
Select-String -Path SKILL.md -Pattern "## Agent Workflow"
# Expected: Match on line 10
```

### Step 7: Review Full File

Perform a final visual review of `SKILL.md`:

**Checklist**:
- [ ] Line 2: `name: conversation`
- [ ] Line 3: Description mentions "Enables conversation with users"
- [ ] Line 6: `# Conversation`
- [ ] Line 8: Overview mentions "enables conversation with users by"
- [ ] Lines 10-32: Agent Workflow section unchanged
- [ ] No syntax errors in YAML frontmatter
- [ ] No broken markdown formatting

### Step 8: Commit Changes

```powershell
# Stage the changes
git add SKILL.md

# Commit with descriptive message
git commit -m "Rename skill from 'whatsapp-audio-sender' to 'conversation'

- Update name field in YAML frontmatter
- Update description to emphasize conversation capability
- Update title and overview paragraph
- Preserve Agent Workflow section unchanged

Refs: 003-rename-skill-conversation"

# Push to remote
git push origin 003-rename-skill-conversation
```

### Step 9: Cleanup

```powershell
# Remove backup file
Remove-Item SKILL.md.backup
```

## Verification

After completing all steps, verify the rename was successful:

```powershell
# Search for any remaining references to old name (excluding specs)
Get-ChildItem -Path . -Recurse -Include *.md -Exclude specs | Select-String "whatsapp-audio-sender"
# Expected: No matches (specs intentionally excluded)
```

## Rollback Procedure

If issues arise, rollback using the backup:

```powershell
# Restore from backup
Copy-Item SKILL.md.backup SKILL.md -Force

# Or revert the git commit
git revert HEAD
git push origin 003-rename-skill-conversation
```

## Expected Outcome

After completion:
- ✅ SKILL.md has `name: conversation`
- ✅ Description emphasizes conversation capability
- ✅ Title and overview updated
- ✅ Agent Workflow section unchanged
- ✅ No functional regressions
- ✅ Changes committed to git

## Troubleshooting

### Issue: YAML Syntax Error

**Symptom**: File doesn't parse correctly  
**Solution**: Ensure YAML frontmatter has exactly 3 dashes on lines 1 and 4, with no extra spaces

### Issue: Workflow Section Modified

**Symptom**: Validation shows differences in workflow section  
**Solution**: Restore from backup and carefully re-apply only identity changes

### Issue: Git Merge Conflicts

**Symptom**: Cannot push due to conflicts  
**Solution**: Pull latest changes, resolve conflicts preserving your rename, then push

## Next Steps

After successful rename:
1. Update any external documentation referencing the old skill name
2. Notify team members of the name change
3. Monitor for any integration issues with systems using the skill
4. Consider updating repository name if desired (separate task)

## Time Estimates

- Backup and edit: 2-3 minutes
- Validation: 2-3 minutes
- Commit and push: 1-2 minutes
- **Total**: 5-10 minutes
