%undefine _hardened_build

Name:           btop
Version:        1.4.5
Release:        1%{?dist}
Summary:        Modern and colorful command line resource monitor that shows usage and stats

# The entire source code is ASL 2.0 except:
# include/widechar_width.hpp - Public Domain
License:        Apache-2.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/aristocratos/btop
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  lowdown
%if 0%{?el8}
BuildRequires:  gcc-toolset-12-gcc-c++
BuildRequires:  gcc-toolset-12-annobin-plugin-gcc
BuildRequires:  gcc-toolset-12-binutils
%endif
%if 0%{?el9}
BuildRequires:  gcc-toolset-13-gcc-c++
BuildRequires:  gcc-toolset-13-annobin-plugin-gcc
BuildRequires:  gcc-toolset-13-binutils
%endif

%if 0%{?amzn2023}
%global _hardened_build 0
%global _enable_annobin 0
%global __cc /usr/bin/gcc14-gcc
%global __cxx /usr/bin/gcc14-g++
BuildRequires: gcc14
BuildRequires: gcc14-c++
%endif

# gpu support
%if 0%{?fedora}
%ifnarch i686 s390x
BuildRequires:  rocm-smi-devel
%endif
%endif

Requires:       hicolor-icon-theme

# Bundling was chosen for widecharwidth as it is not versioned upstream
# and doesn't appear to be a widely-used lib.
Provides:       bundled(widecharwidth)

%description
Resource monitor that shows usage and stats for processor,
memory, disks, network and processes.

C++ version and continuation of bashtop and bpytop.

%prep
%autosetup


%build
%{?el8:. /opt/rh/gcc-toolset-12/enable}
%{?el9:. /opt/rh/gcc-toolset-13/enable}

# to build debuginfo
export CXXFLAGS="${CXXFLAGS} -g"
%make_build


%install
%make_install PREFIX=%{_prefix}
rm -f %{buildroot}%{_datadir}/btop/README.md
desktop-file-validate %{buildroot}%{_datadir}/applications/btop.desktop


%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/%{name}
%{_datadir}/applications/btop.desktop
%{_datadir}/btop
%{_datadir}/icons/hicolor/*/apps/btop.*
%{_mandir}/man1/%{name}.1.gz
