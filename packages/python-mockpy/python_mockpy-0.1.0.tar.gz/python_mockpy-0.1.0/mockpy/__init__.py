"""
MockPy - Comprehensive Realistic Data Generation Library

A Python library for generating realistic mock data for testing,
development, and demonstration purposes.
"""

from mockpy.mockpy import (
    MockPy,
    Provider,
    PersonProvider,
    AddressProvider,
    CompanyProvider,
    FinanceProvider,
    InternetProvider,
    LoremProvider,
    DateTimeProvider,
    MockPyError,
    MockPyLocaleError,
    MockPyValueError,
    DataContainer,
    integrations
)

__version__ = "0.1.0"
__all__ = [
    'MockPy',
    'Provider',
    'PersonProvider', 
    'AddressProvider',
    'CompanyProvider',
    'FinanceProvider',
    'InternetProvider',
    'LoremProvider',
    'DateTimeProvider',
    'MockPyError',
    'MockPyLocaleError',
    'MockPyValueError',
    'DataContainer',
    'integrations'
]