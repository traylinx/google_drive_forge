import os
import yaml
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class SkillMetadata:
    def __init__(self, name: str, description: str, folder_path: str):
        self.name = name
        self.description = description
        self.folder_path = folder_path

class SkillLoader:
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir

    def discover_skills(self) -> List[SkillMetadata]:
        """
        Scans the skills directory for valid skill folders (containing SKILL.md).
        """
        skills = []
        if not os.path.exists(self.skills_dir):
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return skills

        for entry in os.scandir(self.skills_dir):
            if entry.is_dir():
                skill_md_path = os.path.join(entry.path, "SKILL.md")
                if os.path.exists(skill_md_path):
                    try:
                        meta = self._parse_skill_md(skill_md_path, entry.path)
                        if meta:
                            skills.append(meta)
                    except Exception as e:
                        logger.error(f"Error parsing {skill_md_path}: {e}")
        
        return skills

    def _parse_skill_md(self, file_path: str, folder_path: str) -> Optional[SkillMetadata]:
        """
        Parses the YAML frontmatter from a SKILL.md file.
        """
        with open(file_path, "r") as f:
            content = f.read()
        
        if not content.startswith("---"):
            return None

        # Basic YAML frontmatter extraction
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        
        try:
            frontmatter = yaml.safe_load(parts[1])
            name = frontmatter.get("name")
            description = frontmatter.get("description")
            
            if name and description:
                return SkillMetadata(name, description, folder_path)
        except Exception:
            return None
            
        return None
