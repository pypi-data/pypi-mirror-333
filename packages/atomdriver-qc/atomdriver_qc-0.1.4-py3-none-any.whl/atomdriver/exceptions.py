#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
class QMBackendException(Exception):
    pass


class BackendUnavailable(QMBackendException):
    pass


class UnknownQMDriver(QMBackendException):
    pass


class BackendRunException(QMBackendException):
    pass


class ProcessFailed(BackendRunException):
    pass


class NoOutputFile(BackendRunException):
    pass


class ConfigurationError(BackendRunException):
    pass


class CommandNotFound(BackendRunException):
    pass


class SCFConvergenceError(BackendRunException):
    pass


class CalculationError(Exception):
    pass


class IncompleteJobsError(CalculationError):
    pass


class JobAlreadyRun(CalculationError):
    pass


class JobNotFinished(CalculationError):
    pass


class JobNotMarkedForRunning(CalculationError):
    pass


class NotTheRightWorker(CalculationError):
    pass


class NoJobInputFile(CalculationError):
    pass


class NoSubmittedJob(CalculationError):
    pass


class WorkerNotConfigured(Exception):
    pass
