import subprocess
import os
import sys
import logging

logger = logging.getLogger(__name__)

class ScriptExecutor:
    def __init__(self, python_path: str, skills_dir: str):
        self.skills_dir = skills_dir
        
        # Resolve the actual python executable
        if os.path.isfile(python_path):
            self.python_exe = python_path
        else:
            # Assume it's a venv directory
            # Support both Unix (bin) and Windows (Scripts)
            bin_path = os.path.join(python_path, "bin", "python")
            if not os.path.exists(bin_path):
                # Fallback for Windows or common alternative structures
                bin_path = os.path.join(python_path, "Scripts", "python.exe")
                if not os.path.exists(bin_path):
                    # Second fallback: check if python is in the folder directly
                    bin_path = os.path.join(python_path, "python")
            
            self.python_exe = bin_path if os.path.exists(bin_path) else python_path
            
        logger.info(f"ScriptExecutor initialized with Python: {self.python_exe}")

    def run_skill(self, skill_name: str, args: list = None) -> str:
        """
        Runs a skill's main script.
        Assumes the skill is in a folder: skills_dir/skill_name/script.py
        """
        script_path = os.path.join(self.skills_dir, skill_name, "script.py")
        
        if not os.path.exists(script_path):
            return f"Error: Skill script not found at {script_path}"

        cmd = [self.python_exe, script_path]
        if args:
            cmd.extend(args)

        try:
            # Add the current project directory to PYTHONPATH so scripts can import google_drive_mcp
            env = os.environ.copy()
            # __file__ is inside google_drive_mcp/, so go up one level to get the package root
            package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Ensure the skills can find the modules by importing 'google_drive_mcp'
            current_pythonpath = env.get("PYTHONPATH", "")
            if current_pythonpath:
                env["PYTHONPATH"] = f"{package_root}{os.pathsep}{current_pythonpath}"
            else:
                env["PYTHONPATH"] = package_root

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                env=env,
                cwd=mcp_root
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n--- Errors/Warnings ---\n{result.stderr}"
            
            return output if output.strip() else "Script executed successfully with no output."

        except Exception as e:
            return f"Failed to execute skill: {str(e)}"
