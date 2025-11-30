#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-tempora.spec)

Summary:	Objects and routines pertaining to date and time
Summary(pl.UTF-8):	Obiekty i funkcje związane z datą i czasem
Name:		python-tempora
# keep 1.x here for python2 support
Version:	1.14.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/tempora/
Source0:	https://files.pythonhosted.org/packages/source/t/tempora/tempora-%{version}.tar.gz
# Source0-md5:	f8b2b0df1adf3f83b829a85e31bddb2d
URL:		https://pypi.org/project/tempora/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:34.4
BuildRequires:	python-setuptools_scm >= 1.15
%if %{with tests}
BuildRequires:	python-backports.unittest_mock
BuildRequires:	python-freezegun
BuildRequires:	python-jaraco.functools >= 1.20
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-flake8
BuildRequires:	python-pytz
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 1:34.4
BuildRequires:	python3-setuptools_scm >= 1.15
%if %{with tests}
BuildRequires:	python3-freezegun
BuildRequires:	python3-jaraco.functools >= 1.20
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-pytz
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-jaraco.packaging >= 3.2
BuildRequires:	python-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Objects and routines pertaining to date and time (tempora).

Modules include:
- tempora (top level package module) contains miscellaneous utilities
  and constants.
- timing contains routines for measuring and profiling.
- schedule contains an event scheduler.

%description -l pl.UTF-8
Obiekty i funkcje związane z datą i czasem (tempora).

Moduły zawierają:
- tempora (główny moduł pakietu) zawiera różne funkcje narzędziowe i
  stałe..
- timing zawiera funkcje do pomiaru i profilowania.
- schedule zawiera planistę zdarzeń.

%package -n python3-tempora
Summary:	Objects and routines pertaining to date and time
Summary(pl.UTF-8):	Obiekty i funkcje związane z datą i czasem
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-tempora
Objects and routines pertaining to date and time (tempora).

Modules include:
- tempora (top level package module) contains miscellaneous utilities
  and constants.
- timing contains routines for measuring and profiling.
- schedule contains an event scheduler.
- utc contains routines for getting datetime-aware UTC values
  (Python 3 only).

%description -n python3-tempora -l pl.UTF-8
Obiekty i funkcje związane z datą i czasem (tempora).

Moduły zawierają:
- tempora (główny moduł pakietu) zawiera różne funkcje narzędziowe i
  stałe..
- timing zawiera funkcje do pomiaru i profilowania.
- schedule zawiera planistę zdarzeń.
- utc zawiera funkcje do pobierania wartości UTC dla danego czasu
  (tylko dla Pythona 3).

%package apidocs
Summary:	API documentation for Python tempora module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona tempora
Group:		Documentation

%description apidocs
API documentation for Python tempora module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona tempora.

%prep
%setup -q -n tempora-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=backports.unittest_mock,pytest_flake8 \
%{__python} -m pytest tempora tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_flake8 \
%{__python3} -m pytest tempora tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-2 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/calc-prorate{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/calc-prorate{,-3}
ln -sf calc-prorate-3 $RPM_BUILD_ROOT%{_bindir}/calc-prorate
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/calc-prorate-2
%{py_sitescriptdir}/tempora
%{py_sitescriptdir}/tempora-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-tempora
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/calc-prorate-3
%{_bindir}/calc-prorate
%{py3_sitescriptdir}/tempora
%{py3_sitescriptdir}/tempora-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
