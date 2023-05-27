%define sover 4
Name:           libqxmpp
Version:        1.5.0
Release:        0
Summary:        Qt XMPP Library
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
URL:            https://github.com/qxmpp-project/qxmpp/
Source0:        https://github.com/qxmpp-project/qxmpp/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake >= 3.7
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  pkgconfig
BuildRequires:  qca-devel
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(libomemo-c)

%description
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package -n %{name}%{sover}
Summary:        Qt XMPP Library
Group:          System/Libraries
Provides:       libqxmpp-qt5-0 = %{version}
Obsoletes:      libqxmpp-qt5-0 < %{version}

%description -n %{name}%{sover}
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package -n %{name}-devel
Summary:        Qxmpp Development Files
Group:          Development/Libraries/C and C++
Requires:       %{name}%{sover} = %{version}
Requires:       pkgconfig(gstreamer-1.0)
Provides:       libqxmpp-qt5-devel = %{version}
Obsoletes:      libqxmpp-qt5-devel < %{version}

%description -n %{name}-devel
Development package for qxmpp.

%package doc
Summary:        Qxmpp library documentation
Group:          Documentation/HTML
BuildArch:      noarch

%description doc
This packages provides documentation of Qxmpp library API.

%prep
%setup -q -n qxmpp-%{version}

%build

%cmake \
  -DWITH_GSTREAMER=ON \
  -DBUILD_DOCUMENTATION=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_TESTS=OFF \
  -DBUILD_OMEMO=ON \

%cmake_build

%install
%cmake_install

%fdupes %{buildroot}%{_datadir}/doc/qxmpp/

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}

# Exclude tests needing a network connection
#%{ctest --exclude-regex "tst_(qxmppcallmanager|qxmppiceconnection|qxmppserver|qxmpptransfermanager|qxmppuploadrequestmanager)"}

%ldconfig_scriptlets -n %{name}%{sover}

%files -n %{name}%{sover}
%license LICENSES/*
%doc AUTHORS CHANGELOG.md README.md
%{_libdir}/%{name}.so.*
%{_libdir}/libQXmppOmemo.so.*

%files -n %{name}-devel
%{_includedir}/qxmpp/
%{_libdir}/%{name}.so
%{_libdir}/cmake/qxmpp/
%{_libdir}/pkgconfig/qxmpp.pc
%{_libdir}/libQXmppOmemo.so
%{_libdir}/cmake/QXmppOmemo/

%files doc
%{_datadir}/doc/qxmpp/

%changelog

