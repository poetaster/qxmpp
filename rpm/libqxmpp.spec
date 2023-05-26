#
# spec file for package libqxmpp
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
%global kf5_version 5.106.0

Name:           opt-kf5-libqxmpp
Version:        1.5
Release:        0
Summary:        Qt XMPP Library
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
URL:            https://github.com/qxmpp-project/qxmpp/
Source0:        %{name}-%{version}.tar.bz2


%global __requires_exclude ^libqca-qt5.*$

## upstreamable patches
%{?opt_kf5_default_filter}

BuildRequires:  cmake >= 3.7
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
#BuildRequires:  doxygen
#BuildRequires:  fdupes

BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qttools-devel
BuildRequires: opt-kf5-rpm-macros >= %{kf5_version}
BuildRequires: opt-qt5-qtbase-gui
BuildRequires: opt-qca-qt5-devel
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(libomemo-c)

%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}

%description
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package        libs 
Summary:        Qt XMPP Library
Group:          System/Libraries

%description    libs
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package        devel
Summary:        Qxmpp Development Files
Group:          Development/Libraries/C and C++
Requires:       %{name}%{?_isa}  = %{version}-%{release}
Requires:       pkgconfig(gstreamer-1.0)

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use qxmpp.

%package doc
Summary:        Qxmpp library documentation
Group:          Documentation/HTML
BuildArch:      noarch

%description doc
This packages provides documentation of Qxmpp library API.

%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%cmake .. \
  -DWITH_GSTREAMER=ON \
  -DBUILD_DOCUMENTATION=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_TESTS=OFF \
  -DWITH_QCA=ON \
  -DBUILD_OMEMO=ON 

%_opt_cmake_kf5 ../

%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%check
#export LD_LIBRARY_PATH=%{buildroot}%{_libdir}

# Exclude tests needing a network connection
#%{ctest --exclude-regex "tst_(qxmppcallmanager|qxmppiceconnection|qxmppserver|qxmpptransfermanager|qxmppuploadrequestmanager)"}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

#%ldconfig_scriptlets -n %{name}%{sover}

%files -n %{name}
%license LICENSES/*
%doc AUTHORS CHANGELOG.md README.md
%{_opt_qt5_libdir}/libQXmppQt5.so.*
%{_opt_qt5_libdir}/libQXmppOmemoQt5.so.*

%files -n %{name}-devel
%{_opt_qt5_includedir}/QXmppQt5/
%{_opt_qt5_libdir}/libQXmppQt5.so
%{_opt_qt5_libdir}/libQXmppQt5.so*
%{_opt_qt5_libdir}/cmake/QXmppQt5/
%{_opt_qt5_libdir}/pkgconfig/QXmppQt5.pc
%{_opt_qt5_libdir}/cmake/QXmpp/
%{_opt_qt5_libdir}/pkgconfig/qxmpp.pc
%{_opt_qt5_libdir}/libQXmppOmemoQt5.so.*
%{_opt_qt5_libdir}/libQXmppOmemoQt5.so
%{_opt_qt5_libdir}/cmake/QXmppOmemoQt5/

%changelog
