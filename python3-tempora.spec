#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Objects and routines pertaining to date and time
Summary(pl.UTF-8):	Obiekty i funkcje związane z datą i czasem
Name:		python3-tempora
Version:	5.8.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/tempora/
Source0:	https://files.pythonhosted.org/packages/source/t/tempora/tempora-%{version}.tar.gz
# Source0-md5:	208d59bfe14a913199d3e284c56f195c
URL:		https://pypi.org/project/tempora/
BuildRequires:	python3-build
BuildRequires:	python3-coherent.licensed
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:77
BuildRequires:	python3-setuptools_scm >= 3.4.1
%if %{with tests}
BuildRequires:	python3-dateutil
BuildRequires:	python3-jaraco.functools >= 1.20
BuildRequires:	python3-pytest >= 6
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-enabler >= 2.2
BuildRequires:	python3-pytest-freezer
#BuildRequires:	python3-pytest-mypy
#BuildRequires:	python3-pytest-ruff >= 0.2.1
#BuildRequires:	python3-types-python-dateutil
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9.3
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
#BuildRequires:	python3-sphinx-lint
BuildRequires:	sphinx-pdg-3 >= 3.5
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Objects and routines pertaining to date and time (tempora).

Modules include:
- tempora (top level package module) contains miscellaneous utilities
  and constants.
- timing contains routines for measuring and profiling.
- schedule contains an event scheduler.
- utc contains routines for getting datetime-aware UTC values.

%description -l pl.UTF-8
Obiekty i funkcje związane z datą i czasem (tempora).

Moduły zawierają:
- tempora (główny moduł pakietu) zawiera różne funkcje narzędziowe i
  stałe..
- timing zawiera funkcje do pomiaru i profilowania.
- schedule zawiera planistę zdarzeń.
- utc zawiera funkcje do pobierania wartości UTC dla danego czasu.

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
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_freezer \
%{__python3} -m pytest tempora tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/calc-prorate{,-3}
ln -sf calc-prorate-3 $RPM_BUILD_ROOT%{_bindir}/calc-prorate

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst SECURITY.md
%attr(755,root,root) %{_bindir}/calc-prorate-3
%{_bindir}/calc-prorate
%{py3_sitescriptdir}/tempora
%{py3_sitescriptdir}/tempora-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
