Name:           libqxmpp
Version:        1.5
Release:        0
Summary:        Qt XMPP Library
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++
URL:            https://github.com/qxmpp-project/qxmpp/
Source0:        %{name}-%{version}.tar.gz
#Patch0:         001-version.patch
#Patch1:         002-Task.patch
#Patch2:         003-Future.patch
#Patch3:         004-Hashing.patch
BuildRequires:  cmake >= 3.7
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  libomemo-c-devel
BuildRequires:  qca-devel

%description
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package        libs
Summary:        Qt XMPP Library
Group:          System/Libraries
Provides:       libqxmpp-qt5 = %{version}
Obsoletes:      libqxmpp-qt5 < %{version}

%description    libs
QXmpp is a cross-platform C++ XMPP client library based on Qt and C++.

%package        devel
Summary:        Qxmpp Development Files
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       pkgconfig(gstreamer-1.0)
Provides:       libqxmpp-qt5-devel = %{version}
Obsoletes:      libqxmpp-qt5-devel < %{version}

%description    devel
Development package for qxmpp.

%package doc
Summary:        Qxmpp library documentation
Group:          Documentation/HTML
BuildArch:      noarch

%description doc
This packages provides documentation of Qxmpp library API.

%prep
%autosetup -n %{name}-%{version}/ronqxmpp -p1

%build
touch .git
mkdir -p build
pushd build

%cmake ../ \
  -DWITH_GSTREAMER=ON \
  -DBUILD_DOCUMENTATION=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_TESTS=OFF \
  -DBUILD_OMEMO=ON \
  -DWITH_OMEMO_V03=ON \

%make_build
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
popd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files -n %{name}
%{_libdir}/libQXmppQt5.so*
%{_libdir}/libQXmppOmemoQt5.so*

%files -n %{name}-devel
%{_includedir}/QXmppQt5/
%{_libdir}/libQXmppQt5.so*
%{_libdir}/cmake/QXmppQt5/
%{_libdir}/cmake/QXmpp/
%{_libdir}/pkgconfig/QXmppQt5.pc
%{_libdir}/pkgconfig/qxmpp.pc
%{_libdir}/libQXmppOmemoQt5.so*
%{_libdir}/cmake/QXmppOmemoQt5/

%files doc
%{_datadir}/doc/qxmpp/

%changelog

