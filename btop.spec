%undefine _hardened_build

Name:           btop
Version:        1.4.7
Release:        1%{?dist}
Summary:        Modern and colorful command line resource monitor that shows usage and stats

# The entire source code is ASL 2.0 except:
# include/widechar_width.hpp - Public Domain
License:        Apache-2.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/aristocratos/btop
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Detect Amazon Linux
%global is_amzn 0
%if 0%{?amzn}
%global is_amzn 1
%endif

# Detect EL major
%global is_el 0
%if 0%{?rhel}
%global is_el 1
%endif

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  lowdown

%if 0%{?el9}
BuildRequires:  gcc-toolset-14-gcc-c++
BuildRequires:  gcc-toolset-14-binutils
%endif

%if %{is_amzn}
BuildRequires:  gcc14
BuildRequires:  gcc14-c++
BuildRequires:  rocm-smi-devel
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
sed -i '1i#define _GNU_SOURCE' src/linux/intel_gpu_top/intel_gpu_top.c


%build
%{?el9:. /opt/rh/gcc-toolset-14/enable}

%if %{is_amzn}
export CC=gcc14-gcc
export CXX=gcc14-g++
%endif

# Fix asprintf() prototype + feature defines
export CPPFLAGS="${CPPFLAGS} -D_GNU_SOURCE"

# If your build environment injects annobin specs, strip it (prevents gcc14 plugin failures)
export CFLAGS="$(echo %{optflags} | sed 's|-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1||g')"
export CXXFLAGS="$(echo %{optflags} | sed 's|-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1||g') -std=c++23"
export LDFLAGS="$(echo %{__global_ldflags} | sed 's|-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1||g')"

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
