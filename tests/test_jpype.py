# SPDX-FileCopyrightText: 2026-present SPDX Contributors
# SPDX-License-Identifier: Apache-2.0

"""Tests for JPype JVM connection, thread management, and SPDX Java library access."""
import os
import threading

import jpype

# Do not remove this line, it is required to import the Java classes.
import jpype.imports  # type: ignore[import]  # noqa: F401
import pytest

TOOL_JAR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tool.jar"
)


@pytest.fixture(scope="module", autouse=True)
def jvm():
    """Start JVM once for this module; JVM cannot be restarted between tests."""
    if not jpype.isJVMStarted():
        assert os.path.exists(TOOL_JAR), f"tool.jar not found at {TOOL_JAR}"
        jpype.startJVM(classpath=[TOOL_JAR], convertStrings=False)
        from org.spdx.library import SpdxModelFactory

        SpdxModelFactory.init()


class TestJVMLifecycle:
    def test_jvm_is_started(self):
        assert jpype.isJVMStarted()

    def test_tool_jar_loaded(self):
        from org.spdx.library import SpdxModelFactory

        assert SpdxModelFactory is not None

    def test_license_info_factory_accessible(self):
        from org.spdx.library import LicenseInfoFactory

        assert LicenseInfoFactory is not None

    def test_compare_helper_accessible(self):
        from org.spdx.utility.compare import LicenseCompareHelper

        assert LicenseCompareHelper is not None


class TestThreadManagement:
    def test_attach_detach_from_worker_thread(self):
        JThread = jpype.JClass("java.lang.Thread")
        attached = []
        errors = []

        def worker():
            try:
                JThread.attachAsDaemon()
                attached.append(JThread.isAttached())
                JThread.detach()
            except Exception as exc:
                errors.append(exc)

        t = threading.Thread(target=worker)
        t.start()
        t.join()

        assert not errors, f"Thread raised: {errors[0]}"
        assert attached == [True]

    def test_context_manager_attach_detach(self):
        """_jvm_thread() context manager attaches and detaches cleanly."""
        from spdx_license_matcher.utils import _jvm_thread

        JThread = jpype.JClass("java.lang.Thread")
        results = []
        errors = []

        def worker():
            try:
                with _jvm_thread():
                    results.append(JThread.isAttached())
            except Exception as exc:
                errors.append(exc)

        t = threading.Thread(target=worker)
        t.start()
        t.join()

        assert not errors, f"Thread raised: {errors[0]}"
        assert results == [True]

    def test_context_manager_detaches_on_exception(self):
        """_jvm_thread() detaches even when the body raises."""
        from spdx_license_matcher.utils import _jvm_thread

        JThread = jpype.JClass("java.lang.Thread")
        still_attached = []
        errors = []

        def worker():
            try:
                with _jvm_thread():
                    raise RuntimeError("intentional")
            except RuntimeError:
                still_attached.append(JThread.isAttached())
            except Exception as exc:
                errors.append(exc)

        t = threading.Thread(target=worker)
        t.start()
        t.join()

        assert not errors
        assert still_attached == [False]


class TestSpdxLibraryIntegration:
    def test_get_listed_license_returns_object(self):
        from spdx_license_matcher.utils import getListedLicense

        license_obj = getListedLicense("MIT")
        assert license_obj is not None

    def test_check_text_standard_license_returns_bool(self):
        from spdx_license_matcher.utils import (
            checkTextStandardLicense,
            getListedLicense,
        )

        license_obj = getListedLicense("MIT")
        result = checkTextStandardLicense(license_obj, "completely different text")
        assert isinstance(result, bool)

    def test_check_text_standard_license_difference_found(self):
        from spdx_license_matcher.utils import (
            checkTextStandardLicense,
            getListedLicense,
        )

        license_obj = getListedLicense("MIT")
        # unrelated text must differ from the MIT license
        result = checkTextStandardLicense(license_obj, "Permission is NOT granted.")
        assert result is True

    def test_ensure_jvm_idempotent(self):
        """Calling _ensure_jvm() when JVM already running must not raise."""
        from spdx_license_matcher.utils import _ensure_jvm

        _ensure_jvm()
        _ensure_jvm()
        assert jpype.isJVMStarted()
