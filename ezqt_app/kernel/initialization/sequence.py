# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
# EzQt_App - A Modern Qt Application Framework
# ///////////////////////////////////////////////////////////////
#
# Author: EzQt_App Team
# Website: https://github.com/ezqt-app/ezqt_app
#
# This file is part of EzQt_App.
#
# EzQt_App is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EzQt_App is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EzQt_App.  If not, see <https://www.gnu.org/licenses/>.
# ///////////////////////////////////////////////////////////////

"""
Initialization Sequence for EzQt_App
====================================

This module defines the explicit initialization sequence for EzQt_App,
providing maximum visibility into what happens during startup.
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from dataclasses import dataclass
from enum import Enum

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..app_functions.printer import get_printer

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import List, Dict, Any, Optional, Callable

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class StepStatus(Enum):
    """Status of initialization steps."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class InitStep:
    """Represents an initialization step."""

    name: str
    description: str
    function: Callable
    required: bool = True
    status: StepStatus = StepStatus.PENDING
    error_message: Optional[str] = None
    duration: Optional[float] = None


class InitializationSequence:
    """
    Manages the explicit initialization sequence for EzQt_App.

    This class provides maximum visibility into the initialization process
    by defining each step explicitly and tracking their execution.
    """

    def __init__(self, verbose: bool = True) -> None:
        """Initialize the initialization sequence."""
        self.steps: List[InitStep] = []
        self.current_step: Optional[InitStep] = None
        self.printer = get_printer(verbose)
        self._setup_steps()

    def _setup_steps(self) -> None:
        """Setup the default initialization steps."""
        from .startup_config import StartupConfig
        from ..app_functions import FileMaker, Kernel

        # Step 1: Configure startup settings
        self.add_step(
            name="Configure Startup",
            description="Configure UTF-8 encoding, locale, and environment variables",
            function=lambda: StartupConfig().configure(),
            required=True,
        )

        # Step 2: Check assets requirements
        self.add_step(
            name="Check Requirements",
            description="Verify that all required assets and dependencies are available",
            function=lambda: Kernel.checkAssetsRequirements(),
            required=True,
        )

        # Step 3: Generate required files
        self.add_step(
            name="Generate Files",
            description="Generate required configuration and resource files",
            function=lambda: Kernel.makeRequiredFiles(mkTheme=True),
            required=True,
        )

        # Step 4: Create asset directories
        self.add_step(
            name="Create Directories",
            description="Create necessary directories for assets, config, and modules",
            function=lambda: FileMaker().make_assets_binaries(),
            required=True,
        )

        # Step 5: Copy YAML configuration
        self.add_step(
            name="Copy Configuration",
            description="Copy YAML configuration file from package to application",
            function=lambda: FileMaker().make_yaml_from_package(),
            required=True,
        )

        # Step 6: Copy theme files
        self.add_step(
            name="Copy Themes",
            description="Copy QSS theme files from package to application",
            function=lambda: FileMaker().make_qss_from_package(),
            required=True,
        )

        # Step 7: Copy translation files
        self.add_step(
            name="Copy Translations",
            description="Copy translation files from package to application",
            function=lambda: FileMaker().make_translations_from_package(),
            required=True,
        )

        # Step 8: Generate QRC file
        self.add_step(
            name="Generate QRC",
            description="Generate Qt resource file from bin directory content",
            function=lambda: FileMaker().make_qrc(),
            required=True,
        )

        # Step 9: Compile resources
        self.add_step(
            name="Compile Resources",
            description="Compile QRC file to Python resource module",
            function=lambda: FileMaker().make_rc_py(),
            required=False,
        )

        # Step 10: Generate resource module
        self.add_step(
            name="Generate Resource Module",
            description="Generate app_resources.py module with asset classes",
            function=lambda: FileMaker().make_app_resources_module(),
            required=True,
        )

    def add_step(
        self, name: str, description: str, function: Callable, required: bool = True
    ) -> None:
        """
        Add a step to the initialization sequence.

        Parameters
        ----------
        name : str
            Name of the step.
        description : str
            Description of what the step does.
        function : Callable
            Function to execute for this step.
        required : bool, optional
            Whether this step is required (default: True).
        """
        step = InitStep(
            name=name, description=description, function=function, required=required
        )
        self.steps.append(step)

    def execute(self, verbose: bool = True) -> Dict[str, Any]:
        """
        Execute the complete initialization sequence.

        Parameters
        ----------
        verbose : bool, optional
            Whether to print progress information (default: True).

        Returns
        -------
        Dict[str, Any]
            Summary of the execution including status and statistics.
        """
        import time

        if verbose:
            self.printer.info(
                "[InitializationSequence] Starting EzQt_App Initialization Sequence"
            )
            self.printer.info(
                f"[InitializationSequence] Total steps: {len(self.steps)}"
            )
            self.printer.verbose_msg("")

        start_time = time.time()
        successful_steps = 0
        failed_steps = 0
        skipped_steps = 0

        for i, step in enumerate(self.steps, 1):
            self.current_step = step

            if verbose:
                self.printer.action(
                    f"[InitializationSequence] [{i:2d}/{len(self.steps):2d}] {step.name}"
                )
                self.printer.verbose_msg(f"    {step.description}")

            # Execute step
            step_start_time = time.time()
            step.status = StepStatus.RUNNING

            try:
                result = step.function()
                step.status = StepStatus.SUCCESS
                step.duration = time.time() - step_start_time
                successful_steps += 1

                if verbose:
                    self.printer.success(
                        f"[InitializationSequence] Step completed successfully ({step.duration:.2f}s)"
                    )

            except Exception as e:
                step.status = StepStatus.FAILED
                step.error_message = str(e)
                step.duration = time.time() - step_start_time
                failed_steps += 1

                if verbose:
                    self.printer.error(
                        f"[InitializationSequence] Step failed ({step.duration:.2f}s): {e}"
                    )

                # If step is required, stop execution
                if step.required:
                    if verbose:
                        self.printer.error(
                            f"[InitializationSequence] Initialization failed at required step: {step.name}"
                        )
                    break

            if verbose:
                self.printer.verbose_msg("")  # Ligne vide

        total_time = time.time() - start_time

        # Summary
        summary = {
            "total_steps": len(self.steps),
            "successful": successful_steps,
            "failed": failed_steps,
            "skipped": skipped_steps,
            "total_time": total_time,
            "success": failed_steps == 0,
            "steps": self.steps,
        }

        if verbose:
            self._print_summary(summary)

        return summary

    def _print_summary(self, summary: Dict[str, Any]) -> None:
        """Print execution summary."""
        self.printer.info("[InitializationSequence] Initialization Summary")
        self.printer.info(
            f"[InitializationSequence] Total Steps: {summary['total_steps']}"
        )
        self.printer.success(
            f"[InitializationSequence] Successful: {summary['successful']}"
        )
        self.printer.error(f"[InitializationSequence] Failed: {summary['failed']}")
        self.printer.warning(f"[InitializationSequence] Skipped: {summary['skipped']}")
        self.printer.info(
            f"[InitializationSequence] Total Time: {summary['total_time']:.2f}s"
        )

        if summary["success"]:
            self.printer.success(
                "[InitializationSequence] Initialization completed successfully!"
            )
        else:
            self.printer.error("[InitializationSequence] Initialization failed!")

    def get_step_status(self, step_name: str) -> Optional[StepStatus]:
        """
        Get the status of a specific step.

        Parameters
        ----------
        step_name : str
            Name of the step.

        Returns
        -------
        Optional[StepStatus]
            Status of the step, or None if not found.
        """
        for step in self.steps:
            if step.name == step_name:
                return step.status
        return None

    def reset(self) -> None:
        """Reset all steps to pending status."""
        for step in self.steps:
            step.status = StepStatus.PENDING
            step.error_message = None
            step.duration = None
        self.current_step = None

    def get_failed_steps(self) -> List[InitStep]:
        """Get list of failed steps."""
        return [step for step in self.steps if step.status == StepStatus.FAILED]

    def get_successful_steps(self) -> List[InitStep]:
        """Get list of successful steps."""
        return [step for step in self.steps if step.status == StepStatus.SUCCESS]
